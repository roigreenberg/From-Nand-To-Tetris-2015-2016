// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	//save R0 in tmp
	@R0
	D=M
	@tmp
	M=D
	
	//set R2 to 0
	@R2
	M=0

	//initialize index i
	@i
	M=1

(Loop)
	//take the i's bit of R1
	@R1
	D=M
	@i
	D=D&M
	
	//continue if D is not zero
	@Endif
	D;JEQ

	//add R2 the value in tmp
	@tmp
	D=M
	@R2
	M=D+M


(Endif)

	//shift left tmp and i
	@tmp
	D=M
	M=D+M
	
	@i
	D=M
	M=D+M
	D=M

	//while i<=32768
	@32768
	D=A-D
	@Loop
	D;JGE
	
