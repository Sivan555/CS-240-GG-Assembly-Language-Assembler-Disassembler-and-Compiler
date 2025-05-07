import sys
import os

#======================================================================
# File: gAssembler.py
# AUTHOR:  Ian Gallardo
# DATE: 05-05-2025
# DESCRIPTION:  Simple assembler for custom language
#======================================================================

'''
-- Registers --
$gz   0x00
$grt  0x01
$gs   0x02
$ga1  0x03
$ga2  0x04

$g1  0x10
$g2  0x11
$g3  0x12
$g5  0x13
$g6  0x14


-- Arithmic --
PLUS    0x0000    - PLUS   $g1, $g2, $g3
MINUS   0x0001    - MINUS  $g1, $g2, $g3
STAR    0x0002    - START  $g1, $g2, $g3
CMP     0x0003    - CMP    $g1, $g2

HOPEQ   0x0004     - HOPEQ $g1, $g2, label        - banch code
HOPGT   0x0005     - HOPEQ $g1, $g2, label        - banch code
HOPLT   0x0006     - HOPEQ $g1, $g2, label        - banch code
LEAP    0x0007     - LEAP label         - jump

SETB    0x0008     - SETB $g1, 0xAB    - load byte
SETW    0x0009     - SETB $g1, 0xABCD  - loadw
SETS    0x000A     - SETS $g1, $g2, "str"


-- Special --
MOD     0x000B     - MOD  $g1, $g2, $g3
PRINTS  0x000C     - PRINTS $gs 
PRINTI  0x000C     - PRINTI $gs
PRINTF  0x000C     - PRINTF $gs
READS   0x000D     - READS $gs
READI   0x000D     - READI $gs
READF   0x000D     - READF $gs
LOW     0x000E     - LOW $g1, $g2
RAND    0x000F     - RAND $g1, $g2, $g3
GAMBLE  0x0010     - GAMBLE

'''
opCodes = {
    "PLUS"   : "00000",
    "MINUS"  : "00001",
    "STAR"   : "00010",
    "CMP"    : "00011",
    "HOPEQ"  : "00100",
    "HOPGT"  : "00101",
    "HOPLT"  : "00110",
    "LEAP"   : "00111",
    "SETB"   : "01000",
    "SETW"   : "01001",
    "SETS"   : "01010",
    "MOD"    : "01011",
    "PRINTS" : "01100",
    "PRINTI" : "01100",
    "PRINTF" : "01100",
    "READS"  : "01101",
    "READI"  : "01101",
    "READF"  : "01101",
    "LOW"    : "01110",
    "RAND"   : "01111",
    "GAMBLE" : "10000",
    "PLUSI"  : "10001",
}
funcCodes = {
    "PRINTS": "10000",
    "PRINTI": "10001",
    "PRINTF": "10010",
    "READS" : "10011",
    "READI" : "10100",
    "READF" : "10101",
}

registers = {
    "$gz"  : "00000",   # zero
    "$grt" : "00001",   # return ptr
    "$gs"  : "00010",   # special register for syscalls
    "$ga1" : "00011",   # argument register
    "$ga2" : "00100",   # argument register
    "$g1"  : "10001",   # temp register
    "$g2"  : "10010",   # temp register
    "$g3"  : "10011",   # temp register
    "$g4"  : "10100",   # temp register
    "$g5"  : "10101",   # temp register
    "$g6"  : "10110",   # temp register
}
shift_logic_amount = "00000"
labelTAG = "11111111"

binaryFile = "gRom.bin"
ofile = open(binaryFile, "w")	

def writebin(b):
    ofile.write(b)
    ofile.write("\n")

#hanlde labels and add special tag in front to know its a label  labelTAG
def convertLabel(label): #labels start with period.  ex  '.label'    
    binary_string = ''.join(format(ord(char), '08b') for char in label)
    return labelTAG + binary_string

#convert string to binary
def convertString(msg): 
    binary_string = ''.join(format(ord(char), '08b') for char in msg)
    return binary_string

