import re

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input.read().split("\n\n")


passports = []
for raw_passport in puzzle_input:
    passport = {}
    for password_piece in raw_passport.replace("\n", " ").strip().split(" "):
        key, value = password_piece.split(":")
        passport[key] = value

    passports.append(passport)


def check_valid_1(passport):
    return all(
        field in passport for field in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    )


def check_valid_2(passport):
    valid_1 = check_valid_1(passport)
    if not valid_1:
        return False

    pass_all_checks = (
        1920 <= int(passport["byr"]) <= 2002
        and 2010 <= int(passport["iyr"]) <= 2020
        and 2020 <= int(passport["eyr"]) <= 2030
        and (
            (passport["hgt"][-2:] == "cm" and 150 <= int(passport["hgt"][:-2]) <= 193)
            or (passport["hgt"][-2:] == "in" and 59 <= int(passport["hgt"][:-2]) <= 76)
        )
        and (
            bool(re.match("^[a-f0-9_-]*$", passport["hcl"][1:]))
            and passport["hcl"][0] == "#"
        )
        and passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        and (
            bool(re.match("^[0-9_-]*$", passport["pid"])) and len(passport["pid"]) == 9
        )
    )
    return pass_all_checks


num_valid_1 = sum(check_valid_1(passport) for passport in passports)
print("First Puzzle Number Valid Passports: %i" % num_valid_1)

num_valid_2 = sum(check_valid_2(passport) for passport in passports)
print("Second Puzzle Number Valid Passports: %i" % num_valid_2)
