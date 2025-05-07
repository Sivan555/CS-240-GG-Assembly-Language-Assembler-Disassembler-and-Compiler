import sys
import os

#======================================================================
# File: gDisAssembler.py
# AUTHOR:  Ian Gallardo
# DATE: 05-05-2025
# DESCRIPTION:  Simple DisAssembler for custom language
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
MOD     0x000B     - MOD  $g1, $g2, $g3

-- Special --
PRINTS  0x000C     - PRINTS $gs 
PRINTI  0x000C     - PRINTS $gs
PRINTF  0x000C     - PRINTS $gs
READS   0x000D     - PRINTS $gs
READI   0x000D     - READI $gs
READF   0x000D     - READF $gs
LOW     0x000E     - LOW $g1, $g2
RAND    0x000F     - RAND $g1, $g2, $g3
GAMBLE  0x0010     - GAMBLE

'''
opCodes = {
    "00000" : "PLUS",
    "00001" : "MINUS",
    "00010" : "STAR:",
    "00011" : "CMP",    
    "00100" : "HOPEQ",
    "00101" : "HOPGT",
    "00110" : "HOPLT",
    "00111" : "LEAP",
    "01000" : "SETB",
    "01001" : "SETW",
    "01010" : "SETS",
    "01011" : "MOD",
    "01100" : "PRINTS",
    "01100" : "PRINTI",
    "01100" : "PRINTF",
    "01101" : "READS",
    "01101" : "READI", 
    "01101" : "READF",
    "01110" : "LOW",
    "01111" : "RAND",
    "10000" : "GAMBLE",
    "10001" : "PLUSI"
}

funcCodes = {
    "10000" : "PRINTS",
    "10001" : "PRINTI",
    "10010" : "PRINTF",
    "10011" : "READS",
    "10100" : "READI", 
    "10101" : "READF"
}

registers = {
    "00000" : "$gz",   # zero
    "00001" : "$grt",   # return ptr
    "00010" : "$gs",   # special register for syscalls
    "00011" : "$ga1",   # argument register
    "00100" : "$ga2",   # argument register
    "10001" : "$g1",   # temp register
    "10010" : "$g2",   # temp register
    "10011" : "$g3",   # temp register
    "10100" : "$g4",   # temp register
    "10101" : "$g5",   # temp register
    "10110" : "$g6"   # temp register
}
shift_logic_amount = "00000"
labelTAG = "11111111"
asmFile = "back2Asm.asm"
ofile = open(asmFile, "w")	

def writebin(b):
    ofile.write(b)
    ofile.write("\n")

def convertLabel(line):
    tag = line[0:8]   
    labelBin =  line[8:]  #remove special tag
    labelStr = ""
    #11111111 00101110
    for i in range( 0, len(labelBin), 8 ):  #read char of label in 8 bits
        ch = labelBin[i:i+8]
        chs = chr(int(ch, 2))
        labelStr = labelStr + chs
    return labelStr

def convertStr(line):
    msgStr = ""
    for i in range( 0, len(line), 8 ):  #read char of label in 8 bits
        ch = line[i:i+8]
        chs = chr(int(ch, 2))
        msgStr = msgStr + chs
    return msgStr

def convertValue(line):
    valStr = ""    
    for i in range( 0, len(line), 8 ):  #read char of label in 8 bits
        chv = line[i:i+8]
        valStr = valStr + str(int(chv, 2))    
    return valStr

def processCmdWithFunc(cmd, line):
    cmdStr = funcCodes [line[5:] ] + " " + registers[line[0:5]]
    writebin(cmdStr)

def process1reg(cmd, line):
    cmdStr = opCodes[cmd] + " " + registers[line[0:5]]
    writebin(cmdStr)

def process2reg(cmd, line):
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]] + ", " +  registers[line[5:10]]
    writebin(cmdStr)

def process3reg(cmd, line):
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]] + ", " +  registers[line[5:10]] + ", " +  registers[line[10:15]]
    writebin(cmdStr)

def processRegLabel(cmd, line):   
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]] + ", " +  registers[line[5:10]] + ", " +  convertLabel(line[10:])
    writebin(cmdStr)

def process1RegValueB(cmd, line):    
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]]  + ", " +  convertValue(line[5:])
    writebin(cmdStr)

def process1RegValueW(cmd, line): 
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]]  + ", " +  convertValue(line[5:])
    writebin(cmdStr)

def process1RegValueS(cmd, line): 
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]]  + ", " +  convertStr(line[5:])
    writebin(cmdStr)

def process2RegValue(cmd, line): 
    cmdStr = opCodes[cmd] + " " +  registers[line[0:5]] + ", " +  registers[line[5:10]] + ", " +  convertValue(line[10:])
    writebin(cmdStr)

def processLabel(cmd, line):    
    cmdStr = opCodes[cmd] + " " +  convertLabel(line)
    writebin(cmdStr)              

def processCommand( cmd, line):
    print("Processing cmd " + opCodes[cmd])
    if ( cmd == "00000" or cmd == "00001" or cmd == "00010" or cmd == "01111" or cmd == "01011"):
        #<CMD>   $g1, $g2, $g3 
        process3reg(cmd, line)        
    elif (cmd == "00011" or cmd == "001110" or cmd == "010000"):
        #<CMD>  $g1, $g2        
        process2reg(cmd, line)
    elif (cmd == "00100" or cmd == "00101" or cmd == "00110" ):
        #<CMD> $g1, $g2, .label  
        processRegLabel(cmd, line)
    elif (cmd == "00111" ):
        #<CMD> .label
        processLabel(cmd, line)
    elif (cmd == "01000"):
        #<CMD> $g1, 0xA     || # SETB $g1, 0xABCD
        process1RegValueB(cmd, line)
    elif ( cmd == "01001" ):
        #<CMD> $g1, 0xABCD 
        process1RegValueW(cmd, line)        
    elif (cmd == "01010"): #SETS
        #<CMD> $g1, "str"  
        process1RegValueS(cmd, line)
    elif (cmd == "01100" or  cmd == "01101"):  #PRINTS PRINTI PRINTF READS READI READF     
        processCmdWithFunc(cmd, line)
    elif( cmd == "10000" ):
        process1reg(cmd, line)
    elif( cmd[0] == "10001"):
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

            #check label
            if (line[0:8] == labelTAG):
                lbl = convertLabel(line)
                writebin(lbl)
                continue

            cmdCode = line[0:5]
            processCommand( cmdCode, line[5:])
            



if __name__ == "__main__":
    main(sys.argv[1])
    print("Code generated to File: " + asmFile)    
