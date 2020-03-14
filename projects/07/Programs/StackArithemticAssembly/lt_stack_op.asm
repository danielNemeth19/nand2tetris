// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 892
    @892
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// push constant 891
    @891
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 258

// lt
    @SP // -> SP to 257
    AM = M - 1
    D = M

    @SP // -> SP to 256
    AM = M - 1
    D = M - D

    @lt.1
    D; JLT

    @SP
    A = M
    M = 0

    @done.lt.1
    0; JMP

(lt.1)
    @SP
    A = M
    M = -1

    @done.lt.1
    0; JMP

(done.lt.1)
    @SP
    M = M + 1
