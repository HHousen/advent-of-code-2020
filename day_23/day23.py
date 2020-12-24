import itertools
from tqdm import tqdm

puzzle_input = "598162734"
original_cups = [int(x) for x in puzzle_input]


def play_slow(cups):
    min_cup_label = min(cups)
    max_cup_label = max(cups)
    for move in range(100):
        current_cup = cups[0]
        picked_up_cups = cups[1:4]
        available_cups = cups[4:]

        destination_cup = current_cup - 1
        while destination_cup not in available_cups:
            destination_cup -= 1
            if destination_cup < min_cup_label:
                destination_cup = max_cup_label

        destination_cup_idx = available_cups.index(destination_cup)
        cups = (
            available_cups[: destination_cup_idx + 1]
            + picked_up_cups
            + available_cups[destination_cup_idx + 1 :]
            + [current_cup]
        )

    return cups


cups = original_cups[:]
cups = play_slow(cups)
index_1 = cups.index(1)
starting_at_label_1 = cups[index_1 + 1 :] + cups[:index_1]
starting_at_label_1_str = "".join(str(x) for x in starting_at_label_1)
print("First Puzzle 10 cups and 100 turns: %s" % starting_at_label_1_str)


class Cup:
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


def build_cups_list(starting_cups, num_cups=None):
    num_cups = (num_cups if num_cups else len(starting_cups)) + 1
    # Cup labeling starts at 1. So cups[0] will always be `None`.
    cups = [None] * num_cups
    labels = itertools.chain(starting_cups, range(len(starting_cups) + 1, num_cups))

    first_cup_label = next(labels)
    first_cup = previous_cup = cups[first_cup_label] = Cup(first_cup_label)

    for label in labels:
        current_cup = cups[label] = Cup(label)
        current_cup.previous = previous_cup
        previous_cup.next = current_cup
        previous_cup = current_cup

    current_cup.next = first_cup

    return cups, first_cup


def play(cups, current_cup, num_moves):
    max_cup_label = len(cups) - 1

    for move_idx in tqdm(range(num_moves), desc="Computing Second Puzzle"):
        picked_1 = current_cup.next
        picked_2 = picked_1.next
        picked_3 = picked_2.next
        picked_up_cups_values = [picked_1.value, picked_2.value, picked_3.value]

        current_cup.next = picked_3.next
        picked_3.next.previous = current_cup

        destination_cup_value = current_cup.value - 1
        while (
            destination_cup_value in picked_up_cups_values or destination_cup_value < 1
        ):
            destination_cup_value = (
                max_cup_label
                if destination_cup_value < 1
                else destination_cup_value - 1
            )

        destination_cup = cups[destination_cup_value]
        picked_3.next = destination_cup.next
        destination_cup.next.previous = picked_3
        destination_cup.next = picked_1
        picked_1.previous = destination_cup

        current_cup = current_cup.next

    return cups


cups = original_cups[:]
cups, first_cup = build_cups_list(cups, int(1e6))
cups = play(cups, first_cup, int(1e7))

label_1_cup = cups[1]
next_cups_mult = label_1_cup.next.value * label_1_cup.next.next.value
print("Second Puzzle 1e6 cups and 1e7 turns: %i" % next_cups_mult)
