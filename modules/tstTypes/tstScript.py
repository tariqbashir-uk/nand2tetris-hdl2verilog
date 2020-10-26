from modules.core.logger import Logger
from modules.tstTypes.tstSetSequence import TstSetSequence
from modules.tstTypes.tstSetOperation import TstSetOperation

class TstScript():
    def __init__(self):
        self.logger           = Logger()
        self.testName         = None
        self.testHdlModule    = None
        self.outputFile       = None
        self.compareFile      = None
        self.testChip         = None
        self.outputFormatList = []
        self.setSequences     = []
        return

    ##########################################################################
    def AddSetSequence(self, setSequence):
        self.setSequences.append(setSequence)
        return

    ##########################################################################
    def SetOutputFormat(self, outputFormatList):
        self.outputFormatList = outputFormatList
        return

    ##########################################################################
    def DumpTestDetails(self):
        self.logger.Debug("***** START: %s Test Script *****" % (self.testName))
        self.logger.Debug("Test module:   %s" % (self.testHdlModule))
        self.logger.Debug("Output file:   %s" % (self.outputFile))
        self.logger.Debug("Compare file:  %s" % (self.compareFile))
        self.logger.Debug("Output format: %s" % (', '.join(self.outputFormatList)))

        sequenceNumber = 1
        for setSequence in self.setSequences: #Type: TstSetSequence
            self.logger.Debug("  Sequence: %d" % (sequenceNumber))
            for setOperation in setSequence.setOperations: #Type: TstSetOperation
                self.logger.Debug("    Operation: %s = %s" % (setOperation.pinName, setOperation.pinValue))
            sequenceNumber += 1

        self.logger.Debug("***** END:   %s Test Script  *****" % (self.testName))
        return    