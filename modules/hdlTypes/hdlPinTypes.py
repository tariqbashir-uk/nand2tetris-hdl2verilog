from enum import Enum

class HdlPinTypes(Enum):
    Input    = 1
    Output   = 2
    Internal = 3
    Unknown  = 4

    def __str__(self):
        return self.name

    def GetValue(self):
        return str(self.value)