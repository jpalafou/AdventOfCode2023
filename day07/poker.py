import numpy as np

face_values = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "T": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}


class Hand:
    def __init__(self, s: str):
        """
        args:
            s   5 characters representing cards
        """
        self.enumerated_faces = [face_values[card] for card in s]
        self._determine_type()

    def _determine_type(self):
        """
        returns:
            self.type   hand types ranked increasingly from 1 to 7
        """
        uniq, counts = np.unique(np.array(self.enumerated_faces), return_counts=True)
        uniques, clusters = len(uniq), np.sort(counts)
        if uniques == 1:  # 5 of a kind
            hand_type = 7
        elif uniques == 2:
            if np.all(clusters == np.array([1, 4])):  # 4 of a kind
                hand_type = 6
            elif np.all(clusters == np.array([2, 3])):  # full house
                hand_type = 5
        elif uniques == 3:
            if np.all(clusters == np.array([1, 1, 3])):  # 3 of a kind
                hand_type = 4
            elif np.all(clusters == np.array([1, 2, 2])):  # 2 pair
                hand_type = 3
        elif uniques == 4:  # 1 pair
            hand_type = 2
        else:  # high hard
            hand_type = 1
        self.type = hand_type


def base_n_int(digits: np.ndarray, n: int) -> int:
    """
    args:
        digits  shape (# integers, # digits)
        n       number base
    returns:
        out     shape (# integers,)
    """
    num_ints, num_digits = digits.shape
    multiplier = np.power(n, np.arange(num_digits - 1, -1, -1))
    multipliers = np.tile(multiplier, (num_ints, 1))
    out = np.sum(digits * multipliers, axis=1)
    return out


with open("inputs.txt") as file:
    list_of_hands = []
    list_of_bets = []
    for line in file:
        card_string, bet_string = line.strip().split(" ")
        hand = Hand(card_string)
        enumerated_hand = [hand.type] + hand.enumerated_faces
        list_of_hands.append(enumerated_hand)
        list_of_bets.append(int(bet_string))
    n_hands = len(list_of_hands)
    hands = np.array(list_of_hands)
    bets = np.array(list_of_bets)

# rank hands as base 13 integers with 6 digits, then sort
ranks = base_n_int(hands, n=13)
sorted_idxs = np.argsort(ranks)

# find total winnings using the (1, 2, 3, ...) ranking system
total_winnings = np.sum(bets[sorted_idxs] * np.arange(1, n_hands + 1))
print(f"Total winnings: {total_winnings}")
