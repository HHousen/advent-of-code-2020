import math
from collections import defaultdict

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input.read()


ticket_fields, my_ticket, nearby_tickets = puzzle_input.split("\n\n")
ticket_fields = ticket_fields.split("\n")
ticket_fields = [field.split(": ") for field in ticket_fields]
ticket_fields = {
    name: [[int(y) for y in x.split("-")] for x in value.split(" or ")]
    for name, value in ticket_fields
}

my_ticket = my_ticket.split("\n")[1].split(",")
nearby_tickets = [
    [int(i) for i in ticket.split(",")] for ticket in nearby_tickets.split("\n")[1:]
]


def check_correct_value(field_value):
    value_is_valid = False
    for ticket_field_set in ticket_fields.values():
        (low1, high1), (low2, high2) = ticket_field_set
        if low1 <= field_value <= high1 or low2 <= field_value <= high2:
            value_is_valid = True
            break
    return value_is_valid


error_rate = 0
valid_tickets = []
for ticket in nearby_tickets:
    ticket_is_valid = True
    for field_value in ticket:
        value_is_valid = check_correct_value(field_value)
        if not value_is_valid:
            ticket_is_valid = False
            error_rate += field_value

    if ticket_is_valid:
        valid_tickets.append(ticket)

print("First Puzzle Error Rate: %i" % error_rate)

# Find possible columns for each field criteria. Many columns will match the
# criteria of multiple fields, which is a problem the next algorithm solves.
ticket_field_possible_cols = defaultdict(list)
for ticket_field_name, ticket_field_data in ticket_fields.items():
    (low1, high1), (low2, high2) = ticket_field_data
    # Loop over each column and test the current field's criteria on each
    # ticket's value for that column.
    for col in range(len(valid_tickets[0])):
        field_position_is_possible = True
        for ticket in valid_tickets:
            field_value = ticket[col]
            if not (low1 <= field_value <= high1 or low2 <= field_value <= high2):
                field_position_is_possible = False
                break
        # If all of the items in the colum matched the criteria for the
        # tested field.
        if field_position_is_possible:
            ticket_field_possible_cols[ticket_field_name].append(col)

# Sort by ascending amount of possible indexes.
ticket_field_possible_cols = list(ticket_field_possible_cols.items())
ticket_field_possible_cols.sort(key=lambda x: len(x[1]))

field_cols = {}
for idx, (ticket_field_name, possible_col_idxs) in enumerate(
    ticket_field_possible_cols
):
    # This assumes each possibilities list in `ticket_field_possible_cols`
    # contains one more item than the previous possibilities list. It also
    # assumes each previous possibilities list contained all values but one
    # in the current possibilities list.
    if len(possible_col_idxs) == 1:
        final_col_idx = possible_col_idxs[0]
        field_cols[ticket_field_name] = final_col_idx

        # Remove the newly determined final col index from all remaining
        # possible col indexes.
        for remaining_idx in range(idx + 1, len(ticket_field_possible_cols)):
            ticket_field_possible_cols[remaining_idx][1].remove(final_col_idx)

# Get the column indexes of the "departure" values.
departure_field_idxs = [
    col for field_name, col in field_cols.items() if "departure" in field_name
]
# Create a list of the "departure" values in `my_ticket`
departure_field_values = [int(my_ticket[x]) for x in departure_field_idxs]
departure_field_values_mult = math.prod(departure_field_values)

print("Second Puzzle Product of Departure Values: %i" % departure_field_values_mult)
