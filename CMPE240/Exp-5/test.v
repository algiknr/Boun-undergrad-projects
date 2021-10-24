`timescale 1ns/1ns
module testbench();
wire [1:0] y,s,n;
reg [9:0] inp1;
integer index;
reg clk;
initial clk = 1;
always #10 clk = ~clk;
reg rst;
//initial rst =0;
initial rst =1;
reg x;
initial x =0;


source upcounter(y, s, n, x, rst, clk);
initial begin
 $dumpfile("TimingDiagram.vcd");
 $dumpvars(0, y, s, n, x, rst, clk);

	#30
	rst=0;
	x=1;
	#30
	rst=0;
	x=1;
	#20
	rst=0;
	x=0;
	#40
	rst=0;
	x=0;
	#20
	rst=0;
	x=0;
	#20
	rst=0;
	x=0;
	#40
	rst=0;
	x=1;
    #20
	rst=0;
	x=1;
	#20
	rst=0;
	x=0;
	#40
	rst=0;
	x=1;
	#20
		
 $finish;
end
endmodule
