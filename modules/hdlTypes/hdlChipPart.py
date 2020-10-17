from modules.hdlTypes.hdlPinTypes import HdlPinTypes

class HdlChipPart():
    def __init__(self, partName):
        self.partName    = partName
        self.connections = []
        return

    ##########################################################################
    def AddConnection(self, chipConnection):
        self.connections.append(chipConnection)
        return

    ##########################################################################
    def GetConnections(self):
        return self.connections
        
    ##########################################################################
    def SetPinTypes(self, inputPins, outputPins):
        for connection in self.connections:
            pinFound = False

            for inputPin in inputPins:
                if inputPin.pinName == connection.pin2.pinName:
                    connection.pin2.pinType = inputPin.pinType
                    pinFound = True
                    break

            for outputPin in outputPins:
                if outputPin.pinName == connection.pin2.pinName:
                    connection.pin2.pinType = outputPin.pinType
                    pinFound = True
                    break

            if pinFound == False:
                connection.pin2.pinType = HdlPinTypes.Internal
        return

    ##########################################################################
    def GetConnectionStr(self):
        return ', '.join([str(x.GetPinStr()) for x in self.connections])