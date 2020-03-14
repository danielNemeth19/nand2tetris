// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 32767
    @32767
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// push constant 32766
    @32766
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 258

// gt
    @SP
    AM = M - 1
    D = M

    @SP
    AM = M - 1
    D =  M - D

    @gt.1
    D; JGT

    @SP
    A = M
    M = 0

    @done.gt.1
    0; JMP

(gt.1)
    @SP
    A = M
    M = -1

    @done.gt.1
    0; JMP

(done.gt.1)
    @SP
    M = M + 1


