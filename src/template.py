import argparse
import logging

Default_log_level = logging.WARNING

DAY = 0

parser = argparse.ArgumentParser(
    prog=f"Advent of Code 2023: day {DAY}",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser.add_argument("filename")
parser.add_argument("-v", "--verbose", action="count", default=0)


def part_one(f):
    pass


def part_two(f):
    pass


def main():
    args = parser.parse_args()

    log_level = max((0, Default_log_level - (args.verbose * 10)))
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    with open(args.filename, "r") as f:
        print(f"Part 1: {part_one(f)}")
        print(f"Part 2: {part_two(f)}")


if __name__ == "__main__":
    main()
