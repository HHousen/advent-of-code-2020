import math
import urllib

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

# PART 1

earliest_timestamp = int(puzzle_input[0])
all_bus_ids = puzzle_input[1].split(",")
bus_ids = [int(x) for x in all_bus_ids if x != "x"]

return_times = []
for bus_id in bus_ids:
    time_on_journey = earliest_timestamp % bus_id
    time_return_to_station = bus_id - time_on_journey

    return_times.append((time_return_to_station, bus_id))

nearest_bus = min(return_times)
nearest_bus_multiplied = math.prod(nearest_bus)

# PART 2
# Saying a bus ID `n` departs at timestamp `t` actually means `t` divides `n` evenly
# because each bus only departs at timestamps which divide its ID. The modulo operator
# `%` takes the place of "divides evenly."
# More info here: https://www.reddit.com/r/adventofcode/comments/kc4njx/2020_day_13_solutions/gfnbwzc

offsets = [idx for idx, x in enumerate(all_bus_ids) if x != "x"]

# Chinese Remainder Theorem (CRT) code from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
# The CRT allows us to solve simultaneous equations of the form:
# x % n[0] == a[0]
# x % n[1] == a[1]
# x % n[2] == a[2]
# CRT: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
#      https://brilliant.org/wiki/chinese-remainder-theorem/
#      https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


# Show the modular arithmetic necessary to format the equations and obtain `n` and `a`.
# Modular arithmetic: https://en.wikipedia.org/wiki/Modular_arithmetic
for offset, bus_id in zip(offsets, bus_ids):
    # t + offset % bus_id == 0,
    # so t % bus_id = (-offset) % bus_id,
    # so t ≡ (-offset % bus_id) (mod bus_id)
    print("t + %i %% %i = 0" % (offset, bus_id), end="")
    print(", so t %% %i = (-%i) %% %i" % (bus_id, offset, bus_id), end="")
    print(", so t ≡ %i (mod %i)" % (-offset % bus_id, bus_id))

n = list(bus_ids)
a = [-offset % bus_id for offset, bus_id in zip(offsets, bus_ids)]
print("n = %s" % n)
print("a = %s" % a)

print(
    "WolframAlpha Solve: https://www.wolframalpha.com/input/?i="
    + urllib.parse.quote(",".join("t+%imod%i=0" % ob for ob in zip(offsets, bus_ids))),
    end="",
)
print("   --> Use 0 for n since the question asks for the first time.")

print("First Puzzle Bus ID Times Time: %i" % nearest_bus_multiplied)
print("Second Puzzle Earliest Timestamp Offsets Match: %i" % chinese_remainder(n, a))
