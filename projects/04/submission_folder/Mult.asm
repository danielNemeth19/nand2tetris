// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @R0
    D = M
    @ZERO
    D; JEQ
    @x
    M = D

    @R1
    D = M
    @ZERO
    D;JEQ
    @y
    M = D

    @i
    M = 0

    @sum
    M = 0

(LOOP)
    @i
    D = M
    @y
    D = D - M

    @STOP
    D; JGE

    @x
    D = M
    @sum
    M = M + D

    @i
    M = M + 1

    @LOOP
    0; JMP

(ZERO)
    @R2
    M = 0
    @END
    0; JMP


(STOP)
    @sum
    D = M

    @R2
    M = D

    @STOP
    0; JMP

(END)
    @END
    0; JMP
