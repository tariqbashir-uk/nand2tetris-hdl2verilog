from os.path import isfile, join
from os import listdir
from modules.core.fileActions import FileActions
from modules.core.logger import Logger

from modules.core.textFile import TextFile

from modules.fileHandlers.hdlFile import HdlFile
from modules.hdlTypes.hdlChipList import HdlChipList
from modules.hdlTypes.hdlChip import HdlChip
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

from modules.fileHandlers.tstFile import TstFile
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

import modules.settings as settings

class Hdl2verilogMain():
    def __init__(self):
        self.logger      = Logger()
        self.fileActions = FileActions()
        return

    ##########################################################################
    def Run(self, inputFolder, outputFolder):
        hdlStoreFolder = join(outputFolder, settings.HDL_STORE_FOLDER)
        self.fileActions.CreateFolderIfNeeded(hdlStoreFolder)

        hdlFilenames = self._GetFilesWithExtInFolder(inputFolder, 'hdl')
        for hdlFilename in hdlFilenames:
            self.logger.Info("Copying %s to store" % (hdlFilename))
            fullInputFilename = join(inputFolder, hdlFilename)
            self.fileActions.CopyFile(fullInputFilename, join(hdlStoreFolder, hdlFilename))

        hdlFilenames = self._GetFilesWithExtInFolder(hdlStoreFolder, 'hdl')
        hdlChipList  = HdlChipList()
        for hdlFilename in hdlFilenames:
            self.logger.Info("Reading %s .." % (hdlFilename))
            fullInputFilename = join(hdlStoreFolder, hdlFilename)
            hdlFile = HdlFile(fullInputFilename)
            hdlChip = hdlFile.ParseFile()
            hdlChipList.AddChip(hdlChip)

        hdlChipList.UpdateAllPin1BitWidths()

        for hdlChip in hdlChipList.chipList:  
            self.CreateVerilogModule(hdlChip, hdlChipList, outputFolder)

        tstFilenames = self._GetFilesWithExtInFolder(inputFolder, 'tst')
        
        tstScripts = []
        tstsToRun  = []
        for tstFilename in tstFilenames:
            testName, ext = self.fileActions.GetFileNameAndExt(tstFilename)
            self.logger.Info("Reading %s .." % (tstFilename))
            tstFile   = TstFile(join(inputFolder, tstFilename))
            tstScript = tstFile.ParseFile(testName)
            tstScripts.append(tstScript)

            tstScript.testChip = hdlChipList.GetChip(tstScript.testHdlModule)            
            self.CreateVerilogModuleTB(tstScript, outputFolder)
            tstsToRun.append(tstScript)

            #print(hdlChip.GetChipDependencyList())

        runSHFile   = TextFile(join(outputFolder, 'runme.sh'))
        runContents = "set -e\n"

        for tstToRun in tstsToRun: # type: TstScript
            moduleList = hdlChipList.GetChipDependencyList(tstToRun.testChip)
            moduleList = [x + ".v" for x in moduleList]

            runContents += ("echo \"Building and running test for %s\"\n" % (tstToRun.testName))
            runContents += ("iverilog -o ./out/%s %s %s\n" % (tstToRun.testName, tstToRun.testName + "_tb.v", " ".join([x for x in moduleList])))
            # iverilog -o ./out/And And_tb.v Not.v And.v Nand.v
            runContents += ("vvp ./out/%s\n" % (tstToRun.testName))
            runContents += ("diff -w %s/%s %s\n" % (inputFolder, tstToRun.compareFile, tstToRun.outputFile))
            runContents += "\n"

        runSHFile.WriteFile(runContents)

        self.WriteNandV(outputFolder)
        return    

    ##########################################################################
    def WriteNandV(self, outputFolder):
        nand_v  = TextFile(join(outputFolder, 'Nand.v'))
        nandContents  = "module Nand(out, a, b);\n"
        nandContents += "  input a, b;\n"
        nandContents += "  output out;\n"
        nandContents += "  nand (out, a, b);\n"
        nandContents += "endmodule\n"
        nand_v.WriteFile(nandContents)
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
            portList.append(self._HdlPinToVerilogPort(inputPin))
        verilogModuleTB.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(outputPin))
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
            portList.append(self._HdlPinToVerilogPort(inputPin))
        verilogMainModule.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            portList.append(self._HdlPinToVerilogPort(outputPin))
        verilogMainModule.AddOutputPorts(portList)

        verilogSubmoduleCalls = []
        verilogSubmoduleDict  = {}
        for part in partList:
            connections = part.GetConnections() #type: list[HdlConnection]

            if part.partName not in verilogSubmoduleDict:
                verilogSubmoduleDict[part.partName] = 0
            else:
                verilogSubmoduleDict[part.partName] += 1

            verilogSubmoduleCall = VerilogSubmoduleCall(part.partName, verilogSubmoduleDict[part.partName])

            pinDict = {}
            for connection in connections:
                pin1, pin2 = connection.GetPins() # type: HdlPin, HdlPin
              
                # For internal pins we need to know their width and we can get this from the pin width of the chip that is being called
                if pin1.IsOutput() and pin2.IsInternal():
                    bitWidth = hdlChipList.GetBitWidthForPin(part.partName, pin1.pinName)
                    # Check if we have a split pin output case, we can tell this is pin1.bitwidth is defined and different to the chip bitwidth */ 
                    if pin1.bitWidth != bitWidth:
                        bitWidth = pin1.bitWidth
                    hdlChip.UpdatePin2Width(pin2.pinName, bitWidth)

                subModulePort     = self._HdlPinToVerilogPort(pin1)
                internalParamPort = self._HdlPinToVerilogPort(pin2)

                keyName = pin1.pinName
                if keyName not in pinDict:
                    pinDict[keyName] = VerilogSubmoduleCallParam(subModulePort, 
                                                                 internalParamPort, 
                                                                 connection.pin2StartBitOfBus,
                                                                 connection.pin2EndBitOfBus,
                                                                 connection.pin2BitIndex)
                    verilogSubmoduleCall.AddCallParam(pinDict[keyName])
                else:
                    # Handling case where input bits are made from concatinated internal variable bits
                    pinDict[keyName].IncrementBitCount()

            verilogSubmoduleCalls.append(verilogSubmoduleCall)

        verilogMainModule.AddSubmoduleCalls(verilogSubmoduleCalls)
        verilogMainModule.DumpModuleDetails()
        #print(moduleCalls)
        verilogModGen.CreateModule(verilogMainModule)
        return

    ##########################################################################
    def _HdlPinToVerilogPort(self, hdlPin : HdlPin):
        portDirection = VerilogPortDirectionTypes.unknown

        if hdlPin.pinType == HdlPinTypes.Input:
            portDirection = VerilogPortDirectionTypes.input
        elif hdlPin.pinType == HdlPinTypes.Output:
            portDirection = VerilogPortDirectionTypes.output

        return VerilogPort(hdlPin.pinName, portDirection, "", hdlPin.GetPinBitWidth(), hdlPin.IsInternal())

    ##########################################################################
    def _GetFilesWithExtInFolder(self, folder, ext):
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        files = [k for k in files if ext in k]
        return files