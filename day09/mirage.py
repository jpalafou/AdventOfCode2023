import numpy as np


def extrapolate_next(arr: np.ndarray) -> np.ndarray:
    """
    args:
        arr     (n,)
    returns:
        out     (n+1,) arr with extrapolated value at the end
    """
    list_of_arrays = [np.asarray(arr)]
    while not np.all(list_of_arrays[-1] == np.zeros_like(list_of_arrays[-1])):
        list_of_arrays.append(list_of_arrays[-1][1:] - list_of_arrays[-1][:-1])
    for i in range(len(list_of_arrays))[::-1]:
        if i == len(list_of_arrays) - 1:
            list_of_arrays[i] = np.append(list_of_arrays[i], 0)
        else:
            this_array = list_of_arrays[i]
            prev_array = list_of_arrays[i + 1]
            list_of_arrays[i] = np.append(this_array, this_array[-1] + prev_array[-1])
    out = list_of_arrays[0]
    return out


list_of_extrapped_values = []
with open("inputs.txt") as file:
    for line in file:
        time_series = [int(i) for i in line.strip().split(" ")]
        new_time_series = extrapolate_next(time_series)
        list_of_extrapped_values.append(new_time_series[-1])
print(f"Sum of extrapolated values: {np.sum(np.array(list_of_extrapped_values))}")
