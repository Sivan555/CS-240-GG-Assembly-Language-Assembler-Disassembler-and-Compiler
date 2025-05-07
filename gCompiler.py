#================================
# Name: gCompiler
# Takes C code and writes it as gCode
# 
#================================
import sys
import os

output = []
lastLabel = ""

binaryFile = "gasm.asm"
ofile = open(binaryFile, "w")


def main(filename):
    global output
    global loopStack
    global lastLabel
    output = []  # Reset output for each compilation

    with open(filename) as lines:
        for line in lines:
            line = line.strip()
            print("Line: " + line)
            # skipping empty lines and comments
            if not line or line.startswith("//"):
                continue
            
            if "int main" in line or "return" in line or "include" in line:
                continue  # Skip the main function declaration

            if "int" in line and '=' in line:
                setG(line)
                
            elif "printf" in line:
                printfG(line)

            elif "scanf" in line:
                readG(line)
            
            elif 'if' in line:
                sLine = line.replace(';', '').replace('if', '').strip()
                condition = sLine.replace('(', '').replace(')', '').strip()
                conditionals(condition)                

            elif 'while' in line:
                sLine = line.replace(';', '').replace('while', '').strip()
                condition = sLine.replace('(', '').replace(')', '').strip()
                output.append(".LOOP")
                conditionals(condition) 

            elif '}' in line:
                output.append(lastLabel)
                lastLabel = ""
            elif 'else' in line:
                #output.append(lastLabel)
                lastLabel = ".END"
                output.append(lastLabel)

            elif '=' in line and '+' in line:
                plusG(line)
            
            elif '=' in line and '-' in line:
                minusG(line)

            elif '=' in line and '*' in line:
                starG(line)

            elif '%' in line:
                modG(line)

            elif 'fabs' in line:
                sLine = line.replace(';', '').replace('fabs', '').strip().split('=')
                var = sLine[1].replace('(', '').replace(')', '').strip()
                output.append(f'SETB $g2, {var}')
                output.append('LOW $g1, $g2')
                
            elif 'rand' in line:
                sLine = line.replace(';', '').replace('rand', '').strip().split('=')
                var = sLine[1].replace('(', '').replace(')', '').strip()
                output.append('RAND $g1, $g2, $g3')

    writebin(output)


def writebin(b):
    for i in b:
        ofile.write(i)
        ofile.write("\n")

def setG(line):
    global output
    sLine = line.replace(';', '').replace('int', '').replace('float', '').strip()
    name = line.split('=')[0].strip()
    var = line.split('=')[1].strip()
    if 'int' in line:
        output.append(f"SETB $g1, {var}")
    elif 'float' in line:
        output.append(f"SETW $g1, {var}")

def printfG(line):
    global output
    sLine = line.replace(';', '').replace('printf', '').strip()
    str = sLine.replace('(', '').replace(')', '').replace('"', '').strip()
    output.append(f"SETS $gs, {str}")
    if '%d' in str:        
        output.append(f"PRINTI $gs")
    elif '%f' in str:
        output.append(f"PRINTF $gs")
    else:
        output.append(f"PRINTS $gs")

def readG(line):
    global output
    sLine = line.replace(';', '').replace('scanf', '').strip()
    str = sLine.replace('(', '').replace(')', '').replace('"', '').strip()
    if '%d' in str:
        output.append(f"READI $g1")
    elif '%f' in str:
        output.append(f"READF $g1")
    elif '%s' in str:
        output.append(f"READS $g1")

def plusG(line):
    global output
    sLine = line.replace(';', '').replace('=', '').strip()
    name = sLine.split('+')[0].strip()
    var = sLine.split('+')[1].strip()
    if var.isdigit():
        output.append(f"PLUSI $g1, {var}")
    else:
        output.append(f"PLUS $g1, $g2, $g3")

def minusG(line):
    global output
    sLine = line.replace(';', '').replace('=', '').strip()
    name = sLine.split('-')[0].strip()
    var = sLine.split('-')[1].strip()
    output.append(f"MINUS $g1, $g2, $g3")

def starG(line):
    global output
    sLine = line.replace(';', '').replace('=', '').strip()
    name = sLine.split('*')[0].strip()
    var = sLine.split('*')[1].strip()
    output.append(f"STAR $g1, $g2, $g3")

def modG(line):
    global output
    sLine = line.replace(';', '').replace('=', '').strip()
    name = sLine.split('%')[0].strip()
    var = sLine.split('%')[1].strip()
    output.append(f"MOD $g1, $g2, $g3")

def conditionals(condition):
    global output
    global lastLabel

    if '==' in condition:
        sLine = condition.replace('==', ' ').strip()
        var1 = sLine.split()[0].strip()
        var2 = sLine.split()[1].strip()
        lbl = ".LABEL"
        lastLabel = lbl 
        output.append(f"HOPEQ $g1, $g2, {lbl}")
    elif '<=' in condition:
        sLine = condition.replace('<=', ' ').strip()
        var1 = sLine.split()[0].strip()
        var2 = sLine.split()[1].strip()
        lbl = ".ENDL"
        lastLabel = lbl 
        output.append(f"HOPEQ $g1, $g2, {lbl}")        
    elif '<' in condition:
        sLine = condition.replace('<', ' ').strip()
        var1 = sLine.split()[0].strip()
        var2 = sLine.split()[1].strip()
        lbl = ".LABEL" 
        lastLabel = lbl
        output.append(f"HOPLT $g1, $g2, {lbl}")
    elif '>' in condition:
        sLine = condition.replace('>', ' ').strip()
        var1 = sLine.split()[0].strip()
        var2 = sLine.split()[1].strip()
        lbl = ".LABEL" 
        lastLabel = lbl
        output.append(f"HOPGT $g1, $g2, {lbl}")



if __name__ == "__main__":    
    main(sys.argv[1])
    #main('C:\\code\\workspace\\iang\\final\\iang\\fizzbuzz.c')
    #print("Code generated to File: " + binaryFile)
        