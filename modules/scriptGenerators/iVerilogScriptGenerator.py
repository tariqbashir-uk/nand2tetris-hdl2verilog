from os.path import join
from modules.core.fileActions import FileActions
from modules.core.logger import Logger

from modules.core.textFile import TextFile
import modules.settings as settings

class IVerilogScriptGenerator():
    def __init__(self, outputFolder):
        self.logger       = Logger()
        self.fileActions  = FileActions()
        self.outputFolder = outputFolder
        return

    ##########################################################################
    def CreateScript(self, inputFolder, tstsToRun, hdlChipList, verilogModuleList):
        runmeFilename = join(self.outputFolder, 'runme.sh')
        runSHFile    = TextFile(runmeFilename)
        runContents  = "set -e\n"
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
        self.fileActions.MakeExecutable(runmeFilename)
        return
