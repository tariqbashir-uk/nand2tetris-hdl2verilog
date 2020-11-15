from enum import Enum

class HdlConnectionTypes(Enum):
    AllBits   = 1
    SingleBit = 2
    BitRange  = 3

    def __str__(self):
        return self.name

    def GetValue(self):
        return str(self.value)