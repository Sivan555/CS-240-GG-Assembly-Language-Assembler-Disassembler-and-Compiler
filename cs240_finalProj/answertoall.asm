SETB $g1, 0
SETB $g2, 42
SETS $gs, What is the Answer to life?
PRINTS $gs
READI $g1
HOPEQ $g1, $g2, .GOOD
SETS $gs, Wrong!
PRINTS $gs
LEAP .END
.GOOD   
SETS $gs, Right!
PRINTS $gs

.END
