from os.path import isfile, join
from modules.core.textFile import TextFile

class VerilogDFFModule():
    def __init__(self):
        return

    @staticmethod
    ##########################################################################
    def WriteModule(outputFolder):
        nand_v  = TextFile(join(outputFolder, 'DFF.v'))
        nandContents  = "module DFF(in, out);\n"
        nandContents += "  input in;\n"
        nandContents += "  output out;\n"
        nandContents += "  assign in=out;\n"
        nandContents += "endmodule\n"
        nand_v.WriteFile(nandContents)
        return

