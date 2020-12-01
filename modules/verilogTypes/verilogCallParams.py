class VerilogCallParams():
    def __init__(self, paramList=None):
        if not paramList:
             self.paramList = []
        else:
            self.paramList = paramList
        return

    ##########################################################################
    def AddParam(self, param):
        self.paramList.append(param)
        return

    ##########################################################################
    def GetCallStr(self):
        paramName = ""

        if len(self.paramList) > 1:  
            paramName += "{"
        paramName += ', '.join(x for x in self.paramList)
        if len(self.paramList) > 1:  
            paramName += "}"
        return paramName

    ##########################################################################
    def DumpInfo(self):
        print(self.paramList)
        return
