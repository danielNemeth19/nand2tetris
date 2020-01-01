// Computes: RAM[1] = 1 + 2 + ... + RAM[n]

    @R0
    D = M
    @n
    M = D       // n = R0

    @i
    M = 1       // initializing i as 1

    @sum
    M = 0       // initializing sum as 0

(LOOP)
    @i
    D = M
    @n
    D = D - M       // D will be i - n here

    @STOP
    D; JGT      // if i > n goto STOP

    @i
    D = M
    @sum
    M = D + M       // sum = sum + 1

    @i
    M = M + 1       // i = i + 1

    @LOOP
    0; JMP

(STOP)
    @sum
    D = M
    @R1
    M = D
    @END
    0; JMP

(END)
    @END
    0; JMP