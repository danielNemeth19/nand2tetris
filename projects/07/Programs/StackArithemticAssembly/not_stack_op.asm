// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 90
    @90
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// not
    @SP
    AM = M - 1
    D = M

    M = M - D
    M = M - D
    M = M - 1

    @SP
    M = M + 1