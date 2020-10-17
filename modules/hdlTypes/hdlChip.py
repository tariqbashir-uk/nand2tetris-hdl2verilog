from modules.core.logger import Logger
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlChipPart import HdlChipPart

class HdlChip():
    def __init__(self):
        self.logger     = Logger()
        self.chipName   = None
        self.inputPins  = []
        self.outputPins = []
        self.partList   = []
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
    def GetChipDependencyList(self):
        dependencyList = []

        for part in self.partList: #type: HdlChipPart
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