from modules.core.logger import Logger
from modules.verilogTypes.verilogPort import VerilogPort
from modules.verilogTypes.verilogPortDirectionTypes import VerilogPortDirectionTypes

from modules.tstTypes.tstSetSequence import TstSetSequence
from modules.tstTypes.tstSetOperation import TstSetOperation

class VerilogModuleTB():
    def __init__(self, moduleName, testModuleName, dumpFilename, outFilename):
        self.logger         = Logger()
        self.moduleName     = moduleName
        self.testModuleName = testModuleName
        self.dumpFilename   = dumpFilename
        self.outFilename    = outFilename
        self.inputPorts     = []
        self.outputPorts    = []
        self.outputFormats  = []
        self.testSequences  = []
        return

    ##########################################################################
    def AddInputPorts(self, inputs):
        self.logger.Debug("AddInputPorts: %d" % (len(inputs)))
        for inputPort in inputs:
            self.inputPorts.append(inputPort)
        return

    ##########################################################################
    def AddOutputPorts(self, outputs):
        self.logger.Debug("AddOutputPorts: %d" % (len(outputs)))
        for outputPort in outputs:
            self.outputPorts.append(outputPort)
        return

    ##########################################################################
    def AddOutputFormatList(self, outputFormatList):
        self.logger.Debug("AddOutputFormatList: %d" % (len(outputFormatList)))
        self.outputFormatList = outputFormatList
        return

    ##########################################################################
    def AddTestSequence(self, testSequence : TstSetSequence):
        self.testSequences.append(testSequence)
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
    def GetOutputFormatList(self):
        return self.outputFormatList

    ##########################################################################
    def DumpModuleDetails(self):
        self.logger.Info("***** START: %s Verilog TestBench Module *****" % (self.moduleName))
        self.logger.Info("Interface:")
        self.logger.Info("  Inputs:  %s" % (', '.join(self.GetInputNameList())))
        self.logger.Info("  Outputs: %s" % (', '.join(self.GetOutputNameList())))

        sequenceNumber = 1
        self.logger.Info("Test Steps:")
        for setSequence in self.testSequences: #Type: TstSetSequence
            self.logger.Info("  Test Step: %d" % (sequenceNumber))
            for setOperation in setSequence.setOperations: #Type: TstSetOperation
                self.logger.Info("    Operation: %s = %s" % (setOperation.pinName, setOperation.pinValue))
            sequenceNumber += 1
        self.logger.Info("***** END: %s Verilog TestBench Module *****" % (self.moduleName))
        return    