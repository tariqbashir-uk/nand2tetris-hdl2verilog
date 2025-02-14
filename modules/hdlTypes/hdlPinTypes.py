from enum import Enum

class HdlPinTypes(Enum):
    Input    = 1
    Output   = 2
    Internal = 3
    Clk      = 4
    Unknown  = 5

    def __str__(self):
        return self.name

    def GetValue(self):
        return str(self.value)