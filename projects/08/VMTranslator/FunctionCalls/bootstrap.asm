// Translating file: bootstrap
// call Sys.init 0
// -->Saving return address and pushing to stack
@Sys.init$ret.1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// -->Push LCL of the caller
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push ARG of the caller
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THIS of the caller
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Push THAT of the caller
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
// -->Reposition of arg
@5
D = A
@SP
D = M - D
@ARG
M = D
// -->Reposition LCL
@SP
D = M
@LCL
M = D
// -->goto function now
@Sys.init
0; JMP
// -->return label
(Sys.init$ret.1)
