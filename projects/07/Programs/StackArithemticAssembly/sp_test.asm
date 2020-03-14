// Exercise to implement:
// *SP = 17; SP ++
// In a stack machine state where RAM[0] = 258

    @258
    D = A
    @SP
    M = D

    @17
    D = A

    @SP
    A = M // RAM[258] will be selected
    M = D

    @SP
    M = M + 1

 (END)
    @END
    0; JMP