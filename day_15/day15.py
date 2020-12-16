puzzle_input = [15,5,1,4,7,0]

answers = []
for limit in [2020, 30_000_000]:
    # Create a dictionary of values and their positions in the list of spoken numbers.
    # This way we can easily update a value's index if the number is a duplicate (aka
    # it was previously spoken).
    numbers = {value: turn_index for turn_index, value in enumerate(puzzle_input[:-1], 1)}
    # Initialize the next number that will be spoken
    num_to_add = puzzle_input[-1]
    # Loop through all of the turns
    for turn_num in range(len(numbers)+1, limit):
        # If the current number has been spoken before, then the next number is the age
        # (number of turns apart the current number is from when it was previously spoken)
        # of the current number.
        if num_to_add in numbers.keys():
            next_number = turn_num - numbers[num_to_add]
        # If the current number has not been spoken before, then the next number is 0.
        else:
            next_number = 0
        # "Speak" the current number by updating its index in the dictionary of numbers
        # (equivalent to "adding" the current number to the list of spoken numbers). This
        # needs to be done after determining the next number because otherwise (if the
        # current number were added as the first instruction in this loop) the check if
        # the current number is in the list would always pass.
        numbers[num_to_add] = turn_num
        # Set the number to add to the list to the calculated next number for the next
        # iteration of the loop.
        num_to_add = next_number

    answers.append(next_number)

print("First Puzzle 2020th Number: %i" % answers[0])
print("Second Puzzle 30,000,000th Number: %i" % answers[1])
