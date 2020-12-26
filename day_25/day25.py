# The below is a brute force solution. Alternatively, here is an
# explanation of mathematical method using discrete logarithms: https://github.com/mebeim/aoc/blob/master/2020/README.md#purely-mathematical-solution
# Basically, this problem is the Diffie-Hellman key exchange algorithm,
# so we can use the baby-step giant-step algorithm to solve it.

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

public_key_1 = int(puzzle_input[0])
public_key_2 = int(puzzle_input[1])

subject_number = 7
value = 7
loop_size = 1
while value != public_key_1 and value != public_key_2:
    # Modular Exponentiation: `subject_number` to the power of `loop_size`
    # modulo `20201227`
    value = (value * subject_number) % 20201227
    # Next line slower than above because below line computes the full
    # exponentiation while above line does a single arbitrarily large
    # exponentiation one step at a time, stopping when needed.
    # value = pow(subject_number, loop_size, 20201227)
    loop_size += 1

# If we found the loop size for public_key_1 then decode public_key_2
# and vice versa.
secret_key = pow(
    public_key_2 if value == public_key_1 else public_key_1, loop_size, 20201227
)
print("First Puzzle: %i" % secret_key)
