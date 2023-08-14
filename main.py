'''
Assembler (project.py)
Program Description: This is our project and we want to create an assembler with python.
                     Which can support and , or , add , sub , jump and it should have ability of working with memory.
Author: Mohammad Hossein Jabbari
University: Shiraz University
Student Number: 9932125
version: 3.1.1
Creation Date: 12/27/2021

Sources: https://x86.puri.sm/ , http://www.c-jump.com/CIS77/CPU/x86/lecture.html#X77_0080_mod_reg_r_m_byte_reg
         http://www.c-jump.com/CIS77/images/x86_register_encoding.png , https://stackoverflow.com/questions/384871/building-an-assembler ,...
         
         
         
Some conditions:

            Registers:
                We check if the entered name available in reg_8, reg_16 or reg_32.
                
            Label:
                We check if the line include label by looking for ":".
                
            Memory:
                We check if the name is memory by checking if it's in brackets and
                The inner name is valid register.
                
            Validity:
                Check if entered instruction isn't supported!
                Check invalidity of amount of operands of instruction!
                Check invalidity Type of destination and source operands!
                Check incompatibility of destination and source size!
                
            Instruction:
                We have to check the included instruction of the line if it's in supported instructions of project.
                
Machine code convert solution:
            JMP -> <Opcode + Bytes Between JMP Instruction and the Label>
            Add, SUB, AND, OR -> <Opcode + MOD + R/M>

Passing bytes method:
            for JMP / 8-bit / 32-bit: add(2)
            for 16-bit: add(3)
            
'''

# Constant datas, that we're gonna use in the assembler.
opcode_table = { 
            "ADD": {8: {False: r"\x00", True: r"\x02"}, 16: {False: r"\x66\x01", True: r"\x66\x03"}, 32: {False: r"\x01", True: r"\x03"}},
            "SUB": {8: {False: r"\x28", True: r"\x2A"}, 16: {False: r"\x66\x29", True: r"\x66\x2B"}, 32: {False: r"\x29", True: r"\x2B"}},
            "AND": {8: {False: r"\x20", True: r"\x22"}, 16: {False: r"\x66\x21", True: r"\x66\x23"}, 32: {False: r"\x21", True: r"\x23"}},
             "OR": {8: {False: r"\x08", True: r"\x0A"}, 16: {False: r"\x66\x09", True: r":\x66\x0B"},32: {False: r"\x09", True: r"\x0B"}}
        }

REG_values_of_registers = {  
        "AL": "000", "AX": "000", "EAX": "000",
        "CL": "001", "CX": "001", "ECX": "001",
        "DL": "010", "DX": "010", "EDX": "010",
        "BL": "011", "BX": "011", "EBX": "011",
        "AH": "100", "SP": "100", "ESP": "100",
        "CH": "101", "BP": "101", "EBP": "101",
        "DH": "110", "SI": "110", "ESI": "110",
        "BH": "111", "DI": "111", "EDI": "111"
    }

reg_8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
reg_16 = ["AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI"]
reg_32 = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]

supported_instructions = ["ADD", "SUB", "AND", "OR", "JMP"]
is_running = True


# A function to find REG & R/M byte with the help of REG valuse of registers.
def REG_RM_builder(goal_op,from_op):

    if (goal_op.startswith('[') and goal_op.endswith(']') and is_reg(goal_op[1:][:-1])):
        REG = REG_values_of_registers[from_op]
        RM = REG_values_of_registers[goal_op[1:][:-1]]
        
    elif (from_op.startswith('[') and from_op.endswith(']') and is_reg(from_op[1:][:-1])):
        REG = REG_values_of_registers[goal_op]
        RM = REG_values_of_registers[from_op[1:][:-1]]
        
    else:
        REG = REG_values_of_registers[from_op]
        RM = REG_values_of_registers[goal_op]

    return REG + RM


# Mod finder function in recognizing between memory or register.
def mod_setter(goal_op,from_op):
    
    if (goal_op.startswith('[') and goal_op.endswith(']')
        and is_reg(goal_op[1:][:-1])) or (from_op.startswith('[')
                                          and from_op.endswith(']') and is_reg(from_op[1:][:-1])):
        return "00"
    else:
        return "11"


# A function that convert decimal number to hexadecimal.
def signedDecimal2hexadecimalConvertor(signedDecimal):
    
    convertedNumber = str(hex((signedDecimal) & (2**8-1)))[2:].upper()
    return r"\x0" + convertedNumber if len(convertedNumber) == 1 else r"\x" + convertedNumber


# A function that convert binary to hexadecimal.
def binary2hexadecimalConvertor(binaryNumber):
    
    convertedNumber = str(hex(int(binaryNumber, 2)))[2:].upper()
    return r"\x0" + convertedNumber if len(convertedNumber) == 1 else r"\x" + convertedNumber


