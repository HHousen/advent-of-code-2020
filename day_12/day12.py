with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

DIRECTION_TO_COORD = {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)}


class Ship:
    def __init__(self):
        self.ship_x = 0
        self.ship_y = 0
        self.direction = 90

    def get_manhattan_distance(self):
        return abs(self.ship_x) + abs(self.ship_y)

    def do_basic_moves(self, instruction, amount, x, y):
        if instruction == "N":
            y += amount
        elif instruction == "S":
            y -= amount
        elif instruction == "E":
            x += amount
        elif instruction == "W":
            x -= amount
        return x, y

    def do_complex_moves(self, instruction, amount):
        if instruction == "L":
            self.direction = (self.direction - amount) % 360
        elif instruction == "R":
            self.direction = (self.direction + amount) % 360
        elif instruction == "F":
            x_add, y_add = DIRECTION_TO_COORD[self.direction]
            self.ship_x += x_add * amount
            self.ship_y += y_add * amount

    def do_moves(self, input_instructions):
        for instruction_set in input_instructions:
            instruction, amount = instruction_set[0], int(instruction_set[1:])

            self.ship_x, self.ship_y = self.do_basic_moves(
                instruction, amount, self.ship_x, self.ship_y
            )
            self.do_complex_moves(instruction, amount)


class WaypointShip(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint_x = 10
        self.waypoint_y = 1

    def do_complex_moves(self, instruction, amount):
        if instruction == "L":
            num_rotations = amount // 90
            for _ in range(num_rotations):
                self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x
        elif instruction == "R":
            num_rotations = amount // 90
            for _ in range(num_rotations):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x
        elif instruction == "F":
            self.ship_x += self.waypoint_x * amount
            self.ship_y += self.waypoint_y * amount

    def do_moves(self, input_instructions):
        for instruction_set in input_instructions:
            instruction, amount = instruction_set[0], int(instruction_set[1:])

            self.waypoint_x, self.waypoint_y = self.do_basic_moves(
                instruction, amount, self.waypoint_x, self.waypoint_y
            )
            self.do_complex_moves(instruction, amount)


ship = Ship()
ship.do_moves(puzzle_input)
print("First Puzzle Manhattan Distance: %i" % ship.get_manhattan_distance())

waypoint_ship = WaypointShip()
waypoint_ship.do_moves(puzzle_input)
print("Second Puzzle Manhattan Distance: %i" % waypoint_ship.get_manhattan_distance())
