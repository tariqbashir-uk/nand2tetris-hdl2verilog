from modules.parser.hdlParser import HdlParser
from modules.core.textFile import TextFile

class HdlFile(TextFile):
    def __init__(self, hdlFilename):
        TextFile.__init__(self, hdlFilename)

        self.hdlParser = HdlParser()
        return

    ##########################################################################
    def ParseFile(self):
        fileContents = self.ReadFile() 
        hdlChip = self.hdlParser.Parse(fileContents)
        hdlChip.SetChipFilename(self.filename)
        return hdlChip