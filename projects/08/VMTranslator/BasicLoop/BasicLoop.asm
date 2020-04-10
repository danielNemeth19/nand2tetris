// Translating file: BasicLoop
// push constant 0
@SP
A = M
M = 0
@SP
M = M + 1
// pop local 0
@SP
AM = M - 1
D = M
@LCL
A = M
M = D
// label LOOP_START
(null$LOOP_START)
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@LCL
A = M
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
// pop local 0
@SP
AM = M - 1
D = M
@LCL
A = M
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
// pop argument 0
@SP
AM = M - 1
D = M
@ARG
A = M
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
// if-goto LOOP_START
@SP
AM = M - 1
D = M
@null$LOOP_START
D; JNE
// push local 0
@LCL
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
