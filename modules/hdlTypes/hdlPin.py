from modules.hdlTypes.hdlPinTypes import HdlPinTypes

class HdlPin():
    def __init__(self, pinName, pinType=HdlPinTypes.Unknown, bitWidth="1"):
        self.pinName  = pinName
        self.pinType  = pinType  #Type: HdlPinTypes
        self.bitWidth = bitWidth
        return

    ##########################################################################
    def IsInternal(self):
        return True if self.pinType == HdlPinTypes.Internal else False

    ##########################################################################
    def GetPinBitRange(self):
        bitStart = -1
        bitEnd   = -1
        
        if self.bitWidth:
            bitWdith = self.bitWidth.replace("[", "").replace("]", "")
            if ".." in bitWdith:
                b = bitWdith.split("..")
                bitStart = int(b[1])
                bitEnd   = int(b[0])
            else:
                bitStart = int(bitWdith)

        return bitStart, bitEnd

    ##########################################################################
    def GetPortStr(self, isDefinition=False):
        bitStart, bitEnd = self.GetPinBitRange()
        pinBit = ""
        if isDefinition:
            if bitStart != -1:
                pinBit += "[" + str(bitStart)
        else:
            if bitStart != -1:
                pinBit += "[" + str(bitStart)
            if bitEnd != -1:
                pinBit += ".." + str(bitEnd)

        if len(pinBit) > 0:
            pinBit += "]"

        return self.pinName + pinBit