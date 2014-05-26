# codeloader front end
import time


def getOpcode(operator):
    if operator == "ADD":
        return 0b0000, 0
    elif operator == "AND":
        return 0b0001, 0
    elif operator == "OR":
        return 0b0010, 0
    elif operator == "XOR":
        return 0b0011, 0
    elif operator == "NOR":
        return 0b0100, 0
    elif operator == "BEQ":
        return 0b0111, 0
    elif operator == "SUB":
        return 0b1000, 0
    elif operator == "WRITE":
        return 0b1100, 1
    elif operator == "LT":
        return 0b1101, 0
    elif operator == "BRANCH":
        return 0b1110, 2
    elif operator == "READ":
        return 0b1111, 3
    print "Compilation Error: '" + operator + "' is not a valid operator"
    input()
    exit(1)

def getRegister(token):
        rc = 0
        try:
            reg = int(token.replace("$", ""))
            if (reg < 16 and reg >= 0):
                return reg
            else:
                rc = 1
        except:
            rc = 2
        if (rc == 1 or rc == 2):
            print "Compilation Error: '" + token + "' is not a valid register, registers have an integer value between 0 and 15, preceeded by a '$'"
            input()
            exit(1)
    
def assemble_line(line):
    tokens = line.split(" ")
    operator = tokens[0]
    opcode, opType = getOpcode(operator.upper());
    instr = opcode
    # build instruction
    if opType == 0:
        instr = (instr * 16) + getRegister(tokens[1])
        instr = (instr * 16) + getRegister(tokens[2])
        instr = (instr * 16) + getRegister(tokens[3])
    elif opType == 1:
        instr = (instr * 256) + int(tokens[1])
        instr = (instr * 16) + getRegister(tokens[2])
    elif opType == 2:
        instr = (instr * 256) + int(tokens[1])
        instr = (instr * 16)
    elif opType == 3:
        instr = (instr * 256)
        instr = (instr * 16) + getRegister(tokens[1])
    return instr

def assemble(code):
    mc = []
    for line in code.split("\n"):
        if line == "":
            continue
        try:
            instr = assemble_line(line)
        except:
            print "Compilation Error - Invalid Command Structure: " + line
            return []
        msb = instr / 256
        lsb = instr - (msb * 256)
        mc += [msb, lsb]
    return mc


    
def main():
    code = "WRITE 1 $0\nADD $1 $0 $1\nBRANCH 1"
    mc = assemble(code)
    print mc


if __name__ == "__main__":
	main()    
    
