from modules.verilogTypes.verilogPort import VerilogPort
from modules.verilogTypes.verilogCallParams import VerilogCallParams

import modules.commonDefs as commonDefs

class VerilogSubmoduleCallParam():
    def __init__(self, toPort : VerilogPort, fromPort : VerilogPort, callParamList : VerilogCallParams):
        self.toPort        = toPort
        self.fromPort      = fromPort
        self.callParamList = callParamList
        return

    ##########################################################################
    def IsFromPortInternal(self):
        return True if self.fromPort and self.fromPort.IsInternal() else False

    ##########################################################################
    def GetStrForCall(self):
        return self.callParamList.GetCallStr()

    ##########################################################################
    def GetCallStr(self):
        return self.fromPort.portName