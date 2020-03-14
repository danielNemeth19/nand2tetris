// push constant 892
@892
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 891
@891
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
// push constant 891
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 892
@892
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
@lt_2
D;JLT
@SP
A = M
M = 0
@done.lt_2
0; JMP
(lt_2)
@SP
A = M
M = -1
(done.lt_2)
@SP
M = M + 1
// push constant 891
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 891
@891
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
@lt_3
D;JLT
@SP
A = M
M = 0
@done.lt_3
0; JMP
(lt_3)
@SP
A = M
M = -1
(done.lt_3)
@SP
M = M + 1
