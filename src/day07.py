import argparse
import logging
from dataclasses import dataclass, field
from collections import Counter
from enum import IntEnum

Default_log_level = logging.WARNING

DAY = 7

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


class Hand_Types(IntEnum):
    High_Card = 1
    Pair = 2
    Two_Pair = 3
    Three_Of_Kind = 4
    Full_House = 5
    Four_Of_Kind = 6
    Five_Of_Kind = 7


@dataclass
class Hand:
    cards: str
    bid: int
    joker: bool = False
    ranks: list[str] = field(default_factory=list)
    hand_type: Hand_Types = field(init=False)

    def __post_init__(self):
        if self.joker:
            self.ranks.extend(
                ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
            )
        else:
            self.ranks.extend(
                ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
            )
        self.hand_type = self._hand_type()

    def _hand_type(self):
        card_counts = Counter(self.cards)
        if self.joker:
            if card_counts.get("J", 0) < 5:
                logger.debug(card_counts)
                jokers = card_counts.pop("J", 0)
                logger.debug(f"{jokers=} {card_counts=}")
                most_common_card = card_counts.most_common(1)
                logger.debug(f"{most_common_card=}")
                card_counts[most_common_card[0][0]] += jokers
                logger.debug(f"{card_counts=}")
        match list(card_counts.values()):
            case [5]:
                return Hand_Types.Five_Of_Kind
            case x if 4 in x:
                return Hand_Types.Four_Of_Kind
            case x if 3 in x and 2 in x:
                return Hand_Types.Full_House
            case x if 3 in x:
                return Hand_Types.Three_Of_Kind
            case x if x.count(2) == 2:
                return Hand_Types.Two_Pair
            case x if 2 in x:
                return Hand_Types.Pair
            case _:
                return Hand_Types.High_Card

    def __lt__(self, other) -> bool:
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type == other.hand_type:
            logger.debug(f"Same Type {self.cards} - {other.cards}")
            for s, o in zip(self.cards, other.cards):
                logger.debug(f"Compare {s} {o}")
                if self.ranks.index(s) < other.ranks.index(o):
                    logger.debug(f"{s} is lower than {o}")
                    return True
                if self.ranks.index(s) > other.ranks.index(o):
                    return False
        return False


def part_one(f):
    hands = [
        Hand(cards, int(rank)) for cards, rank in [row.strip().split() for row in f]
    ]
    logger.debug(f"Input hands: {hands}")
    hands.sort()
    logger.debug(f"Sorted hands: {hands}")
    return sum([hand.bid * rank for rank, hand in enumerate(hands, start=1)])


def part_two(f):
    hands = [
        Hand(cards, int(rank), joker=True)
        for cards, rank in [row.strip().split() for row in f]
    ]
    logger.debug(f"Input hands: {hands}")
    hands.sort()
    logger.debug(f"Sorted hands: {hands}")
    return sum([hand.bid * rank for rank, hand in enumerate(hands, start=1)])


def main():
    with open(args.filename, "r") as f:
        print(f"Part 1: {part_one(f)}")
        f.seek(0)
        print(f"Part 2: {part_two(f)}")


if __name__ == "__main__":
    main()
