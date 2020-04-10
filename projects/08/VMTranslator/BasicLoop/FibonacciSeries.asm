// Translating file: FibonacciSeries
// push argument 1
@ARG
A = M + 1
D = M
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
// push constant 0
@SP
A = M
M = 0
@SP
M = M + 1
// pop that 0
@SP
AM = M - 1
D = M
@THAT
A = M
M = D
// push constant 1
@SP
A = M
M = 1
@SP
M = M + 1
// pop that 1
@SP
AM = M - 1
D = M
@THAT
A = M + 1
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
// pop argument 0
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// label MAIN_LOOP_START
(null$MAIN_LOOP_START)
// push argument 0
@ARG
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto COMPUTE_ELEMENT
@SP
AM = M - 1
D = M
@null$COMPUTE_ELEMENT
D; JNE
// goto END_PROGRAM
@null$END_PROGRAM
0; JMP
// label COMPUTE_ELEMENT
(null$COMPUTE_ELEMENT)
// push that 0
@THAT
A = M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push that 1
@THAT
A = M + 1
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
// pop that 2
@2
D = A
@THAT
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// push pointer 1
@THAT
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
// add
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M + D
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
// goto MAIN_LOOP_START
@null$MAIN_LOOP_START
0; JMP
// label END_PROGRAM
(null$END_PROGRAM)
