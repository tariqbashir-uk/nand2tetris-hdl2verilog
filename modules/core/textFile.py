from modules.core.logger import Logger

class TextFile:
    def __init__(self, filename):
        self.logger = Logger()

        self.filename = filename
        return

    ##########################################################################
    def ReadFile(self):
        fileContents = None
        inFile = open(self.filename, "r")

        if inFile:
            fileContents = inFile.read()
            inFile.close()
            
        return fileContents

    ##########################################################################
    def WriteFile(self, text):
        outFile = open(self.filename, "w")

        if outFile:
            outFile.write(text)
            outFile.close()
            
        return