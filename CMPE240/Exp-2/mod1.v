`timescale 1 ns/ 1 ns

module Mux(r,c,g,p,b);

input r,c,g,p;
output b;

wire W1,W2,W3,W4,W5;

not1 N_1(p,W1);
and1 A_1(c,g,W2);
or1 O_1(c,g,W3);
and1 A_2(r,W1,W4);
and1 A_3(W4,W3,W5);
or1 O_2 (W2,W5,b);



endmodule
