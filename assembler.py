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

first_line = file.readline()
parts = first_line.split()

if "START" in parts:
    locctr = int(parts[-1], 16)
else:
    locctr = 0
    file.seek(0) # Reset the file pointer to the beginning of the file

print("Location Counter: " + hex(locctr)) # Print the location counter

for line in file:
    split_line = line.split(".") # Remove comments from the line
    instruction = split_line[0].rstrip("\n") # Remove newline character from the instruction

    parts = instruction.split() # Split the instruction into parts (label, opcode, operand)
    if len(parts) == 2: # If the instruction has no label
        print("Opcode: " + parts[0])
        print("Operand: " + parts[1])
        if parts[0] in OPTAB: # If the opcode is in the OPTAB, print its format
            print("Format: " + OPTAB[parts[0]]["format"] + "\n")
            if OPTAB[parts[0]]["format"] == "3/4": # If the format is 3/4, increment the location counter by 3
                locctr += 3
            elif OPTAB[parts[0]]["format"] == "2": # If the format is 2, increment the location counter by 2
                locctr += 2
            elif OPTAB[parts[0]]["format"] == "1": # If the format is 1, increment the location counter by 1
                locctr += 1
            SYMTAB[parts[0]] = [format(locctr, "04X")] # Add the symbol and its location to the symbol table
        elif parts[0] not in OPTAB: # If the opcode is not in the OPTAB, print "N/A" for format
            print("Format: " + "N/A" + "\n")
    elif len(parts) == 3: # If the instruction has a label
        print("label: " + parts[0])
        print("Opcode: " + parts[1])
        print("Operand: " + parts[2])
        if parts[1] in OPTAB: # If the opcode is in the OPTAB, print its format
            print("Format: " + OPTAB[parts[1]]["format"] + "\n")
            if OPTAB[parts[1]]["format"] == "3/4": # If the format is 3/4, increment the location counter by 3
                locctr += 3
            elif OPTAB[parts[1]]["format"] == "2": # If the format is 2, increment the location counter by 2
                locctr += 2
            elif OPTAB[parts[1]]["format"] == "1": # If the format is 1, increment the location counter by 1
                locctr += 1
            SYMTAB[parts[1]] = [format(locctr, "04X")] # Add the symbol and its location to the symbol table
        elif parts[1] not in OPTAB: # If the opcode is not in the OPTAB, print "N/A" for format
            print("Format: " + "N/A" + "\n")

print("SYMTAB: " + str(SYMTAB)) # Print the symbol table