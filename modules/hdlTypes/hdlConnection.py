from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

class HdlConnection():
    def __init__(self, pin1 : HdlPin, pin2 : HdlPin):
        self.pin1 = pin1
        self.pin2 = pin2
        return

    ##########################################################################
    def GetPins(self):
        return self.pin1, self.pin2

    ##########################################################################
    def GetPinStr(self):
        return ("[%s : %s (%s)]" % (self.pin1.pinName, self.pin2.GetPortStr(), self.pin2.pinType)) 