from os.path import isfile, join
from os import listdir
from modules.core.fileActions import FileActions
from modules.core.logger import Logger

from modules.hdlTypes.hdlChipList import HdlChipList
from modules.hdlTypes.hdlChip import HdlChip
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlConnectionTypes import HdlConnectionTypes
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

from modules.tstTypes.tstScript import TstScript
from modules.tstTypes.tstSetSequence import TstSetSequence
from modules.tstTypes.tstSetOperation import TstSetOperation

from modules.verilogTypes.verilogModule import VerilogModule
from modules.verilogTypes.verilogModuleTB import VerilogModuleTB
from modules.verilogTypes.verilogPort import VerilogPort
from modules.verilogTypes.verilogPortDirectionTypes import VerilogPortDirectionTypes
from modules.verilogTypes.verilogWireAssignment import VerilogWireAssignment
from modules.verilogTypes.verilogCallParams import VerilogCallParams
from modules.verilogTypes.verilogSubmoduleCall import VerilogSubmoduleCall
from modules.verilogTypes.verilogSubmoduleCallParam import VerilogSubmoduleCallParam
from modules.generator.verilogModuleGenerator import VerilogModuleGenerator
from modules.generator.verilogTestBenchGenerator import VerilogTestBenchGenerator

from modules.mappers.hdlToVerilogParamMapper import HdlToVerilogParamMapper

import modules.settings as settings
import modules.commonDefs as commonDefs

