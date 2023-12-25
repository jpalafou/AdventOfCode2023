import numpy as np
import itertools


def count_contiguous_group(s: str, key: str) -> list:
    """
    args:
        s       string which may contain groups of key
        key     character which may occur
    returns:
        out     list of lengths of groups of key in s
    """
    list_of_groups = ("".join("#" if x == key else "." for x in s)).split(".")
    out = [len(x) for x in list_of_groups if x]
    return out


sum_of_counts_of_arragnements = 0
with open("inputs.txt") as file:
    for line in file:
        arrangements = 0
        record, groups_str = line.strip().split(" ")
        groups = [int(i) for i in groups_str.split(",")]
        unknown_pos = [i for i, c in enumerate(record) if c == "?"]
        group_pos = [i for i, c in enumerate(record) if c == "#"]
        n_in_group = np.sum(np.asarray(groups))
        n_group_to_fill = n_in_group - len(group_pos)

        # loop over possible arrangments of "#" in "?" and count those which are valid
        for temp_group_pos in itertools.combinations(unknown_pos, n_group_to_fill):
            temp_record = list(record)
            temp_record = "".join(
                "#" if i in temp_group_pos else s for i, s in enumerate(temp_record)
            )
            temp_record = temp_record.translate({ord("?"): "."})
            if count_contiguous_group(temp_record, "#") == groups:
                arrangements += 1
        if sum_of_counts_of_arragnements < 100:
            print(arrangements)
        sum_of_counts_of_arragnements += arrangements
print(f"Sum of counts of arrangements: {sum_of_counts_of_arragnements}")
