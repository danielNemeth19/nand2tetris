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
