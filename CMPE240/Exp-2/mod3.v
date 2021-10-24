`timescale 1 ns/ 1 ns

module and1(X,Y,b);

input X,Y;
output b;
reg b;

 always @(X,Y) begin
 b<= X&Y;
 
 end
 
 endmodule

module or1(X,Y,b);

input X, Y;
output b;
reg b;

 always @(X, Y) begin
 b <= X | Y;

 end

 endmodule

module not1(X, b);
input X;
output b;
reg b;

 always @(X) begin
 b <= ~X;
 end
 
 endmodule
