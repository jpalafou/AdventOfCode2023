import numpy as np
import itertools

translation = {ord("."): "0", ord("#"): "1"}


def galaxy_expansion(arr: np.ndarray) -> np.ndarray:
    """
    args:
        arr     2d array of integers
    returns:
        out     arr with duplicated rows/cols containing only 0s
    """
    no_gals_along_cols = np.where(np.all(galaxy == 0, axis=1))[0]
    no_gals_along_rows = np.where(np.all(galaxy == 0, axis=0))[0]
    row_insert = np.zeros(arr.shape[1], dtype="int")
    out = np.insert(arr, no_gals_along_cols, row_insert, axis=0)
    col_insert = np.zeros((out.shape[0], 1), dtype="int")
    out = np.insert(out, no_gals_along_rows, col_insert, axis=1)
    return out


def step_counter(x1: int, y1: int, x2: int, y2: int):
    """
    args:
        coordinate pairs (x1, y1), (x2, y2)
    returns:
        the minimum number of steps it takes to move from (x1, y1) to (x2, y2)
    """
    return abs(y2 - y1) + abs(x2 - x1)


with open("inputs.txt") as file:
    galaxy = np.asarray(
        [[int(i) for i in line.strip().translate(translation)] for line in file]
    )
    nonzero = 1
    for j in range(galaxy.shape[1]):
        for i in range(galaxy.shape[0]):
            if galaxy[i, j] != 0:
                galaxy[i, j] = nonzero
                nonzero += 1

# expand spaces between galaxies
for expansion_factor in [2, 1000000]:
    # gather coordinate pairs of galaxies
    coord_pairs = np.vstack(np.where(galaxy != 0)).T

    # identify rows and columsn which don't contain galaxies
    empty_rows = np.where(np.all(galaxy == 0, axis=1))[0]
    empty_cols = np.where(np.all(galaxy == 0, axis=0))[0]

    # update row indices of galacy coordinate pairs while keeping track of vertical shift
    vertical_shift = expansion_factor - 1
    for i in range(len(empty_rows)):
        coord_pairs[:, 0] = np.where(
            coord_pairs[:, 0] > empty_rows[i],
            coord_pairs[:, 0] + vertical_shift,
            coord_pairs[:, 0],
        )
        empty_rows = np.where(
            empty_rows > empty_rows[i], empty_rows + vertical_shift, empty_rows
        )

    # same as above but column indices and horizontal shift
    horizontal_shift = expansion_factor - 1
    for j in range(len(empty_cols)):
        coord_pairs[:, 1] = np.where(
            coord_pairs[:, 1] > empty_cols[j],
            coord_pairs[:, 1] + horizontal_shift,
            coord_pairs[:, 1],
        )
        empty_cols = np.where(
            empty_cols > empty_cols[j], empty_cols + horizontal_shift, empty_cols
        )

    # compute the sum of the distances between galaxies
    sum_of_distances = 0
    for (x1, y1), (x2, y2) in itertools.combinations(coord_pairs, 2):
        sum_of_distances += step_counter(x1, y1, x2, y2)
    print(f"{expansion_factor=}")
    print(f"\tSum of distances between all pairs of galaxies {sum_of_distances}")
