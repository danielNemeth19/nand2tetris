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

    @4000
    D = A
    @THAT
    M = D

    // -->Push LCL of the caller
    @LCL
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
    // -->Push ARG of the caller
    @ARG
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
    // -->Push THIS of the caller
    @THIS
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
    // -->Push THAT of the caller
    @THAT
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1

    @7
    D = A
    @SP
    D = M - D
    @ARG
    M = D

    @SP
    D = M
    @LCL
    M = D