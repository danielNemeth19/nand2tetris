// Sets n length of registers to -1 starting from the address denoted by variable arr
// Assume that n=10 and arr=100

    @10     // Note that A register is used here as a data register (not as an address register)
    D = A
    @n
    M = D       // initializing n as 10

    @100
    D = A
    @arr
    M = D       // initializing arr as 100

    @i
    M = 0

(LOOP)
    @i
    D = M
    @n
    D = D - M

    @END
    D; JGE      // or use JEQ (equals to 0)

    @arr
    D = M
    @i
    A = D + M       // setting A register to arr + i and by that selecting RAM[arr + i]
    M = -1          // setting value of RAM[arr + i] = -1

    @i
    M = M + 1

    @LOOP
    0; JMP

(END)
    @END
    0; JMP