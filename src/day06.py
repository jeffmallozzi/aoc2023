import argparse
import logging
from math import prod

Default_log_level = logging.WARNING

DAY = 0

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

times = []
distances = []
winning_times = []

def part_one():
    for time, distance in zip(times, distances):
        winners = 0
        for speed in range(time):
            if speed * (time - speed) > distance:
                winners += 1
        winning_times.append(winners)

    return prod(winning_times)


def part_two():
    time = int("".join([str(x) for x in times]))
    distance = int("".join([str(x) for x in distances]))

    return sum([1 for speed in range(time)
                if speed * (time - speed) > distance])


def main():

    with open(args.filename, "r") as f:
        times.extend([int(x) for x in f.readline().split(":")[-1].split()])
        distances.extend([int(x) for x in f.readline().split(":")[-1].split()])
    
    print(f"Part 1: {part_one()}")
    print(f"Part 2: {part_two()}")


if __name__ == "__main__":
    main()
