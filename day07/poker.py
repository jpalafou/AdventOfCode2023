import numpy as np

sorted_cards_jack = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
sorted_cards_joker = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class Hand:
    def __init__(self, s: str, J_is_joker: bool = False):
        """
        args:
            s           5 characters representing cards
            J_is_joker  whether the J card is a joker
        """
        self.J_is_joker = J_is_joker
        sorted_cards = sorted_cards_jack
        if self.J_is_joker:
            sorted_cards = sorted_cards_joker
        face_values = {c: v for c, v in zip(sorted_cards, range(len(sorted_cards)))}
        self.enumerated_faces = [face_values[card] for card in s]
        self._determine_type()

    def _determine_type(self):
        """
        returns:
            self.type   hand types ranked increasingly from 1 to 7
        """
        Jvalue = -1
        Js = [-1]
        if self.J_is_joker:
            Jvalue = 0
            Js = range(13)
        original_faces = np.array(self.enumerated_faces)
        best_hand_type = 0
        for trial_J in Js:
            trial_faces = np.where(original_faces == Jvalue, trial_J, original_faces)
            uniq, counts = np.unique(trial_faces, return_counts=True)
            clusters = np.sort(counts)
            if len(uniq) == 1:  # 5 of a kind
                hand_type = 7
            elif len(uniq) == 2:
                if np.all(clusters == np.array([1, 4])):  # 4 of a kind
                    hand_type = 6
                elif np.all(clusters == np.array([2, 3])):  # full house
                    hand_type = 5
            elif len(uniq) == 3:
                if np.all(clusters == np.array([1, 1, 3])):  # 3 of a kind
                    hand_type = 4
                elif np.all(clusters == np.array([1, 2, 2])):  # 2 pair
                    hand_type = 3
            elif len(uniq) == 4:  # 1 pair
                hand_type = 2
            else:  # high hard
                hand_type = 1
            best_hand_type = max(best_hand_type, hand_type)
        self.type = best_hand_type


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


for J_is_joker in [False, True]:
    with open("inputs.txt") as file:
        list_of_hands = []
        list_of_bets = []
        for line in file:
            card_string, bet_string = line.strip().split(" ")
            hand = Hand(card_string, J_is_joker=J_is_joker)
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
    print(f"Total winnings ({J_is_joker=}): {total_winnings}")
