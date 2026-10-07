# OPTAB dictionary containing the opcode and format of each SIC/XE instruction
OPTAB =  {
    "ADD":{
        "format": "3/4",
        "Opcode": "18"
    },

    "ADDR":{
        "format": "2",
        "Opcode": "90"
    },

    "COMPR":{
        "format": "2",
        "Opcode": "A0"
    },

    "JLT":{
        "format": "3/4",
        "Opcode": "38"
    },

    "LDA":{
        "format": "3/4",
        "Opcode": "00"
    },

    "LDS":{
        "format": "3/4",
        "Opcode": "6C"
    },

    "LDT":{
        "format": "3/4",
        "Opcode": "74"
    },

    "LDX":{
        "format": "3/4",
        "Opcode": "04"
    },

    "STA":{
        "format": "3/4",
        "Opcode": "0C"
    }
}

SYMTAB = {} # Initialize the symbol table as an empty dictionary

locctr = 0 # Initialize the location counter to 0

file = open("input/basic.txt", "r")
intermediate = open("output/intermediate.txt", "w") # Open the intermediate file for writing
intermediate.write(f"{'LOCCTR':<10}{'LABEL':<10}{'OPCODE':<10}{'OPERAND':<10}\n") # Write the header to the intermediate file

first_line = file.readline()
parts = first_line.split()

if "START" in parts:
    locctr = int(parts[-1], 16)
else:
    locctr = 0
    file.seek(0) # Reset the file pointer to the beginning of the file

# PASS 1
for line in file:
    split_line = line.split(".") # Remove comments from the line
    instruction = split_line[0].rstrip("\n") # Remove newline character from the instruction

    parts = instruction.split() # Split the instruction into parts (label, opcode, operand)
    if len(parts) == 2:
        label = ""
        opcode = parts[0]
        operand = parts[1]
    elif len(parts) == 3:
        label = parts[0]
        opcode = parts[1]
        operand = parts[2]

    if label != "":
        SYMTAB[label] = locctr # Add the symbol and its location to the symbol table
    intermediate.write(f"{format(locctr, '04X'):<10}{label:<10}{opcode:<10}{operand:<10}\n") # Write the instruction to the intermediate file
    if opcode in OPTAB: # If the opcode is in the OPTAB, print its format
        if OPTAB[opcode]["format"] == "3/4":
            locctr += 3
        elif OPTAB[opcode]["format"] == "2":
            locctr += 2 
        elif OPTAB[opcode]["format"] == "1":
            locctr += 1
    elif opcode not in OPTAB: # If the opcode is not in the OPTAB, print "N/A" for format
        if opcode == "WORD": 
            locctr += 3
        elif opcode == "RESW":
            locctr += 3 * int(operand)
        elif opcode == "RESB":
            locctr += int(operand)
        elif opcode == "BYTE":
            locctr += len(operand) - 3 # Subtract 3 to account for the C'' or X'' notation
        else:
            print("Format: " + "N/A" + "\n")
print("SYMTAB: " + str(SYMTAB)) # Print the symbol table
