from modules.core.logger import Logger
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlChip import HdlChip

class HdlDFFChip():
    def __init__(self):
        return

    @staticmethod
    ##########################################################################
    def GetChip():
        dffChip = HdlChip()
        dffChip.SetChipName("DFF")
        dffChip.AddInputPins([HdlPin("in", HdlPinTypes.Input, "[1]")])
        dffChip.AddInputPins([HdlPin("clk", HdlPinTypes.Clk, "[1]")])
        dffChip.AddOutputPins([HdlPin("out", HdlPinTypes.Output, "[1]")])
        #dffChip.DumpChipDetails()
        return dffChip

