// push constant 10
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@SP
AM = M - 1
D = M
@LCL
A = M
M = D
// push constant 21
@21
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 22
@22
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 2
@2
D = A
@ARG
D = D + M
@pop_to
M = D
@SP
AM = M - 1
D = M
@pop_to
A = M
M = D
// pop argument 1
@SP
AM = M - 1
D = M
@ARG
A = M + 1
M = D
