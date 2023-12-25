# I had to look at other people's solutions in order to write one for Part 2.
# I especially followed the approach of fuglede
# (https://github.com/fuglede/adventofcode/blob/master/2023/day12/solutions.py)
# and jonathanpaulson
# (https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/12.py)

from functools import cache


@cache
def count_possible(record: str, groups: tuple, hash_counter: int = 0) -> int:
    """
    args:
        record          arbitrary series of ".", "#", and "?"
        groups          number of contiguous strings of "#" to form
        hash_counter    how many hashtags have we seen in a row?
    returns:
        out             number of configurations of the "?" characters in record which
                        result in contiguous strings of "#" matching groups
    """
    out = 0
    if not groups and not hash_counter and "#" not in record:
        return 1
    if not record or not groups:
        return 0
    if record[0] in [".", "?"]:
        if hash_counter == groups[0]:
            out += count_possible(record[1:], groups[1:])
        elif hash_counter == 0:
            out += count_possible(record[1:], groups)
    if record[0] in ["#", "?"]:
        out += count_possible(record[1:], groups, hash_counter + 1)
    return out


for rep in [1, 5]:
    data = [s.split(" ") for s in open("inputs.txt").read().split("\n")]
    data = [(r, tuple(int(i) for i in g.split(","))) for r, g in data]
    count = sum(count_possible("?".join([r] * rep) + ".", g * rep) for r, g in data)
    print(f"Sum of possible configs ({rep=}): {count}")
