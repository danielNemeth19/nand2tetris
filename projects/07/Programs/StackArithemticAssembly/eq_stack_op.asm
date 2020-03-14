// SP is at 256, i.e. RAM[0] = 256

    @256
    D = A
    @SP
    M = D

// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 257

// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 258

// equality 1
    @SP // -> SP to 257
    AM = M - 1
    D = M

    @SP // -> SP to 256
    AM = M - 1
    D = M - D

// need to check the condition for D
    @eq.1
    D; JEQ

    @SP
    A = M
    M = 0

    @done.eq1
    0; JMP

(eq.1)
    @SP
    A = M
    M = -1

(done.eq1)
    @SP
    M = M + 1 // -> SP to 257

// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 258

// push constant 16
    @16
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 259

// equality 2
    @SP // -> SP to 258
    AM = M - 1
    D = M

    @SP // -> SP to 257
    AM = M - 1
    D = M - D

// need to check the condition for D
    @eq.2
    D; JEQ

    @SP
    A = M
    M = 0


    @done.eq2
    0; JMP

(eq.2)
    @SP
    A = M
    M = -1

(done.eq2)
    @SP
    M = M + 1 // -> SP to 258

// push constant 16
    @16
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 259

// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1 // -> SP to 260

// equality 3
    @SP
    AM = M - 1 // SP to 259
    D = M

    @SP
    AM = M - 1 // SP to 258
    D = M - D

    @eq.3
    D; JEQ

    @SP
    A = M
    M = 0

    @done.eq3
    0; JMP

(eq.3)
    @SP
    A = M
    M = -1

(done.eq3)
    @SP
    M = M + 1 // SP to 259 if not equal












