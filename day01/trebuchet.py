import numpy as np

int_names = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


def get_calibration_number(line: str, include_digit_names: bool = False):
    """
    print the concatenation of the first and last digit in a string
    """
    first_occurence_idxs = [np.inf] * 10
    last_occurence_idxs = [-np.inf] * 10
    for i, name in int_names.items():
        str_i = str(i)
        if str_i in line:
            first_occurence_idxs[i] = line.find(str_i)
            last_occurence_idxs[i] = line.rfind(str_i)
        if include_digit_names and name in line:
            first_occurence_idxs[i] = min(first_occurence_idxs[i], line.find(name))
            last_occurence_idxs[i] = max(last_occurence_idxs[i], line.rfind(name))
    # string index of first/last digit occurance
    first_idx = min(first_occurence_idxs)
    last_idx = max(last_occurence_idxs)
    # first/last digit to occur
    first = np.argmin(first_occurence_idxs)
    last = np.argmax(last_occurence_idxs)
    if not isinstance(first_idx, int) or not isinstance(last_idx, int):
        raise Exception(f"Could not resolve first and last integers from {line}")
    return 10 * first + last


for include_digit_names in [False, True]:
    sum_of_calibration_numbers = 0
    with open("trebuchet_inputs.txt") as file:
        for line in file:
            raw_line = line.rstrip()
            sum_of_calibration_numbers += get_calibration_number(
                raw_line, include_digit_names=include_digit_names
            )
    print(
        f"Sum of calibration numbers ({include_digit_names=}): {sum_of_calibration_numbers}"
    )
