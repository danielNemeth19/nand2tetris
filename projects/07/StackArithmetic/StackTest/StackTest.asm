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
// push constant 32767
@32767
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D =  M - D
@gt_1
D;JGT
@SP
A = M
M = 0
@done.gt_1
0; JMP
(gt_1)
@SP
A = M
M = -1
(done.gt_1)
@SP
M = M + 1
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32767
@32767
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D =  M - D
@gt_2
D;JGT
@SP
A = M
M = 0
@done.gt_2
0; JMP
(gt_2)
@SP
A = M
M = -1
(done.gt_2)
@SP
M = M + 1
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@SP
AM = M - 1
D = M
@SP
AM = M - 1
D =  M - D
@gt_3
D;JGT
@SP
A = M
M = 0
@done.gt_3
0; JMP
(gt_3)
@SP
A = M
M = -1
(done.gt_3)
@SP
M = M + 1
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
AM = M - 1
M = M + D
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
// not
@SP
AM = M - 1
D = M
M = M - D
M = M - D
M = M - 1
@SP
M = M + 1
