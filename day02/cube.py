def determine_handful_possbility(handful: dict, bag: dict):
    """
    args:
        handful     dict of handful amounts
        bag         dict of total amounts
    returns:
        out         whether the handful was possible to draw from the bag
    """
    out = True
    for key in handful.keys():
        if key not in bag.keys():
            raise Exception(f"Key '{key}' not in bag")
        if handful[key] > bag[key]:
            out = False
    return out


def minimum_set_of_cubes(game: list):
    """
    args:
        game            list of dict handfuls, each showing the amount of each colored
                        cube drawn
    out:
        minimum_set     dict showing the minmium amount of each colored cube for the
                        game to be possible
    """
    minimum_set = {}
    for handful in game:
        for key in handful.keys():
            if key not in minimum_set.keys():
                minimum_set[key] = handful[key]
            minimum_set[key] = max(minimum_set[key], handful[key])
    return minimum_set


def power(set_of_cubes: dict):
    """
    args:
        set_of_cubes    {'red': # of red cubes, 'green': ..., 'blue': ...}
    returns:
        out             product of the counts of each colored cube
    """
    out = 1
    for key in ["red", "green", "blue"]:
        if key not in set_of_cubes.keys():
            return 0
        out *= set_of_cubes[key]
    return out


def string2dict(s: str):
    """
    args:
        s       string of comma separated ints and keys
                "n1 key1, n2 key2, etc"
    returns:
        out     dictionary representation of s
                {key1: n1, key2: n2, etc}
    """
    out = {}
    for this in s.split(", "):
        this_split = this.split(" ")
        amount, key = int(this_split[0]), this_split[1]
        out[key] = amount
    return out


bag = dict(red=12, green=13, blue=14)
sum_of_possible_game_IDs = 0
sum_of_minimum_set_powers = 0


with open("inputs.txt") as file:
    for line in file:
        # clean up text
        raw_line = line.rstrip()
        game_id_string, game_log = raw_line.split(": ")
        game_id = int(game_id_string.replace("Game ", ""))
        handfuls = [string2dict(handful) for handful in game_log.split("; ")]
        # determine if game is possible and, if so, add its ID
        game_is_possible = True
        for handful in handfuls:
            if not determine_handful_possbility(handful=handful, bag=bag):
                game_is_possible = False
        if game_is_possible:
            sum_of_possible_game_IDs += game_id
        # find the minimum set of cubes for the game, add its power
        sum_of_minimum_set_powers += power(minimum_set_of_cubes(handfuls))
print(f"Sum of possible game IDs: {sum_of_possible_game_IDs}")
print(f"Sum of powers of minimum game sets: {sum_of_minimum_set_powers}")
