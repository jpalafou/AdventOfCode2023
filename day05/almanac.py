import time
import numpy as np
from functools import reduce


def piecewise_addition(
    x: np.ndarray,
    x_lower: np.ndarray,
    y_lower: np.ndarray,
    length: np.ndarray,
) -> np.ndarray:
    """
    args:
        x           vector input
        x_lower     source range starting values, length n
        y_lower     destination range starting points, length n
        length      lengths of source/destination ranges, length n
    returns:
        out         same shape as x
    """
    x_upper = x_lower + length
    shift = y_lower - x_lower
    condarray = np.logical_and(x >= x_lower[:, np.newaxis], x < x_upper[:, np.newaxis])
    condlist = [row for row in condarray]
    funclist = [lambda x, y=h: x + y for h in y_lower - x_lower] + [lambda x: x]
    start_time = time.time()
    out = np.piecewise(x, condlist, funclist)
    evaltime = time.time() - start_time
    print(f"piecewise_addition(): Evaluated {len(x)} values in {evaltime:.4e} s.")
    return out


sections = [
    "seeds",
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]

data = {}
with open("inputs.txt") as file:
    current_section = None
    for line in file:
        # check if current line is a section line
        section_line = False
        for section in sections:
            if line.startswith(section):
                current_section = section
                section_line = True
        stripped_line = line.strip()
        if stripped_line == "":
            continue
        # read data for each section
        if current_section == "seeds":
            data["seeds"] = np.asarray(
                [int(x) for x in stripped_line.replace("seeds: ", "").split(" ")]
            )
        elif not section_line:
            if current_section not in data.keys():
                data[current_section] = np.empty((0, 3), dtype="int")
            row_data = np.array([int(x) for x in stripped_line.split(" ")])
            data[current_section] = np.vstack((data[current_section], row_data))
# build composed piecewise addition maps
map_list = []
for section in sections[1:]:
    dat = data[section]
    current_map = lambda x, dat=dat: piecewise_addition(
        x, x_lower=dat[:, 1], y_lower=dat[:, 0], length=dat[:, 2]
    )
    map_list.append(current_map)
composed_map = reduce(lambda f, g: lambda x: g(f(x)), map_list)

# find location of each seed and take the minimum
seeds = data["seeds"]
print(f"Comparing seeds {seeds.tolist()}")
min_location = np.min(composed_map(seeds))
print(f"-> Lowest location number: {min_location}")

# find location of each seed in batches of specified ranges and take the minimum
min_location = np.max(data["seeds"])  # initial wrong value
for i, (lower, length) in enumerate(zip(data["seeds"][::2], data["seeds"][1::2])):
    upper = lower + length
    lowers = np.arange(lower, upper, 100000000)  # 100000000 is max batch size
    uppers = np.minimum(lowers + 100000000, upper)
    for sub_lower, sub_upper in zip(lowers, uppers):
        seeds = np.arange(sub_lower, sub_upper)
        print(f"\nBatch ({i + 1}/{len(data['seeds']) / 2:g}) for {len(seeds)} seeds")
        min_batch_location = np.min(composed_map(seeds))
        print(f"Lowest batch location number: {min_batch_location}")
        min_location = min(min_location, min_batch_location)
print(f"-> Lowest location number of all batches: {min_location}")
