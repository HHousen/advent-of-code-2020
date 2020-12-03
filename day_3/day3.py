import math

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [list(line.strip()) for line in puzzle_input]
    num_cols = len(puzzle_input[0])

def calc_num_trees(right, down):
    num_trees = 0
    cur_col_idx = 0

    for row_idx in range(down, len(puzzle_input), down):
        cur_col_idx += right
        
        if cur_col_idx >= num_cols:
            cur_col_idx -= (num_cols)
        
        if puzzle_input[row_idx][cur_col_idx] == "#":
            num_trees += 1
    
    return num_trees

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
num_trees = [calc_num_trees(right, down) for right, down in slopes]

num_trees_prod = math.prod(num_trees)

print("First Puzzle: Number of Trees with Slope Right 3 Down 1: %i" % num_trees[1])
print("Second Puzzle: Multipied Number of Trees: %i" % num_trees_prod)