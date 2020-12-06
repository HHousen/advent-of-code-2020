import math

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

def bsp_decode(boarding_pass, top, bottom):
    min_row = 0
    max_row = 2 ** len(boarding_pass) - 1

    for character in boarding_pass[:-1]:
        middle = int((min_row + max_row) / 2)
        if character == top:
            max_row = middle
        elif character == bottom:
            not_divisible = (min_row + max_row) % 2
            if not_divisible:
                middle += 1
            min_row = middle
    
    if boarding_pass[-1] == top:
        return min_row
    elif boarding_pass[-1] == bottom:
        return max_row

seat_ids = []

for boarding_pass in puzzle_input:
    row = bsp_decode(boarding_pass[:7], top="F", bottom="B")
    column = bsp_decode(boarding_pass[-3:], top="L", bottom="R")

    seat_id = row * 8 + column
    seat_ids.append(seat_id)

highest_seat_id = max(seat_ids)
print("First Puzzle Highest Seat ID: %i" % highest_seat_id)

all_seat_ids = set(range(min(seat_ids), max(seat_ids)))
missing_seat_ids = all_seat_ids - set(seat_ids)

your_seat_id = missing_seat_ids.pop()
print("Second Puzzle Your Seat ID: %i" % your_seat_id)
