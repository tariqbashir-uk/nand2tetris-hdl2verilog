from os.path import isfile, join
from modules.core.textFile import TextFile

class VerilogNandModule():
    def __init__(self):
        return

    @staticmethod
    ##########################################################################
    def WriteModule(outputFolder):
        nand_v  = TextFile(join(outputFolder, 'Nand.v'))
        nandContents  = "module Nand(out, a, b);\n"
        nandContents += "  input a, b;\n"
        nandContents += "  output out;\n"
        nandContents += "  nand (out, a, b);\n"
        nandContents += "endmodule\n"
        nand_v.WriteFile(nandContents)
        return

