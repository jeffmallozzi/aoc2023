import argparse
import logging
from itertools import cycle

Default_log_level = logging.WARNING

DAY = 8

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

directions = []

maps = {}

def part_one():
    location = "AAA"
    for steps, direction in enumerate(cycle(directions)):
        location = maps[location][direction]
        if location = "ZZZ": return steps
        


def part_two():
    pass


def main():
    with open(args.filename, "r") as f:
        directions = f.readline().strip()
        f.readline()
        for line in f:
            maps = {
                start.strip() : {
                    "LR"[x] : end.strip()
                    for x, end in enumerate(lr.strip("()").split(",")
                }
                for start, lr in line.split("=")
            }
    print(f"Part 1: {part_one()}")
    print(f"Part 2: {part_two()}")


if __name__ == "__main__":
    main()
