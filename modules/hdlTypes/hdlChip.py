from modules.core.logger import Logger
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection

class HdlChip():
    def __init__(self):
        self.logger     = Logger()
        self.chipName   = None
        self.inputPins  = []  # type: list[HdlPin]
        self.outputPins = []  # type: list[HdlPin]
        self.partList   = []  # type: list[HdlChipPart]
        return

    ##########################################################################
    def SetChipName(self, chipName):
        self.chipName = chipName
        return

    ##########################################################################
    def AddInputPins(self, inputs):
        self.logger.Debug("AddInputPins: %d" % (len(inputs)))
        for inputPin in inputs:
            self.inputPins.append(HdlPin(inputPin.pinName, pinType=HdlPinTypes.Input, bitWidth=inputPin.bitWidth))
        return

    ##########################################################################
    def AddOutputPins(self, outputs):
        self.logger.Debug("AddOutputPins: %d" % (len(outputs)))
        for outputPin in outputs:
            self.outputPins.append(HdlPin(outputPin.pinName, pinType=HdlPinTypes.Output, bitWidth=outputPin.bitWidth))
        return

    ##########################################################################
    def AddPart(self, chipPart):
        self.logger.Debug("AddPart: %s" % (chipPart.partName))
        chipPart.SetPinTypes(self.inputPins, self.outputPins)
        self.partList.append(chipPart)
        return

    ##########################################################################
    def UpdatePin2Width(self, pinName, bitWidth):
        for part in self.partList:
            for connection in part.connections: # type: HdlConnection
                if connection.pin2.pinName == pinName:
                    connection.pin2.bitWidth = bitWidth   
        return

    ##########################################################################
    def UpdatePin1Width(self, pinName, bitWidth):
        for part in self.partList:
            for connection in part.connections: # type: HdlConnection
                if connection.pin1.pinName == pinName:
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
    def GetOutputPinList(self):
        return self.outputPins

    ##########################################################################
    def GetChipPartList(self):
        return self.partList

    ##########################################################################
    def _GetInputNameList(self):
        return [str(x.GetPortStr(isDefinition=True)) for x in self.inputPins]

    ##########################################################################
    def _GetOutputNameList(self):
        return [str(x.GetPortStr(isDefinition=True)) for x in self.outputPins]

    ##########################################################################
    def DumpChipDetails(self):
        self.logger.Debug("***** START: %s HDL Chip *****" % (self.chipName))
        self.logger.Debug("Interface:")
        self.logger.Debug("  Inputs:  %s" % (', '.join(self._GetInputNameList())))
        self.logger.Debug("  Outputs: %s" % (', '.join(self._GetOutputNameList())))

        self.logger.Debug("Implementation:")
        for part in self.partList:
            self.logger.Debug("  Part %s: %s" % (part.partName, part.GetConnectionStr()))
        self.logger.Debug("***** END: %s HDL Chip *****" % (self.chipName))
        return    