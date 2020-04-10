// Bootstrap code
@256
D = A
@SP
M = D
// Boostrap: calling Sys.init
// -->Saving return address and pushing to stack
@Sys.init.Main$ret.1
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
(Sys.init.Main$ret.1)
// Translating file: Main
// function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = M - D
@lt_1
D;JLT
@SP
A = M
M = 0
@done.lt_1
0; JMP
(lt_1)
@SP
A = M
M = -1
(done.lt_1)
@SP
M = M + 1
// if-goto IF_TRUE
@SP
AM = M - 1
D = M
@Main.fibonacci$IF_TRUE
D; JNE
// goto IF_FALSE
@Main.fibonacci$IF_FALSE
0; JMP
// label IF_TRUE
(Main.fibonacci$IF_TRUE)
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
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
// label IF_FALSE
(Main.fibonacci$IF_FALSE)
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
// call Main.fibonacci 1
// -->Saving return address and pushing to stack
@Main.fibonacci.Main$ret.1
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
@Main.fibonacci
0; JMP
// -->return label
(Main.fibonacci.Main$ret.1)
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@SP
A = M
M = 1
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
// call Main.fibonacci 1
// -->Saving return address and pushing to stack
@Main.fibonacci.Main$ret.2
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
@Main.fibonacci
0; JMP
// -->return label
(Main.fibonacci.Main$ret.2)
// add
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
@SP
M = M + 1
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
// Translating file: Sys
// function Sys.init 0
(Sys.init)
// push constant 4
@4
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Main.fibonacci 1
// -->Saving return address and pushing to stack
@Main.fibonacci.Sys$ret.1
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
@Main.fibonacci
0; JMP
// -->return label
(Main.fibonacci.Sys$ret.1)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE
0; JMP
