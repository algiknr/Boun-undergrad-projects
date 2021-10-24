`timescale 1ns/1ns
module source(y,n,s,b,rst,clk);
output reg [2:0] y;
output reg [3:0] n;
output reg [3:0] s;
input wire b;
input wire rst;
input wire clk;
always @(s,b)
 begin
 case (s)
 4'b0000:
 begin
 y <=3'b000;
 if (b == 1'b0)
 n <= 4'b0000;
 else 
 n <= 4'b0001;
 end
 4'b0001:
 begin
 y <=3'b000;
 if (b == 1'b0)
 n <= 4'b0010;
 else 
 n <= 4'b0001;
 end
 
 4'b0010:
 begin
 y <=3'b000;
 if (b == 1'b0)
 n <= 4'b0011;
 else 
 n <= 4'b1001;
 end
 
 4'b0011:
 begin
 y <=3'b000;
 if (b == 1'b0)
 n <= 4'b0100;
 else 
 n <= 4'b1000;
 end
 
 4'b0100:
 begin
 y <=3'b000;
 if (b == 1'b0)
 n <= 4'b0101;
 else 
 n <= 4'b0111;
 end
 
 4'b0101:
 begin
 y <=3'b000;
 if (b == 1'b0)
 n <= 4'b0101;
 else 
 n <= 4'b0110;
 end
 
 4'b0110:
 begin
 y <=3'b111;
 if (b == 1'b0)
 n <= 4'b0000;
 else 
 n <= 4'b0001;
 end
 
 4'b0111:
 begin
 y <=3'b011;
 if (b == 1'b0)
 n <= 4'b0000;
 else 
 n <= 4'b0001;
 end
 
 4'b1000:
 begin
 y <=3'b010;
 if (b == 1'b0)
 n <= 4'b0000;
 else 
 n <= 4'b0001;
 end
 
 4'b1001:
 begin
 y <=3'b001;
 if (b == 1'b0)
 n <= 4'b0000;
 else 
 n <= 4'b0001;
 end
 endcase
 end
 
// Sync reset
always @(rst, posedge clk) begin
 if (rst)
 s <= 4'b0000;
 else
 s <= n;
end
endmodule
