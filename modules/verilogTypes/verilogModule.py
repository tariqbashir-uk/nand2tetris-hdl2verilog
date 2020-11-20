from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort
from modules.verilogTypes.verilogPortDirectionTypes import VerilogPortDirectionTypes

class VerilogModule():
    def __init__(self, moduleName):
        self.logger          = Logger()
        self.moduleName      = moduleName
        self.inputPorts      = []
        self.outputPorts     = []
        self.submoduleCalls  = []
        self.wireAssignments = []
        return

    ##########################################################################
    def AddInputPorts(self, inputs):
        #self.logger.Debug("AddInputPorts: %d" % (len(inputs)))
        for inputPort in inputs:
            self.inputPorts.append(inputPort)
        return

    ##########################################################################
    def AddOutputPorts(self, outputs):
        #self.logger.Debug("AddOutputPorts: %d" % (len(outputs)))
        for outputPort in outputs:
            self.outputPorts.append(outputPort)
        return

    ##########################################################################
    def AddSubmoduleCall(self, submoduleCall):
        self.submoduleCalls.append(submoduleCall)
        return

    ##########################################################################
    def AddWireAssignment(self, wireAssignment):
        self.wireAssignments.append(wireAssignment)
        return

    ##########################################################################
    def GetInputPortList(self):
        return self.inputPorts

    ##########################################################################
    def GetOutputPortList(self):
        return self.outputPorts

    ##########################################################################
    def GetPortFromName(self, portName):
        port = None

        for inputPort in self.inputPorts:  # type: VerilogPort
            if portName == inputPort.portName:
                port = inputPort

        for outputPort in self.outputPorts: # type: VerilogPort
            if portName == outputPort.portName:
                port = outputPort

        return port

    ##########################################################################
    def GetSubmoduleCalls(self):
        return self.submoduleCalls

    ##########################################################################
    def GetWireAssignments(self):
        return self.wireAssignments

    ##########################################################################
    def DumpModuleDetails(self):
        self.logger.Info("***** START: %s Verilog Module *****" % (self.moduleName))
        self.logger.Info("Interface:")
        self.logger.Info("  Inputs:  %s" % (', '.join([str(x.GetPortStr()) for x in self.inputPorts])))
        self.logger.Info("  Outputs: %s" % (', '.join([str(x.GetPortStr()) for x in self.outputPorts])))

        self.logger.Info("Implementation:")
        for submoduleCall in self.GetSubmoduleCalls():
             self.logger.Info("  Submodule %s: %s" % (submoduleCall.GetModuleName(), submoduleCall.GetCallParamsStr()))
        self.logger.Info("***** END: %s Verilog Module *****" % (self.moduleName))
        return    