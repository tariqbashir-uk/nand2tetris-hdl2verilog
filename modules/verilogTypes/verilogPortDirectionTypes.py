from enum import Enum

class VerilogPortDirectionTypes(Enum):
    input    = 1
    output   = 2
    inout    = 3
    unknown  = 4

    def __str__(self):
        return self.name

    def GetValue(self):
        return str(self.value)