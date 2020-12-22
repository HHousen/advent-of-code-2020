from collections import deque

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input.read()

deck_1, deck_2 = puzzle_input.split("\n\n")
deck_1, deck_2 = deck_1.split("\n")[1:], deck_2.split("\n")[1:]

# Deque is preferred over list in the cases where we need quicker append
# and pop operations from both the ends of container, as deque provides
# an O(1) time complexity for append and pop operations as compared to
# list which provides O(n) time complexity. - https://www.geeksforgeeks.org/deque-in-python/
deck_1, deck_2 = deque(map(int, deck_1)), deque(map(int, deck_2))


def play_combat(deck_1, deck_2):
    while len(deck_1) > 0 and len(deck_2) > 0:
        deck_1_top = deck_1.popleft()
        deck_2_top = deck_2.popleft()

        if deck_1_top > deck_2_top:
            deck_1.extend([deck_1_top, deck_2_top])
        else:
            deck_2.extend([deck_2_top, deck_1_top])

    winner_deck = deck_1 if len(deck_1) > 0 else deck_2
    return winner_deck


def calculate_score(winner_deck):
    return sum((idx + 1) * val for idx, val in enumerate(winner_deck))


winner_deck_1 = play_combat(deck_1.copy(), deck_2.copy())
winner_deck_1.reverse()
winner_score_1 = calculate_score(winner_deck_1)
print("First Puzzle Winner Score: %i" % winner_score_1)


def play_recursive_combat_round(deck_1, deck_2):
    previous_deck_states = set()
    while len(deck_1) > 0 and len(deck_2) > 0:
        deck_state = (tuple(deck_1), tuple(deck_2))
        if deck_state in previous_deck_states:
            return 1, deck_1

        previous_deck_states.add(deck_state)

        deck_1_top = deck_1.popleft()
        deck_2_top = deck_2.popleft()

        if len(deck_1) >= deck_1_top and len(deck_2) >= deck_2_top:
            deck_1_next = deque(deck_1[x] for x in range(deck_1_top))
            deck_2_next = deque(deck_2[x] for x in range(deck_2_top))
            player_1_wins, _ = play_recursive_combat_round(deck_1_next, deck_2_next)
        else:
            player_1_wins = deck_1_top > deck_2_top

        if player_1_wins:
            deck_1.extend([deck_1_top, deck_2_top])
        else:
            deck_2.extend([deck_2_top, deck_1_top])

    winner = len(deck_1) > 0
    winner_deck = deck_1 if len(deck_1) > 0 else deck_2
    return winner, winner_deck


_, winner_deck_2 = play_recursive_combat_round(deck_1.copy(), deck_2.copy())
winner_deck_2.reverse()
winner_score_2 = calculate_score(winner_deck_2)
print("Second Puzzle Winner Score: %i" % winner_score_2)
