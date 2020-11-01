from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

import modules.commonDefs as commonDefs

class HdlConnection():
    def __init__(self, pin1 : HdlPin, pin2 : HdlPin):
        self.pin1 = pin1
        self.pin2 = pin2

        self.pin2BitIndex      = commonDefs.NO_BIT_VALUE
        self.pin2StartBitOfBus = commonDefs.NO_BIT_VALUE
        self.pin2EndBitOfBus   = commonDefs.NO_BIT_VALUE

        bitWidthString = self.pin2.GetPinBitWidthString()
        if bitWidthString:
            if ".." in bitWidthString:
                bitValues = bitWidthString.split("..")
                self.pin2StartBitOfBus = int(bitValues[0])
                self.pin2EndBitOfBus   = int(bitValues[1])
            else:
                self.pin2BitIndex      = int(bitWidthString)         
        return

    ##########################################################################
    def GetPins(self):
        return self.pin1, self.pin2

    ##########################################################################
    def GetPinStr(self):
        pin1Name  = self.pin1.pinName
        pin2Name  = self.pin2.pinName
        pin2Extra = ""

        if self.pin2BitIndex != commonDefs.NO_BIT_VALUE:
            pin2Extra += "[" + str(self.pin2BitIndex) + "]"
        elif self.pin2StartBitOfBus != commonDefs.NO_BIT_VALUE:
            pin2Extra += "[" + str(self.pin2StartBitOfBus) + ".." + str(self.pin2EndBitOfBus) + "]"

        return ("[%s : %s%s (%s)]" % (pin1Name, pin2Name, pin2Extra, self.pin2.pinType)) 