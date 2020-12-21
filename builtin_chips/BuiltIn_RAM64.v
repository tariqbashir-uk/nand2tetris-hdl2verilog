module RAM64(in, load, address, clk, out);
    input [15:0] in;
    input        load;
    input [5:0]  address;
    input        clk;
    output [15:0] out;

    reg [15:0] mem [63:0];

    integer i;
    initial begin
        for (i=0; i < 64; i=i+1) begin
            mem[i] <= 16'b0; //reset array
        end
    end

    always @(posedge clk) begin
        if (load)
            mem[address] <= in;
    end
    assign out = mem[address];
endmodule