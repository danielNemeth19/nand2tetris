// push constant 90
@90
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
AM = M - 1
D = M
M = !M
@SP
M = M + 1
