module DFF(in, clk, out);
input in;   // Data input
input clk;  // clock input
output reg out; // output Q

initial begin
  out=0;
end

always @(posedge clk)
begin
  out <= in;
end
endmodule
