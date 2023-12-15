import numpy as np


def extrapolate_next(arr: np.ndarray, forward: bool = True) -> np.ndarray:
    """
    args:
        arr         (n,)
        forward     extrapolates end of array if true, beginning if false
    returns:
        out         (n+1,) arr with extrapolated value at the beginning/end
    """
    list_of_arrays = [np.asarray(arr)]
    while not np.all(list_of_arrays[-1] == np.zeros_like(list_of_arrays[-1])):
        list_of_arrays.append(list_of_arrays[-1][1:] - list_of_arrays[-1][:-1])
    for i in range(len(list_of_arrays))[::-1]:
        if i == len(list_of_arrays) - 1:
            if forward:
                list_of_arrays[i] = np.append(list_of_arrays[i], 0)
            else:
                list_of_arrays[i] = np.append(0, list_of_arrays[i])
        else:
            array = list_of_arrays[i]
            prev_array = list_of_arrays[i + 1]
            if forward:
                list_of_arrays[i] = np.append(array, array[-1] + prev_array[-1])
            else:
                list_of_arrays[i] = np.append(array[0] - prev_array[0], array)
    out = list_of_arrays[0]
    return out


for forward in [True, False]:
    list_of_extrapped_values = []
    with open("inputs.txt") as file:
        for line in file:
            time_series = [int(i) for i in line.strip().split(" ")]
            new_time_series = extrapolate_next(time_series, forward=forward)
            list_of_extrapped_values.append(new_time_series[-1 if forward else 0])
            sum_of_values = np.sum(np.array(list_of_extrapped_values))
    print(f"Sum of extrapolated values {forward=}: {sum_of_values}")
