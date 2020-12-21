import os
from modules.core.logger import Logger

class TextFile:
    def __init__(self, filename):
        self.logger = Logger()

        self.fullFilename = filename
        self.filepath, self.filename = os.path.split(filename)
        return

    ##########################################################################
    def ReadFile(self):
        fileContents = None
        inFile = open(self.fullFilename, "r")

        if inFile:
            fileContents = inFile.read()
            inFile.close()
            
        return fileContents

    ##########################################################################
    def WriteFile(self, text):
        outFile = open(self.fullFilename, "w")

        if outFile:
            outFile.write(text)
            outFile.close()
            
        return