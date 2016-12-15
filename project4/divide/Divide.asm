//set bit at MSB of the denominator
@16384
D=A
@currBit
M=D
(Setbit)
	@R13
	D=M
	@currBit
	D=D&M
	M=M>>
	@Setbit
	D;JEQ

//fix redundent shift
@currBit
M=M<< 

// init result
@R15
M=0

@tmp
M=0

(Loop)
	@tmp
	M=M<<
	//check the current bit at the denominator
	@R13
	D=M
	@currBit
	D=D&M
	//skip if bit=0
	@Continue
	D;JEQ
	//add temp the next bit
	D=1
	@tmp
	M=D|M

(Continue)
	//check if tmp - R14 > 0 
	@tmp
	D=M
	@R14
	D=D-M
	//skip if false
	@Endif
	D;JLT
	@tmp
	M=D
	@currBit
	D=M
	//save current result
	@R15
	M=D|M
(Endif)
	//end if curr bit is 0
	@currBit
	D=M
	@End
	D;JEQ
	
	@currBit
	M=M>>
	@Loop
	0;JMP

(End)
	
