from enum import Enum

class TstSetSequenceTypes(Enum):
    eval   = 1
    tick   = 2
    tock   = 3
    set    = 4
    output = 5

    def __str__(self):
        return self.name

    def GetValue(self):
        return str(self.value)