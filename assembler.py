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
intermediate.write("LOCCTR\tLABEL\tOPCODE\tOPERAND\n") # Write the header to the intermediate file

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
    if len(parts) == 2: # If the instruction has no label
        intermediate.write(format(locctr, "04X") + "\t\t\t" + parts[0] + "\t\t" + parts[1] + "\n") # Write the instruction to the intermediate file
        if parts[0] in OPTAB: # If the opcode is in the OPTAB, print its format
            if OPTAB[parts[0]]["format"] == "3/4": # If the format is 3/4, increment the location counter by 3
                locctr += 3
            elif OPTAB[parts[0]]["format"] == "2": # If the format is 2, increment the location counter by 2
                locctr += 2
            elif OPTAB[parts[0]]["format"] == "1": # If the format is 1, increment the location counter by 1
                locctr += 1
        elif parts[0] not in OPTAB: # If the opcode is not in the OPTAB, print "N/A" for format
            if parts[0] == "WORD": 
                locctr += 3
            elif parts[0] == "RESW":
                locctr += 3 * int(parts[1])
            elif parts[0] == "RESB":
                locctr += int(parts[1])
            elif parts[0] == "BYTE":
                locctr += len(parts[1]) - 3 # Subtract 3 to account for the C'' or X'' notation
            else:
                print("Format: " + "N/A" + "\n")
    elif len(parts) == 3: # If the instruction has a label
        SYMTAB[parts[0]] = locctr # Add the symbol and its location to the symbol table
        intermediate.write(format(locctr, "04X") + "\t" + parts[0] + "\t" + parts[1] + "\t" + parts[2] + "\n") # Write the instruction to the intermediate file
        if parts[1] in OPTAB: # If the opcode is in the OPTAB, print its format
            if OPTAB[parts[1]]["format"] == "3/4": # If the format is 3/4, increment the location counter by 3
                locctr += 3
            elif OPTAB[parts[1]]["format"] == "2": # If the format is 2, increment the location counter by 2
                locctr += 2
            elif OPTAB[parts[1]]["format"] == "1": # If the format is 1, increment the location counter by 1
                locctr += 1
        elif parts[1] not in OPTAB: # If the opcode is not in the OPTAB, print "N/A" for format
            if parts[1] == "WORD": 
                locctr += 3
            elif parts[1] == "RESW":
                locctr += 3 * int(parts[2])
            elif parts[1] == "RESB":
                locctr += int(parts[2])
            elif parts[1] == "BYTE":
                locctr += len(parts[2]) - 3 # Subtract 3 to account for the C'' or X'' notation
            else:
                print("Format: " + "N/A" + "\n")
print("SYMTAB: " + str(SYMTAB)) # Print the symbol table