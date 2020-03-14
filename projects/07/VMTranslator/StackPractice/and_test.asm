// push constant 57
@57
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 84
@84
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 112
@112
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
// neg
@SP
AM = M - 1
D = M
M = M - D
M = M - D
@SP
M = M + 1
// and
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = D & M
@SP
M = M + 1
