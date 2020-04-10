// Translating file: function_labels
// label LOOP
(null$LOOP)
// if-goto LOOP
@SP
AM = M - 1
D = M
@null$LOOP
D; JNE
// label END
(null$END)
// goto END
@null$END
0; JMP
// function main.main 0
(main.main)
// label LOOP
(main.main$LOOP)
// if-goto LOOP
@SP
AM = M - 1
D = M
@main.main$LOOP
D; JNE
// label END
(main.main$END)
// goto END
@main.main$END
0; JMP
// function main.run 0
(main.run)
// label LOOP
(main.run$LOOP)
// if-goto LOOP
@SP
AM = M - 1
D = M
@main.run$LOOP
D; JNE
// label END
(main.run$END)
// goto END
@main.run$END
0; JMP
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
