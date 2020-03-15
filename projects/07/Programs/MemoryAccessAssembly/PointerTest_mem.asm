// PonterTest.vm
// init section starts

    @256
    D = A
    @SP
    M = D

// init section ends

// push constant 3030
    @3030
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop pointer 0
    @SP
    AM = M - 1 // SP -> 256
    D = M

    @THIS
    M = D

// push constant 3040
    @3040
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop pointer 1
    @SP
    AM = M - 1 // SP -> 256
    D = M

    @THAT
    M = D

// push constant 32
    @32
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop this 2
    @2
    D = A
    @THIS
    D = M + D
    @pop_to
    M = D

    @SP
    AM = M - 1 // SP -> 256
    D = M

    @pop_to
    A = M
    M = D

// push constant 46
    @46
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop that 6
    @6
    D = A
    @THAT
    D = M + D
    @pop_to
    M = D

    @SP
    AM = M - 1 // SP -> 256
    D = M

    @pop_to
    A = M
    M = D

// push pointer 0
    @THIS
    D = M
    @SP
    A = M
    M = D

    @SP
    M = M + 1  // SP -> 257

// push pointer 1
    @THAT
    D = M
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// add
    @SP
    AM = M - 1 // SP -> 257
    D = M

    @SP
    AM = M - 1 // SP -> 256
    M = M + D

    @SP
    M = M + 1 // SP -> 257

// push this 2
    @2
    D = A
    @THIS
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// sub
    @SP
    AM = M - 1 // SP -> 257
    D = M

    @SP
    AM = M - 1 // SP -> 256
    M = M - D

    @SP
    M = M + 1 // SP -> 257

// push that 6
    @6
    D = A
    @THAT
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// add
    @SP
    AM = M - 1 // SP -> 257
    D = M

    @SP
    AM = M - 1 // SP -> 256
    M = M + D

    @SP
    M = M + 1 // SP -> 257


