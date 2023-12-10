def string2dict(s: str):
    """
    args:
        s       string of comma separated amounts and keys
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


bag_dict = dict(red=12, green=13, blue=14)
sum_of_possible_game_IDs = 0


with open("inputs.txt") as file:
    for line in file:
        # clean up text
        raw_line = line.rstrip()
        game_id_string, game_log = raw_line.split(": ")
        game_id = int(game_id_string.replace("Game ", ""))
        cube_handfuls = game_log.split("; ")
        # analyze each handufl in the game
        game_is_possible = True
        for handful in cube_handfuls:
            if not determine_handful_possbility(
                handful=string2dict(handful), bag=bag_dict
            ):
                game_is_possible = False
        if game_is_possible:
            sum_of_possible_game_IDs += game_id

print(f"Sum of possible game IDs: {sum_of_possible_game_IDs}")
