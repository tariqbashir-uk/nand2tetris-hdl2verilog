from modules.core.logger import Logger
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
    def GetChip(self, chipName):
        result = None
        for hdlChip in self.chipList:
            if hdlChip.chipName == chipName:
                result = hdlChip
                break

        return result

    ##########################################################################
    def UpdateAllPin1BitWidths(self):
        for hdlChip in self.chipList:
            for part in hdlChip.partList: # type: HdlChipPart
                for connection in part.connections: # type: HdlConnection
                    if part.partName != 'Nand':
                        pin      = self.GetPin(part.partName, connection.pin1.pinName) # type: HdlPin
                        bitWidth = self.GetBitWidthForPin(part.partName, pin.pinName)
                        hdlChip.UpdatePin1Width(part.partName, pin.pinName, bitWidth)
                        hdlChip.UpdatePin1Type(pin.pinName, pin.pinType)

        return

    ##########################################################################
    def UpdateAllPartConnections(self):
        for hdlChip in self.chipList:
            for part in hdlChip.partList: # type: HdlChipPart
                for connection in part.connections: # type: HdlConnection
                    connection.UpdateConnectionBitWidths()
        return

    ##########################################################################
    def GetPin(self, chipName, pinName):
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
