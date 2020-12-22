from os.path import join
from modules.core.fileActions import FileActions
from modules.core.logger import Logger

from modules.core.textFile import TextFile

from modules.fileHandlers.tstFile import TstFile
from modules.fileHandlers.hdlFile import HdlFile
from modules.fileHandlers.verilogFile import VerilogFile
from modules.core.hdlChipList import HdlChipList
from modules.core.verilogModuleList import VerilogModuleList
from modules.verilogTypes.verilogModule import VerilogModule
from modules.mappers.hdlToVerilogMapper import HdlToVerilogMapper
from modules.scriptGenerators.iVerilogScriptGenerator import IVerilogScriptGenerator

import modules.settings as settings
import modules.commonDefs as commonDefs

class Hdl2verilogMain():
    def __init__(self):
        self.logger      = Logger()
        self.fileActions = FileActions()
        self.mapper      = HdlToVerilogMapper()
        return

    ##########################################################################
    def Run(self, inputFolder, builtInChipFolder, outputFolder):
        verilogModuleList = VerilogModuleList(builtInChipFolder)
        # Read in the built-in Verilog modules
        verilogFilenames = [join(builtInChipFolder, x) for x in self.fileActions.GetFilesWithExtInFolder(builtInChipFolder, '.v')]
        for verilogFilename in verilogFilenames:
            self.logger.Info("Reading %s .." % (verilogFilename))
            verilogFile   = VerilogFile(verilogFilename)
            verilogModule = verilogFile.ParseFile()
            verilogModuleList.AddBuiltInModule(verilogModule)

        hdlChipList  = HdlChipList()
        # Read in the built-in HDL chips
        hdlFilenames = [join(builtInChipFolder, x) for x in self.fileActions.GetFilesWithExtInFolder(builtInChipFolder, '.hdl')]
        for hdlFilename in hdlFilenames:
            self.logger.Info("Reading %s .." % (hdlFilename))
            hdlFile = HdlFile(hdlFilename)
            hdlChip = hdlFile.ParseFile()
            hdlChipList.AddBuiltInChip(hdlChip)

        # Read in the input HDL chips to be converted
        hdlFilenames = [join(inputFolder, x) for x in self.fileActions.GetFilesWithExtInFolder(inputFolder, '.hdl')]
        for hdlFilename in hdlFilenames:
            self.logger.Info("Reading %s .." % (hdlFilename))
            hdlFile = HdlFile(hdlFilename)
            hdlChip = hdlFile.ParseFile()
            hdlChipList.AddChip(hdlChip)

        result, builtInChipsUsedList = self.CheckChipDependencies(hdlChipList, verilogModuleList)
        if not result:
            return

        hdlChipList.CheckAndAddClockInputs()
        hdlChipList.UpdateAllPinBitWidths()
        hdlChipList.UpdateAllPartConnections()

        # Create the Verilog Modules from input HDL chips
        for hdlChip in hdlChipList.chipList:  
            self.mapper.CreateVerilogModule(hdlChip, hdlChipList, verilogModuleList)

        # Read-in the Tst files and create the Verilog Testbench Modules
        tstsToRun    = []
        tstFilenames = self.fileActions.GetFilesWithExtInFolder(inputFolder, '.tst')        
        for tstFilename in tstFilenames:
            testName, ext = self.fileActions.GetFileNameAndExt(tstFilename)
            self.logger.Info("Reading %s .." % (tstFilename))
            tstFile   = TstFile(join(inputFolder, tstFilename))
            tstScript = tstFile.ParseFile(testName)

            tstScript.testChip = hdlChipList.GetChip(tstScript.testHdlModule)            
            self.mapper.CreateVerilogModuleTB(tstScript, outputFolder)
            tstsToRun.append(tstScript)

        verilogModuleList.WriteModules(outputFolder)
        verilogModuleList.CopyInternalModules(outputFolder, builtInChipsUsedList)

        ivlScriptGen = IVerilogScriptGenerator(outputFolder)
        ivlScriptGen.CreateScript(inputFolder, tstsToRun, hdlChipList, verilogModuleList)
        return    

    ##########################################################################
    def CheckChipDependencies(self, hdlChipList, verilogModuleList):
        passed = True
        missingChipList, builtInChipsUsedList, noimplementationChipList = hdlChipList.CheckChipDependencies()
        
        if len(missingChipList) > 0:
            self.logger.Error("Missing chips detected! Following dependencies were not found in the input folder or built-in chip folder: %s" % (missingChipList))
            passed = False

        if len(builtInChipsUsedList) > 0:
            missingBuiltInModuleList = verilogModuleList.CheckModulesInBuiltInList(builtInChipsUsedList)

            if len(missingBuiltInModuleList) > 0:
                self.logger.Error("Missing built-in verilog modules detected! Following expected built-in modules were not found in the built-in chip folder: %s" % (missingBuiltInModuleList))
                passed = False

        if len(noimplementationChipList) > 0:
            self.logger.Error("Some HDL chips are missing implementation! Please check the following HDL chips run and pass tests using the nand2tetris HardwareSimulator : %s" % (noimplementationChipList))
            passed = False

        return passed, builtInChipsUsedList