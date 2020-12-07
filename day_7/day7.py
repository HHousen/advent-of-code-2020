with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input.read().split(".\n")

bags = {}
for line in puzzle_input:
    bag_type, contents = line.split(" contain ")
    bag_type = bag_type[:-5]  # remove the word "bags"
    
    if contents == "no other bags":
        formatted_contents = None
    else:
        formatted_contents = {}
        for x in contents.rstrip(".").split(", "):
            num, inner_bag_type = x.split(" ", 1)
            inner_bag_type = inner_bag_type.replace("bags", "").replace("bag", "").strip()
            formatted_contents[inner_bag_type] = num
    
    bags[bag_type] = formatted_contents


def contains_bag_search(input_bag):
    if "shiny gold" == input_bag:
        return True
    if bags[input_bag] is not None:
        for inner_bag in bags[input_bag]:
            result_in_bag = contains_bag_search(inner_bag)
            if result_in_bag:
                return result_in_bag
    return False

bags_with_shiny_gold = [contains_bag_search(bag) for bag in bags if bag is not None]
# Subtract 1 because the shiny gold bag itself will be counted
total_bags_with_shiny_gold = sum(bags_with_shiny_gold) - 1

print("First Puzzle Total Number Bags Containing Shiny Gold Bags: %i" % total_bags_with_shiny_gold)

def count_bags_inside(input_bag):
    counter = 0
    if bags[input_bag] is not None:
        for inner_bag, num_bags in bags[input_bag].items():
            counter += int(num_bags)  # add bag count
            counter += int(num_bags) * count_bags_inside(inner_bag)  # add inner bags
    return counter

def countBagsInside(bags, outerBag):
    return sum(n * (countBagsInside(bags, bag) + 1) for bag, n in bags[outerBag].items())

bags_inside_shiny_gold = count_bags_inside("shiny gold")

print("Second Puzzle Total Number Bags Inside Shiny Gold Bags: %i" % bags_inside_shiny_gold)