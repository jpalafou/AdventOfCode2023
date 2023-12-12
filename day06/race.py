import numpy as np


def _remove_empty(l: list) -> list:
    """
    args:
        l       iterable
    returns:
        list with empty elements omitted
    """
    return [x for x in l if x]


def boat_strategies(time: int) -> np.ndarray:
    """
    args:
        time    race duration
    returns:
        out     pairs of time spent charging and the resulting distance
    """
    list_of_outcomes = []
    for charge_time in range(time):
        sail_time = time - charge_time
        distance = sail_time * charge_time
        list_of_outcomes.append((charge_time, distance))
    out = np.asarray(list_of_outcomes)
    return out


# read race data
with open("inputs.txt") as file:
    rows = file.readlines()
    data = []
    for row, label in zip(rows, ["Time:", "Distance:"]):
        data_string = row.replace(label, "").strip()
        data.append([int(i) for i in _remove_empty(data_string.split(" "))])
    times, records = data

# count the number of ways to beat the record for each race
winning_strategy_product = 1
for time, record in zip(times, records):
    outcomes = boat_strategies(time)
    winning_stratgies = np.sum(np.where(outcomes[:, 1] > record, 1, 0))
    winning_strategy_product *= winning_stratgies
print(f"Product of winning race strategies: {winning_strategy_product}")
