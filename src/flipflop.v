`default_nettype none
module flipflop_demo(
    input wire  clk,
    input wire  d,
    output reg  q
    );

    always @(posedge clk) 
            q <= d;

endmodule
