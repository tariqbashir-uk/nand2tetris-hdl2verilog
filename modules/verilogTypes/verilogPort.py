from modules.verilogTypes.verilogPortDirectionTypes import VerilogPortDirectionTypes

class VerilogPort():
    def __init__(self, portName, portDirection, portDataType, portBitStart, portBitEnd, isInternalPort):
        self.portName       = portName
        self.portDirection  = portDirection #Type: VerilogPortDirectionTypes
        self.portDataType   = portDataType  
        self.portBitStart   = portBitStart
        self.portBitEnd     = portBitEnd
        self.isInternalPort = isInternalPort
        return

    ##########################################################################
    def IsInternal(self):
        return self.isInternalPort

    ##########################################################################
    def GetPortStr(self, isDefinition=False):
        portBit = ""
        if isDefinition:
            if self.portBitStart != -1:
                portBit += "[" + str(self.portBitStart - 1)
            if isDefinition and self.portBitStart != -1:
                portBit += ":0"
        else:
            if self.portBitStart != -1:
                portBit += "[" + str(self.portBitStart)
            if self.portBitEnd != -1:
                portBit += ":" + str(self.portBitEnd)

        if len(portBit) > 0:
            portBit += "]"

        if isDefinition:
            return portBit + " " + self.portName
        else:
            return self.portName + portBit
