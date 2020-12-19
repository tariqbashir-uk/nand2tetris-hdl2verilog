from modules.parser.verilogModuleParser import VerilogModuleParser
from modules.core.textFile import TextFile

class VerilogFile(TextFile):
    def __init__(self, verilogFilename):
        TextFile.__init__(self, verilogFilename)

        self.verilogModuleParser = VerilogModuleParser()
        return

    ##########################################################################
    def ParseFile(self):
        fileContents  = self.ReadFile()
        verilogModule = self.verilogModuleParser.Parse(fileContents)
        verilogModule.SetModuleFilename(self.filename)
        return verilogModule