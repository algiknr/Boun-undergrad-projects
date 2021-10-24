`timescale 1ns/1ns
module source(output reg [4:0] F,
output reg [0:0] Cout,
input [1:0] S,
input [4:0] X,
input [4:0] Y,
input [0:0] Cin
);

parameter S0 = 2'b00, S1 = 2'b01, S2 = 2'b10, S3 = 2'b11;
reg [2:0] s;
reg [4:0] temp;
integer i;

always @(S, X, Y, Cin) begin
  begin
		if(S == S0) begin
			Cout = X <=Y;
			F <= 5'b00000;
		end
		else if(S == S1) begin
      		temp = Y[2:1];
	  		if (temp==2'b00)begin
	  			Cout=1'b0;
	  			F=5'b00000;
	  		end
	  		else if(temp==2'b01)begin
	  			{Cout, F} = X;
			end
			else if(temp==2'b10)begin
				temp=(~X+ 5'b00001)<<1;
				{Cout,F}=temp;
			end
			else if(temp==2'b11)begin
				temp=(~X+ 5'b00001);
				{Cout,F}=temp;
			end
		end
		else if(S == S2) begin
      		{Cout, F} = X[4:2]* Y[2:0];
		end
    	else if(S == S3) begin
      		temp = { 2'b00,Y[2:0]};
      		temp = ~temp + 5'b00001;
	  		temp=temp+Cin;
      		{Cout, F} = X + temp;
    	end
	end
end
endmodule
