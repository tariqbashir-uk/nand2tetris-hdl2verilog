module DMux8Way(in, sel, a, b, c, d, e, f, g, h);

input  in;
input  [2:0] sel;
output a;
output b;
output c;
output d;
output e;
output f;
output g;
output h;

assign a=(in & ~sel[2] & ~sel[1] &~sel[0]),
       b=(in & ~sel[2] & ~sel[1] &sel[0]),
       c=(in & ~sel[2] & sel[1] &~sel[0]),
       d=(in & ~sel[2] & sel[1] &sel[0]),
       e=(in & sel[2] & ~sel[1] &~sel[0]),
       f=(in & sel[2] & ~sel[1] &sel[0]),
       g=(in & sel[2] & sel[1] &~sel[0]),
       h=(in & sel[2] & sel[1] &sel[0]);

endmodule