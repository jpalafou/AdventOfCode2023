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
    charge_times = np.arange(time)[:, np.newaxis]
    sail_times = time - charge_times
    distances = sail_times * charge_times
    out = np.hstack((charge_times, distances))
    return out


# read race data
for multiple_races in [True, False]:
    with open("inputs.txt") as file:
        rows = file.readlines()
        data = []
        for row, label in zip(rows, ["Time:", "Distance:"]):
            stripped_row = row.replace(label, "").strip()
            if multiple_races:
                data.append([int(i) for i in _remove_empty(stripped_row.split(" "))])
            else:
                data.append([int(stripped_row.replace(" ", ""))])

    # count the number of ways to beat the record for each race
    times, records = data
    winning_strategy_product = 1
    for time, record in zip(times, records):
        outcomes = boat_strategies(time)
        winning_stratgies = np.sum(np.where(outcomes[:, 1] > record, 1, 0))
        winning_strategy_product *= winning_stratgies
    print(f"{multiple_races=}")
    print(f"\tProduct of winning race strategies: {winning_strategy_product}")
