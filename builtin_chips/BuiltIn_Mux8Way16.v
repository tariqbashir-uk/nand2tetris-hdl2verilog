module Mux8Way16(a, b, c, d, e, f, g, h, sel, out);
    input  [15:0] a;
    input  [15:0] b;
    input  [15:0] c;
    input  [15:0] d;
    input  [15:0] e;
    input  [15:0] f;
    input  [15:0] g;
    input  [15:0] h;
    input  [2:0]  sel;
    output [15:0] out;

    assign out = (sel== 3'b000) ? a : 16'bz, 
           out = (sel== 3'b001) ? b : 16'bz,
           out = (sel== 3'b010) ? c : 16'bz,
           out = (sel== 3'b011) ? d : 16'bz,
           out = (sel== 3'b100) ? e : 16'bz,
           out = (sel== 3'b101) ? f : 16'bz,
           out = (sel== 3'b110) ? g : 16'bz,
           out = (sel== 3'b111) ? h : 16'bz;

endmodule