import numpy as np


def roll(arr: np.ndarray, direction: str) -> np.ndarray:
    """
    args:
        arr         2d array with 0 for open space, 1 for round rocks, and 2 for cube
                    rocks
        direction   "north", "south", "east", or "west"
    returns:
        out         arr where round rocks have rolled in the specified direciton
    """
    if direction in ["north", "south"]:
        axis = 1
        l, n_slices = arr.shape
    else:
        axis = 0
        n_slices, l = arr.shape
    slices = [slice(None), slice(None)]
    out = np.copy(arr)
    for i in range(n_slices):
        slices[axis] = i
        arr1d = out[tuple(slices)]  # reference to out
        cube_pos = np.append(-1, np.append(np.where(arr1d == 2)[0], l))
        round_pos = np.where(arr1d == 1)[0]
        for bound1, bound2 in zip(cube_pos[:-1], cube_pos[1:]):
            rollable_pos = round_pos[
                np.logical_and(round_pos >= bound1, round_pos < bound2)
            ]
            if rollable_pos.size:
                arr1d[rollable_pos] = 0
                if direction in ["north", "west"]:
                    new_pos = np.arange(len(rollable_pos)) + bound1 + 1
                else:
                    new_pos = np.arange(0, -len(rollable_pos), -1) + bound2 - 1
                arr1d[new_pos] = 1
    assert np.sum(arr == 1) == np.sum(out == 1)
    assert np.sum(arr == 2) == np.sum(out == 2)
    return out


int_map = {ord("."): "0", ord("O"): "1", ord("#"): "2"}
int_rows = [row.translate(int_map) for row in open("inputs.txt").read().split("\n")]
arr = np.asarray([[int(i) for i in row] for row in int_rows])

# tilt platform to the north and compute total load
arr = roll(arr, "north")
total_load = np.sum(np.sum(arr == 1, axis=1) * np.arange(arr.shape[0], 0, -1))
print(total_load)
