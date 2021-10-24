`timescale 1ns/1ns
module Mux8to1(I7, I6, I5, I4, I3, I2, I1, I0, S2, S1, S0, ALARM);

input I0, I1, I2, I3, I4, I5, I6, I7;
input S0, S1, S2;
output ALARM;
reg ALARM;

always @(I7, I6, I5, I4, I3, I2, I1, I0, S2, S1, S0)
  begin
    if(S2==0 && S1 == 0 && S0==0)
      ALARM <= I0;
    else if( S2==0 && S1 == 0 && S0==1 )
      ALARM <= I1;
    else if( S2==0 && S1 == 1 && S0==0 )
      ALARM <= I2;
    else if(S2 == 0 && S1 == 1 && S0 == 1)
     ALARM<= I3;
    else if(S2 == 1 && S1 == 0 && S0 == 0)
     ALARM<= I4;
    else if(S2 == 1 && S1 == 0 && S0 == 1)
     ALARM <= I5;
    else if(S2 == 1 && S1 == 1 && S0 == 0)
     ALARM <= I6;
    else if(S2 == 1 && S1 == 1 && S0 == 1)
      ALARM <= I7;
  end
endmodule