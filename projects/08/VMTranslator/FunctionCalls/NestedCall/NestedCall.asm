// Bootstrap code
@256
D = A
@SP
M = D
// Boostrap: calling Sys.init
// -->Saving return address and pushing to stack
@Sys.init.Sys$ret.1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// -->Push LCL of the caller
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push ARG of the caller
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THIS of the caller
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THAT of the caller
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Reposition of arg
@5
D = A
@SP
D = M - D
@ARG
M = D
// -->Reposition LCL
@SP
D = M
@LCL
M = D
// -->goto function now
@Sys.init
0; JMP
// -->return label
(Sys.init.Sys$ret.1)
// Translating file: Sys
// function Sys.init 0
(Sys.init)
// push constant 4000
@4000
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push constant 5000
@5000
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// call Sys.main 0
// -->Saving return address and pushing to stack
@Sys.main.Sys$ret.1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// -->Push LCL of the caller
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push ARG of the caller
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THIS of the caller
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THAT of the caller
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Reposition of arg
@5
D = A
@SP
D = M - D
@ARG
M = D
// -->Reposition LCL
@SP
D = M
@LCL
M = D
// -->goto function now
@Sys.main
0; JMP
// -->return label
(Sys.main.Sys$ret.1)
// pop temp 1
@SP
AM = M - 1
D = M
@R6
M = D
// label LOOP
(Sys.init$LOOP)
// goto LOOP
@Sys.init$LOOP
0; JMP
// function Sys.main 5
(Sys.main)
// func setup: push constant 0 for local var 0
@SP
A = M
M = 0
@SP
M = M + 1
// func setup: pop local 0
@SP
AM = M - 1
D = M
@LCL
A = M
M = D
// func setup: push local 0 to stack
@LCL
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// func setup: push constant 0 for local var 1
@SP
A = M
M = 0
@SP
M = M + 1
// func setup: pop local 1
@SP
AM = M - 1
D = M
@LCL
A = M + 1
M = D
// func setup: push local 1 to stack
@LCL
A = M + 1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// func setup: push constant 0 for local var 2
@SP
A = M
M = 0
@SP
M = M + 1
// func setup: pop local 2
@2
D = A
@LCL
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// func setup: push local 2 to stack
@2
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// func setup: push constant 0 for local var 3
@SP
A = M
M = 0
@SP
M = M + 1
// func setup: pop local 3
@3
D = A
@LCL
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// func setup: push local 3 to stack
@3
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// func setup: push constant 0 for local var 4
@SP
A = M
M = 0
@SP
M = M + 1
// func setup: pop local 4
@4
D = A
@LCL
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// func setup: push local 4 to stack
@4
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 4001
@4001
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push constant 5001
@5001
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push constant 200
@200
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@SP
AM = M - 1
D = M
@LCL
A = M + 1
M = D
// push constant 40
@40
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 2
@2
D = A
@LCL
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 3
@3
D = A
@LCL
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// push constant 123
@123
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.add12 1
// -->Saving return address and pushing to stack
@Sys.add12.Sys$ret.1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// -->Push LCL of the caller
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push ARG of the caller
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THIS of the caller
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THAT of the caller
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Reposition of arg
@6
D = A
@SP
D = M - D
@ARG
M = D
// -->Reposition LCL
@SP
D = M
@LCL
M = D
// -->goto function now
@Sys.add12
0; JMP
// -->return label
(Sys.add12.Sys$ret.1)
// pop temp 0
@SP
AM = M - 1
D = M
@R5
M = D
// push local 0
@LCL
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@LCL
A = M + 1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 4
@4
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
@SP
A = M - 1
M = M + D
// add
@SP
AM = M - 1
D = M
@SP
A = M - 1
M = M + D
// add
@SP
AM = M - 1
D = M
@SP
A = M - 1
M = M + D
// add
@SP
AM = M - 1
D = M
@SP
A = M - 1
M = M + D
// return
// -->Saving endframe
@LCL
D = M
@R13
M = D
// -->Saving return address
@5
A = D - A
D = M
@R14
M = D
// -->Reposition return value for the caller
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// -->Reposition SP of the caller
@ARG
D = M
@SP
M = D + 1
// -->Restore THAT of the caller
@R13
A = M - 1
D = M
@THAT
M = D
// -->Restore THIS of the caller
@2
D = A
@R13
A = M - D
D = M
@THIS
M = D
// -->Restore ARG of the caller
@3
D = A
@R13
A = M - D
D = M
@ARG
M = D
// -->Restore LCL of the caller
@4
D = A
@R13
A = M - D
D = M
@LCL
M = D
// -->goto to return address
@R14
A = M
0; JMP
// function Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push constant 5002
@5002
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
@SP
A = M - 1
M = M + D
// return
// -->Saving endframe
@LCL
D = M
@R13
M = D
// -->Saving return address
@5
A = D - A
D = M
@R14
M = D
// -->Reposition return value for the caller
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// -->Reposition SP of the caller
@ARG
D = M
@SP
M = D + 1
// -->Restore THAT of the caller
@R13
A = M - 1
D = M
@THAT
M = D
// -->Restore THIS of the caller
@2
D = A
@R13
A = M - D
D = M
@THIS
M = D
// -->Restore ARG of the caller
@3
D = A
@R13
A = M - D
D = M
@ARG
M = D
// -->Restore LCL of the caller
@4
D = A
@R13
A = M - D
D = M
@LCL
M = D
// -->goto to return address
@R14
A = M
0; JMP
