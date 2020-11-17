from os.path import isfile, join
from os import listdir
from modules.core.fileActions import FileActions
from modules.core.logger import Logger

from modules.core.textFile import TextFile

from modules.fileHandlers.tstFile import TstFile
from modules.fileHandlers.hdlFile import HdlFile
from modules.hdlTypes.hdlChipList import HdlChipList
from modules.verilogTypes.verilogNandModule import VerilogNandModule
from modules.verilogTypes.verilogDFFModule import VerilogDFFModule
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

        hdlChipList.UpdateAllPinBitWidths()
        hdlChipList.UpdateAllPartConnections()

        for hdlChip in hdlChipList.chipList:  
            self.mapper.CreateVerilogModule(hdlChip, hdlChipList, outputFolder)

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
            self.mapper.CreateVerilogModuleTB(tstScript, outputFolder)
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
            runContents += ("diff -w %s/%s %s\n" % (self.fileActions.GetAbsoluteFilename(inputFolder), tstToRun.compareFile, tstToRun.outputFile))
            runContents += "\n"

        runSHFile.WriteFile(runContents)

        VerilogNandModule.WriteModule(outputFolder)
        VerilogDFFModule.WriteModule(outputFolder)
        return    

    ##########################################################################
    def _GetFilesWithExtInFolder(self, folder, ext):
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        files = [k for k in files if ext in k]
        return files