SETB $g1, 1
SETB $g2, 100
SETB $g6, 1

.LOOP
HOPEQ $g1, $g2, .END
PLUS $g1, $g1, $g6

SETB $g3, 15
MOD $g4, $g1, $g3
HOPEQ $g4, $gz .FIFTEEN

SETB $g3, 3
MOD $g4, $g1, $g3
HOPEQ $g4, $gz .THREE

SETB $g3, 5
MOD $g4, $g1, $g3
HOPEQ $g4, $gz .FIVE

PRINTI $g1
LEAP .LOOP

.FIFTEEN
SETS $gs FizzBuzz
PRINTS $gs
LEAP .LOOP

.THREE
SETS $gs Fizz
PRINTS $gs
LEAP .LOOP

.FIVE
SETS $gs Buzz
PRINTS $gs
LEAP .LOOP

.END
