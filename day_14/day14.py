# Really interesting alternative solution: https://github.com/sophiebits/adventofcode/blob/main/2020/day14.py
import itertools

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

def binary_string_to_int(num):
    return int("".join(num), 2)

def emulator(create_memory):
    memory = {}
    mask = None
    for instruction_and_value in puzzle_input:
        instruction, value = instruction_and_value.split(" = ")
        if instruction == "mask":
            mask = list(value)
        elif instruction.startswith("mem"):
            memory_address = int(instruction[4:-1])
            
            create_memory(memory_address, value, mask, memory)
    
    return sum(memory.values())

def part_1_create_memory(memory_address, value, mask, memory):
    # Explanation of below statement: https://stackoverflow.com/a/10411108
    # - `{}` places `int(value)` into a string
    # - `0` takes the variable at argument position 0
    # - `:` adds formatting options for this variable (otherwise it would represent decimal value)
    # - `036` formats the number to eight digits zero-padded on the left
    # - `b` converts the number to its binary representation
    masked_value = list("{0:036b}".format(int(value)))

    for idx, new_num in enumerate(mask):
        if new_num != "X":
            masked_value[idx] = new_num
    
    masked_value = binary_string_to_int(masked_value)
    memory[memory_address] = masked_value

def get_all_addresses_recursive(address):
    # Try to get the location of the next floating value (`X`)/
    try:
        X_location = address.index("X")
    # If there is no floating value (`X`) in the address, then return
    # the finished address/
    except ValueError:
        yield binary_string_to_int(address)
    # If there is a floating value (`X`) in the address, then substitute both
    # possible values for it (`0` and `1`) and get all the next address (which
    # will substitute in `0` or `1` for the next floating value and so on).
    else:
        for bit in ["0", "1"]:
            next_address = address[:]
            next_address[X_location] = bit
            yield from get_all_addresses(next_address)

def get_all_addresses_itertools(address):
    # Count the number of floating values (`X`'s).
    variations = address.count('X')
    # Replace all floating values with a template.
    address = str(address).replace("X", "{}")
    # For every possible combination of `0`s and `1`s that is the length of the
    # number of floating values, yield the address with the floating values
    # replaced with the binary digits.
    for permutation in itertools.product("01", repeat=variations):
        yield address.format(*permutation)

def part_2_create_memory(memory_address, value, mask, memory):
    masked_address = list("{0:036b}".format(memory_address))
        
    for idx, new_num in enumerate(mask):
        if new_num != "0":
            masked_address[idx] = new_num
    
    for address in get_all_addresses_itertools(masked_address):
        memory[address] = int(value)

memory_sum_1 = emulator(part_1_create_memory)
print("First Puzzle Sum of Values in Memory: %i" % memory_sum_1)
memory_sum_2 = emulator(part_2_create_memory)
print("First Puzzle Sum of Values in Memory: %i" % memory_sum_2)
