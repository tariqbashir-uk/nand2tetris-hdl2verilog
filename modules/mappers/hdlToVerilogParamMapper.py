from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort

class HdlToVerilogParamMapper():
    def __init__(self, toPort : VerilogPort, fromPort : VerilogPort):
        self.toPort         = toPort
        self.fromPort       = fromPort
        self.paramList      = []
        self.bitsMappedList = [0] * toPort.portBitWidth
        self.logger         = Logger()
        return

    ##########################################################################
    def AddAllBitMapping(self, fromName, bitWidth):
        for i in range(0, len(self.bitsMappedList)):
            verilogBitNumber = self._HdlBitNumberToVerilog(i, self.toPort.portBitWidth)
            self.bitsMappedList[verilogBitNumber] = 1
 
        if not self.paramList:
            self.paramList = []

        self.paramList.insert(0, fromName)
        return

    ##########################################################################
    def AddMultiBitMapping(self, fromName, fromBit, toBit):
        if toBit >= len(self.bitsMappedList):
            self.logger.Error("SubmoduleCallParam %s: Portwidth = %d, len bits mapped list = %d, but trying to set bits from %d to %d" % 
                               (self.toPort.portName, self.toPort.portBitWidth, len(self.bitsMappedList), fromBit, toBit))

        for i in range(fromBit, toBit + 1):
            verilogBitNumber = self._HdlBitNumberToVerilog(i, self.toPort.portBitWidth)
            self.bitsMappedList[verilogBitNumber] = 1
        #print("%d, %d" % (fromBit, toBit))
        #print(self.bitsMappedList)
 
        if not self.paramList:
            self.paramList = []

        self.paramList.insert(0, fromName)
        return

    ##########################################################################
    def AddSingleBitMapping(self, hdlBitNumber, fromName):
        verilogBitNumber = self._HdlBitNumberToVerilog(hdlBitNumber, self.toPort.portBitWidth)
        self.bitsMappedList[verilogBitNumber] = 1

        if not self.paramList:
            self.paramList = ["false"] * self.toPort.portBitWidth
        
        if verilogBitNumber >= len(self.paramList):
            self.logger.Error("SubmoduleCallParam %s: Portwidth = %d, but trying to set single bit number %d" % 
                               (self.toPort.portName, self.toPort.portBitWidth, verilogBitNumber))
        else:
            self.paramList[verilogBitNumber] = fromName
        return

    ##########################################################################
    def FinaliseParamList(self):
        if self._GetNumBitsMapped() != self.toPort.portBitWidth and self.toPort.portBitWidth != -1:
            self.logger.Debug("SubmoduleCallParam %s: Not enough bits mapped: %d bits mapped, width = %d, param list len = %d" %
                               (self.toPort.portName, self._GetNumBitsMapped(), self.toPort.portBitWidth, len(self.paramList)))
        return

    ##########################################################################
    def GetParamList(self):
        return self.paramList

    ##########################################################################
    def _GetNumBitsMapped(self):
        count = 0
        for i in range(0, len(self.bitsMappedList)):
            if self.bitsMappedList[i] == 1:
                count += 1
        return count
    
    ##########################################################################
    def _HdlBitNumberToVerilog(self, hdlBitNumber, numberOfBits):
        return numberOfBits - hdlBitNumber - 1