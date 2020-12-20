import re
import regex

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input.read()

raw_rules, messages = puzzle_input.split("\n\n")
messages = messages.split("\n")

# Format rules properly
rules = {}
for rule in raw_rules.split("\n"):
    index, rule = rule.split(": ")
    if rule[0] == '"':
        rule = rule[1:-1]
    else:
        rule_parts = rule.split(" | ")
        rule = [x.split(" ") for x in rule_parts]
    rules[index] = rule


def parse(rule_idx, loop=False):
    current_rule = rules[rule_idx]
    # Effectively checks if the current rule being applied is not a "a" or "b".
    if type(current_rule) is list:
        # `42 | 42 8` translates to `42+` in regex because `42 | 42 8` means
        # rule 42 or 42 followed by rule 8, which can either be 42 or 42
        # followed by 8. Thus, it means 42 or 42 followed by 42 or 42 followed
        # by 42 followed by 42 etc. So just match an unlimited number of rule
        # 42s.
        if loop and rule_idx == "8":
            return parse("42", loop) + "+"
        # Recursive regex for rule 11. `42 31 | 42 11 31` translates to
        # `42 11? 31` in regex: Rule 11 contains rule 42 then might contain
        # another rule 11 (another set of 42 then 31) and then rule 31.
        # Details about recursive regex here: https://pypi.org/project/regex/#recursive-patterns-hg-issue-27
        if loop and rule_idx == "11":
            return f'(?P<self>{parse("42", loop)}(?&self)?{parse("31", loop)})'

        # Parse each rule number of each portion (separated by `|`in the
        # `puzzle_input`) of the current rule. If there is only one portion
        # then there will be one item in the `additional_regex` list. This
        # one item will simply be returned in two parentheses.
        additional_regex = [
            "".join(parse(num, loop) for num in rule_part) for rule_part in current_rule
        ]

        return "(" + "|".join(additional_regex) + ")"
    # If the current rule is just "a" or "b" hen return that letter.
    else:
        return rules[rule_idx]


def count_matches(rule, messages):
    # Count the number of matches
    matches = [bool(regex.match(rule, message)) for message in messages]
    return sum(matches)


# Need to add a `$` to stop checking once the regex ends. Anything
# extra in the message makes it invalid.
rule_0 = parse("0", loop=False) + "$"
print("First Puzzle: %i" % count_matches(rule_0, messages))

rule_0 = parse("0", loop=True) + "$"
print("Second Puzzle: %i" % count_matches(rule_0, messages))
