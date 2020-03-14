// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 24
    @24
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// push constant 82
    @82
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 258

// or
    @SP
    AM = M - 1
    D = M

    @SP
    AM = M - 1
    M = D | M

    @SP
    M = M + 1