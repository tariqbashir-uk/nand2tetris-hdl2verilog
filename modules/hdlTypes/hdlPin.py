from modules.hdlTypes.hdlPinTypes import HdlPinTypes

import modules.commonDefs as commonDefs

class HdlPin():
    def __init__(self, pinName, pinType=HdlPinTypes.Unknown, bitWidthString=None):
        self.pinName        = pinName
        self.pinType        = pinType  # type: HdlPinTypes
        self.bitWidthString = bitWidthString
        self.bitWidth       = commonDefs.NO_BIT_VALUE
        self.startBitOfBus  = commonDefs.NO_BIT_VALUE
        self.endBitOfBus    = commonDefs.NO_BIT_VALUE

        bitWidthStr = self.GetPinBitWidthString()
        if bitWidthStr and not ".." in bitWidthStr:
            self.bitWidth = int(bitWidthStr)
        return

    ##########################################################################
    def IsOutput(self):
        return True if self.pinType == HdlPinTypes.Output else False

    ##########################################################################
    def IsInternal(self):
        return True if self.pinType == HdlPinTypes.Internal else False

    ##########################################################################
    def GetPinStr(self):
        pinStr = self.pinName

        if self.bitWidth > 1:
            pinStr += "[" + str(self.bitWidth) + "]"
        return pinStr

    ##########################################################################
    def GetPinBitWidth(self):
        return self.bitWidth

    ##########################################################################
    def GetPinBitWidthString(self):
        if self.bitWidthString:
            return self.bitWidthString.replace("[", "").replace("]", "")
        else:
            return None