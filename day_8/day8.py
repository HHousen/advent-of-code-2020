with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

def run_program(instruction_set):
    accumulator = 0
    line_num = 0
    lines_ran = []
    looped = False
    while True:
        if line_num in lines_ran:
            looped = True
            break
        lines_ran.append(line_num)

        try:
            full_instruction = instruction_set[line_num]
        except IndexError:
            # Break if a 'jmp' operator went out of bounds
            break
        
        instruction, parameter = full_instruction.split(" ")
        parameter = int(parameter)

        if instruction == "acc":
            accumulator += parameter
            line_num += 1
        elif instruction == "jmp":
            line_num += parameter
        elif instruction == "nop":
            line_num += 1
    
    return accumulator, looped

program = puzzle_input
accumulator_first, _ = run_program(program)

print("First Puzzle Accumulator Value: %i" % accumulator_first)

# Bruteforce approach: Try every possible program by replacing each 'jmp' to 'nop' and vice versa for each instruction
for idx, _ in enumerate(program):
    # Clone the program
    modified_program = program[:]
    if "jmp" in program[idx]:
        modified_program[idx] = program[idx].replace("jmp", "nop")
    elif "nop" in program[idx]:
        modified_program[idx] = program[idx].replace("nop", "jmp")

    accumulator_second, looped = run_program(modified_program)
    # Break when the program executed successfully without looping indefinitely
    if not looped:
        break

print("Second Puzzle Accumulator Value: %i" % accumulator_second)
