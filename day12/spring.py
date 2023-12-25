# I had to look at other people's solutions in order to write one for Part 2.
# I especially followed the approach of fuglede
# (https://github.com/fuglede/adventofcode/blob/master/2023/day12/solutions.py)

from functools import cache
# import numpy as np
import cProfile

@cache
def count_possible(record: str, groups: tuple, num_possible: int = 0) -> int:
    """
    args:
        record          arbitrary series of ".", "#", and "?"
        groups          number of contiguous strings of "#" to form
        num_possible    number of configurations of the "?" characters in record which
                        result in contiguous strings of "#" matching groups
                        initialized as 0 and then increases recursively
    returns:
        num_possible
    """
    # print(record, groups)
    if sum(groups) - record.count("#") > record.count("?"):
        # invalid case
        return num_possible
    # scan with kernel with length of leftmost group (+1 for ".")
    k = groups[0]
    prev_char = None
    for i in range(len(record) - k):
        scan = record[i : i + k + 1]
        ambiguous_start = prev_char is None or prev_char in ["?", "."]
        group_can_be_formed = "." not in scan[:-1]
        ambiguous_end = scan[-1] in ["?", "."]
        if ambiguous_start and group_can_be_formed and ambiguous_end:
            shorter_record = record[i + k + 1 :]
            if len(groups) > 1:
                # if the leftmost group could be formed, try forming subsequent groups
                num_possible = count_possible(shorter_record, groups[1:], num_possible)
            else:
                # no subseqeuent groups, so this must be a possible configuration
                # print("\t", scan)
                if "#" not in shorter_record:
                    num_possible += 1
        if scan[0] == "#":
            # starting with a # implies this group cannot be any further
            break
    return num_possible



# data = [s.split(" ") for s in open("test.txt").read().split("\n")]
# data = [(r, tuple(int(i) for i in g.split(","))) for r, g in data]
# total = 0
# for r, g in data:
#     num_possible = count_possible("?".join([r] * 1) + ".", g * 1)
#     total += num_possible
#     if total < 100:
#         print(num_possible)


# print(count_possible("?#####??#?????.?#.." + ".", (9,2,1)))

# p

for rep in [1, 5]:
    data = [s.split(" ") for s in open("test.txt").read().split("\n")]
    data = [(r, tuple(int(i) for i in g.split(","))) for r, g in data]
    counter = 0
    for i, row in enumerate(data):
        print(f"{i + 1}/{len(data)}")
        record, group = row
        counter += count_possible("?".join([record] * rep) + ".", group * rep)
    print(counter)
