import re

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

# Using axial coordinates from https://www.redblobgames.com/grids/hexagons/#coordinates-axial
direction_mapping = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "ne": (1, -1),
    "nw": (0, -1),
}


def compass_to_coords(directions):
    x, y = 0, 0

    for direction in directions:
        x_offset, y_offset = direction_mapping[direction]
        x += x_offset
        y += y_offset

    return x, y


black_tiles = set()
for tile_compass in puzzle_input:
    directions = re.findall("e|se|sw|w|nw|ne", tile_compass)
    coords = compass_to_coords(directions)

    if coords in black_tiles:
        # The tile is black but is being flipped to white again.
        black_tiles.remove(coords)
    else:
        # Tile is being flipped from white to black.
        black_tiles.add(coords)

num_black_tiles = len(black_tiles)
print("First Puzzle Number Black Tiles: %i" % num_black_tiles)


def get_num_black_adjacent(black_tiles, coords):
    x, y = coords
    return sum(
        (x + x_offset, y + y_offset) in black_tiles
        for x_offset, y_offset in direction_mapping.values()
    )


def get_all_tile_coords(black_tiles):
    return set(
        (x + x_offset, y + y_offset)
        for x, y in black_tiles
        for x_offset, y_offset in direction_mapping.values()
    )


for turn in range(100):
    new_black_tiles = set()

    complete_grid = get_all_tile_coords(black_tiles)
    for tile_coords in complete_grid:
        num_black_adjacent = get_num_black_adjacent(black_tiles, tile_coords)

        tile_is_black = tile_coords in black_tiles

        # Implement rules for changes in terms of black tiles only. The new grid
        # starts as all white so only determine which tiles are black.
        # This modifies the first rule to determine which tiles should stay
        # black instead of determining which should become white.
        if (
            tile_is_black and not (num_black_adjacent == 0 or num_black_adjacent > 2)
        ) or ((not tile_is_black) and num_black_adjacent == 2):
            new_black_tiles.add(tile_coords)

    black_tiles = new_black_tiles

num_black_tiles = len(black_tiles)
print("Second Puzzle Number Black Tiles: %i" % num_black_tiles)
