from modules.parser.tstParser import TstParser
from modules.core.textFile import TextFile

class TstFile(TextFile):
    def __init__(self, hdlFilename):
        TextFile.__init__(self, hdlFilename)

        self.tstParser = TstParser()
        return

    ##########################################################################
    def ParseFile(self):
        fileContents = self.ReadFile() 
        return self.tstParser.Parse(fileContents)