;we set these numbers in order to refresh default setting of these values
MOV DH,0H		
MOV CL,0H
;In read_char we are going to take characters from screen 1 by 1.
READ_CHAR:
	MOV     AH,01H		;reads input
    INT     21H
	MOV 	AH,0H		;casts to zero because we just need AL
    CMP		AL, 0DH
	JE 		JUMPSTEP		;for long jump
    CMP     AL,02BH		;compares the input character with +
    JE      EVALPLUS
    CMP     AL,02AH		;compares the input character with *
    JE      EVALMUL
    CMP     AL,02FH		;compares the input character with /
    JE      EVALDIV
    CMP     AL,026H     ;compares the input character with &
    JE      EVALAND
    CMP     AL,07CH		;compares the input character with |
    JE      EVALOR
    CMP     AL,05EH		;compares the input character with ^
    JE      EVALXOR
    CMP     AL,020H		;compares the input character with (SPACE)
    JE      TOPUSH

;Transforms characters into their hexadecimal counterparts
CONV_ASCII:
    CMP     AL,39H		;checks if less than 9
    JLE     CONVERT

    SUB     AL,37H		;extracts the hexadecimal above 9
    JMP     MERGE		

;Extracts the hexadecimal below 9
CONVERT:
    SUB     AL,30H		

;Evaluates the hexadecimal value of adjacent characters
MERGE:  
    INC     CL			;CL is a counter that identifıes whether the value consists of adjacent characters 
	CMP     CL,1H
    JE     	BETWEEN
        
	MOV 	BX,AX		;combines the adjacent characters
	MOV 	AX,DX
	MOV 	DX,010H
	MUL		DX
	ADD 	AX, BX
    MOV 	DX,AX
    JMP     READ_CHAR

;Stores the hexadecimal value of a single character input
BETWEEN:
	MOV DL,AL
	JMP READ_CHAR

;Pushes to the stack
TOPUSH:
    CMP     CH,1H		;CH is a counter to understand if there are consecutive operations
    JE		RESETCH
	MOV 	AX,DX
    PUSH    AX
    MOV     CL, 0H			;resets the CL counter
    JMP     READ_CHAR
	
;Resets CH counter
RESETCH:
    MOV	CH,0H
	JMP	READ_CHAR

;Implements addition
EVALPLUS:
    POP     AX
    POP     BX

    ADD     AX,BX
    PUSH    AX
    MOV     CH,1H		;declares the last taken value as an operation sign
    JMP     READ_CHAR

;Used for high jump
JUMPSTEP:
	JMP		END_OF_IN

;Implements multiplication
EVALMUL:
    POP     BX
    POP     AX
    MUL     BX
    PUSH    AX
	MOV     CH,1H		;declares the last taken value as an operation sign
    JMP     READ_CHAR
		
;Implements integer division
EVALDIV:
    MOV     BX,DX
    POP     CX
    POP     AX
    MOV     DX,0H
    DIV     CX
    MOV 	AH,0H
    PUSH    AX
    MOV     DX,BX
	MOV     CH,1H		;declares the last taken value as an operation sign
    JMP     READ_CHAR
	
;Implements AND operation
EVALAND:
    POP     BX
    POP     AX
    AND     AX,BX
    PUSH    AX
	MOV     CH,1H		;declares the last taken value as an operation sign
    JMP     READ_CHAR

;Implements OR operation
EVALOR:
    POP     BX
    POP     AX
    OR      AX,BX
    PUSH    AX
	MOV     CH,1H		;declares the last taken value as an operation sign
    JMP     READ_CHAR

;Implements XOR operation
EVALXOR:
    POP     BX
    POP     AX
    XOR     AX,BX
    PUSH    AX
	MOV     CH,1H		;declares the last taken value as an operation sign
    JMP     READ_CHAR

;End of input read
END_OF_IN:
	POP 	AX
	PUSH	021H		;this chosen value later indicates that we reached the end of the stack
	MOV 	CX, 10H		;will be used for dividing hexadecimal values to characters
	JMP		OUT_CONV

;Converts hexadecimal values to characters
OUT_CONV:
	MOV 	DX,0H
	DIV		CX
	PUSH	DX			;pushes the remainder to stack
	CMP		AL, 0H		;checks if the quotient is zero
	JNE		OUT_CONV

;Pops the individual hexadecimal values
TO_POP:
	POP		BX
	CMP		BX, 021H
	JE		THE_END
	CMP		BX, 09H
	JLE		TO_DIGIT

	ADD		BX, 037H		;Transforms the values between A-F to ASCII
	JMP		PRINT_OUT

;Transforms to values between 0-9 to ASCII
TO_DIGIT:
	ADD		BX, 030H
	JMP		PRINT_OUT

;Displays the result
PRINT_OUT:
	MOV		DL, BL	
	MOV 	AH,02H
	INT		21H
	JMP		TO_POP	

;Concludes the program
THE_END:
	INT 	20H
