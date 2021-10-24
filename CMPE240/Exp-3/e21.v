`timescale 1ns/1ns
module mysource(A,B,C,D,E,ALARM);

input A,B,C,D,E;
output ALARM;

wire w1, w2, w3, w4,w5,w6,w7;

Dcd2x4 dcd(D,E,w7,w1,w2,w6);
not (w5, D);
not (w4, w2);
not (w3,w1);
Mux8to1 mux(w4, w5, w1, w3, w1, w1, w2, D, A, B, C, ALARM);

endmodule
