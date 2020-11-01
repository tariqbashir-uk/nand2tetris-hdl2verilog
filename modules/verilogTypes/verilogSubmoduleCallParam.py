from modules.verilogTypes.verilogPort import VerilogPort

import modules.commonDefs as commonDefs

class VerilogSubmoduleCallParam():
    def __init__(self, 
                 subModulePort : VerilogPort,
                 internalParamPort : VerilogPort,
                 startBitOfBus = commonDefs.NO_BIT_VALUE,
                 endBitOfBus   = commonDefs.NO_BIT_VALUE,
                 bitIndex      = commonDefs.NO_BIT_VALUE):

        self.subModulePort     = subModulePort
        self.internalParamPort = internalParamPort
        self.bitCount          = 1

        self.startBitOfBus = startBitOfBus
        self.endBitOfBus   = endBitOfBus
        self.bitIndex      = bitIndex               
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
            if self.bitIndex == commonDefs.NO_BIT_VALUE:
                paramName = self.internalParamPort.portName
            else:
                paramName = self.internalParamPort.portName + "[" + str(self.bitIndex) + "]"
        else:
            paramName += "{" 
            if self.bitIndex == commonDefs.NO_BIT_VALUE:
                paramName += ', '.join([x.portName for x in paramNameList])
            else:
                paramName += ', '.join([x.portName + "[" + str(self.bitIndex) + "]" for x in paramNameList])
                #paramName += ', '.join([x.GetPortStr() for x in paramNameList])
            paramName += "}" 

        return paramName

    ##########################################################################
    def GetCallStr(self):
        paramStr = self.internalParamPort.portName
        if self.bitIndex != commonDefs.NO_BIT_VALUE:
            paramStr += "[" + str(self.bitIndex) + "]"

        return self.subModulePort.portName + " : " + paramStr