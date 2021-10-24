`timescale 1ns/1ns
module testbench();

wire [4:0] F;
wire [0:0] Cout;
reg [0:0] Cin;
reg [1:0] S;
reg [4:0] X;
reg [4:0] Y;
initial Cin=0;

source s(
	.F(F),
	.Cout(Cout),
  .S(S),
  .X(X),
  .Y(Y),
  .Cin(Cin)  
);

initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, S, X, Y, F,Cout,Cin );

      S = 2'b00;
      X = 5'b00110;
      Y = 5'b00111;
      #40
      S = 2'b00;
      X = 5'b01110;
      Y = 5'b00011;
      #40
      S = 2'b01;
      X = 5'b01010;
      Y = 5'b00011;
      #40
      S = 2'b01;
      X = 5'b10001;
      Y = 5'b00111;
      #40
      S = 2'b01;
      X = 5'b11001;
      Y = 5'b11101;
      #40
      S = 2'b10;
      X = 5'b01001;
      Y = 5'b00001;
      #40
      S = 2'b10;
      X = 5'b11111;
      Y = 5'b11111;
      #40
      S = 2'b10;
      X = 5'b01111;
      Y = 5'b01111;
      #40
      S = 2'b11;
      X = 5'b10001;
      Y = 5'b00011;
      Cin= 1'b1;
      #40
      S = 2'b11;
      X = 5'b00111;
      Y = 5'b00001;
      Cin= 1'b1;
      #40
    $finish;
end

endmodule
