from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlConnectionTypes import HdlConnectionTypes
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes

import modules.commonDefs as commonDefs

class H2VParamMappingItem:
    def __init__(self, hdlStartBit, hdlEndBit, pinBitWdith, verilogParam):
        self.hdlStartBit  = hdlStartBit 
        self.hdlEndBit    = hdlEndBit
        self.verilogParam = verilogParam
        self.pinBitWdith  = pinBitWdith
        self.vStartBit    = self._HdlBitNumberToVerilog(hdlStartBit, pinBitWdith)
        self.vEndBit      = self._HdlBitNumberToVerilog(hdlEndBit, pinBitWdith)
        return

    ##########################################################################
    def GetNumBits(self):
        return self.hdlEndBit - self.hdlStartBit + 1

    ##########################################################################
    def _HdlBitNumberToVerilog(self, hdlBitNumber, pinBitWdith):
        return pinBitWdith - hdlBitNumber - 1

    ##########################################################################
    def GetDebugInfo(self):
        return ("Mapped: %d -> %d (%d -> %d): %d bits (%s), bits mapped = %d" % 
                   (self.hdlStartBit,
                    self.hdlEndBit,
                    self.vStartBit,
                    self.vEndBit,
                    self.pinBitWdith,
                    self.verilogParam,
                    self.GetNumBits()))

class H2VParamMappingList:
    def __init__(self):
        self.logger = Logger()
        self.verilogParamList = []
        self.paramMappingList = [] #type: list[H2VParamMappingItem]
        return

    ##########################################################################
    def AddItem(self, hdlStartBit, hdlEndBit, pinBitWdith, verilogParam):
        itemAdded       = False
        overlapDetected = False
        for item in self.paramMappingList:
            if hdlStartBit >= item.hdlStartBit and hdlEndBit <= item.hdlEndBit:
                overlapDetected = True
                break

        if not overlapDetected:
            self.paramMappingList.append(H2VParamMappingItem(hdlStartBit, hdlEndBit, pinBitWdith, verilogParam))
            itemAdded = True

        return itemAdded

    ##########################################################################
    def CompleteMapping(self, pin1, pin2, pin1BitWidth):
        numMappedBits = self._CountMappedBits(self.paramMappingList)
        if numMappedBits < pin1BitWidth:
            self.logger.Debug("Not enough bits mapped: %s to %s: Bit Width: %d, Mapped Bits: %d. Will add padding." % 
                                (pin1.pinName, pin2.pinName, pin1BitWidth, numMappedBits))
        
            self._PadMissingBits(pin1.pinName,
                                 pin2.pinName,
                                 pin1BitWidth, 
                                 self.paramMappingList, 
                                 True if pin1.pinType == HdlPinTypes.Output else False)

        newlist = sorted(self.paramMappingList, key=lambda x: x.vStartBit)
        for item in newlist:
            self.verilogParamList.append(item.verilogParam)
        return

    ##########################################################################
    def GetVerilogParamList(self): 
        return self.verilogParamList
        
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

class H2VMappedParamsList:
    def __init__(self):
        self.logger = Logger()
        self.hdlMappedParamsList = [] #type: list[H2VParamMappingList]
        return

    ##########################################################################
    def AddItem(self, hdlStartBit, hdlEndBit, pinBitWdith, verilogParam):
        itemMapped = False
        for paramMappingList in self.hdlMappedParamsList:
            if paramMappingList.AddItem(hdlStartBit, hdlEndBit, pinBitWdith, verilogParam):
                itemMapped = True
                break

        if not itemMapped:
            paramMappingList = H2VParamMappingList()
            paramMappingList.AddItem(hdlStartBit, hdlEndBit, pinBitWdith, verilogParam)
            self.hdlMappedParamsList.append(paramMappingList)
        return

    ##########################################################################
    def CompleteMapping(self, pin1, pin2, pin1BitWidth):
        for paramMapingList in self.hdlMappedParamsList:
            paramMapingList.CompleteMapping(pin1, pin2, pin1BitWidth)
        return

    ##########################################################################
    def GetNumParamsForCall(self):
        return len(self.hdlMappedParamsList)

    ##########################################################################
    def GetVerilogParamList(self, index): 
        return self.hdlMappedParamsList[index].GetVerilogParamList()

class HdlToVerilogParamMapper():
    def __init__(self, chipName, partName, lineNo, toPort : VerilogPort, fromPort : VerilogPort):
        self.chipName       = chipName
        self.partName       = partName 
        self.lineNo         = lineNo
        self.toPort         = toPort
        self.fromPort       = fromPort
        self.logger         = Logger()
        self.hdlConnections = [] #type: list[HdlConnection]
        self.mappedParams   = H2VMappedParamsList()
        return

    ##########################################################################
    def AddHdlConnection(self, connection : HdlConnection):
        self.hdlConnections.append(connection)
        return

    ##########################################################################
    def DoMapping(self):
        pin1, pin2   = self.hdlConnections[0].GetPins()
        pin1BitWidth = pin1.GetPinBitWidth()

        self.logger.Info("Start: Chip: %s, part: %s (line %d), pin: %s" % (self.chipName, self.partName, self.lineNo, pin1.pinName))
        for connection in self.hdlConnections:
            pin1, pin2 = connection.GetPins() # type: HdlPin, HdlPin

            self.logger.Info("Mapping: %s" % (connection.GetPinStr()))

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
                self.mappedParams.AddItem(0, pin1BitWidth - 1, pin1BitWidth, paramFullName)

            # Cases:
            # bit range  <-- input single bit
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                  pin2ConnectionType == HdlConnectionTypes.SingleBit):
                for hdlBitNumber in range(connection.pin1StartBitOfBus, connection.pin1EndBitOfBus):
                    self.mappedParams.AddItem(hdlBitNumber, hdlBitNumber, pin1BitWidth, paramFullName)

            # Cases:
            # bit range  <-- input all bits
            # bit range  <-- internal all bits
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                  pin2ConnectionType == HdlConnectionTypes.AllBits):
                self.mappedParams.AddItem(pin1StartBitOfBus, pin1EndBitOfBus, pin1BitWidth, paramFullName)

            # Cases:
            # bit range  <-- input bit range
            elif (pin1ConnectionType == HdlConnectionTypes.BitRange and 
                  pin2ConnectionType == HdlConnectionTypes.BitRange):
                self.mappedParams.AddItem(pin1StartBitOfBus, pin1EndBitOfBus, pin1BitWidth, paramFullName)

            # Cases:
            # single bit <-- input all bits     
            # single bit <-- input single bit 
            # single bit <-- internal all bits
            else:
                self.mappedParams.AddItem(connection.pin1BitIndex, connection.pin1BitIndex, pin1BitWidth, paramFullName)

        self.mappedParams.CompleteMapping(pin1, pin2, pin1BitWidth)
        
        self.logger.Info("End: Mapping chip: %s, part:%s (line %d), pin: %s" % (self.chipName, self.partName, self.lineNo, pin1.pinName))
        return

    ##########################################################################
    def GetMappedParams(self):
        return self.mappedParams
    
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