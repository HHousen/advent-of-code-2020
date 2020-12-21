import re

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

# Create a subclass of integer with modified operator functions.
# Only operators in input are multiply and add. In python, multiplication
# has greater precedence than addition and subtraction. But addition and
# subtraction have equal precedence and will be evaluated left-to-right.
class new_int(int):
    def __sub__(self, x):
        # Cast self back to int so proper multiplication is applied.
        return new_int(int(self) * x)
    def __add__(self, x):
        # Need to redefine an add function so the output is a `new_int`
        # and thus any future "subtraction" (aka multiplication) calls
        # will perform the correct operation (`new_int`s instructions
        # instead of `int`s instructions).
        return new_int(int(self) + x)
    def __mul__(self, x):
        return new_int(int(self) + x)

def evaluate(expression, use_part_2=False):
    # Replace multiplication with subtraction so neither operator has
    # precedence. The correct operation for subtraction (aka multiplication)
    # will be applied due to the `new_int` class.
    expression = expression.replace("*", "-")
    if use_part_2:
        # Addition is replaced with multiplication so that it has a higher
        # precedence. Multiplication is replaced with subtraction as before
        # so it has a lower precedence. The overridden `__mul__` method
        # undoes this swap.
        expression = expression.replace("+", "*")
    # Convert all integers to `new_int`s
    expression = re.sub(r"(\d)", r"new_int(\1)", expression)
    # Evaluate the expression using the `new_int` class.
    return eval(expression, {"new_int": new_int})

same_precedence = sum(evaluate(expression) for expression in puzzle_input)
print("First Puzzle Same Precedence: %i" % same_precedence)
greater_precedence = sum(evaluate(expression, use_part_2=True) for expression in puzzle_input)
print("Second Puzzle Greater Precedence: %i" % greater_precedence)
