// Draws a filled rectangle at the screen's top left corner
// Rectangle's width is 16, the height is defined in RAM[0]

    @R0
    D = M
    @height
    M = D       // initializing height = RAM[0]

    @i
    M = 0       // initializing i as 0

    @32
    D = A
    @wordsperrow
    M = D       // one row consists of 32 words, each 16-bits -> as 16 * 32= 512

    @SCREEN
    D = A
    @address
    M = D       // address = 16384 (base address of the HACK screen)

(LOOP)
    @i
    D = M
    @height
    D = D - M

    @END
    D; JEQ      // or JGE - note that JGT would make height + 1 rows!!

    @address
    D = M
    A = D
    M = -1

    @i
    M = M + 1

    @wordsperrow
    D = M
    @address
    M = D + M

    @LOOP
    0; JMP

(END)
    @END
    0; JMP