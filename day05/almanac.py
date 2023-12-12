import numpy as np
from functools import reduce


def piecewise_addition(
    x: np.ndarray, x_lower: list, y_lower: list, length: list
) -> np.ndarray:
    """
    args:
        x           vector input
        x_lower     iterable of source range starting values, length n
        y_lower     iterable of destination range starting points, length n
        length      iterable of lengths of source/destination ranges, length n
    returns:
        out         same shape as x
    """
    x_lower_arr = np.asarray(x_lower)
    y_lower_arr = np.asarray(y_lower)
    length_arr = np.asarray(length)
    x_upper_arr = x_lower_arr + length_arr
    shift_arr = y_lower_arr - x_lower_arr
    condarray = np.logical_and(
        x >= x_lower_arr[:, np.newaxis], x < x_upper_arr[:, np.newaxis]
    )
    condlist = [row for row in condarray]
    funclist = [lambda x, y=h: x + y for h in shift_arr] + [lambda x: x]
    out = np.piecewise(x, condlist, funclist)
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
                break
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
            data[current_section] = np.vstack(
                (
                    data[current_section],
                    np.array([int(x) for x in stripped_line.split(" ")]),
                )
            )
# build list of piecewise addition maps
map_list = []
for section in sections[1:]:
    dat = data[section]
    current_map = lambda x, dat=dat: piecewise_addition(
        x, x_lower=dat[:, 1], y_lower=dat[:, 0], length=dat[:, 2]
    )
    map_list.append(current_map)
composed_map = reduce(lambda f, g: lambda x: g(f(x)), map_list)


# find location of each seed
seeds = data["seeds"]
locations = composed_map(seeds)
print(f"seeds: {list(seeds)}")
print(f"lowest location number: {min(locations)}")
