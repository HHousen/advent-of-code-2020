import numpy as np
from scipy.ndimage import convolve

with open("puzzle_input.txt") as puzzle_input:
    puzzle_input = [list(line.strip()) for line in puzzle_input]

energy_source = np.array([[y == "#" for y in x] for x in puzzle_input])

def conway_cubes(energy_source, num_dims=3):
    # `tuple(range(num_dims-2))` simply creates a tuple of `(0)` for 3 dimensions
    # or `(0,1)` for 4 dimensions.
    energy_source = np.expand_dims(energy_source, axis=tuple(range(num_dims-2)))
    
    # Create kernel to find neighbors.
    kernel = np.ones((3,) * num_dims)
    # Set the middle value of the kernel to 0 so it does not count the current
    # cube and only sums the surrounding cubes.
    kernel[(1,) * num_dims] = 0

    for _ in range(6):
        # Increase the size on all dimensions by 1 since the energy source
        # can grow at max 1 unit each time step.
        energy_source = np.pad(energy_source, 1).astype(int)
        # Convolve each element into the number of elements surrounding it
        # that are active.
        neighbors = convolve(energy_source, kernel, mode="constant")
        # Apply the boot up rules to determine the active (value of 1) elements/cubes:
        # - Find all the elements in the energy source that are active (they
        #   have a value of 1) and that have either 2 or 3 neighbors (the
        #   coresponding value in the neighbors tensor is 2 or 3).
        # - Find all the elements in the energy source that are inactive (they
        #   have a value of 0) and that have 3 neighbors (the coresponding
        #   value in the neighbors tensor is 3).
        # The bitwise "and" and "or" operators work as follows:
        # - `(neighbors == 2)` sets all values in the `neighbors` tensor to True
        #   if the value is 2 and False otherwise. The same goes for
        #   `(neighbors == 3)` but if the value is 3.
        # - `(a | b)` (where a=`(neighbors == 2)` and b=`(neighbors == 3)` compares
        #   those two tensors of True and False values and returns a new tensor where
        #   each cell is True if either value in each cell of `a` or `b` is True.
        # - Finally, `(energy_source == 1) & c` (where c is the result of the above
        #   step) sets each cell to True (aka 1 or "active") if teh value is True in
        #   both `energy_source` and `c`. This translates to: if the neighbors are 2
        #   or 3 and the cube is active.
        energy_source = (energy_source == 1) & ((neighbors == 2) | (neighbors == 3)) | (energy_source == 0) & (neighbors == 3)

    # Return the number of active cubes
    return np.sum(energy_source)


dimensions_3 = conway_cubes(np.copy(energy_source), 3)
dimensions_4 = conway_cubes(np.copy(energy_source), 4)
print("First Puzzle 3 Dimensions Number Active Cubes: %i" % dimensions_3)
print("First Puzzle 4 Dimensions Number Active Cubes: %i" % dimensions_4)
