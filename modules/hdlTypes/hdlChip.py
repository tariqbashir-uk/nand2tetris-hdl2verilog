from modules.core.logger import Logger
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection

class HdlChip():
    def __init__(self):
        self.logger     = Logger()
        self.chipName   = None
        self.filename   = None
        self.inputPins  = []  # type: list[HdlPin]
        self.outputPins = []  # type: list[HdlPin]
        self.partList   = []  # type: list[HdlChipPart]
        return

    ##########################################################################
    def SetChipName(self, chipName):
        self.chipName = chipName
        return

    ##########################################################################
    def SetChipFilename(self, filename):
        self.filename = filename
        return

    ##########################################################################
    def AddInputPins(self, inputs):
        #self.logger.Debug("AddInputPins: %d" % (len(inputs)))
        for inputPin in inputs:
            bitWidthString = None
            if inputPin.bitWidthString:
                bitWidthString = inputPin.bitWidthString
            
            pinType = inputPin.pinType
            if inputPin.pinType == HdlPinTypes.Unknown:
               pinType = HdlPinTypes.Input
            self.inputPins.append(HdlPin(inputPin.pinName, 
                                         pinType=pinType, 
                                         bitWidthString=bitWidthString))

        return

    ##########################################################################
    def AddClockedPins(self, inputs):
        #self.logger.Debug("AddClockedPins: %d" % (len(inputs)))
        for inputPin in inputs:
            bitWidthString = None
            if inputPin.bitWidthString:
                bitWidthString = inputPin.bitWidthString            
            self.inputPins.append(HdlPin(inputPin.pinName, 
                                         pinType=HdlPinTypes.Clk, 
                                         bitWidthString=bitWidthString))
        return

    ##########################################################################
    def AddOutputPins(self, outputs):
        #self.logger.Debug("AddOutputPins: %d" % (len(outputs)))
        for outputPin in outputs:
            bitWidthString = None
            if outputPin.bitWidthString:
                bitWidthString = outputPin.bitWidthString
            self.outputPins.append(HdlPin(outputPin.pinName, 
                                          pinType=HdlPinTypes.Output, 
                                          bitWidthString=bitWidthString))
        return

    ##########################################################################
    def AddPart(self, chipPart):
        #self.logger.Debug("AddPart: %s" % (chipPart.partName))
        chipPart.SetPinTypes(self.inputPins, self.outputPins)
        self.partList.append(chipPart)
        return

    ##########################################################################
    def UpdatePin2Width(self, pinName, bitWidth):
        for part in self.partList:
            for connection in part.connections: # type: HdlConnection
                if connection.pin2.pinName == pinName:
                    if connection.pin2.bitWidth != bitWidth:
                        self.logger.Debug("Updating chip %s, line %d, part %s: Pin2 \"%s\" width changed from %s to %s" % 
                                            (self.chipName, part.lineNo, part.partName, connection.pin2.pinName, connection.pin2.bitWidth, bitWidth))
                        connection.pin2.bitWidth = bitWidth   
        return

    ##########################################################################
    def UpdatePin1Width(self, partName, pinName, bitWidth):
        for part in self.partList:
            for connection in part.connections: # type: HdlConnection
                if connection.pin1.pinName == pinName and part.partName == partName:
                    if connection.pin1.bitWidth != bitWidth:
                        self.logger.Debug("Updating chip %s, line %d, part %s: Pin1 \"%s\" width changed from %s to %s (from %s)" % 
                                            (self.chipName, part.lineNo, part.partName, connection.pin1.pinName, connection.pin1.bitWidth, bitWidth, partName))
                        connection.pin1.bitWidth = bitWidth
        return

    ##########################################################################
    def UpdatePin1Type(self, pinName, pinType):
        for part in self.partList:
            for connection in part.connections: # type: HdlConnection
                if connection.pin1.pinName == pinName:
                    connection.pin1.pinType = pinType   
        return

    ##########################################################################
    def GetPin(self, pinName):
        pin = None
 
        for inputPin in self.inputPins: 
            if inputPin.pinName == pinName:
                pin = inputPin
                break

        if pin == None:
            for outputPin in self.outputPins: 
                if outputPin.pinName == pinName:
                    pin = outputPin
                    break

        return pin

    ##########################################################################
    def GetBitWidthForPin(self, pinName):
        bitWidth = None
 
        for inputPin in self.inputPins: 
            if inputPin.pinName == pinName:
                bitWidth = inputPin.bitWidth
                break

        if bitWidth == None:
            for outputPin in self.outputPins: 
                if outputPin.pinName == pinName:
                    bitWidth = outputPin.bitWidth
                    break
        
        #self.logger.Debug("Chip %s, pin \"%s\" bitwidth = %s" % (self.chipName, pinName, bitWidth))
        return bitWidth

    ##########################################################################
    def GetChipDependencyList(self):
        dependencyList = []

        for part in self.partList:
            if part.partName not in dependencyList:
                dependencyList.append(part.partName)

        return dependencyList

    ##########################################################################
    def GetInputPinList(self):
        return self.inputPins

    ##########################################################################
    def GetClkPin(self):
        clkPin = None
        for pin in self.GetInputPinList():
            if pin.pinType == HdlPinTypes.Clk:
                clkPin = pin
                break
        return clkPin

    ##########################################################################
    def GetOutputPinList(self):
        return self.outputPins

    ##########################################################################
    def GetChipPartList(self):
        return self.partList

    ##########################################################################
    def DumpChipDetails(self):
        self.logger.Debug("*************** START: %s HDL Chip ***************" % (self.chipName))
        self.logger.Debug("Interface:")
        self.logger.Debug("  Inputs:  %s" % (', '.join([str(x.GetPinStr()) for x in self.inputPins])))
        self.logger.Debug("  Outputs: %s" % (', '.join([str(x.GetPinStr()) for x in self.outputPins])))

        self.logger.Debug("Implementation:")
        for part in self.partList:
            self.logger.Debug("  Part %s (line %d): %s" % (part.partName, part.lineNo, part.GetConnectionStr()))
        self.logger.Debug("*************** END: %s HDL Chip ***************" % (self.chipName))
        return