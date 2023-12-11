# global variables
symbols = "!@#$%^&*()[]{};:,/<>?\|`~-=_+"  # excludes '.'
numbers = "0123456789"


def _remove_empty(l: list) -> list:
    return [x for x in l if x]


def build_list_of_EngineSchematicItems(s: str, targets: str, row: int) -> list:
    """
    args:
        s           single row of engine schematic
        targets     chars to search for
        row         row index
    returns:
        list        EngineSchematicItems
    """
    # replace all symbols with . except targets
    filter_symbols = numbers + symbols
    for target in targets:
        filter_symbols = filter_symbols.replace(target, "")
    translation_dict = {ord(c): "." for c in filter_symbols}
    string_of_items = s.translate(translation_dict)
    raw_item_list = _remove_empty(string_of_items.split("."))
    out = []
    for item in raw_item_list:
        out.append(
            EngineSchematicItem(row=row, first=string_of_items.find(item), value=item)
        )
        string_of_items = string_of_items.replace(item, "." * len(item), 1)
    return out


class EngineSchematicItem:
    def __init__(self, row: int, first: int, value: str):
        """
        args:
            row     row index
            first   index of first character of item
            value
        """
        self.row = row
        self.col = (first, first + len(value) - 1)
        try:
            self.value = int(value)
        except ValueError:
            self.value = value

    def is_adjacent(self, other):
        if not (self.row == other.row and self.col == other.col):
            if abs(self.row - other.row) <= 1:
                for edge in [other.col[0], other.col[-1]]:
                    if edge >= self.col[0] - 1 and edge <= self.col[-1] + 1:
                        return True
        return False


part_sum = 0
gear_ratio_sum = 0

with open("inputs.txt") as file:
    rows = file.readlines()
    # clean up text
    rows = [row.rstrip() for row in rows]
    # define trivial boundary rows and set as first and last
    boundary_row = "." * len(rows[0])
    rows = [boundary_row] + rows + [boundary_row]
    # build lists of EngineSchematicItems with keys for item type
    item_lists = []
    for i, row in enumerate(rows):
        row_dict = {}
        for item_type, targets in zip(["n", "s", "a"], [numbers, symbols, "*"]):
            row_dict[item_type] = build_list_of_EngineSchematicItems(
                s=row, targets=targets, row=i
            )
        item_lists.append(row_dict)
    # loop through three rows at a time, identify quantities of interest
    for kern_items in zip(item_lists[:-2], item_lists[1:-1], item_lists[2:]):
        current_items = kern_items[1]
        kernel_symbols = kern_items[0]["s"] + kern_items[1]["s"] + kern_items[2]["s"]
        kernel_numbers = kern_items[0]["n"] + kern_items[1]["n"] + kern_items[2]["n"]
        # find numbers adjacent to kernels
        for n in current_items["n"]:
            for s in kernel_symbols:
                if s.is_adjacent(n):
                    part_sum += n.value
                    break
        # find asterisks adjacent to two numbers
        for a in current_items["a"]:
            adjacent_ns = []
            for n in kernel_numbers:
                if n.is_adjacent(a):
                    adjacent_ns.append(n.value)
            if len(adjacent_ns) == 2:
                gear_ratio_sum += adjacent_ns[0] * adjacent_ns[1]
print(f"Sum of part numbers: {part_sum}")
print(f"Sum of gear ratios: {gear_ratio_sum}")
