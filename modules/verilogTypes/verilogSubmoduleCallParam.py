from modules.verilogTypes.verilogPort import VerilogPort
from modules.core.logger import Logger

import modules.commonDefs as commonDefs

class VerilogSubmoduleCallParam():
    def __init__(self, toPort : VerilogPort, fromPort):

        self.toPort     = toPort
        self.fromPort   = fromPort
        self.bitMapping = None
        self.logger     = Logger()
        return

    ##########################################################################
    def AddAllBitMapping(self, fromName):
        if not self.bitMapping:
            self.bitMapping = [fromName] * 1
        return

    ##########################################################################
    def AddMultiBitMapping(self, fromName):
        if not self.bitMapping:
            self.bitMapping = []
        self.bitMapping.append(fromName)
        return

    ##########################################################################
    def AddSingleBitMapping(self, bitNumber, fromName):
        if not self.bitMapping:
            self.bitMapping = ["false"] * self.toPort.portBitWidth
        
        if bitNumber >= len(self.bitMapping):
            self.logger.Error("SubmoduleCallParam %s: Portwidth = %d, but trying to set single bit number %d" % 
                               (self.toPort.portName, self.toPort.portBitWidth, bitNumber))
        else:
            self.bitMapping[len(self.bitMapping) - bitNumber - 1] = fromName
        return

    ##########################################################################
    def IsFromPortInternal(self):
        return True if self.fromPort and self.fromPort.IsInternal() else False

    ##########################################################################
    def GetParamNameForCall(self):
        paramName = ""

        if self.bitMapping and len(self.bitMapping) == 1:
            paramName += self.bitMapping[0]
        elif self.bitMapping:
            paramName += "{"
            paramName += ', '.join(x for x in self.bitMapping)
            paramName += "}"
        return paramName

    ##########################################################################
    def GetCallStr(self):
        return self.fromPort.portName