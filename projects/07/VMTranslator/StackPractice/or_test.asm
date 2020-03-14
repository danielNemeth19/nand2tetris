// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 82
@82
D = A
@SP
A = M
M = D
@SP
M = M + 1
// or
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = D | M
@SP
M = M + 1
