import argparse
import logging

Default_log_level = logging.WARNING

DAY = 4

parser = argparse.ArgumentParser(
    prog=f"Advent of Code 2023: day {DAY}",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser.add_argument("filename")
parser.add_argument("-v", "--verbose", action="count", default=0)
args = parser.parse_args()

log_level = max((0, Default_log_level - (args.verbose * 10)))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


class Lottery_Card:
    def __init__(self, card) -> None:
        card = card.split(":")
        self.id = int(card[0].split()[-1])
        card = card[1].split("|")
        self.winning_numbers = [int(x) for x in card[0].split()]
        self.player_numbers = [int(x) for x in card[1].split()]

    @property
    def count_winning_numbers(self):
        return sum([1 for x in self.player_numbers if x in self.winning_numbers])

    @property
    def points(self) -> int:
        if self.count_winning_numbers:
            return 2 ** (self.count_winning_numbers - 1)
        return 0


def part_one(f):
    cards = [Lottery_Card(line.strip()) for line in f]
    return sum([card.points for card in cards])


def part_two(f):
    cards = {
        int(line.split(":")[0].split()[-1]): Lottery_Card(line.strip()) for line in f
    }
    card_counts = {card: 1 for card in cards}

    for id, card in sorted(cards.items(), key=lambda x: x[0]):
        if (wins := card.count_winning_numbers) > 0:
            for x in range(id + 1, id + wins + 1):
                card_counts[x] += card_counts.get(id)

    return sum(card_counts.values())


def main():
    with open(args.filename, "r") as f:
        print(f"Part 1: {part_one(f)}")
        f.seek(0)
        print(f"Part 2: {part_two(f)}")


if __name__ == "__main__":
    main()
