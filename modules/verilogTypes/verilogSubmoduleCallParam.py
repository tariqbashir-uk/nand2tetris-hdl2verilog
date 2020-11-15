from modules.verilogTypes.verilogPort import VerilogPort

import modules.commonDefs as commonDefs

class VerilogSubmoduleCallParam():
    def __init__(self, toPort : VerilogPort, fromPort : VerilogPort, paramList):
        self.toPort    = toPort
        self.fromPort  = fromPort
        self.paramList = paramList
        return

    ##########################################################################
    def IsFromPortInternal(self):
        return True if self.fromPort and self.fromPort.IsInternal() else False

    ##########################################################################
    def GetParamNameForCall(self):
        paramName = ""

        if len(self.paramList) > 1:  
            paramName += "{"
        paramName += ', '.join(x for x in self.paramList)
        if len(self.paramList) > 1:  
            paramName += "}"
        return paramName

    ##########################################################################
    def GetCallStr(self):
        return self.fromPort.portName