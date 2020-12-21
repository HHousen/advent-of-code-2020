with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

all_ingredients = []
possible_causes = {}
for food in puzzle_input:
    ingredients, allergens = food.split(" (contains ")
    ingredients = set(ingredients.split(" "))
    allergens = set(allergens[:-1].split(", "))

    all_ingredients.extend(ingredients)

    for allergen in allergens:
        if allergen in possible_causes:
            possible_causes[allergen] &= ingredients  # Compute intersection.
        else:
            # `.copy()` prevents changes from being reflected in the original
            # `set`, which was added to `all_ingredients` and thus should not
            # be modified.
            possible_causes[allergen] = ingredients.copy()

# Next line equivalent to: `set(itertools.chain.from_iterable(possible_causes.values()))``
possible_allergens = set.union(*possible_causes.values())
not_allergens = set(all_ingredients) - possible_allergens

num_not_allergens = sum(ingredient in not_allergens for ingredient in all_ingredients)
print("First Puzzle Number Not Allergens: %i" % num_not_allergens)

# Sort by ascending amount of possible indexes.
possible_causes = list(possible_causes.items())
possible_causes.sort(key=lambda x: len(x[1]))


def solve_guaranteed_allergens(possible_causes, guaranteed_allergens):
    solved = True
    # If there are no more possible causes then the allergens have been determined.
    if sum([len(x[1]) for x in possible_causes]) == 0:
        return solved

    # This solves a problem similar to Day 16 but does make any of the same
    # assumptions. The next possibilities list may contain more than 1 item
    # and each previous possibilities list does not have to contain all
    # values but one in the current possibilities list.
    for (allergen_name, possible_ingredients) in possible_causes:
        if len(possible_ingredients) == 1:
            final_ingredient = possible_ingredients.pop()
            guaranteed_allergens[allergen_name] = final_ingredient

            # Remove the newly determined final ingredient from all allergens.
            for idx, _ in enumerate(possible_causes):
                try:
                    possible_causes[idx][1].remove(final_ingredient)
                except KeyError:
                    # Ignore any future allergens that may not have this ingredient
                    # as a possibility.
                    pass
        # If there is an allergen that had more than 1 possibility then we will solve
        # it by running this function again. The discrepancy will be removed by a
        # later iteration of this loop.
        else:
            solved = False
    return solved


guaranteed_allergens = {}
answers_found = False
while not answers_found:
    answers_found = solve_guaranteed_allergens(possible_causes, guaranteed_allergens)


alphabetized_allergens = [x[1] for x in sorted(guaranteed_allergens.items())]
dangerous_ingredients = ",".join(alphabetized_allergens)
print("Second Puzzle Canonical Dangerous Ingredient List: %s" % dangerous_ingredients)
