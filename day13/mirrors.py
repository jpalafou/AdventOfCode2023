import numpy as np


def find_sym_idx(arr: np.ndarray, fix_smudge: bool = False):
    """
    args:
        arr         2d array
        fix_smudge  if one nonzero element in arr is preventing symmetry, set it to 0
    returns:
        out         number of rows above horizontal axis of reflection
                    0 if no axis of reflection
        modified    whether arr was modified
    """
    for i in range(1, arr.shape[0]):
        region = arr[:i]
        region_inv = arr[i:]
        lim = min(region.shape[0], region_inv.shape[0])
        upper_side = region[-lim:, :]
        lower_side = np.flipud(region_inv[:lim, :])
        if fix_smudge:
            if np.sum(np.abs(upper_side - lower_side)) == 1:
                # sm_i, sm_j    smudge indices
                sm_i, sm_j = np.where(np.abs(upper_side - lower_side) == 1)
                if np.sum(upper_side - lower_side) == 1:
                    # upper_side has the smudge
                    sm_i_arr = i - lim + sm_i
                else:
                    # lower_side has the smudge
                    sm_i_arr = i + lim - sm_i - 1
                arr[sm_i_arr, sm_j] = 0
                return i, True
        else:
            if (upper_side == lower_side).all():
                return i, False
    return 0, False


for fix_smudge in [False, True]:
    sum_of_summaries = 0
    with open("inputs.txt") as file:
        mirrors = file.read().split("\n\n")
        for mirror in mirrors:
            list_of_rows = []
            for row in mirror.split("\n"):
                formatted_row = [
                    int(i) for i in row.replace(".", "0").replace("#", "1")
                ]
                list_of_rows.append(formatted_row)
            mirror_arr = np.asarray(list_of_rows)
            # find the axis of symmetry of mirror_arr. move on once the axis is found
            horizontal_axis, modified = find_sym_idx(mirror_arr, fix_smudge)
            if (not fix_smudge and horizontal_axis) or (fix_smudge and modified):
                sum_of_summaries += 100 * horizontal_axis
                continue
            # transpose array to search for vertical axis of symmetry
            sum_of_summaries += find_sym_idx(mirror_arr.T, fix_smudge)[0]
    print(f"{fix_smudge=}, {sum_of_summaries=}")
