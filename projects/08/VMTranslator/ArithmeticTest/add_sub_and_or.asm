// Translating file: add_sub_and_or
// push constant 57
@57
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 53
@53
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
A = M - 1
M = M - D
// push constant 88
@88
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
// and
@SP
AM = M - 1
D = M
@SP
A = M - 1
M = D & M
// push constant 50
@50
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
A = M - 1
M = D | M
// neg
@SP
A = M - 1
M = -M
// not
@SP
A = M - 1
M = !M
// push constant 57
@57
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
A = M - 1
D = M - D
@eq_add_sub_and_or_1
D;JEQ
@SP
A = M
M = 0
@done.eq_add_sub_and_or_1
D;JMP
(eq_add_sub_and_or_1)
@SP
A = M - 1
M = -1
(done.eq_add_sub_and_or_1)
// push constant 500
@500
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
A = M - 1
D = M - D
@eq_add_sub_and_or_2
D;JEQ
@SP
A = M
M = 0
@done.eq_add_sub_and_or_2
D;JMP
(eq_add_sub_and_or_2)
@SP
A = M - 1
M = -1
(done.eq_add_sub_and_or_2)
// push constant 1000
@1000
D = A
@SP
A = M
M = D
@SP
M = M + 1
