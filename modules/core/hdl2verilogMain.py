from os.path import isfile, join
from os import listdir
from modules.core.fileActions import FileActions
from modules.core.logger import Logger

from modules.core.textFile import TextFile

from modules.fileHandlers.hdlFile import HdlFile
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

class Hdl2verilogMain():
    def __init__(self):
        self.logger      = Logger()
        self.fileActions = FileActions()
        return

    ##########################################################################
    def Run(self, inputFolder, outputFolder):
        hdlFilenames = self._GetFilesWithExtInFolder(inputFolder, 'hdl')

        hdlChips = []
        for hdlFilename in hdlFilenames:
            self.logger.Info("Reading %s .." % (hdlFilename))
            hdlFile = HdlFile(join(inputFolder, hdlFilename))
            hdlChip = hdlFile.ParseFile()
            hdlChips.append(hdlChip)
            self.CreateVerilogModule(hdlChip, outputFolder)

        tstFilenames = self._GetFilesWithExtInFolder(inputFolder, 'tst')
        
        tstScripts = []
        tstsToRun  = []
        for tstFilename in tstFilenames:
            self.logger.Info("Reading %s .." % (tstFilename))
            tstFile   = TstFile(join(inputFolder, tstFilename))
            tstScript = tstFile.ParseFile()
            tstScripts.append(tstScript)

            for hdlChip in hdlChips:
                if hdlChip.chipName == tstScript.testHdlModule:
                    tstScript.testChip = hdlChip            
                    self.CreateVerilogModuleTB(tstScript, outputFolder)
                    tstsToRun.append(tstScript)

            #print(hdlChip.GetChipDependencyList())

        runSHFile   = TextFile(join(outputFolder, 'runme.sh'))
        runContents = "set -e\n"

        for tstToRun in tstsToRun: # Type: TstScript
            moduleList = self._GetVerilogDependencyFileList(tstToRun, hdlChips)

            runContents += ("echo \"Building and running test for %s\"\n" % (tstToRun.testHdlModule))
            runContents += ("iverilog -o ./out/%s %s %s\n" % (tstToRun.testHdlModule, tstToRun.testHdlModule + "_tb.v", " ".join([x for x in moduleList])))
            # iverilog -o ./out/And And_tb.v Not.v And.v Nand.v
            runContents += ("vvp ./out/%s\n" % (tstToRun.testHdlModule))
            runContents += ("diff -w ../hdl_input/%s %s\n" % (tstToRun.compareFile, tstToRun.outputFile))
            runContents += "\n"

        runSHFile.WriteFile(runContents)

        self.WriteNandV(outputFolder)
        return    

    ##########################################################################
    def _GetVerilogDependencyFileList(self, tstToRun : TstScript, hdlChips):
        # Get the direct dependencies of the chip being tested
        moduleList = tstToRun.testChip.GetChipDependencyList()

        indirectModules = ['Nand']
        # Get the indirect dependencies
        for module in moduleList: #type: list[string]
            for hdlChip in hdlChips:  #type: HdlChip
                if module == hdlChip.chipName:
                    indirectModules.extend(hdlChip.GetChipDependencyList())

        for indirectModule in indirectModules:
            if indirectModule not in moduleList:
                moduleList.append(indirectModule)

        moduleList.append(tstToRun.testHdlModule)
        moduleList = [x + ".v" for x in moduleList]

        return moduleList

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

        verilogModuleTB = VerilogModuleTB(tstScript.testHdlModule + "_tb",
                                          tstScript.testHdlModule,
                                          tstScript.testHdlModule + ".vcd",
                                          tstScript.outputFile)

        portList = []
        for inputPin in hdlChip.GetInputPinList(): #type: HdlPin
            bitStart, bitEnd = inputPin.GetPinBitRange()
            pinName = inputPin.pinName

            portList.append(VerilogPort(pinName, VerilogPortDirectionTypes.input, "", bitStart, bitEnd, inputPin.IsInternal()))
        verilogModuleTB.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            bitStart, bitEnd = outputPin.GetPinBitRange()
            pinName = outputPin.pinName

            portList.append(VerilogPort(pinName, VerilogPortDirectionTypes.output, "", bitStart, bitEnd, outputPin.IsInternal()))
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
    def CreateVerilogModule(self, hdlChip : HdlChip, outputFolder):
        verilogModGen = VerilogModuleGenerator(outputFolder)

        partList = hdlChip.GetChipPartList() #type: list[HdlChipPart]

        verilogMainModule = VerilogModule(hdlChip.chipName)

        portList = []
        for inputPin in hdlChip.GetInputPinList(): #type: HdlPin
            bitStart, bitEnd = inputPin.GetPinBitRange()
            pinName = inputPin.pinName

            portList.append(VerilogPort(pinName, VerilogPortDirectionTypes.input, "", bitStart, bitEnd, inputPin.IsInternal()))
        verilogMainModule.AddInputPorts(portList)

        portList = []
        for outputPin in hdlChip.GetOutputPinList(): #type: HdlPin
            bitStart, bitEnd = outputPin.GetPinBitRange()
            pinName = outputPin.pinName

            portList.append(VerilogPort(pinName, VerilogPortDirectionTypes.output, "", bitStart, bitEnd, outputPin.IsInternal()))
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
                pin1, pin2        = connection.GetPins()
                bitStart, bitEnd  = pin2.GetPinBitRange()
                internalParamPort = VerilogPort(pin2.pinName, VerilogPortDirectionTypes.unknown, "", bitStart, bitEnd, pin2.IsInternal())
                
                keyName = pin1.pinName + ":" + pin2.pinName
                if keyName not in pinDict:
                    pinDict[keyName] = VerilogSubmoduleCallParam(pin1.pinName, internalParamPort)
                    verilogSubmoduleCall.AddCallParam(pinDict[keyName])
                else:
                    # Handling case where input bits are made from concatinated internal variable bits
                    pinDict[keyName].IncrementBitCount()

            verilogSubmoduleCalls.append(verilogSubmoduleCall)

        verilogMainModule.AddSubmoduleCalls(verilogSubmoduleCalls)
        #verilogMainModule.DumpModuleDetails()
        #print(moduleCalls)
        verilogModGen.CreateModule(verilogMainModule)
        return

    ##########################################################################
    def _GetFilesWithExtInFolder(self, folder, ext):
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        files = [k for k in files if ext in k]
        return files