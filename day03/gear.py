def remove_empty(strings):
    """
    args:
        strings     list
    returns:
        list with '' elements removed
    """
    return [x for x in strings if x]


def is_adjacent_to_symbol(
    rows: list, first: int, length: int, symbol_character: str = "s"
):
    """
    args:
        rows                list of three strings of equal length
        first               index of first digit number of interest in the middle row
        length              digits of number of interest
        symbol_character    character which indicates a symbol
    returns:
        adjacent            is number of interest adjacent to a symbol
    """
    kernel = ""
    left_kernel_width, right_kernel_width = 1, 1
    if first == 0:
        left_kernel_width = 0
    if first + length == len(rows[0]):
        right_kernel_width = 0
    for row in rows:
        kernel += row[first - left_kernel_width : first + length + right_kernel_width]
    return symbol_character in kernel


symbols = "!@#$%^&*()[]{};:,/<>?\|`~-=_+"
part_sum = 0


with open("inputs.txt") as file:
    rows = file.readlines()
    # clean up text
    rows = [row.rstrip() for row in rows]
    # replace special characters with 's'
    translation_dict = {ord(c): "s" for c in symbols}
    rows = [row.translate(translation_dict) for row in rows]
    # define trivial boundary rows and set as first and last
    boundary_row = "." * len(rows[0])
    rows = [boundary_row] + rows + [boundary_row]
    for kernel_rows in zip(rows[:-2], rows[1:-1], rows[2:]):
        current_row = kernel_rows[1]
        # get numbers and symbols
        not_periods = remove_empty(current_row.split("."))
        list_of_n_idxs = []
        for not_period in not_periods:
            numbers = remove_empty(not_period.split("s"))
            for n in numbers:
                n_len = len(n)
                n_i = current_row.find(n)
                n_is_part = is_adjacent_to_symbol(kernel_rows, first=n_i, length=n_len)
                if n_is_part:
                    part_sum += int(n)
                    # replace part with .'s since it was already accounted for
                    current_row = current_row.replace(n, "." * n_len, 1)
print(f"Sum of part numbers: {part_sum}")
