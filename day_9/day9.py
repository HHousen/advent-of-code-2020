from itertools import combinations

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [int(line.strip()) for line in puzzle_input]

def check_combinations(previous_25, number):
    for number_combo in combinations(previous_25, 2):
        if sum(number_combo) == number:
            return True
    return False

for idx, number in enumerate(puzzle_input[25:], start=25):
    previous_25 = puzzle_input[idx-25:idx]
    
    if not check_combinations(previous_25, number):
        breaking_number = number

print("First Puzzle Number That Isn't Sum of 2 of 25 Previous Numbers: %i" % breaking_number)

def compute_next_numbers_sum(puzzle_input, breaking_number, idx):
    number_sum = 0
    for inner_idx, inner_number in enumerate(puzzle_input[idx:], start=idx):
        if number_sum == breaking_number:
            number_range = puzzle_input[idx:inner_idx]
            return min(number_range), max(number_range)
        if number_sum > breaking_number:
            return False
        number_sum += inner_number

for idx, number in enumerate(puzzle_input):
    number_min_max = compute_next_numbers_sum(puzzle_input, breaking_number, idx)
    if number_min_max != False:
        break

number_sum = sum(number_min_max)

print("Second Puzzle Sum of Smallest and Largest Numbers in Contiguous Range: %i" % number_sum)
