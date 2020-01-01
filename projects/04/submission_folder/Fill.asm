// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    @KBD
    D = A
    @keyboard
    M = D

    @8192
    D = A
    @registers
    M = D       // number of registers (words) in screen memory (256 rows * 32 words / row = 8192)

(LOOP)
    @SCREEN
    D = A
    @address
    M = D       // address = 16384 (base address of the HACK screen)

    @0
    D = A
    @i
    M = D

    @keyboard
    D = M
    A = D
    D = M
    @BLACKLOOP
    D; JNE
    @WHITELOOP
    D; JEQ


(BLACKLOOP)
    @i
    D = M
    @registers
    D = D - M
    @LOOP
    D; JEQ

    @address
    D = M
    A = D
    M = -1

    @i
    M = M + 1

    @address
    M = M + 1

    @BLACKLOOP
    0; JMP

(WHITELOOP)
    @i
    D = M
    @registers
    D = D - M
    @LOOP
    D; JEQ

    @address
    D = M
    A = D
    M = 0

    @i
    M = M + 1

    @address
    M = M + 1

    @WHITELOOP
    0; JMP
