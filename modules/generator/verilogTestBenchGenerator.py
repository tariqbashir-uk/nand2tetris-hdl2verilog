from os.path import join
from modules.core.logger import Logger
from modules.core.textFile import TextFile
from modules.verilogTypes.verilogModuleTB import VerilogModuleTB
import modules.settings as settings

class VerilogTestBenchGenerator:
    def __init__(self, outputFolder):
        self.outputFolder = outputFolder
        self.logger = Logger()
        return

    ##########################################################################
    def CreateModule(self, verilogModuleTB : VerilogModuleTB):
        indent = 0
        period = 20
        verilogFile = TextFile(join(self.outputFolder, verilogModuleTB.moduleName + '.v'))

        verilogText  = "//`timescale 100 us/10 us // time-unit = 10 ns, precision = 1 ns\n\n"
        verilogText += ("module %s;\n" % (verilogModuleTB.moduleName))

        indent += settings.DEFAULT_INDENT
        paramList = []
        paramList.extend([("%sreg  %s" % (" ".rjust(indent), x.GetPortStr(isDefinition=True))) for x in verilogModuleTB.GetInputPortList()])
        paramList.extend([("%swire %s" % (" ".rjust(indent), x.GetPortStr(isDefinition=True))) for x in verilogModuleTB.GetOutputPortList()])

        if len(paramList) > 0:
            verilogText += (';\n'.join([x for x in paramList]))
            verilogText += ';'

        paramNameList = []
        paramNameList.extend([("%s" % (x.portName)) for x in verilogModuleTB.GetInputPortList()])
        paramNameList.extend([("%s" % (x.portName)) for x in verilogModuleTB.GetOutputPortList()])

        testModuleParams   = []
        testOutputFormat   = []
        screenOutputFormat = []
        for paramName in paramNameList:
            testModuleParams.append(".%s (%s)" % (paramName, paramName))
            testOutputFormat.append("%b")
            screenOutputFormat.append("%s = %%b" % (paramName))

        verilogText += "\n"
        verilogText += "\n"
        verilogText += ("%s%s %s(%s);\n" % (" ".rjust(indent), 
                                            verilogModuleTB.testModuleName, 
                                            verilogModuleTB.moduleName,
                                            ', '.join([x for x in testModuleParams])))

        verilogText += "\n"
        verilogText += ("%sinteger write_data;\n" % (" ".rjust(indent)))
        verilogText += "\n"
        verilogText += ("%slocalparam period = %d;\n" % (" ".rjust(indent), period))
        verilogText += "\n"
        verilogText += ("%sinitial\n" % (" ".rjust(indent)))
        verilogText += ("%sbegin\n" % (" ".rjust(indent)))

        indent += settings.DEFAULT_INDENT
        verilogText += ("%s$dumpfile(\"%s\");\n" % (" ".rjust(indent), verilogModuleTB.dumpFilename))
        verilogText += ("%s$dumpvars(0, %s);\n" % (" ".rjust(indent), verilogModuleTB.moduleName))
        verilogText += ("%swrite_data = $fopen(\"%s\");\n" % (" ".rjust(indent), verilogModuleTB.outFilename))
        verilogText += "\n"
        verilogText += ("%s$fdisplay(write_data, \"| %s |\");\n" % (" ".rjust(indent), ' | '.join([x for x in paramNameList])))
        verilogText += "\n"
        
        for setSequence in verilogModuleTB.testSequences: #Type: TstSetSequence
            for setOperation in setSequence.setOperations: #Type: TstSetOperation
                verilogText += ("%s%s = %s;\n" % (" ".rjust(indent), setOperation.pinName, setOperation.pinValue))
            verilogText += ("%s#period;\n" % (" ".rjust(indent)))
            verilogText += ("%s$fdisplay(write_data, \"| %s |\", %s);\n" % 
                               (" ".rjust(indent), 
                                ' | '.join([x for x in testOutputFormat]),
                                ', '.join([x for x in paramNameList])))
            verilogText += "\n"

        verilogText += ("%s#period;\n" % (" ".rjust(indent)))
        
        verilogText += "\n"
        verilogText += ("%s$finish;\n" % (" ".rjust(indent)))
        verilogText += ("%s$fclose(write_data);  // close the file\n" % (" ".rjust(indent)))
        indent -= settings.DEFAULT_INDENT
        verilogText += ("%send\n" % (" ".rjust(indent)))
        verilogText += "\n"

        verilogText += ("%sinitial\n" % (" ".rjust(indent)))
        verilogText += ("%sbegin\n" % (" ".rjust(indent)))
        indent += settings.DEFAULT_INDENT
        verilogText += ("%s$monitor($time,\": %s\", %s);\n" % 
                           (" ".rjust(indent),
                            ' | '.join([x for x in screenOutputFormat]),
                            ', '.join([x for x in paramNameList])))

        indent -= settings.DEFAULT_INDENT
        verilogText += ("%send\n" % (" ".rjust(indent)))
        verilogText += "\n"

        verilogText += "endmodule"
        verilogFile.WriteFile(verilogText)
        return    