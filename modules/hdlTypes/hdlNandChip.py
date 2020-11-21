from modules.core.logger import Logger
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlChip import HdlChip

class HdlNandChip():
    def __init__(self):
        return

    @staticmethod
    ##########################################################################
    def GetChip():
        nandChip = HdlChip()
        nandChip.SetChipName("Nand")
        nandChip.AddInputPins([HdlPin("a", HdlPinTypes.Input, None)])
        nandChip.AddInputPins([HdlPin("b", HdlPinTypes.Input, None)])
        nandChip.AddOutputPins([HdlPin("out", HdlPinTypes.Output, None)])
        #nandChip.DumpChipDetails()
        return nandChip

