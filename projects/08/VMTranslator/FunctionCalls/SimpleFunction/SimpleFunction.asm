// Translating file: SimpleFunction
// function SimpleFunction.test 2
(SimpleFunction.test)
// func setup: push constant 0 for local var 0
@0
D = A
@SP
A = M
M = D
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
@0
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// func setup: push constant 0 for local var 1
@0
D = A
@SP
A = M
M = D
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
@1
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
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
AM = M - 1
M = M + D
@SP
M = M + 1
// not
@SP
AM = M - 1
D = M
M = !M
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
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
AM = M - 1
M = M + D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = D + M
D = M
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
