from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort
from modules.verilogTypes.verilogPortDirectionTypes import VerilogPortDirectionTypes

class VerilogModule():
    def __init__(self, moduleName):
        self.logger         = Logger()
        self.moduleName     = moduleName
        self.inputPorts     = []
        self.outputPorts    = []
        self.submoduleCalls = []
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
    def AddSubmoduleCalls(self, submoduleCalls):
        self.submoduleCalls = submoduleCalls
        return

    ##########################################################################
    def GetInputNameList(self):
        return [str(x.portName) for x in self.inputPorts]

    ##########################################################################
    def GetOutputNameList(self):
        return [str(x.portName) for x in self.outputPorts]

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
    def DumpModuleDetails(self):
        self.logger.Info("***** START: %s Verilog Module *****" % (self.moduleName))
        self.logger.Info("Interface:")
        self.logger.Info("  Inputs:  %s" % (', '.join(self.GetInputNameList())))
        self.logger.Info("  Outputs: %s" % (', '.join(self.GetOutputNameList())))

        self.logger.Info("Implementation:")
        for submoduleCall in self.GetSubmoduleCalls():
             self.logger.Info("  Submodule %s: %s" % (submoduleCall.GetModuleName(), submoduleCall.GetCallParamsStr()))
        self.logger.Info("***** END: %s Verilog Module *****" % (self.moduleName))
        return    