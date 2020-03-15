// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 84
    @84
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// neg
    @SP
    AM = M - 1
    D = M

    M = -M

    @SP
    M = M + 1