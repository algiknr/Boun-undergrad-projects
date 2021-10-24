`timescale 1ns/1ns
module source(y,s,n,x,rst,clk);	
	output reg [1:0] y, s, n;
	input wire x, rst, clk;

always @(s,x)
 	begin

 case (s)

 	2'b00:
 	begin
 		if (x == 1'b0)
 		begin
 			y <= 2'b10;
 			n <= 2'b10;
 		end
 		else
 		begin
 			y <= 2'b11; 
 			n <= 2'b00;
 		end
 	end

	2'b10:
 	begin
 		if (x == 1'b0) 
 		begin
 			y <= 2'b10;
 			n <= 2'b10;
 		end
 		else
 		begin 
 			y <= 2'b10;
 			n <= 2'b11;
 		end
	end

 	2'b11:
 	begin
 		if (x == 1'b0) begin
 			 y <= 2'b11;
			 n <= 2'b10;
			
 		end
 		else
 		begin 
 			y <= 2'b01;
 			n <= 2'b11;
		end
 	end
 
 endcase
 end
 
// Sync reset
always @(posedge clk) begin
 if (rst)
 s <= 2'b00;
 else
 s <= n;
end

endmodule
