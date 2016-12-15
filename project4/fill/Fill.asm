// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.



(Loopkbd)
	//save the value of if keyboard is in use
	@KBD
	D=M

	// keyboard is in use - blacken screen
	@Loopscrb
	D@JGT
	
	// keyboard isn't in use - whiten screen
	@Loopscrw
	0;JMP

(Loopscrb)
	// init variable for screen location
	@SCREEN
	D=A
	@i
	M=D

(Loop2)
	// running for all screen cells and blacken them
	@i
	A=M
	M=-1
	
	@i	
	M=M+1
	D=M
	
	@KBD
	D=D-A

	@Loop2
	D;JLT

	@Loopkbd
	0;JMP

(Loopscrw)
	// init variable for screen location
	@SCREEN
	D=A
	@i
	M=D

(Loop3)
	// running for all screen cells and blacken them
	@i
	A=M
	M=0
	
	@i
	M=M+1
	D=M
	@KBD
	D=D-A
	@Loop3
	D;JLT
	@Loopkbd
	0;JMP
