// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 57
    @57
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// push constant 28
    @28
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 258

// and
    @SP
    AM = M - 1
    D = M

    @SP
    AM = M - 1
    M = D & M

    @SP
    M = M + 1