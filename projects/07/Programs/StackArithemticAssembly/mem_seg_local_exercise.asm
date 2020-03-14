// Exercise to implement:
// addr = LCL + 2, SP--, *addr=*SP
// In a stack machine state where:
//      SP / RAM[0] = 258; LCL / RAM[1] = 1015; stack has values 12 and 5
//      and stack base memory address is 256; local segment's base address is 1015

    @258        // setting stack pointer to 258
    D = A
    @SP
    M = D

    @1015       // memory segment local's base address
    D = A
    @LCL
    M = D

    @12         // RAM[256] = 12
    D = A
    @256
    M = D

    @5          // RAM[257] = 5
    D = A
    @257
    M = D

    @2          // setting up address to be used for pop local 2 command
    D = A       // target address will be 1017 = local's segment base address (1015) + 2 = 1017
    @LCL
    D = M + D
    @addr
    M = D       // memory pointer for target address is stored in a variable

    @SP         // decrementing SP pointer:
    M = M - 1       // RAM[0] now points to memory location RAM[257]

    A = M       // *SP -> RAM[257] selected:
    D = M           // it's value is stored in the data register

    @addr       // *addr = D -> selecting:
    A = M           // RAM[addr] is selected
    M = D           // RAM[addr] is now D -> result RAM[1057] = 5

(END)
    @END
    0; JMP

