

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

num_passwords_valid_1 = 0
num_passwords_valid_2 = 0

for entry in puzzle_input:
    max_min, letter, password = entry.split(" ")
    minimum, maximum = max_min.split("-")
    letter = letter[0]
    num_occurrences = password.count(letter)

    if int(minimum) <= num_occurrences <= int(maximum):
        num_passwords_valid_1 += 1
    

    position_letters = (password[int(minimum)-1], password[int(maximum)-1])

    one_position_has_letter = position_letters[0] == letter or position_letters[1] == letter
    both_positions_are_letter = position_letters[0] == letter and position_letters[1] == letter
    
    if one_position_has_letter and not both_positions_are_letter:
        num_passwords_valid_2 += 1

print("First Puzzle: Number of Valid Passwords: %i" % num_passwords_valid_1)

print("Second Puzzle: Number of Valid Passwords: %i" % num_passwords_valid_2)

