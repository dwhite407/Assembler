file = open("input/basic.txt", "r")

for line in file:
    split_line = line.split(".")
    instruction = split_line[0].rstrip("\n")

    parts = instruction.split()
    if len(parts) == 2:
        print("Opcode: " + parts[0])
        print("Operand: " + parts[1] + "\n")
    elif len(parts) == 3:
        print("label: " + parts[0])
        print("Opcode: " + parts[1])
        print("Operand: " + parts[2] + "\n")