# 25/9 scorer video explanation: https://www.youtube.com/watch?v=cE88K2kFZn0

from collections import Counter

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [int(line.strip()) for line in puzzle_input]

adapter_chain = puzzle_input[:]
adapter_chain.sort()

adapter_chain_differences = [
    adapter_chain[i + 1] - adapter_chain[i] for i in range(len(adapter_chain) - 1)
]

# Add difference between outlet and first adapter
first_difference = adapter_chain_differences[0]
adapter_chain_differences.insert(0, first_difference)
# Add built-in (to the device) adapter joltage
device_adapter_difference = 3
adapter_chain_differences.append(device_adapter_difference)

num_differences = Counter(adapter_chain_differences)
num_3_by_num_1 = num_differences[3] * num_differences[1]

print("First Puzzle 1-jolt Times 3-jolt Differences: %i" % num_3_by_num_1)

adapter_chain_extended = [0] + adapter_chain + [max(adapter_chain) + 3]

# Optimized (dynamic programming) recursion
num_permutations_by_index = {}
def permute(adapter_idx):
    """
    Calculates the number of ways to complete the adapter chain starting at 
    index `adapter_idx` in `adapter_chain_extended`. Is optimized to run with 
    linear complexity due to dynamic programming: https://www.geeksforgeeks.org/dynamic-programming/.
    """
    # If paths from the last value are requested then return 1, because there is
    # only 1 way to reach 1 item.
    if adapter_idx == len(adapter_chain_extended) - 1:
        return 1
    # Memoization: If we already have calculated the number of paths from
    # adapter_idx to the end, then simply return that value instead of
    # recalculating it. This reduces execution time from exponential to
    # linear and ensures the below loop only runs a maximum of
    # `len(adapter_chain_extended)` times. If there are 3 paths to 4, it
    # is unnecessary to reevaluate `permute(4)` 3 different times.
    if adapter_idx in num_permutations_by_index:
        return num_permutations_by_index[adapter_idx]
    # Initialize counter for number of ways to reach then end of the list
    total_num_permutations = 0
    # Determine the permutations for the next three adapters. Only the next three are
    # calculated because the largest separation is 3 jolts.
    for next_idx, next_adapter in enumerate(
        adapter_chain_extended[adapter_idx + 1 : adapter_idx + 4], start=adapter_idx + 1
    ):
        current_adapter = adapter_chain_extended[adapter_idx]
        # Only check future permutations if the jump to the next adapter is less than 3 jolts
        if next_adapter - current_adapter <= 3:
            total_num_permutations += permute(next_idx)

    # Storage the calculation so it can be reused with memoization.
    num_permutations_by_index[adapter_idx] = total_num_permutations
    return total_num_permutations


print("Second Puzzle Number of Permutations: %i" % permute(0))
