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

args = parser.parse_args()

log_level = max((0, Default_log_level - (args.verbose * 10)))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


def part_number(schimatic, number):
    for row in range(number["row"] - 1, number["row"] + 2):
        for col in range(number["col"] - 1, number["col"] + 1 + len(number["digits"])):
            logger.debug(f"Checking {row}, {col}")
            try:
                test_symbol = schimatic[row][col]
                logger.debug(f"Test Symbol: {test_symbol}")
            except IndexError:
                continue
            if not test_symbol.isdecimal() and test_symbol != ".":
                logger.debug(f"Found a part number {number}")
                return int("".join(number["digits"]))
    return 0


def gear_ratio(schimatic, col):
    numbers = []
    current_number = []

    for row in schimatic:
        for col_index, symbol in enumerate(row):
            if symbol.isdecimal():
                current_number.append(symbol)
            elif current_number:
                if col_index - (len(current_number) + 1) <= col <= col_index:
                    numbers.append(int("".join(current_number)))
                    if len(numbers) > 2:
                        return 0
                current_number.clear()
        if current_number:
            if len(row) - (len(current_number) + 2) < col < len(row):
                numbers.append(int("".join(current_number)))
                if len(numbers) > 2:
                    return 0

    if len(numbers) == 2:
        return numbers[0] * numbers[1]

    return 0


def part_one(schimatic):
    part_sum = 0

    for row_index, row in enumerate(schimatic):
        logger.debug(f"Row: {row_index}")
        number = {
            "digits": [],
            "row": row_index,
            "col": None,
        }
        for col_index, character in enumerate(row):
            logger.debug(f"Column: {col_index}")
            if character.isdecimal():
                number["digits"].append(character)
                number["col"] = col_index if not number["col"] else number["col"]
            else:
                if number["digits"]:
                    logger.debug(f"Number: {number}")
                    part_sum += part_number(schimatic, number)
                    number["digits"].clear()
                    number["col"] = None
        if number["digits"]:
            part_sum += part_number(schimatic, number)

    return part_sum


def part_two(schimatic):
    gear_sum = 0

    for row_index, row in enumerate(schimatic):
        for col_index, symbol in enumerate(row):
            if symbol == "*":
                gear_sum += gear_ratio(
                    schimatic[row_index - 1 : row_index + 2], col_index
                )

    return gear_sum


def main():
    with open(args.filename, "r") as f:
        schimatic = []
        for line in f:
            schimatic.append(list(line.strip()))

    logger.debug(schimatic)

    print(f"Part 1: {part_one(schimatic)}")
    print(f"Part 2: {part_two(schimatic)}")


if __name__ == "__main__":
    main()
