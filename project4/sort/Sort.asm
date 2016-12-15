//init the value to length
@R15
D=M
@length
M=D


(Loop)
	// save the starting location of the array
	@R14
	D=M
	@currentLocation
	M=D

	// updating the remained length to sort
	@length
	M=M-1
	D=D+M
	@endLocation
	M=D

	
	// init the value for the first node in array
	@currentLocation
	A=M
	D=M
	@currentVal
	M=D
	
		
	


// running for all the array values
(Mainloop)
	// updating the location in array, and saving the value of 'next'	
	@currentLocation
	M=M+1
	A=M
	D=M
	@nextVal
	M=D

	// check if need to swap
	@currentVal
	D=M-D
	@Swap
	D;JLT
	
(Continue)
	// updating the currentVal
	@currentLocation
	A=M
	D=M
	@currentVal
	M=D
	
	@currentLocation
	D=M
	@endLocation
	D=M-D
	// back to running over the array till the end of it
	@Mainloop
	D;JGT
	//go to outer loop
	@length
	D=M-1
	@Loop
	D;JGT
	@End
	0;JMP

(Swap)
	@currentVal
	D=M
	@currentLocation
	A=M
	M=D

	@nextVal
	D=M
	@currentLocation
	A=M-1
	M=D
	
	@Continue
	0;JMP

(End)


