class TstOutputParam():
    def __init__(self, paramName, paramFormat):
        self.paramName   = paramName
        self.paramFormat = paramFormat
        return

    ##########################################################################
    def GetParamName(self):
        return self.paramName

    ##########################################################################
    def GetVerilogFormat(self):
        return ("%%%s" % (self.paramFormat[0].casefold()))