# The counter which
def label_looking_counter(project_test_case,test_cases,goal_op):

    counter = 0
    for j in test_cases:
        j = j.split()
        
        if j[0][:-1] == goal_op:
            break
        
        else:
            if test_case_validity(project_test_case) and not j[0].endswith(':'):
                
                if j[0] == "JMP":
                    counter += 2
                    
                else:
                    if j[1][:-1] in reg_16 or j[2] in reg_16:
                        counter += 3
                        
                    else:
                        counter += 2
    return counter


# This function return the number of bits of the entered register. 
def x_bits(register_n):
    
    if (register_n.startswith('[') and register_n.endswith(']')) and is_reg(register_n[1:][:-1]):
        register_n = register_n[1:][:-1]
    
    if register_n in reg_8:
        return 8
    
    elif register_n in reg_16:
        return 16
    
    elif register_n in reg_32:
        return 32


# A function that help us with OPCODE-table to build the opcode of the entered instruction.
def opcode_builder(instruction,goal_op,from_op):
    if instruction == "JMP":
        return r"\xEB"
    else:
        return opcode_table[instruction][x_bits(goal_op)][from_op.startswith('[') and from_op.endswith(']') and is_reg(from_op[1:][:-1])]


# This function is the solver of project by converting assembly code to machine code, what we want. 
def machine_code_cal(instruction,goal_op,from_op,test_cases,project_test_case,finisher_counter):

    if instruction == "JMP":
        opcode = opcode_builder(instruction,goal_op,from_op)
        main_counter_helper = label_looking_counter(project_test_case,test_cases,goal_op) - finisher_counter

        machine_code = opcode + \
            signedDecimal2hexadecimalConvertor(main_counter_helper)
    else:
        opcode = opcode_builder(instruction,goal_op,from_op)
        MOD = mod_setter(goal_op,from_op)
        REG_RM = REG_RM_builder(goal_op,from_op)

        machine_code = opcode + binary2hexadecimalConvertor(MOD + REG_RM)

    return machine_code


# A function that check if the entered name is a valid Register.
def is_reg(var):
    return_value = False
    if var in reg_8 or var in reg_16 or var in reg_32:
        return_value = True
    return return_value


# A function that check if the entered name is a valid Memory.
def is_memory(var):
    return (var.startswith('[') and var.endswith(']')) and is_reg(var[1:][:-1])


# The validity test case checker function.
def test_case_validity(project_test_case):

    if not project_test_case[0] in supported_instructions:
        print("Input:", project_test_case)
        print("Entered instruction is'nt valid!\n")
        return False

    two_able_instructions = ["JMP"]
    three_able_instructions = ["ADD", "SUB", "AND", "OR"]
    
    if project_test_case[0] in two_able_instructions:
        if len(project_test_case) != 2:
            print(f"Incorrect number of operands for {project_test_case[0]}'s instruction!\n")
            return False

    elif project_test_case[0] in three_able_instructions:
        if len(project_test_case) != 3:
            print("Input:", project_test_case)
            print(f"Incorrect number of operands for {project_test_case[0]}'s instruction!\n")
            return False

        if not ((is_reg(project_test_case[1][:-1]) or (project_test_case[1][:-1].startswith('[') and
                                                       project_test_case[1][:-1].endswith(']')) and is_reg(project_test_case[1][:-1][1:][:-1])
                                                        ) and ((is_reg(project_test_case[2])
                                                        or (project_test_case[2].startswith('[') and
                                                        project_test_case[2].endswith(']')) and is_reg(project_test_case[2][1:][:-1])))):
            print("Input:", project_test_case)
            print("Invalid type for destination or source operand!\nMust be a valid register or memory.\n")
            return False

        if not (project_test_case[2].startswith('[') and project_test_case[2].endswith(']')
                ) and is_reg(project_test_case[2][1:][:-1]) and x_bits(project_test_case[1][:-1]) != x_bits(project_test_case[2]):
            print("Input:", project_test_case)
            print("Invalid type for destination or source operand!\nMust have the same size.\n")
            return False
    return True


# A function that help us to make our project file readable.
def read_file():
    input_file = open('inp.txt', 'r')
    test_cases = [test_case[:-1].upper() if test_case.endswith("\n")
             else test_case.upper() for test_case in input_file.readlines()]
    return test_cases


# Here we go!
def main():
    
    # A counter to count passed bytes.
    finisher_counter = 0
    test_cases = read_file()
    for i in range(len(test_cases)):
        project_test_case = test_cases[i].split(' ')
        if not project_test_case[0].endswith(':') and test_case_validity(project_test_case):
            
            if project_test_case[0] == "JMP":
                finisher_counter += 3
            else:
                if project_test_case[1][:-1] in reg_16 or project_test_case[2] in reg_16:
                    finisher_counter += 3
                else:
                    finisher_counter += 2
                    
            instruction = project_test_case[0].upper()
            if instruction == "JMP":
                goal_op = project_test_case[1]
            else:
                goal_op = project_test_case[1][:-1].upper()
                from_op = project_test_case[2].upper()
            print("Input:", test_cases[i])
            solve = machine_code_cal(instruction,goal_op,from_op,test_cases,project_test_case,finisher_counter)
            if solve != None:
                print("Machine Code Output:",solve,end="\n*\n")
 


# Go ahead!
main()