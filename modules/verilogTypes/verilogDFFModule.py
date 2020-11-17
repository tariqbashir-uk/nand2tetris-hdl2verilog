from os.path import isfile, join
from modules.core.textFile import TextFile

class VerilogDFFModule():
    def __init__(self):
        return

    @staticmethod
    ##########################################################################
    def WriteModule(outputFolder):
        dff_v  = TextFile(join(outputFolder, 'DFF.v'))
        dffContents  = "module DFF(in, out);\n"
        dffContents += "  input in;\n"
        dffContents += "  output out;\n"
        dffContents += "  assign in=out;\n"
        dffContents += "endmodule\n"

        # module DFF(in, clk, out);
        #   input in;   // Data input 
        #   input clk;  // clock input 
        #   output out; // output Q 
        #   always @(posedge clk) 
        #   begin
        #     out <= in; 
        #   end 
        # endmodule         
        dff_v.WriteFile(dffContents)
        return

