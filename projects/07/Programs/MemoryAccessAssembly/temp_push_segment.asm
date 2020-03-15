// push constant 510
// pop temp 6
// push local 0
// push that 5

// init section starts

    @256
    D = A
    @SP
    M = D

    @300
    D = A
    @LCL
    M = D

    @400
    D = A
    @ARG
    M = D

    @3000
    D = A
    @THIS
    M = D

    @3010
    D = A
    @THAT
    M = D

    @10
    D = A
    @LCL
    A = M
    M = D

    @45
    D = A
    @3015
    M = D


// init section ends

// push constant 510
    @510
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop temp 6
    @SP
    AM = M - 1 // SP -> 256
    D = M

    @R11
    M = D

// push local 0
    @0
    D = A
    @LCL
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1

// push that 5
    @5
    D = A
    @THAT
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1




