from os.path import isfile, join
from modules.core.textFile import TextFile

class VerilogDFFModule():
    def __init__(self):
        return

    @staticmethod
    ##########################################################################
    def WriteModule(outputFolder):
        dff_v  = TextFile(join(outputFolder, 'DFF.v'))

        dffContents  = "module DFF(in, clk, out);\n"
        dffContents += "input in;   // Data input\n"
        dffContents += "input clk;  // clock input\n" 
        dffContents += "output reg out; // output Q\n"
        dffContents += "\n"
        dffContents += "initial begin\n"
        dffContents += "  out=0;\n"
        dffContents += "end\n"
        dffContents += "\n"
        dffContents += "always @(posedge clk)\n" 
        dffContents += "begin\n"
        dffContents += "  out <= in;\n" 
        dffContents += "end\n"
        dffContents += "endmodule\n"        
        dff_v.WriteFile(dffContents)
        return

