`timescale 1ns/1ns
module testbench();
wire [2:0] y;
wire [3:0] n;
wire [3:0] s;
reg [31:0] inp1, inp2, inp3, inp4, inp5;
integer index;
reg clk;
initial clk = 1;
always #10 clk = ~clk;
reg rst;
initial rst =1;
reg b;
initial b = 0;

source upcounter(y, n, s, b, rst, clk);
initial begin
 $dumpfile("TimingDiagram.vcd");
 $dumpvars(0, y, n, s, b, rst, clk);

inp1 = 32'b01000011001001010010001010010110; 
inp2 = 32'b01111111100111110111100001111111; 
inp3 = 32'b01010101100101001010101011011100; 
inp4 = 32'b10011000100011011100110110100101; 
inp5 = 32'b11011011000110100110001101010001;
    
	
    #20;
	
	for(index=31; index >=0; index=index-1) begin
	rst =0;
	b <= inp1[index];
	#20;
	end
	#20;
	rst<=1;
	
	for(index=31; index >=0; index=index-1) begin
	rst =0;
	b <= inp2[index];
	#20;
	end
	#20
	rst<=1;
	
	for(index=31; index >=0; index=index-1) begin
	rst=0;
	b <= inp3[index];
	#20;
	end
	#20;
	rst<=1;
	
	for(index=31; index >=0; index=index-1) begin
	rst=0;
	b <= inp4[index];
	#20;
	end
	#20;
	rst<=1;	
	
	
	for(index=31; index >=0; index=index-1) begin
	rst=0;
	b <= inp5[index];
	#20;
	end
	#20;
	
 $finish;
end
endmodule
