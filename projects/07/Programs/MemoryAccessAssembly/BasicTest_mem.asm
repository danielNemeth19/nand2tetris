// whole BasicTest.vm implemented

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

// init section ends

// push constant 10
    @10
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop local 0
    @SP
    AM = M - 1 // SP -> 256
    D = M

    @LCL
    A = M
    M = D

// push constant 21
    @21
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// push constant 22
    @22
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// pop argument 2
    @2
    D = A
    @ARG
    D = D + M
    @pop_to
    M = D

    @SP
    AM = M - 1 // SP -> 257
    D = M

    @pop_to
    A = M
    M = D

// pop argument 1
    @SP
    AM = M - 1 // SP -> 256
    D = M

    @ARG
    A = M + 1
    M = D

// push constant 36
    @36
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// pop this 6
    @6
    D = A
    @THIS
    D = D + M
    @pop_to
    M = D

    @SP
    AM = M - 1 // SP -> 256
    D = M

    @pop_to
    A = M
    M = D

// push constant 42
    @42
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 257

// push constant 45
    @45
    D = A
    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// pop that 5
    @5
    D = A
    @THAT
    D = D + M
    @pop_to
    M = D

    @SP
    AM = M - 1 // SP -> 257
    D = M

    @pop_to
    A = M
    M = D

// pop that 2
    @2
    D = A
    @THAT
    D = D + M
    @pop_to
    M = D

    @SP
    AM = M - 1 // SP -> 256
    D = M

    @pop_to
    A = M
    M = D

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
    M = M + 1 // SP -> 257

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
    M = M + 1 // SP -> 258

// add
    @SP
    AM = M - 1 // -> SP to 257
    D = M

    @SP
    AM = M - 1 // -> SP to 256
    M = M + D

    @SP
    M = M + 1 // SP -> 257

// push argument 1
    @1
    D = A
    @ARG
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// sub
    @SP
    AM = M - 1 // -> SP to 257
    D = M

    @SP
    AM = M - 1 // -> SP to 256
    M = M - D

    @SP
    M = M + 1 // SP -> 257

// push this 6
    @6
    D = A
    @THIS
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// push this 6
    @6
    D = A
    @THIS
    A = D + M
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 259

// add
    @SP
    AM = M - 1 // -> SP to 258
    D = M

    @SP
    AM = M - 1 // -> SP to 257
    M = M + D

    @SP
    M = M + 1 // SP -> 258

// sub
    @SP
    AM = M - 1 // -> SP to 257
    D = M

    @SP
    AM = M - 1 // -> SP to 256
    M = M - D

    @SP
    M = M + 1 // SP -> 257

// push temp 6
    @R11
    D = M

    @SP
    A = M
    M = D

    @SP
    M = M + 1 // SP -> 258

// add
    @SP
    AM = M - 1 // -> SP to 257
    D = M

    @SP
    AM = M - 1 // -> SP to 256
    M = M + D

    @SP
    M = M + 1 // SP -> 257