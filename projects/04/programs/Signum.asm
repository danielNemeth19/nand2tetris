// Computes: if RAM[0] > 0
//              RAM[1] = 1
//           else:
//              RAM[1] = 0

    @R0
    D = M

    @POSITIVE
    D; JGT

    @R1
    M = 0

    @END
    0; JMP

(POSITIVE)
    @R1
    M = 1

(END)
    @END
    0; JMP