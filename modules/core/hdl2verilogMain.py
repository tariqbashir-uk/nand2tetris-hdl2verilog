from os.path import isfile, join
from os import listdir
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
        hdlStoreFolder = join(outputFolder, settings.HDL_STORE_FOLDER)
        self.fileActions.CreateFolderIfNeeded(hdlStoreFolder)

        verilogModuleList = VerilogModuleList(builtInChipFolder)
        verilogFilenames = [join(builtInChipFolder, x) for x in self._GetFilesWithExtInFolder(builtInChipFolder, '.v')]
        for verilogFilename in verilogFilenames:
            self.logger.Info("Reading %s .." % (verilogFilename))
            verilogFile   = VerilogFile(verilogFilename)
            verilogModule = verilogFile.ParseFile()
            verilogModuleList.AddBuiltInModule(verilogModule)

        hdlChipList  = HdlChipList()
        hdlFilenames = [join(builtInChipFolder, x) for x in self._GetFilesWithExtInFolder(builtInChipFolder, '.hdl')]
        for hdlFilename in hdlFilenames:
            self.logger.Info("Reading %s .." % (hdlFilename))
            hdlFile = HdlFile(hdlFilename)
            hdlChip = hdlFile.ParseFile()
            hdlChipList.AddBuiltInChip(hdlChip)

        hdlFilenames = [join(inputFolder, x) for x in self._GetFilesWithExtInFolder(inputFolder, '.hdl')]
        for hdlFilename in hdlFilenames:
            self.logger.Info("Reading %s .." % (hdlFilename))
            hdlFile = HdlFile(hdlFilename)
            hdlChip = hdlFile.ParseFile()
            hdlChipList.AddChip(hdlChip)

        if not self.CheckChipDependencies(hdlChipList, verilogModuleList):
            return

        hdlChipList.CheckAndAddClockInputs()
        hdlChipList.UpdateAllPinBitWidths()
        hdlChipList.UpdateAllPartConnections()

        for hdlChip in hdlChipList.chipList:  
            self.mapper.CreateVerilogModule(hdlChip, hdlChipList, verilogModuleList)

        tstFilenames = self._GetFilesWithExtInFolder(inputFolder, '.tst')
        
        tstScripts = []
        tstsToRun  = []
        for tstFilename in tstFilenames:
            testName, ext = self.fileActions.GetFileNameAndExt(tstFilename)
            self.logger.Info("Reading %s .." % (tstFilename))
            tstFile   = TstFile(join(inputFolder, tstFilename))
            tstScript = tstFile.ParseFile(testName)
            tstScripts.append(tstScript)

            tstScript.testChip = hdlChipList.GetChip(tstScript.testHdlModule)            
            self.mapper.CreateVerilogModuleTB(tstScript, outputFolder)
            tstsToRun.append(tstScript)

        runSHFile   = TextFile(join(outputFolder, 'runme.sh'))
        runContents = "set -e\n"
        runContents += "\n"
        runContents += "if [[ ! -d ./out ]]; then\n"
        runContents += "  mkdir out\n"
        runContents += "fi\n"
        runContents += "\n"

        verboseFlag = ""
        #verboseFlag = "-v -u -Wall"
        for tstToRun in tstsToRun: # type: TstScript
            moduleList   = hdlChipList.GetChipDependencyList(tstToRun.testChip)
            filenameList = verilogModuleList.GetFilenamesForModules(moduleList)

            runContents += ("echo \"Building and running test for %s\"\n" % (tstToRun.testName))
            runContents += ("iverilog %s -o ./out/%s %s %s\n" % (verboseFlag, tstToRun.testName, tstToRun.testName + "_tb.v", " ".join([x for x in filenameList])))
            runContents += ("vvp ./out/%s\n" % (tstToRun.testName))
            runContents += ("diff -w %s/%s %s\n" % (self.fileActions.GetAbsoluteFilename(inputFolder), tstToRun.compareFile, tstToRun.outputFile))
            runContents += "\n"

        runSHFile.WriteFile(runContents)

        # Do this last
        verilogModuleList.WriteModules(outputFolder)
        return    

    ##########################################################################
    def CheckChipDependencies(self, hdlChipList, verilogModuleList):
        passed = True
        missingChipList, builtInChipsUsedList = hdlChipList.CheckChipDependencies()
        
        if len(missingChipList) > 0:
            self.logger.Error("Missing chips detected! Following dependencies were not found in the input folder or built-in chip folder: %s" % (missingChipList))
            passed = False

        if len(builtInChipsUsedList) > 0:
            missingBuiltInModuleList = verilogModuleList.CheckModulesInBuiltInList(builtInChipsUsedList)

            if len(missingBuiltInModuleList) > 0:
                self.logger.Error("Missing built-in verilog modules detected! Following expected built-in modules were not found in the built-in chip folder: %s" % (missingBuiltInModuleList))
                passed = False

        return passed

    ##########################################################################
    def _GetFilesWithExtInFolder(self, folder, ext):
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        files = [k for k in files if ext in k]
        return files