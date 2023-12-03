import argparse
import logging
from math import prod

Default_log_level = logging.WARNING

DAY = 2

# 12 red cubes, 13 green cubes, and 14 blue cubes
bag = {"red": 12, "green": 13, "blue": 14}

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


def part_one(f):
    id_sum = 0

    for game in f:
        possible = True
        game = game.split(":")
        id = int(game[0].split()[-1])
        logger.debug(f"Game id: {id}")
        hands = game[1].split(";")
        for hand in hands:
            cubes_by_color = hand.split(",")
            for color in cubes_by_color:
                color = color.split()
                logger.debug(color)
                if int(color[0]) > bag.get(color[1]):
                    possible = False
                    break
            if not possible:
                break
        if possible:
            id_sum += id

    return id_sum


def part_two(f):
    power_sum = 0

    for game in f:
        logger.debug(game)
        game = game.split(":")
        hands = game[1].split(";")
        min_cubes = {"red": 0, "green": 0, "blue": 0}
        for hand in hands:
            logger.debug(hand)
            cubes_by_color = hand.split(",")
            for color in cubes_by_color:
                logger.debug(color)
                color = color.split()
                logger.debug(color)
                min_cubes[color[1]] = max((min_cubes.get(color[1]), int(color[0])))
        power_sum += prod(min_cubes.values())

    return power_sum


def main():
    with open(args.filename, "r") as f:
        print(f"Part 1: {part_one(f)}")
        f.seek(0)
        print(f"Part 2: {part_two(f)}")


if __name__ == "__main__":
    main()
