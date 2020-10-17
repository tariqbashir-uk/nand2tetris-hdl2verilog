from modules.verilogTypes.verilogPort import VerilogPort

class VerilogSubmoduleCallParam():
    def __init__(self, portName, internalParamPort : VerilogPort):
        self.portName          = portName
        self.internalParamPort = internalParamPort
        self.bitCount          = 1
        return

    ##########################################################################
    def IncrementBitCount(self):
        self.bitCount += 1
        return

    ##########################################################################
    def GetParamNameForCall(self):
        paramName     = ""
        paramNameList = [self.internalParamPort for i in range(self.bitCount)]

        if self.bitCount == 1:
            paramName = self.internalParamPort.GetPortStr()
        else:
            paramName += "{" 
            paramName += ', '.join([x.GetPortStr() for x in paramNameList])
            paramName += "}" 

        return paramName

    ##########################################################################
    def GetCallStr(self):
        return self.portName + " : " + self.internalParamPort.GetPortStr()