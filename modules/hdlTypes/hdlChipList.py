from modules.core.logger import Logger
from modules.hdlTypes.hdlNandChip import HdlNandChip
from modules.hdlTypes.hdlDFFChip import HdlDFFChip
from modules.hdlTypes.hdlChip import HdlChip
from modules.hdlTypes.hdlPin import HdlPin
from modules.hdlTypes.hdlPinTypes import HdlPinTypes
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection

class HdlChipList():
    def __init__(self):
        self.logger   = Logger()
        self.chipList = [] # type: list[HdlChip]
        return

    ##########################################################################
    def AddChip(self, chip):
        self.chipList.append(chip)
        return

    ##########################################################################
    def _GetChipsFromNameList(self, chipNameList):
        chipList = []
        for chipName in chipNameList:
            chipList.append(self.GetChip(chipName))
        return chipList

    ##########################################################################
    def GetChip(self, chipName):
        result = None
        for hdlChip in self.chipList:
            if hdlChip.chipName == chipName:
                result = hdlChip
                break

        if not result and chipName == 'Nand':
            result = HdlNandChip.GetChip()

        if not result and chipName == 'DFF':
            result = HdlDFFChip.GetChip()

        return result

    ##########################################################################
    def UpdateAllPinBitWidths(self):
        self.logger.Info("Started: UpdateAllPinBitWidths")
        for hdlChip in self.chipList:
            for part in hdlChip.partList: # type: HdlChipPart
                for connection in part.connections: # type: HdlConnection
                    pin1, pin2  = connection.GetPins()
                    pinFromChip = self.GetPinFromChip(part.partName, pin1.pinName) # type: HdlPin                    
                    hdlChip.UpdatePin1Width(part.partName, pin1.pinName, pinFromChip.GetPinBitWidth())
                    hdlChip.UpdatePin1Type(pin1.pinName, pinFromChip.pinType)
                    hdlChip.UpdatePin2Width(pin2.pinName, pinFromChip.GetPinBitWidth())                        

        self.logger.Info("Completed: UpdateAllPinBitWidths")
        return

    ##########################################################################
    def CheckAndAddClockInputs(self):
        self.logger.Info("Started: CheckAndAddClockInputs")
        for hdlChip in self.chipList:
            clkPin             = None
            partsNeedingClkCon = []
            for part in hdlChip.partList: # type: HdlChipPart
                partChip  = self.GetChip(part.partName)
                tmpClkPin = self._GetClkPinInDependencies(partChip)
                if tmpClkPin:
                    partsNeedingClkCon.append(part)
                    clkPin = tmpClkPin
            
            # If one of the parts contains a chip with a clk input, then add the input
            # to it an create a connection in the part.
            if clkPin:
                if not hdlChip.GetClkPin():
                    hdlChip.AddInputPins([clkPin])

                for part in partsNeedingClkCon:
                    part.AddConnection(HdlConnection(clkPin, clkPin))
        
        self.logger.Info("Completed: CheckAndAddClockInputs")
        return

    ##########################################################################
    def _GetClkPinInDependencies(self, hdlChip : HdlChip):
        chipDependencyList = self.GetChipDependencyList(hdlChip)
        chipList           = self._GetChipsFromNameList(chipDependencyList)

        clkPin = None
        for chip in chipList:
            clkPin = chip.GetClkPin()
            if clkPin:
               break

        return clkPin

    ##########################################################################
    def UpdateAllPartConnections(self):
        self.logger.Info("Started: UpdateAllPartConnections")
        for hdlChip in self.chipList:
            for part in hdlChip.partList: # type: HdlChipPart
                for connection in part.connections: # type: HdlConnection
                    connection.UpdateConnectionBitWidths()
        
        self.logger.Info("Completed: UpdateAllPartConnections")
        return

    ##########################################################################
    def GetPinFromChip(self, chipName, pinName):
        pin     = None
        hdlChip = self.GetChip(chipName)

        if hdlChip: # type: HdlChip
            pin = hdlChip.GetPin(pinName)

        return pin

    ##########################################################################
    def GetBitWidthForPin(self, chipName, pinName):
        bitWidth = None
        hdlChip  = self.GetChip(chipName)

        if hdlChip: # type: HdlChip
            bitWidth = hdlChip.GetBitWidthForPin(pinName)

        #self.logger.Debug("Chip %s, pin \"%s\" bitwidth = %s" % (chipName, pinName, bitWidth))
        return bitWidth
    
    ##########################################################################
    def GetChipDependencyList(self, hdlChip : HdlChip):
        # Get the direct dependencies of the chip being tested
        moduleList = hdlChip.GetChipDependencyList()

        indirectModules = ['Nand']
        moduleLength    = len(indirectModules)
        runLoop         = True
        inModuleList    = moduleList
        while runLoop == True:
            # Get the indirect dependencies
            for module in inModuleList: #type: list[string]
                for chip in self.chipList:  #type: HdlChip
                    if module == chip.chipName:
                        newDependencies = chip.GetChipDependencyList()
                        for newDependency in newDependencies:
                            if newDependency not in indirectModules:
                                indirectModules.append(newDependency)
            if moduleLength == len(indirectModules):
                runLoop = False
            else:
                moduleLength = len(indirectModules)
                inModuleList = indirectModules

        for indirectModule in indirectModules:
            if indirectModule not in moduleList:
                moduleList.append(indirectModule)

        moduleList.append(hdlChip.chipName)
        return moduleList
