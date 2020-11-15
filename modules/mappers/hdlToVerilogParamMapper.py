from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlConnectionTypes import HdlConnectionTypes
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

import modules.commonDefs as commonDefs

class H2VParamMappingItem:
    def __init__(self, hdlStartBit, hdlEndBit, numberOfBits, verilogParam):
        self.hdlStartBit  = hdlStartBit 
        self.hdlEndBit    = hdlEndBit
        self.verilogParam = verilogParam
        self.vStartBit    = self._HdlBitNumberToVerilog(hdlStartBit, numberOfBits)
        self.vEndBit      = self._HdlBitNumberToVerilog(hdlEndBit, numberOfBits)

        return

    ##########################################################################
    def GetNumBits(self):
        return self.hdlEndBit - self.hdlStartBit + 1

    ##########################################################################
    def _HdlBitNumberToVerilog(self, hdlBitNumber, numberOfBits):
        return numberOfBits - hdlBitNumber - 1

    ##########################################################################
    def DebugInfo(self):
        print("%d -> %d (%d -> %d): %d bits (%s), bits mapped = %d" % (hdlStartBit, hdlEndBit, self.vStartBit, self.vEndBit, numberOfBits, verilogParam, self.GetNumBits()))
        return

class HdlToVerilogParamMapper():
    def __init__(self, toPort : VerilogPort, fromPort : VerilogPort):
        self.toPort         = toPort
        self.fromPort       = fromPort
        self.logger         = Logger()
        self.paramList      = []
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

        self.paramMappingList = []

        #print("%s: %d, expecting: %d" % (pin1.pinName, pin1BitWidth, len(self.hdlConnections)))
        for connection in self.hdlConnections:
            pin1, pin2 = connection.GetPins() # type: HdlPin, HdlPin
            
            # Note: Cases todo..
            # all bits   <-- input all bits (different bit length)

            pin1BitIndex, pin1StartBitOfBus, pin1EndBitOfBus, pin1ConnectionWidth, pin1ConnectionType = connection.GetPin1Params()
            pin2BitIndex, pin2StartBitOfBus, pin2EndBitOfBus, pin2ConnectionWidth, pin2ConnectionType = connection.GetPin2Params()

            paramFullName = self._MakeParamFullName(pin2.pinName,
                                                    pin2BitIndex,
                                                    pin2StartBitOfBus,
                                                    pin2EndBitOfBus,
                                                    pin2ConnectionWidth,
                                                    True if pin1.pinType == HdlPinTypes.Input else False)

            # Cases:
            # all bits   <-- input all bits (same bit length)
            # all bits   <-- input single bit
            # all bits   <-- input bit range
            # all bits   <-- internal all bits
            if pin1ConnectionType == HdlConnectionTypes.AllBits:
                if pin1BitWidth != pin2ConnectionWidth:
                    self.logger.Error("Mapping all input bits of '%s' to '%s' but bit sizes differ. (Pin size: %d, connection size: %d)" %
                                        (pin1.pinName, pin2.pinName, pin1BitWidth, pin2ConnectionWidth))
                self.paramMappingList.append(H2VParamMappingItem(0, pin1BitWidth - 1, pin1BitWidth, paramFullName))

            # Cases:
            # bit range  <-- input single bit
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                  pin2ConnectionType == HdlConnectionTypes.SingleBit):
                for hdlBitNumber in range(connection.pin1StartBitOfBus, connection.pin1EndBitOfBus):
                    self.paramMappingList.append(H2VParamMappingItem(hdlBitNumber, hdlBitNumber, pin1BitWidth, paramFullName))

            # Cases:
            # bit range  <-- input all bits
            # bit range  <-- internal all bits
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                  pin2ConnectionType == HdlConnectionTypes.AllBits):
                self.paramMappingList.append(H2VParamMappingItem(pin1StartBitOfBus, pin1EndBitOfBus, pin1BitWidth, paramFullName))

            # Cases:
            # bit range  <-- input bit range
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                  pin2ConnectionType == HdlConnectionTypes.BitRange):
                self.paramMappingList.append(H2VParamMappingItem(pin1StartBitOfBus, pin1EndBitOfBus, pin1BitWidth, paramFullName))

            # Cases:
            # single bit <-- input all bits     
            # single bit <-- input single bit 
            # single bit <-- internal all bits
            else:
                self.paramMappingList.append(H2VParamMappingItem(connection.pin1BitIndex, connection.pin1BitIndex, pin1BitWidth, paramFullName))
            
        numMappedBits = self._CountMappedBits(self.paramMappingList)
        if numMappedBits != pin1BitWidth:
            self.logger.Debug("Not enough bits mapped: %s to %s: Bit Width: %d, Mapped Bits: %d. Will add padding." % 
                               (pin1.pinName, pin2.pinName, pin1BitWidth, numMappedBits))
        
            self._PadMissingBits(pin1.pinName, pin2.pinName,
                                 pin1BitWidth, 
                                 self.paramMappingList, 
                                 True if pin1.pinType == HdlPinTypes.Output else False)

        newlist = sorted(self.paramMappingList, key=lambda x: x.vStartBit)
        for item in newlist:
            self.paramList.append(item.verilogParam)
        #     item.DebugInfo()
        return

    ##########################################################################
    def GetParamList(self):
        return self.paramList

    ##########################################################################
    def _PadMissingBits(self, pin1Name, pin2Name, pinBitWidth, paramMappingList, isOutputPin):
        bitMapList = [0] * pinBitWidth

        for item in paramMappingList:
            for i in range(item.hdlStartBit, item.hdlEndBit + 1):
                bitMapList[i] = 1

        if isOutputPin:
            for i in range(0, pinBitWidth):
                if bitMapList[i] == 0:
                    paramMappingList.append(H2VParamMappingItem(i, i, pinBitWidth, "false")) 
        else:
            startPos = -1
            endPos   = -1
            for i in range(0, pinBitWidth):
                if startPos == -1 and bitMapList[i] == 0:
                    startPos = i
                if startPos != -1 and bitMapList[i] == 1:
                    endPos = i
                    width  = endPos - startPos
                    paramMappingList.append(H2VParamMappingItem(startPos, endPos, pinBitWidth, str(width) + "'b0")) 
                    startPos = -1
                    endPos   = -1

            if startPos != -1 and endPos == -1:
                width = pinBitWidth - startPos
                paramMappingList.append(H2VParamMappingItem(startPos, pinBitWidth - 1, pinBitWidth, str(width) + "'b0"))

        #print("%s --> %s: %s" % (pin1Name, pin2Name, bitMapList))
        return

    ##########################################################################
    def _CountMappedBits(self, paramMappingList):
        totalBits = 0
        for item in paramMappingList:
            totalBits += item.GetNumBits()
        return totalBits
    
    ##########################################################################
    def _MakeParamFullName(self, pinName, pinBitIndex, pinStartBitOfBus, pinEndBitOfBus, pinConnectionWidth, isInputPin):
        paramName  = pinName
        paramExtra = ""

        # If the pin is an Input then swap false to 1'b0
        if isInputPin and pinName == 'false':
            paramName = ("%d'b%s" % (pinConnectionWidth, '0'.join(['0' * pinConnectionWidth])))

        # If the pin is an Input then swap true to 1'b1
        if isInputPin and pinName == 'true':
            paramName = ("%d'b%s" % (pinConnectionWidth, '1'.join(['1' * pinConnectionWidth])))

        if pinBitIndex != commonDefs.NO_BIT_VALUE:
            paramExtra += "[" + str(pinBitIndex) + "]"
        elif pinStartBitOfBus != commonDefs.NO_BIT_VALUE:
            paramExtra += "[" + str(pinEndBitOfBus) + ":"  + str(pinStartBitOfBus) +  "]"

        return ("%s%s" % (paramName, paramExtra))