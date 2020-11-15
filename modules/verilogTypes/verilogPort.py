from modules.verilogTypes.verilogPortDirectionTypes import VerilogPortDirectionTypes

class VerilogPort():
    def __init__(self, portName, portDirection, portDataType, portBitWidth, isInternalPort):
        self.portName       = portName
        self.portDirection  = portDirection #Type: VerilogPortDirectionTypes
        self.portDataType   = portDataType  
        self.portBitWidth   = portBitWidth
        self.isInternalPort = isInternalPort
        return

    ##########################################################################
    def IsInternal(self):
        return self.isInternalPort

    ##########################################################################
    def GetPortStr(self):
        portStr = ""

        if self.portBitWidth > 1:
            portStr += "[" + str(self.portBitWidth - 1) + ":0] "
        return portStr + self.portName