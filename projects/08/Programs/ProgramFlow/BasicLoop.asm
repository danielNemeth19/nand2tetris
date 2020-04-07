// Computes the sum 1 + 2 + ... + argument[0] and pushes the
// result onto the stack. Argument[0] is initialized by the test
// script before this code starts running.

//initialization start
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

    @3
    D = A
    @ARG
    A = M
    M = D

//initialization end

    @sum
    M = 0

(LOOP_START)
    @ARG
    A = M
    D = M


    @sum
    M = M + D

    @ARG
    A = M
    M = M - 1
    D = M

    @LOOP_START
    D; JGT

    @sum
    D = M
    @SP
    A = M
    M = D

    @SP
    M = M + 1









