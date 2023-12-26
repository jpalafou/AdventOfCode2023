import numpy as np


def find_sym_idx(arr: np.ndarray):
    """
    args:
        arr     2d array
    returns:
        number of rows above horizontal axis of reflection
        0 if no axis of reflection
    """
    l = arr.shape[0]
    for i in range(1, l):
        region = arr[:i]
        region_inv = arr[i:]
        lim = min(region.shape[0], region_inv.shape[0])
        if (region[-lim:, :] == np.flipud(region_inv[:lim, :])).all():
            return i
    return 0


summary = 0
with open("inputs.txt") as file:
    mirrors = file.read().split("\n\n")
    for mirror in mirrors:
        list_of_rows = []
        for row in mirror.split("\n"):
            formatted_row = [int(i) for i in row.replace(".", "0").replace("#", "1")]
            list_of_rows.append(formatted_row)
        mirror_arr = np.asarray(list_of_rows)
        summary += 100 * find_sym_idx(mirror_arr) + find_sym_idx(mirror_arr.T)
print(f"{summary=}")
