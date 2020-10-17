from modules.verilogTypes.verilogSubmoduleCallParam import VerilogSubmoduleCallParam

class VerilogSubmoduleCall():
    def __init__(self, submoduleName, submoduleNumber):
        self.submoduleName   = submoduleName
        self.submoduleNumber = submoduleNumber
        self.callParams      = []
        return

    ##########################################################################
    def GetModuleName(self):
        return self.submoduleName

    ##########################################################################
    def GetModuleCallName(self):
        return ("%s_%d" % (self.submoduleName.lower(), self.submoduleNumber))

    ##########################################################################
    def AddCallParam(self, callParams):
        self.callParams.append(callParams)
        return

    ##########################################################################
    def GetCallParams(self):
        return self.callParams

    ##########################################################################
    def GetCallParamsStr(self):
        return ', '.join([str(x.GetCallStr()) for x in self.callParams])