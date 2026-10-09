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
file.close() # Close the input file
intermediate.close() # Close the intermediate file

# PASS 2
intermediate = open("output/intermediate.txt", "r") # Open the intermediate file for reading
intermediate.readline() # Skip the header line

for line in intermediate:
    xbpe = [0, 0, 0, 0] # Initialize the xbpe flags to 0
    parts = line.split() # Split the line into parts (locctr, label, opcode, operand)

    if len(parts) == 3: # If the line has 3 parts, it means there is no label
        locctr = parts[0]
        label = ""
        opcode = parts[1]
        operand = parts[2]
    elif len(parts) == 4: # If the line has 4 parts, it means there is a label
        locctr = parts[0]
        label = parts[1]
        opcode = parts[2]
        operand = parts[3]    

    if opcode in OPTAB: # If the opcode is in the OPTAB, print its binary representation
        opcode_value = int(OPTAB[opcode]["Opcode"], 16)
        if operand.startswith('#'): # If the operand starts with '#', it is an immediate addressing mode
            opcode_value += 1 # Add 1 to the opcode binary to indicate immediate addressing mode
            operand_number = operand[1:] # Remove the '#' from the operand
            xbpe_binary = ''.join(str(bit) for bit in xbpe) # Convert the xbpe flags to binary
            full_binary = format(opcode_value, '08b') + xbpe_binary + format(int(operand_number), '012b') # Concatenate the opcode binary and the xbpe binary
            object_code = format(int(full_binary, 2), '06X') # Convert the full binary to hexadecimal
            if operand_number.isdigit(): # If the operand is a number, convert it to decimal
                operand_value = format(int(operand_number), '012b') # Convert the operand to binary
            else: # If the operand is a symbol, look it up in the SYMTAB
                if operand_number in SYMTAB:
                    operand_value = SYMTAB[operand_number]
                else:
                    print(f"Error: Symbol {operand_number} not found in SYMTAB")
                    continue
        elif ",X" in operand: # If the operand contains ',X', it is an indexed addressing mode
            xbpe[0] = 1 # Set the x flag to 1
            opcode_value += 3 # Add 3 to the opcode binary to indicate indexed addressing mode
            target_address = SYMTAB.get(operand.split(",")[0], 0) # Get the target address from the SYMTAB
            Pc = int(locctr, 16) + 3 # Calculate the program counter (PC) by adding 3 to the current location counter
            displacement = target_address - Pc # Calculate the displacement by subtracting the PC from the target address
            if displacement >= -2048 and displacement <= 2047: # If the displacement is within the range of -2048 to 2047, it can be represented in 12 bits
                xbpe[2] = 1 # Set the p flag to 1
                operand_value = format(displacement & 0xFFF, '012b') # Convert the displacement to binary and mask it to 12 bits
            xbpe_binary = ''.join(str(bit) for bit in xbpe) # Convert the xbpe flags to binary
            full_binary = format(opcode_value, '08b') + xbpe_binary + operand_value # Concatenate the opcode binary and the xbpe binary
            object_code = format(int(full_binary, 2), '06X') # Convert the full binary to hexadecimal
        print(f"Opcode: {opcode}, Hex: {format(opcode_value, '02X')}, Binary: {format(opcode_value, '08b')}, Operand: {operand}, Address: {operand_value}, Object Code: {object_code}")
    elif SYMTAB: # If the opcode is not in the OPTAB, check if it is in the SYMTAB
        if label in SYMTAB:
            print(f"Operand: {label}, Decimal: {SYMTAB[label]}, Address: {format(SYMTAB[label], '04X')}")
        else:
            print(f"Operand: {operand}, Address: N/A")

    