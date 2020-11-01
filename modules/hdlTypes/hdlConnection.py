from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

import modules.commonDefs as commonDefs

class HdlConnection():
    def __init__(self, pin1 : HdlPin, pin2 : HdlPin):
        self.pin1 = pin1
        self.pin2 = pin2

        self.pin1BitIndex, self.pin1StartBitOfBus, self.pin1EndBitOfBus = (
            self._SetPinBitParams(self.pin1.GetPinBitWidthString()))
      
        self.pin2BitIndex, self.pin2StartBitOfBus, self.pin2EndBitOfBus = (
            self._SetPinBitParams(self.pin2.GetPinBitWidthString()))
        return

    ##########################################################################
    def GetPins(self):
        return self.pin1, self.pin2

    ##########################################################################
    def GetPinStr(self):
        pin1Name  = self.pin1.pinName
        pin1Extra = self._GetPinExtraStr(self.pin1BitIndex, self.pin1StartBitOfBus, self.pin1EndBitOfBus)

        pin2Name  = self.pin2.pinName        
        pin2Extra = self._GetPinExtraStr(self.pin2BitIndex, self.pin2StartBitOfBus, self.pin2EndBitOfBus)

        return ("[%s%s : %s%s (%s)]" % (pin1Name, pin1Extra, pin2Name, pin2Extra, self.pin2.pinType))

    ##########################################################################
    def _SetPinBitParams(self, bitWidthString):
        pinBitIndex      = commonDefs.NO_BIT_VALUE
        pinStartBitOfBus = commonDefs.NO_BIT_VALUE
        pinEndBitOfBus   = commonDefs.NO_BIT_VALUE

        if bitWidthString:
            if ".." in bitWidthString:
                bitValues = bitWidthString.split("..")
                pinStartBitOfBus = int(bitValues[0])
                pinEndBitOfBus   = int(bitValues[1])
            else:
                pinBitIndex      = int(bitWidthString)   

        return pinBitIndex, pinStartBitOfBus, pinEndBitOfBus

    ##########################################################################
    def _GetPinExtraStr(self, pinBitIndex, pinStartBitOfBus, pinEndBitOfBus):
        pinExtraStr = ""
        if pinBitIndex != commonDefs.NO_BIT_VALUE:
            pinExtraStr += "[" + str(pinBitIndex) + "]"
        elif pinStartBitOfBus != commonDefs.NO_BIT_VALUE:
            pinExtraStr += "[" + str(pinStartBitOfBus) + ".." + str(pinEndBitOfBus) + "]"
        return pinExtraStr

