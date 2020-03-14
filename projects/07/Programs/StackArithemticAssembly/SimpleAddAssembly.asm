// SP is at 256, i.e. RAM[0] = 256
// push constant 7
// push constant 8
// add

    @256
    D = A
    @SP
    M = D

// push constant 7
    @7
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

// processing add
    @SP
    M = M - 1 // -> SP is 257
    A = M
    D = M

    @SP
    M = M - 1 // -> SP is 256
    A = M
    M = M + D

    @SP
    M = M + 1

(END)
    @END
    0; JMP

