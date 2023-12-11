def _remove_empty(l: list) -> list:
    """
    args:
        l       iterable
    returns:
        list with empty elements omitted
    """
    return [x for x in l if x]


class Scratchcard:
    def __init__(self, s: str):
        """
        args:
            s                   sequence of winning numbers | sequence of card numbers
        """
        winning_string, card_string = s.split("| ")
        self.winning_numbers = [
            int(n) for n in _remove_empty(winning_string.split(" "))
        ]
        self.card_numbers = [int(n) for n in _remove_empty(card_string.split(" "))]
        self.already_scratched = False

    def scratch(self):
        """
        returns:
            self.num_matches    number of matching pairs
            self.points         number of points the scratchcard is worth
        """
        if self.already_scratched:
            return
        points = 0
        num_matches = 0
        for i in self.card_numbers:
            if i in self.winning_numbers:
                if num_matches == 0:
                    points = 1
                else:
                    points *= 2
                num_matches += 1
        self.already_scratched = True
        self.num_matches = num_matches
        self.points = points


class ScratchcardDeck:
    def __init__(self, scratchcards: list):
        """
        args:
            scratchcards    list of scratchcards
        """
        self.scratchcards = scratchcards

    def point_game(self):
        """
        returns:
            self.total_points   points won by deck of scratchcads
        """
        self.total_points = 0
        for scratchcard in self.scratchcards:
            scratchcard.scratch()
            self.total_points += scratchcard.points

    def recursive_game(self, search: tuple = None):
        """
        args:
            search:             indices of cards to play and earn more cards
        returns:
            self.winning_stack  list of Scratchcards won by recursively replaying the
                                n subsequent cards where n is the number of points
        """
        if search == None:
            self.winning_stack = []
            start, stop = 0, len(self.scratchcards)
        else:
            start, stop = search
        for i in range(start, stop):
            current_scratchcard = self.scratchcards[i]
            current_scratchcard.scratch()
            self.winning_stack.append((i, current_scratchcard))
            for j in range(i + 1, i + current_scratchcard.num_matches + 1):
                if j > len(self.scratchcards) - 1:
                    break
                self.recursive_game(search=(j, j + 1))


with open("inputs.txt") as file:
    rows = file.readlines()
    # clean up text
    list_of_scratchcards = []
    for row in rows:
        raw_line = row.rstrip()
        list_of_scratchcards.append(Scratchcard(raw_line.split(": ")[1]))
    deck = ScratchcardDeck(list_of_scratchcards)
deck.point_game()
print(f"Total scratchcard points: {deck.total_points}")
deck.recursive_game()
print(f"# won cards: {len(deck.winning_stack)}")
