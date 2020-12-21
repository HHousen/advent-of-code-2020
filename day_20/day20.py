import math
import itertools
from collections import OrderedDict, defaultdict
import numpy as np

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = puzzle_input.read()

tiles = puzzle_input.split("\n\n")
tiles = [tile.split(":\n") for tile in tiles]
tiles = {
    tile_id.split(" ")[1]: np.array([list(x) for x in content.split("\n")]) == "#"
    for tile_id, content in tiles
}


def get_tile_edges(tile):
    # `tile[:, -1]` = right side
    # `tile[:, 0]` = left side
    # `tile[0]` = top
    # `tile[-1]` = bottom
    return tile[:, -1], tile[:, 0], tile[0], tile[-1]


def list_binary_to_int(to_convert):
    return int("".join(str(int(x)) for x in to_convert), 2)


def find_matches(tiles):
    # Create dictionary of edges.
    edges = {
        tile_id: {
            "normal": [list_binary_to_int(x) for x in get_tile_edges(tile)],
            "reversed": [list_binary_to_int(np.flip(x)) for x in get_tile_edges(tile)],
        }
        for tile_id, tile in tiles.items()
    }

    # Remove duplicates by starting each match with a `set`.
    matches = defaultdict(set)
    # Check each tile against every other tile.
    for tile_id, tile in edges.items():
        for inner_tile_id, inner_tile in edges.items():
            # If we are checking a tile against itself then skip this iteration.
            if tile_id == inner_tile_id:
                continue
            # Create list of every possible edge configuration (all combinations
            # of rotating and flipping).
            outer_edges = tile["normal"] + tile["reversed"]
            inner_edges = inner_tile["normal"] + inner_tile["reversed"]
            for edge1, edge2 in itertools.product(outer_edges, inner_edges):
                # If the edges match then the inner tile can be connected to
                # the outer tile.
                if edge1 == edge2:
                    matches[tile_id].add(inner_tile_id)

    return matches


# unique_edges = np.unique(edges)
# corner_tiles = []
# tile_ids = list(tiles.keys())
# for idx, tile_edges in enumerate(edges):
#     # Count number of unique edges.
#     num_unique_edges = sum(
#         [1 if edge in unique_edges else 0 for edge in tile_edges]
#     )
#     # If two edges are unique then the tile is a corner piece.
#     if num_unique_edges == 2:
#         tile_id = tile_ids[idx]
#         corner_tiles.append(tile_id)


matches = find_matches(tiles)

# Corner tiles can only connect to two other tiles.
corner_tile_ids = [
    tile_id for tile_id, connections in matches.items() if len(connections) == 2
]

corner_tile_ids_mult = math.prod(int(x) for x in corner_tile_ids)
print("First Puzzle Corner Tile IDs Multiplied: %i" % corner_tile_ids_mult)


def generate_possible_tiles(tile):
    rotate90 = np.rot90(tile)
    rotate180 = np.rot90(tile, 2)
    rotate270 = np.rot90(tile, 3)
    flipud = np.flipud(tile)
    flip_rotate90 = np.rot90(flipud)
    flip_rotate180 = np.rot90(flipud, 2)
    flip_rotate270 = np.rot90(flipud, 3)
    return (
        tile,
        flipud,
        rotate90,
        rotate180,
        rotate270,
        flip_rotate90,
        flip_rotate180,
        flip_rotate270,
    )


def find_adjacent_tile(side_name, side, top_left_matches):
    side = list_binary_to_int(side)
    for inner_match_id in top_left_matches:
        inner_match_tile = tiles[inner_match_id]
        possible_tiles = generate_possible_tiles(inner_match_tile)
        for possible_tile in possible_tiles:
            possible_tile_edges = get_tile_edges(possible_tile)
            possible_tile_edges = [list_binary_to_int(x) for x in possible_tile_edges]
            _, possible_tile_left, possible_tile_top, _ = possible_tile_edges
            if (
                side_name == "right" and possible_tile_left == side
            ):  # Match and orientation found
                return possible_tile, inner_match_id
            elif side_name == "bottom" and possible_tile_top == side:
                return possible_tile, inner_match_id


num_tiles_on_side = int(math.sqrt(len(tiles)))
image_tiles = [[0 for _ in range(num_tiles_on_side)] for _ in range(num_tiles_on_side)]
image_tiles_ids = [
    [0 for _ in range(num_tiles_on_side)] for _ in range(num_tiles_on_side)
]

num_cols = len(image_tiles[0])
for row in range(len(image_tiles)):
    for col in range(num_cols):
        if row == 0 and col == 0:
            top_left_id = corner_tile_ids[0]
            top_left_matches = matches[top_left_id]
            top_left_tile = tiles[top_left_id]

            image_tiles[0][0] = top_left_tile
            image_tiles_ids[0][0] = top_left_id
        elif col == 0:
            # image_tiles = [np.flipud(x) for x in image_tiles[0]]
            previous_tile = image_tiles[row - 1][0]
            previous_tile_id = image_tiles_ids[row - 1][0]

            previous_tile_edges = get_tile_edges(previous_tile)
            previous_tile_matches = matches[previous_tile_id]
            right, _, _, bottom = previous_tile_edges

            adjacent_tile, adjacent_tile_id = find_adjacent_tile(
                "bottom", bottom, previous_tile_matches
            )
            image_tiles[row][col] = adjacent_tile
            image_tiles_ids[row][col] = adjacent_tile_id
        else:
            previous_tile = image_tiles[row][col - 1]
            previous_tile_id = image_tiles_ids[row][col - 1]

            previous_tile_edges = get_tile_edges(previous_tile)
            previous_tile_matches = matches[previous_tile_id]
            right, _, _, bottom = previous_tile_edges

            adjacent_tile, adjacent_tile_id = find_adjacent_tile(
                "right", right, previous_tile_matches
            )
            image_tiles[row][col] = adjacent_tile
            image_tiles_ids[row][col] = adjacent_tile_id


# Remove border of each tile.
image_tiles = [[item[1:-1, 1:-1] for item in row] for row in image_tiles]
# Combine image tiles into final image matrix.
image_tiles = [np.hstack(row) for row in image_tiles]
final_image = np.vstack(image_tiles)

sea_monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
sea_monster_lines = sea_monster.split("\n")

sea_monster_offsets = [
    (line_idx, value_idx)
    for line_idx, line in enumerate(sea_monster_lines)
    for value_idx, value in enumerate(line)
    if value == "#"
]

final_image_orientations = np.fliplr(final_image), np.flipud(final_image)

num_sea_monsters = 0
num_cols = len(final_image[0])
num_rows = len(final_image)

for final_image_orientation in final_image_orientations:
    for row_idx, row in enumerate(final_image_orientation):
        for col_idx, item in enumerate(row):
            try:
                if all(
                    [
                        final_image_orientation[
                            row_idx + row_offset, col_idx + col_offset
                        ]
                        == True
                        for row_offset, col_offset in sea_monster_offsets
                    ]
                ):
                    num_sea_monsters += 1
            except IndexError:  # Ignore out of bounds exceptions.
                pass
    if num_sea_monsters > 0:
        break

per_sea_monster = sea_monster.count("#")
total_true_values = np.count_nonzero(final_image)
sea_monster_total = num_sea_monsters * per_sea_monster
num_not_part_of_sea_monster = total_true_values - sea_monster_total

print(
    "Second Puzzle Number '#' Not Part of Sea Monster: %i" % num_not_part_of_sea_monster
)
