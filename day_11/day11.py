with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [list(line.strip()) for line in puzzle_input]

adjacent_idxs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
width = len(puzzle_input[0])
height = len(puzzle_input)
OCCUPIED = "#"
EMPTY = "L"
FLOOR = "."


def run_round(layout, method="neighbor"):
    occupied_threshold = 4 if method == "neighbor" else 5
    seats_changed = False
    new_layout = [x[:] for x in layout]
    for row_idx, row in enumerate(layout):
        for col_idx, seat in enumerate(row):
            # Floor is never modified so go to the next seat.
            if seat == FLOOR:
                continue
            num_occupied = 0
            # Check the surrounding seats.
            if method == "neighbor":
                for x_idx, y_idx in adjacent_idxs:
                    new_col = col_idx + x_idx
                    new_row = row_idx + y_idx
                    # Only check if occupied if we do not go out of bounds of the matrix.
                    if (
                        0 <= new_row < height
                        and 0 <= new_col < width
                        and layout[new_row][new_col] == OCCUPIED
                    ):
                        num_occupied += 1
            else:
                for x_idx, y_idx in adjacent_idxs:
                    new_col = col_idx + x_idx
                    new_row = row_idx + y_idx
                    # Only check if occupied if we do not go out of bounds of the matrix.
                    while 0 <= new_row < height and 0 <= new_col < width:
                        seat_to_check = layout[new_row][new_col]
                        if seat_to_check == OCCUPIED:
                            num_occupied += 1
                        if seat_to_check != FLOOR:
                            break

                        new_col += x_idx
                        new_row += y_idx

            # Apply seat rules.
            # Update `new_layout` and not `layout` since the surrounding seats should
            # always be based on the original arrangement and not a half-modified one.
            if seat == EMPTY and num_occupied == 0:
                new_layout[row_idx][col_idx] = OCCUPIED
                seats_changed = True

            elif seat == OCCUPIED and num_occupied >= occupied_threshold:
                new_layout[row_idx][col_idx] = EMPTY
                seats_changed = True

    return new_layout, seats_changed


def equilibrium_occupied_seats(method="neighbor"):
    seats_changed = True
    layout = [x[:] for x in puzzle_input]
    # Continue running rounds until the seating area reaches equilibrium and no seats change.
    while seats_changed:
        layout, seats_changed = run_round(layout, method)

    # Count number of occupied seats
    num_occupied = sum(1 for row in layout for seat in row if seat == OCCUPIED)
    return num_occupied


num_occupied_1 = equilibrium_occupied_seats()
print("First Puzzle Number of Occupied Seats: %i" % num_occupied_1)

num_occupied_2 = equilibrium_occupied_seats("extended")
print("Second Puzzle Number of Occupied Seats: %i" % num_occupied_2)
