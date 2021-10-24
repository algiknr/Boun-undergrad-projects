`timescale 1 ns/ 1 ns

module TestBench();
 
 reg r,c,g,p;
 wire b;
 
Mux CompToTest(r,c,g,p,b);

initial begin

$dumpfile("TimingDiagram.vcd");
 $dumpvars(0,b,r, c, g, p);
 
 r<=0; c<=0; g<=0; p<=0;
 #10 r<=0; c<=0; g<=0; p<=1;
 #10 r<=0; c<=0; g<=1; p<=0;
 #10 r<=0; c<=0; g<=1; p<=1;
 #10 r<=0; c<=1; g<=0; p<=0;
 #10 r<=0; c<=1; g<=0; p<=1;
 #10 r<=0; c<=1; g<=1; p<=0;
 #10 r<=0; c<=1; g<=1; p<=1;
 #10 r<=1; c<=0; g<=0; p<=0;
 #10 r<=1; c<=0; g<=0; p<=1;
 #10 r<=1; c<=0; g<=1; p<=0;
 #10 r<=1; c<=0; g<=1; p<=1;
 #10 r<=1; c<=1; g<=0; p<=0;
 #10 r<=1; c<=1; g<=0; p<=1;
 #10 r<=1; c<=1; g<=1; p<=0;
 #10 r<=1; c<=1; g<=1; p<=1;
 #10;

end

endmodule