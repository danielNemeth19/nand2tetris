// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = M - D
@eq_1
D;JEQ
@SP
A = M
M = 0
@done.eq_1
0; JMP
(eq_1)
@SP
A = M
M = -1
(done.eq_1)
@SP
M = M + 1
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = M - D
@eq_2
D;JEQ
@SP
A = M
M = 0
@done.eq_2
0; JMP
(eq_2)
@SP
A = M
M = -1
(done.eq_2)
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D = M - D
@eq_3
D;JEQ
@SP
A = M
M = 0
@done.eq_3
0; JMP
(eq_3)
@SP
A = M
M = -1
(done.eq_3)
@SP
M = M + 1
