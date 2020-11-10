from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlConnectionTypes import HdlConnectionTypes
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

import modules.commonDefs as commonDefs

class HdlToVerilogParamMapper():
    def __init__(self, toPort : VerilogPort, fromPort : VerilogPort):
        self.toPort         = toPort
        self.fromPort       = fromPort
        self.paramList      = None
        self.bitsMappedList = [0] * toPort.portBitWidth
        self.logger         = Logger()
        self.hdlConnections = [] #type: list[HdlConnection]
        return

    ##########################################################################
    def AddHdlConnection(self, connection : HdlConnection):
        self.hdlConnections.append(connection)
        return

    ##########################################################################
    def DoMapping(self):
        pin1, pin2   = self.hdlConnections[0].GetPins()
        pin1BitWidth = pin1.GetPinBitWidth()

        #self.bitsMappedList = [0] * pin1BitWidth
        #self.paramList      = ['false'] * len(self.hdlConnections)

        print("%s: %d, expecting: %d" % (pin1.pinName, pin1BitWidth, len(self.hdlConnections)))
        for connection in self.hdlConnections:
            pin1, pin2 = connection.GetPins() # type: HdlPin, HdlPin
            
            # Note: Cases todo..
            # bit range  <-- input bit range
            # all bits   <-- input all bits (different bit length)

            pin1BitIndex, pin1StartBitOfBus, pin1EndBitOfBus, pin1ConnectionWidth, pin1ConnectionType = connection.GetPin1Params()
            pin2BitIndex, pin2StartBitOfBus, pin2EndBitOfBus, pin2ConnectionWidth, pin2ConnectionType = connection.GetPin2Params()

            paramFullName = self._MakeParamFullName(pin2.pinName, pin2BitIndex, pin2StartBitOfBus, pin2EndBitOfBus)

            # Cases:
            # all bits   <-- input all bits (same bit length)
            # all bits   <-- input single bit
            # all bits   <-- input bit range
            # all bits   <-- internal all bits
            if pin1ConnectionType == HdlConnectionTypes.AllBits:
                self.AddAllBitMapping(paramFullName, pin1ConnectionWidth)

            # Cases:
            # bit range  <-- input all bits
            # bit range  <-- internal all bits
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                    pin2ConnectionType == HdlConnectionTypes.SingleBit):
                for hdlBitNumber in range(connection.pin1StartBitOfBus, connection.pin1EndBitOfBus):
                    self.AddSingleBitMapping(hdlBitNumber, paramFullName)

            # Cases:
            # bit range  <-- input bit range
            elif pin1ConnectionType == HdlConnectionTypes.BitRange and pin2ConnectionType == HdlConnectionTypes.AllBits:
                self.AddMultiBitMapping(paramFullName, pin1StartBitOfBus, pin1EndBitOfBus)

            # Cases:
            # single bit <-- input all bits     
            # single bit <-- input single bit 
            # single bit <-- internal all bits
            else:
                self.AddSingleBitMapping(connection.pin1BitIndex, paramFullName)
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

    ##########################################################################
    def _MakeParamFullName(self, pinName, pinBitIndex, pinStartBitOfBus, pinEndBitOfBus):
        paramName  = pinName
        paramExtra = ""

        if pinBitIndex != commonDefs.NO_BIT_VALUE:
            paramExtra += "[" + str(pinBitIndex) + "]"
        elif pinStartBitOfBus != commonDefs.NO_BIT_VALUE:
            paramExtra += "[" + str(pinEndBitOfBus) + ":"  + str(pinStartBitOfBus) +  "]"

        return ("%s%s" % (paramName, paramExtra))