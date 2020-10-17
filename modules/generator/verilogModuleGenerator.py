from os.path import join
from modules.core.logger import Logger
from modules.core.textFile import TextFile
from modules.verilogTypes.verilogModule import VerilogModule
from modules.verilogTypes.verilogPort import VerilogPort
from modules.verilogTypes.verilogSubmoduleCall import VerilogSubmoduleCall
from modules.verilogTypes.verilogSubmoduleCallParam import VerilogSubmoduleCallParam

class VerilogModuleGenerator:
    def __init__(self, outputFolder):
        self.outputFolder = outputFolder
        self.logger = Logger()
        return

    ##########################################################################
    def CreateModule(self, verilogMainModule : VerilogModule):
        verilogFile = TextFile(join(self.outputFolder, verilogMainModule.moduleName + '.v'))

        verilogText  = "// Interface\n"
        verilogText += ("module %s(\n" % (verilogMainModule.moduleName))

        paramList = []
        paramList.extend([("    input  " + x.GetPortStr(isDefinition=True)) for x in verilogMainModule.GetInputPortList()])
        paramList.extend([("    output " + x.GetPortStr(isDefinition=True)) for x in verilogMainModule.GetOutputPortList()])

        if len(paramList) > 0:
            verilogText += (',\n'.join([x for x in paramList]))
        verilogText += ");"

        verilogText += "\n"
        verilogText += "\n"

        internalVarDict = {}
        # Add the internal vairable definitions
        for submoduleCall in verilogMainModule.GetSubmoduleCalls(): #Type: VerilogSubmoduleCall
            callParamStr = []
            for callParam in submoduleCall.GetCallParams(): #Type: VerilogSubmoduleCallParam
                if callParam.internalParamPort.IsInternal():
                    keyName = callParam.internalParamPort.GetPortStr(isDefinition=True)
                    if keyName not in internalVarDict:
                        internalVarDict[keyName] = 0
                        verilogText += ("wire %s;\n" % (keyName))

        verilogText += "\n"

        verilogText += "// Implementation Code\n"

        for submoduleCall in verilogMainModule.GetSubmoduleCalls(): #Type: VerilogSubmoduleCall
            callParamStr = []
            for callParam in submoduleCall.GetCallParams(): #Type: VerilogSubmoduleCallParam
                callParamStr.append(("    .%s (%s)" % (callParam.portName, callParam.GetParamNameForCall())))

            verilogText += ("%s %s(\n%s);\n" % (submoduleCall.GetModuleName(), 
                                                submoduleCall.GetModuleCallName(), 
                                                ',\n'.join([x for x in callParamStr])))
            verilogText += "\n"

        verilogText += "endmodule"
        verilogFile.WriteFile(verilogText)
        return
