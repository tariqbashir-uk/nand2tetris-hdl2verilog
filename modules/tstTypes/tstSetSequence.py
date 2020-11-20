
from modules.tstTypes.tstSetSequenceTypes import TstSetSequenceTypes

class TstSetSequence():
    def __init__(self, sequenceType : TstSetSequenceTypes, setOperations):
        self.sequenceType  = sequenceType
        self.setOperations = setOperations
        return