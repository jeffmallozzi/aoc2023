import argparse
import logging

logger = logging.Logger(
    name=__name__
)
logging.basicConfig()

logger.level = logging.DEBUG

DAY = 1

parser = argparse.ArgumentParser(
    prog=f'Advent of Code 2023: day {DAY}',
    description='https://adventofcode.com/2023/day/1',
    epilog='Text at the bottom of help'
)
parser.add_argument('filename')

digit_map = {
    "one" : "1",
    "two" : "2",
    "three" : "3",
    "four" : "4",
    "five" : "5",
    "six" : "6",
    "seven" : "7",
    "eight" : "8",
    "nine" : "9"
}

digits = list(digit_map.keys()) + list(digit_map.values())

def left_digit(line):
    positions = {
        line.find(digit): digit 
        for digit in digits 
        if line.find(digit) >= 0
    }
    lowest = positions[min(positions.keys())]
    return lowest if lowest.isdecimal() else digit_map.get(lowest)

def right_digit(line):
    positions = {
        line.rfind(digit): digit 
        for digit in digits 
        if line.rfind(digit) >= 0
    }
    highest = positions[max(positions.keys())]
    return highest if highest.isdecimal() else digit_map.get(highest)


def part_one(f):
    resp = 0
    for line in f:
        digits = [i for i in line if i.isdecimal()]
        resp += int(digits[0]+digits[-1])
    return resp

def part_two(f):
    resp = 0
    for line in f:
        resp += int(left_digit(line) + right_digit(line))
    return resp

def main():
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        print(f"Part 1: {part_one(f)}")
        f.seek(0)
        print(f"Part 2: {part_two(f)}")

if __name__ == "__main__":
    main()