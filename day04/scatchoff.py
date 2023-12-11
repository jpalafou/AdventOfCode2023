def _remove_empty(l: list) -> list:
    return [x for x in l if x]


class Scratchcard:
    def __init__(self, s: str):
        """
        args:
            s   sequence of winning numbers | sequence of card numbers
        returns:
            Scratchcard()
        """
        winning_string, card_string = s.split("| ")
        self.winning_numbers = [
            int(n) for n in _remove_empty(winning_string.split(" "))
        ]
        self.card_numbers = [int(n) for n in _remove_empty(card_string.split(" "))]

    def scratch(self) -> int:
        """
        returns:
            number of points the scratchcard is worth
        """
        points = 0
        has_matches = False
        for i in self.card_numbers:
            if i in self.winning_numbers:
                if not has_matches:
                    points = 1
                    has_matches = True
                else:
                    points *= 2
        return points


points = 0

with open("inputs.txt") as file:
    for line in file:
        # clean up text
        raw_line = line.rstrip()
        index_string, card_string = raw_line.split(": ")
        i = int(index_string.replace("Card ", ""))
        # define scratchcard
        scratchcard = Scratchcard(card_string)
        points += scratchcard.scratch()
print(f"Total scratchcard points: {points}")
