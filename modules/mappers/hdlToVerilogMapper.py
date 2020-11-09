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
        hdlChip       = tstScript.testChip
        verilogModGen = VerilogTestBenchGenerator(outputFolder)

        verilogModuleTB = VerilogModuleTB(tstScript.testName + "_tb",
                                          tstScript.testHdlModule,
                                          tstScript.testHdlModule + ".vcd",
                                          tstScript.outputFile)

        portList = []
        for inputPin in hdlChip.GetInputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(inputPin, inputPin.GetPinBitWidth()))
        verilogModuleTB.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(outputPin, outputPin.GetPinBitWidth()))
        verilogModuleTB.AddOutputPorts(portList)
        
        for setSequence in tstScript.setSequences: #type: TstSetSequence
            testSequenceV = []
            for setOperation in setSequence.setOperations: #type: TstSetOperation
                testSequenceV.append(TstSetOperation(setOperation.pinName, setOperation.pinValue.replace("%B", "'b")))

            verilogModuleTB.AddTestSequence(TstSetSequence(testSequenceV))

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

        verilogSubmoduleCalls = []
        verilogSubmoduleDict  = {}
        for part in partList:
            self.logger.Debug("Mapping: Chip %s, Part %s (line %d)" % (hdlChip.chipName, part.partName, part.lineNo))
            connections = part.GetConnections() #type: list[HdlConnection]

            paramMapperDict = {}
            for connection in connections:
                pin1, pin2 = connection.GetPins() # type: HdlPin, HdlPin
              
                toPort   = self._HdlPinToVerilogPort(pin1, pin1.GetPinBitWidth())
                fromPort = self._HdlPinToVerilogPort(pin2, connection.pin2ConnectionWidth)

                # Note: Cases todo..
                # bit range  <-- input bit range
                # all bits   <-- input all bits (different bit length)
 
                keyName = pin1.pinName
                if keyName not in paramMapperDict:
                    # pinDict[keyName] = VerilogSubmoduleCallParam(toPort, fromPort)         
                    # verilogSubmoduleCall.AddCallParam(pinDict[keyName])

                    paramMapperDict[keyName] = HdlToVerilogParamMapper(toPort, fromPort)         
                    #verilogSubmoduleCall.AddCallParam(pinDict[keyName])
                
                pin1BitIndex, pin1StartBitOfBus, pin1EndBitOfBus, pin1ConnectionWidth, pin1ConnectionType = connection.GetPin1Params()
                pin2BitIndex, pin2StartBitOfBus, pin2EndBitOfBus, pin2ConnectionWidth, pin2ConnectionType = connection.GetPin2Params()

                paramFullName = self._MakeParamFullName(pin2.pinName, pin2BitIndex, pin2StartBitOfBus, pin2EndBitOfBus)

                # Cases:
                # all bits   <-- input all bits (same bit length)
                # all bits   <-- input single bit
                # all bits   <-- input bit range
                # all bits   <-- internal all bits
                if pin1ConnectionType == HdlConnectionTypes.AllBits:
                    paramMapperDict[keyName].AddAllBitMapping(paramFullName, pin1ConnectionWidth)

                # Cases:
                # bit range  <-- input all bits
                # bit range  <-- internal all bits
                elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                      pin2ConnectionType == HdlConnectionTypes.SingleBit):
                    for hdlBitNumber in range(connection.pin1StartBitOfBus, connection.pin1EndBitOfBus):
                        paramMapperDict[keyName].AddSingleBitMapping(hdlBitNumber, paramFullName)

                # Cases:
                # bit range  <-- input bit range
                elif pin1ConnectionType == HdlConnectionTypes.BitRange and pin2ConnectionType == HdlConnectionTypes.AllBits:
                    paramMapperDict[keyName].AddMultiBitMapping(paramFullName, pin1StartBitOfBus, pin1EndBitOfBus)

                # Cases:
                # single bit <-- input all bits     
                # single bit <-- input single bit 
                # single bit <-- internal all bits
                else:
                    paramMapperDict[keyName].AddSingleBitMapping(connection.pin1BitIndex, paramFullName)

            if part.partName not in verilogSubmoduleDict:
                verilogSubmoduleDict[part.partName] = 0
            else:
                verilogSubmoduleDict[part.partName] += 1

            verilogSubmoduleCall = VerilogSubmoduleCall(part.partName, verilogSubmoduleDict[part.partName])

            for paramMapper in paramMapperDict:
                paramMapperDict[paramMapper].FinaliseParamList()
                paramList = paramMapperDict[paramMapper].GetParamList()
                verilogSubmoduleCallParam = VerilogSubmoduleCallParam(paramMapperDict[paramMapper].toPort,
                                                                      paramMapperDict[paramMapper].fromPort,
                                                                      paramList)
                
                verilogSubmoduleCall.AddCallParam(verilogSubmoduleCallParam)
            
            verilogSubmoduleCalls.append(verilogSubmoduleCall)

        verilogMainModule.AddSubmoduleCalls(verilogSubmoduleCalls)
        verilogMainModule.DumpModuleDetails()
        #print(moduleCalls)
        verilogModGen.CreateModule(verilogMainModule)
        return

    ##########################################################################
    def _MakeParamFullName(self, pinName, pinBitIndex, pinStartBitOfBus, pinEndBitOfBus):
        paramName  = pinName
        paramExtra = ""

        if pinBitIndex != commonDefs.NO_BIT_VALUE:
            paramExtra += "[" + str(pinBitIndex) + "]"
        elif pinStartBitOfBus != commonDefs.NO_BIT_VALUE:
            paramExtra += "[" + str(pinEndBitOfBus) + ":"  + str(pinStartBitOfBus) +  "]"

        return ("%s%s" % (paramName, paramExtra))

    ##########################################################################
    def _HdlPinToVerilogPort(self, hdlPin : HdlPin, bitWidth):
        portDirection = VerilogPortDirectionTypes.unknown

        if hdlPin.pinType == HdlPinTypes.Input:
            portDirection = VerilogPortDirectionTypes.input
        elif hdlPin.pinType == HdlPinTypes.Output:
            portDirection = VerilogPortDirectionTypes.output

        return VerilogPort(hdlPin.pinName, portDirection, "", bitWidth, hdlPin.IsInternal())