from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlConnectionTypes import HdlConnectionTypes

import modules.commonDefs as commonDefs

class HdlConnection():
    def __init__(self, pin1 : HdlPin, pin2 : HdlPin):
        self.pin1 = pin1
        self.pin2 = pin2

        self.UpdateConnectionBitWidths()
        return

    ##########################################################################
    def UpdateConnectionBitWidths(self):
        self.pin1BitIndex, self.pin1StartBitOfBus, self.pin1EndBitOfBus, self.pin1ConnectionWidth, self.pin1ConnectionType = (
            self._SetInitialPinBitParams(self.pin1))
      
        self.pin2BitIndex, self.pin2StartBitOfBus, self.pin2EndBitOfBus, self.pin2ConnectionWidth, self.pin2ConnectionType = (
            self._SetInitialPinBitParams(self.pin2))

        # Following cases we know the pin2ConnectionWidth = pin1ConnectionWidth
        if ((not self.IsConnectionToInput() and self.pin2.IsInternal()) or
            self.pin1ConnectionType.SingleBit or
            self.pin1ConnectionType.BitRange):
            self.pin2ConnectionWidth = self.pin1ConnectionWidth
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
    def GetPin1Params(self):
        return self.pin1BitIndex, self.pin1StartBitOfBus, self.pin1EndBitOfBus, self.pin1ConnectionWidth, self.pin1ConnectionType

    ##########################################################################
    def GetPin2Params(self):
        return self.pin2BitIndex, self.pin2StartBitOfBus, self.pin2EndBitOfBus, self.pin2ConnectionWidth, self.pin2ConnectionType

    ##########################################################################
    def IsConnectionToInput(self):
        return True if self.pin1.pinType == HdlPinTypes.Internal else False

    ##########################################################################
    def GetPin2ConnectionBitWidth(self):
        return self.pin2ConnectionWidth

    ##########################################################################
    def _SetInitialPinBitParams(self, pin : HdlPin):
        bitWidthString     = pin.GetPinBitWidthString()
        pinConnectionWidth = pin.bitWidth
        pinBitIndex        = commonDefs.NO_BIT_VALUE
        pinStartBitOfBus   = commonDefs.NO_BIT_VALUE
        pinEndBitOfBus     = commonDefs.NO_BIT_VALUE
        pinConnectionType  = HdlConnectionTypes.AllBits

        if bitWidthString:
            if ".." in bitWidthString:
                bitValues = bitWidthString.split("..")
                pinStartBitOfBus   = int(bitValues[0])
                pinEndBitOfBus     = int(bitValues[1])
                pinConnectionWidth = pinEndBitOfBus - pinStartBitOfBus + 1
            else:
                pinBitIndex        = int(bitWidthString)
                pinConnectionWidth = 1 

        if pinBitIndex != commonDefs.NO_BIT_VALUE:
            pinConnectionType = HdlConnectionTypes.SingleBit
        elif pinStartBitOfBus != commonDefs.NO_BIT_VALUE:
            pinConnectionType = HdlConnectionTypes.BitRange

        return pinBitIndex, pinStartBitOfBus, pinEndBitOfBus, pinConnectionWidth, pinConnectionType

    ##########################################################################
    def _GetPinExtraStr(self, pinBitIndex, pinStartBitOfBus, pinEndBitOfBus):
        pinExtraStr = ""
        if pinBitIndex != commonDefs.NO_BIT_VALUE:
            pinExtraStr += "[" + str(pinBitIndex) + "]"
        elif pinStartBitOfBus != commonDefs.NO_BIT_VALUE:
            pinExtraStr += "[" + str(pinStartBitOfBus) + ".." + str(pinEndBitOfBus) + "]"
        return pinExtraStr

