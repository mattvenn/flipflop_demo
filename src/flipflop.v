`default_nettype none
module flipflop_demo(
    input wire  clk,
    input wire  data_in,
    output reg  data_out
    );

    always @(posedge clk) 
            data_out <= data_in;

endmodule
