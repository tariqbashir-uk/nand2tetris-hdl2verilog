from modules.verilogTypes.verilogPort import VerilogPort

class VerilogSubmoduleCallParam():
    def __init__(self, portName, internalParamPort : VerilogPort, isCallPortOutput, isModuleAndParamWidthSame):
        self.portName          = portName
        self.internalParamPort = internalParamPort
        self.bitCount          = 1
        self.isCallPortOutput  = isCallPortOutput
        self.isModuleAndParamWidthSame = isModuleAndParamWidthSame
        return

    ##########################################################################
    def IsCallPortOutput(self):
        return self.isCallPortOutput

    ##########################################################################
    def IncrementBitCount(self):
        self.bitCount += 1
        return

    ##########################################################################
    def GetParamNameForCall(self):
        paramName     = ""
        paramNameList = [self.internalParamPort for i in range(self.bitCount)]

        if self.bitCount == 1:
            if self.isModuleAndParamWidthSame:
                paramName = self.internalParamPort.portName
            else:
                paramName = self.internalParamPort.GetPortStr()
        else:
            paramName += "{" 
            if self.isModuleAndParamWidthSame:
                paramName += ', '.join([x.portName for x in paramNameList])
            else:
                paramName += ', '.join([x.GetPortStr() for x in paramNameList])
            paramName += "}" 

        return paramName

    ##########################################################################
    def GetCallStr(self):
        return self.portName + " : " + self.internalParamPort.GetPortStr()