class HdlToVerilogMapper():
    def __init__(self):
        self.logger = Logger()
        return

    ##########################################################################
    def CreateVerilogModuleTB(self, tstScript : TstScript, outputFolder):
        hdlChip       = tstScript.testChip # type: HDLChip
        verilogModGen = VerilogTestBenchGenerator(outputFolder)
        
        clkPinName = None
        clkPin     = hdlChip.GetClkPin()
        if clkPin:
            clkPinName = clkPin.pinName
            
        verilogModuleTB = VerilogModuleTB(tstScript.testName + "_tb",
                                          tstScript.testHdlModule,
                                          tstScript.testName + ".vcd",
                                          tstScript.outputFile,
                                          clkPinName)

        portList = []
        for inputPin in hdlChip.GetInputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(inputPin, inputPin.GetPinBitWidth()))
        verilogModuleTB.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(outputPin, outputPin.GetPinBitWidth()))
        verilogModuleTB.AddOutputPorts(portList)
        
        verilogModuleTB.AddOutputFormatList(tstScript.GetOutputFormatList())
        
        for setSequence in tstScript.setSequences: #type: TstSetSequence
            testSequenceV = []
            if setSequence.setOperations:
                for setOperation in setSequence.setOperations: #type: TstSetOperation
                    testSequenceV.append(TstSetOperation(setOperation.pinName, setOperation.pinValue.replace("%B", "'b")))

            verilogModuleTB.AddTestSequence(TstSetSequence(setSequence.sequenceType, testSequenceV))

        #verilogModuleTB.DumpModuleDetails()
        verilogModGen.CreateModule(verilogModuleTB)
        return

    ##########################################################################
    def CreateVerilogModule(self, hdlChip : HdlChip, hdlChipList : HdlChipList, outputFolder):
        verilogModGen = VerilogModuleGenerator(outputFolder)

        partList = hdlChip.GetChipPartList() #type: list[HdlChipPart]

        verilogMainModule = VerilogModule(hdlChip.chipName)

        portList = []
        for inputPin in hdlChip.GetInputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(inputPin, inputPin.GetPinBitWidth()))
        verilogMainModule.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(outputPin, outputPin.GetPinBitWidth()))
        verilogMainModule.AddOutputPorts(portList)

        tmpVarCounter        = 0
        verilogSubmoduleDict = {}
        for part in partList:
            self.logger.Debug("Mapping: Chip %s, Part %s (line %d)" % (hdlChip.chipName, part.partName, part.lineNo))
            connections = part.GetConnections() #type: list[HdlConnection]

            paramMapperDict = {}
            for connection in connections:
                pin1, pin2 = connection.GetPins() # type: HdlPin, HdlPin
              
                toPort   = self._HdlPinToVerilogPort(pin1, pin1.GetPinBitWidth())
                fromPort = self._HdlPinToVerilogPort(pin2, connection.pin2ConnectionWidth)

                keyName = pin1.pinName
                if keyName not in paramMapperDict:
                    paramMapperDict[keyName] = HdlToVerilogParamMapper(hdlChip.chipName, part.partName, part.lineNo, toPort, fromPort)         
                
                paramMapperDict[keyName].AddHdlConnection(connection)

            if part.partName not in verilogSubmoduleDict:
                verilogSubmoduleDict[part.partName] = 0
            else:
                verilogSubmoduleDict[part.partName] += 1

            verilogSubmoduleCall = VerilogSubmoduleCall(part.partName, verilogSubmoduleDict[part.partName])

            for paramMapper in paramMapperDict:
                paramMapperDict[paramMapper].DoMapping()

                toPort       = paramMapperDict[paramMapper].toPort
                fromPort     = paramMapperDict[paramMapper].fromPort
                mappedParams = paramMapperDict[paramMapper].GetMappedParams()

                numParamsForCall = mappedParams.GetNumParamsForCall()

                # Normal case: All parameters can be mapped onto a single input or output port
                if numParamsForCall == 1:
                    verilogSubmoduleCallParam = VerilogSubmoduleCallParam(toPort, fromPort, mappedParams.GetVerilogParams(0))
                    verilogSubmoduleCall.AddCallParam(verilogSubmoduleCallParam)

                # Multiple param case:
                # We can duplicate outputs in HDL mode calls, which isn't support in verilog. Therefore to map this case to verilog
                # we will have to assign the output pin to a new internal parameter and the use assign calls to set the correct ports.
                # e.g.
                # HDL:      Nand(a=a, b=b, out=out1, out=out2)
                # would map to..
                # Verilog:  Nand nand_1(.a (a), .b(b), .out(outTemp))
                #           assign out1 = outTemp;
                #           assign out2 = outTemp;
                else:
                    # Create the mapping to a new temporary internal parameter, which is the same width as the toPort
                    tmpPinName = ("tempOutput_%d" % (tmpVarCounter))
                    tmpPin     = HdlPin(tmpPinName, HdlPinTypes.Internal, None)
                    tmpPort    = self._HdlPinToVerilogPort(tmpPin, toPort.portBitWidth)

                    verilogSubmoduleCallParam = VerilogSubmoduleCallParam(toPort, tmpPort, VerilogCallParams(paramList=[tmpPort.portName]))
                    verilogSubmoduleCall.AddCallParam(verilogSubmoduleCallParam)
                    tmpVarCounter += 1

                    for i in range(0, numParamsForCall):
                        verilogMainModule.AddWireAssignment(VerilogWireAssignment(mappedParams.GetVerilogParams(i).GetCallStr(), tmpPinName))

            verilogMainModule.AddSubmoduleCall(verilogSubmoduleCall)

        verilogMainModule.DumpModuleDetails()
        verilogModGen.CreateModule(verilogMainModule)
        return

    ##########################################################################
    def _HdlPinToVerilogPort(self, hdlPin : HdlPin, bitWidth):
        portDirection = VerilogPortDirectionTypes.unknown

        if hdlPin.pinType == HdlPinTypes.Input or hdlPin.pinType == HdlPinTypes.Clk:
            portDirection = VerilogPortDirectionTypes.input
        elif hdlPin.pinType == HdlPinTypes.Output:
            portDirection = VerilogPortDirectionTypes.output

        return VerilogPort(hdlPin.pinName, portDirection, "", bitWidth, hdlPin.IsInternal())