def process1reg(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas    
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]]
    if cmd[0] in funcCodes:
        binaryRep = binaryRep + funcCodes[ cmd[0] ]
    writebin(binaryRep)

def process2reg(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas
    cmd[2] = cmd[2].replace(",", "")  #remove commas    

    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + registers[cmd[2]]
    if cmd[0] in funcCodes:
        binaryRep = binaryRep + funcCodes[ cmd[0] ]

    writebin(binaryRep)

def process3reg(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas
    cmd[2] = cmd[2].replace(",", "")  #remove commas
    cmd[3] = cmd[3].replace(",", "")  #remove commas
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + registers[cmd[2]] + registers[cmd[3]]
    if cmd[0] in funcCodes:
        binaryRep = binaryRep + funcCodes[ cmd[0] ]
    writebin(binaryRep)

def processRegLabel(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas
    cmd[2] = cmd[2].replace(",", "")  #remove commas    
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + registers[cmd[2]] + convertLabel( cmd[3] )
    writebin(binaryRep)

def process1RegValueB(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas    
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + format( int(cmd[2]), '08b' )    
    writebin(binaryRep)

def process1RegValueW(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas    
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + format( int(cmd[2]), '32b' )    
    writebin(binaryRep)

def process1RegValueS(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas    
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + convertString( cmd[2] )
    writebin(binaryRep)

def process2RegValue(cmd):    
    cmd[1] = cmd[1].replace(",", "")  #remove commas    
    cmd[2] = cmd[2].replace(",", "")  #remove commas    
    binaryRep = opCodes[cmd[0]] + registers[cmd[1]] + registers[cmd[2]] + format( int(cmd[2]), '08b' )    
    writebin(binaryRep)

def processLabel(cmd):    
    binaryRep = opCodes[cmd[0]] + convertLabel( cmd[1] )
    writebin(binaryRep)

def parseInstruction(line: str):
    print(line)
    cmd = line.split() #split the line by spaces into array
    
    if ( cmd[0] == "PLUS" or cmd[0] == "MINUS" or cmd[0] == "STAR" or cmd[0] == "RAND" or cmd[0] == "MOD"):
        #<CMD>   $g1, $g2, $g3 
        process3reg(cmd)        
    elif (cmd[0] == "CMP" or cmd[0] == "LOW"):
        #<CMD>  $g1, $g2        
        process2reg(cmd)
    elif (cmd[0] == "HOPEQ" or cmd[0] == "HOPGT" or cmd[0] == "HOPLT" ):
        #<CMD> $g1, $g2, .label  
        processRegLabel(cmd)
    elif (cmd[0] == "LEAP" ):
        #<CMD> .label
        processLabel(cmd)
    elif (cmd[0] == "SETB"):
        #<CMD> $g1, 0xA    
        process1RegValueB(cmd)
    elif ( cmd[0] == "SETW" ):
        #<CMD> $g1, 0xABCD 
        process1RegValueW(cmd)        
    elif (cmd[0] == "SETS"):
        #<CMD> $g1, "str"
        process1RegValueS(cmd)
    elif (cmd[0] == "PRINTS" or cmd[0] == "PRINTI"  or cmd[0] == "PRINTF" or \
          cmd[0] == "READS" or cmd[0] == "READI"  or cmd[0] == "READF" or \
          cmd[0] == "GAMBLE" ):
        #<CMD> $g1,
        process1reg(cmd)
    elif( cmd[0] == "PLUSI"):
        #<CMD> $g1, $g2, 0xABCD 
        process2RegValue(cmd)
    else:
        print("Error: unknown command: " + line + "\n")
        exit(1)


def main (filename: str):
    with open(filename) as f:
        for line in f:
            #make sure there is something in the line
            line = line.strip()
            if not line:
                continue

            # Ignore comments
            if line[0]=='#':
                continue

            #keep track of the labels
            if line[0].startswith("."):
                lbl = convertLabel(line)
                writebin(lbl)
                continue
            
            parseInstruction(line)



if __name__ == "__main__":    
    main(sys.argv[1])
    print("Code generated to File: " + binaryFile)
