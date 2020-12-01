
from modules.tstTypes.tstSetSequenceTypes import TstSetSequenceTypes

class TstSetSequence():
    def __init__(self, sequenceType : TstSetSequenceTypes, setOperation):
        self.sequenceType = sequenceType
        self.setOperation = setOperation
        return