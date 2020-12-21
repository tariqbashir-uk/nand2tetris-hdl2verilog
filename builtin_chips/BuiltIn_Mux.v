module Mux(a, b, sel, out);
    input  a;
    input  b;
    input  sel;
    output out;

    assign out = (sel == 0) ? a : b;

endmodule