import math
from itertools import combinations

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [int(line.strip()) for line in puzzle_input]

num_entries = [2, 3]

def find_solution(puzzle_input, num_entries):
    for potential_set in combinations(puzzle_input, num_entries):
        if sum(potential_set) == 2020:
            solution = math.prod(potential_set)
            break

    return solution

for idx, num in enumerate(num_entries):
    solution = find_solution(puzzle_input, num)
    print("Solution %i: %s" % (idx + 1, solution))