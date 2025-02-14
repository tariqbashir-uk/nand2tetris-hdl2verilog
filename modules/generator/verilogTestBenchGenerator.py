from os.path import join
from modules.core.logger import Logger
from modules.core.textFile import TextFile
from modules.verilogTypes.verilogModuleTB import VerilogModuleTB
from modules.tstTypes.tstSetSequence import TstSetSequence
from modules.tstTypes.tstSetSequenceTypes import TstSetSequenceTypes
from modules.tstTypes.tstSetOperation import TstSetOperation
import modules.settings as settings

class VerilogTestBenchGenerator:
    def __init__(self, outputFolder):
        self.outputFolder = outputFolder
        self.logger = Logger()
        return

    ##########################################################################
    def CreateModule(self, verilogModuleTB : VerilogModuleTB):
        clkPortName = verilogModuleTB.GetClkPortName()

        clkInvertStr = ""
        if clkPortName:
            clkInvertStr = ("%s = !%s;" % (clkPortName, clkPortName))
        
        indent = 0
        period = 20
        verilogFile = TextFile(join(self.outputFolder, verilogModuleTB.moduleName + '.v'))

        verilogText  = "//`timescale 100 us/10 us // time-unit = 10 ns, precision = 1 ns\n\n"
        verilogText += ("module %s;\n" % (verilogModuleTB.moduleName.replace("-", "_")))

        indent += settings.DEFAULT_INDENT
        paramList = []
        paramList.extend([("%sreg %s %s" % (" ".rjust(indent), verilogModuleTB.GetPortSignedStr(x.portName), x.GetPortStr())) for x in verilogModuleTB.GetInputPortList()])
        paramList.extend([("%swire signed %s" % (" ".rjust(indent), x.GetPortStr())) for x in verilogModuleTB.GetOutputPortList()])

        if len(paramList) > 0:
            verilogText += (';\n'.join([x for x in paramList]))
            verilogText += ';'

        paramNameList = []
        paramNameList.extend([("%s" % (x.portName)) for x in verilogModuleTB.GetInputPortList()])
        paramNameList.extend([("%s" % (x.portName)) for x in verilogModuleTB.GetOutputPortList()])

        outputFormatList = verilogModuleTB.GetOutputFormatList()
        outputParamList  = verilogModuleTB.GetOutputParamList()

        testModuleParams   = []
        testOutputFormat   = []
        screenOutputFormat = []
        for paramName in paramNameList:
            testModuleParams.append(".%s (%s)" % (paramName, paramName))
        
        outputParamNameList = [x.GetParamName() for x in outputParamList]
        for outputParam in outputFormatList:
            if outputParam.GetParamName() in outputParamNameList:
                testOutputFormat.append(outputParam.GetVerilogFormat())
                screenOutputFormat.append("%s = %s" % (outputParam.GetParamName(), outputParam.GetVerilogFormat()))
        
        verilogText += "\n"
        verilogText += "\n"
        verilogText += ("%s%s %s(%s);\n" % (" ".rjust(indent), 
                                            verilogModuleTB.testModuleName, 
                                            verilogModuleTB.moduleName.replace("-", "_"),
                                            ', '.join([x for x in testModuleParams])))

        verilogText += "\n"
        verilogText += ("%sinteger write_data;\n" % (" ".rjust(indent)))
        verilogText += "\n"
        verilogText += ("%slocalparam period = %d;\n" % (" ".rjust(indent), period))
        verilogText += "\n"
        verilogText += ("%sinitial\n" % (" ".rjust(indent)))
        verilogText += ("%sbegin\n" % (" ".rjust(indent)))

        indent += settings.DEFAULT_INDENT
        if clkPortName:
            verilogText += ("%s%s = 0;\n" % (" ".rjust(indent), clkPortName))
        verilogText += ("%s$dumpfile(\"%s\");\n" % (" ".rjust(indent), verilogModuleTB.dumpFilename))
        verilogText += ("%s$dumpvars(0, %s);\n" % (" ".rjust(indent), verilogModuleTB.moduleName.replace("-", "_")))
        verilogText += ("%swrite_data = $fopen(\"%s\");\n" % (" ".rjust(indent), verilogModuleTB.outFilename))
        verilogText += "\n"
        verilogText += ("%s$fdisplay(write_data, \"| %s |\");\n" % (" ".rjust(indent), ' | '.join([x.GetParamName() for x in outputFormatList])))
        verilogText += "\n"
        
        clkCycleNum  = 0
        timeStr      = ""
        periodDisplayedThisOutputCmd = False 
        for setSequence in verilogModuleTB.testSequences: #type: TstSetSequence
            clkStrThisSeq = ""
            if TstSetSequenceTypes.tick == setSequence.sequenceType:
                timeStr = ("| %d+ " % clkCycleNum)
                clkCycleNum += 1
                clkStrThisSeq = clkInvertStr
            elif TstSetSequenceTypes.tock == setSequence.sequenceType:
                timeStr = ("| %d " % clkCycleNum)
                clkStrThisSeq = clkInvertStr

            if TstSetSequenceTypes.set == setSequence.sequenceType:
                verilogText += ("%s%s = %s;\n" % (" ".rjust(indent), setSequence.setOperation.pinName, setSequence.setOperation.pinValue))
            
            if (TstSetSequenceTypes.eval == setSequence.sequenceType or
                TstSetSequenceTypes.tick == setSequence.sequenceType or 
                TstSetSequenceTypes.tock == setSequence.sequenceType) and not periodDisplayedThisOutputCmd:
                verilogText += ("%s#period; %s\n" % (" ".rjust(indent), clkStrThisSeq))
                periodDisplayedThisOutputCmd = True
            
            if TstSetSequenceTypes.output == setSequence.sequenceType:
                verilogText += ("%s$fdisplay(write_data, \"%s| %s |\", %s);\n" % 
                                   (" ".rjust(indent),
                                    timeStr,
                                    ' | '.join([x for x in testOutputFormat]),
                                    ', '.join([x.GetParamName() for x in outputParamList])))
                verilogText += "\n"
                periodDisplayedThisOutputCmd = False 

        verilogText += ("%s#period; %s\n" % (" ".rjust(indent), clkInvertStr))
        
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
                            ', '.join([x.GetParamName() for x in outputParamList])))

        indent -= settings.DEFAULT_INDENT
        verilogText += ("%send\n" % (" ".rjust(indent)))
        verilogText += "\n"

        verilogText += "endmodule"
        verilogFile.WriteFile(verilogText)
        return    