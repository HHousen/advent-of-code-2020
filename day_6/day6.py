from collections import Counter

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input = puzzle_input.read().split("\n\n")

group_unique_answers = []
group_everyone_answers = []

for group in puzzle_input:
    all_answers = list(group.replace("\n", ""))

    num_unique_answers = len(set(all_answers))
    group_unique_answers.append(num_unique_answers)

    num_people = len(group.split())
    answers_counted = Counter(all_answers)
    # Number of questions where everyone in the group answered yes
    group_num_everyone = sum([1 for x in answers_counted.values() if x == num_people])
    group_everyone_answers.append(group_num_everyone)

total_group_unique_answers = sum(group_unique_answers)
print("First Puzzle Total Group Anyone Yes Answers: %i" % total_group_unique_answers)

total_group_everyone_answers = sum(group_everyone_answers)
print("Second Puzzle Total Group Everyone Yes Answers: %i" % total_group_everyone_answers)
