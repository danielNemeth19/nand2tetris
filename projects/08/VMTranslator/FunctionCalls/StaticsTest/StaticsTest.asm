// Bootstrap code
@256
D = A
@SP
M = D
// Boostrap: calling Sys.init
// -->Saving return address and pushing to stack
@Sys.init.Class1$ret.1
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
(Sys.init.Class1$ret.1)
// Translating file: Class1
// function Class1.set 0
(Class1.set)
// push argument 0
@0
D = A
@ARG
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop static 0
@SP
AM = M - 1
D = M
@Class1.0
M = D
// push argument 1
@1
D = A
@ARG
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop static 1
@SP
AM = M - 1
D = M
@Class1.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
// -->Saving endframe
@LCL
D = M
@R13
M = D
// -->Saving return address
@5
A = D - A
D = M
@R14
M = D
// -->Reposition return value for the caller
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// -->Reposition SP of the caller
@ARG
D = M
@SP
M = D + 1
// -->Restore THAT of the caller
@R13
A = M - 1
D = M
@THAT
M = D
// -->Restore THIS of the caller
@2
D = A
@R13
A = M - D
D = M
@THIS
M = D
// -->Restore ARG of the caller
@3
D = A
@R13
A = M - D
D = M
@ARG
M = D
// -->Restore LCL of the caller
@4
D = A
@R13
A = M - D
D = M
@LCL
M = D
// -->goto to return address
@R14
A = M
0; JMP
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Class1.1
D = M
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
// return
// -->Saving endframe
@LCL
D = M
@R13
M = D
// -->Saving return address
@5
A = D - A
D = M
@R14
M = D
// -->Reposition return value for the caller
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// -->Reposition SP of the caller
@ARG
D = M
@SP
M = D + 1
// -->Restore THAT of the caller
@R13
A = M - 1
D = M
@THAT
M = D
// -->Restore THIS of the caller
@2
D = A
@R13
A = M - D
D = M
@THIS
M = D
// -->Restore ARG of the caller
@3
D = A
@R13
A = M - D
D = M
@ARG
M = D
// -->Restore LCL of the caller
@4
D = A
@R13
A = M - D
D = M
@LCL
M = D
// -->goto to return address
@R14
A = M
0; JMP
// Translating file: Class2
// function Class2.set 0
(Class2.set)
// push argument 0
@0
D = A
@ARG
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop static 0
@SP
AM = M - 1
D = M
@Class2.0
M = D
// push argument 1
@1
D = A
@ARG
A = D + M
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop static 1
@SP
AM = M - 1
D = M
@Class2.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
// -->Saving endframe
@LCL
D = M
@R13
M = D
// -->Saving return address
@5
A = D - A
D = M
@R14
M = D
// -->Reposition return value for the caller
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// -->Reposition SP of the caller
@ARG
D = M
@SP
M = D + 1
// -->Restore THAT of the caller
@R13
A = M - 1
D = M
@THAT
M = D
// -->Restore THIS of the caller
@2
D = A
@R13
A = M - D
D = M
@THIS
M = D
// -->Restore ARG of the caller
@3
D = A
@R13
A = M - D
D = M
@ARG
M = D
// -->Restore LCL of the caller
@4
D = A
@R13
A = M - D
D = M
@LCL
M = D
// -->goto to return address
@R14
A = M
0; JMP
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Class2.1
D = M
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
// return
// -->Saving endframe
@LCL
D = M
@R13
M = D
// -->Saving return address
@5
A = D - A
D = M
@R14
M = D
// -->Reposition return value for the caller
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
// -->Reposition SP of the caller
@ARG
D = M
@SP
M = D + 1
// -->Restore THAT of the caller
@R13
A = M - 1
D = M
@THAT
M = D
// -->Restore THIS of the caller
@2
D = A
@R13
A = M - D
D = M
@THIS
M = D
// -->Restore ARG of the caller
@3
D = A
@R13
A = M - D
D = M
@ARG
M = D
// -->Restore LCL of the caller
@4
D = A
@R13
A = M - D
D = M
@LCL
M = D
// -->goto to return address
@R14
A = M
0; JMP
// Translating file: Sys
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 8
@8
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Class1.set 2
// -->Saving return address and pushing to stack
@Class1.set.Sys$ret.1
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
@7
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
@Class1.set
0; JMP
// -->return label
(Class1.set.Sys$ret.1)
// pop temp 0
@SP
AM = M - 1
D = M
@R5
M = D
// push constant 23
@23
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Class2.set 2
// -->Saving return address and pushing to stack
@Class2.set.Sys$ret.1
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
@7
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
@Class2.set
0; JMP
// -->return label
(Class2.set.Sys$ret.1)
// pop temp 0
@SP
AM = M - 1
D = M
@R5
M = D
// call Class1.get 0
// -->Saving return address and pushing to stack
@Class1.get.Sys$ret.1
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
@Class1.get
0; JMP
// -->return label
(Class1.get.Sys$ret.1)
// call Class2.get 0
// -->Saving return address and pushing to stack
@Class2.get.Sys$ret.1
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
@Class2.get
0; JMP
// -->return label
(Class2.get.Sys$ret.1)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE
0; JMP
