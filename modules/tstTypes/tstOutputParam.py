import re

class TstOutputParam():
    def __init__(self, paramName, paramFormatLMargin, paramWidth, paramRMargin):
        self.paramName    = paramName
        self.paramFormat  = re.findall('\d+|\D+', paramFormatLMargin)[0]
        self.paramLMargin = re.findall('\d+|\D+', paramFormatLMargin)[1]
        self.paramWidth   = paramWidth
        self.paramRMargin = paramRMargin
        return

    ##########################################################################
    def GetParamName(self):
        return self.paramName

    ##########################################################################
    def GetParamWidth(self):
        return self.paramWidth

    ##########################################################################
    def GetVerilogFormat(self):
        return ("%%%s" % (self.paramFormat.casefold()))