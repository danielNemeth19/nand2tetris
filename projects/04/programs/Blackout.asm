// Blackens the whole screen

    @SCREEN
    D = A
    @address
    M = D       // address = 16384 (base address of the HACK screen)

    @8192
    D = A
    @allscreenregisters
    M = D       // number of registers (words) in screen memory (256 rows * 32 words / row = 8192)

    @i
    M = 0

(LOOP)
    @i
    D = M
    @allscreenregisters
    D = D - M

    @STOP
    D; JEQ

    @address
    D = M
    A = D
    M = -1

    @i
    M = M + 1

    @address
    M = M + 1

    @LOOP
    0; JMP

(STOP)
    @STOP
    0; JMP