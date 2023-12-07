import argparse
import logging
from itertools import islice

Default_log_level = logging.WARNING

DAY = 5

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

seeds = []
maps = {}


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def get_from_map(item, map):
    for row in map:
        if row[1] <= item <= (row[1] + row[2]):
            logger.debug(f"{item=} {row=}")
            return row[0] + (item - row[1])

    return item


def get_ranges_from_map(ranges, map):
    result = []

    for item_range in ranges:
        item_start = item_range[0]
        item_end = item_start + (item_range[1] - 1)
        logger.debug(f"Loop {item_range=}")
        for row in map:
            logger.debug(row)
            source_start = row[1]
            source_end = row[1] + (row[2] - 1)
            dest_start = row[0]
            dest_end = row[0] + (row[2] - 1)
            if source_start <= item_start <= item_end <= source_end:
                logger.debug(f"Items fully within: {row=} {item_range=}")
                result.append((dest_start + (item_start - source_start), item_range[1]))

                break
            elif item_start < source_start <= source_end < item_end:
                logger.debug(f"Items fully overlap: {row=} {item_range=}")
                result.append((dest_start, row[2]))
                result.extend(
                    get_ranges_from_map(
                        [
                            (item_start, source_start - item_start),
                            (source_end + 1, item_end - source_end),
                        ],
                        map,
                    )
                )
                break
            elif item_start < source_start <= item_end <= source_end:
                logger.debug(f"Items overlap left: {row=} {item_range=}")
                result.append((dest_start, item_end - (source_start - 1)))
                result.extend(
                    get_ranges_from_map([(item_start, source_start - item_start)], map)
                )
                break
            elif source_start <= item_start < source_end < item_end:
                logger.debug(f"Items overlap right: {row=} {item_range=}")
                result.append(
                    (dest_start + (item_start - source_start), source_end - item_start)
                )
                result.extend(
                    get_ranges_from_map([(source_end + 1, item_end - source_end)], map)
                )
                break
        else:
            result.append(item_range)

    return result


def part_one():
    locations = []

    for seed in seeds:
        logger.debug(f"{seed=}")
        soil = get_from_map(seed, maps["seed-to-soil map"])
        logger.debug(f"{soil=}")
        fertilizer = get_from_map(soil, maps["soil-to-fertilizer map"])
        logger.debug(f"{fertilizer=}")
        water = get_from_map(fertilizer, maps["fertilizer-to-water map"])
        logger.debug(f"{water=}")
        light = get_from_map(water, maps["water-to-light map"])
        logger.debug(f"{light=}")
        temp = get_from_map(light, maps["light-to-temperature map"])
        logger.debug(f"{temp=}")
        humidity = get_from_map(temp, maps["temperature-to-humidity map"])
        logger.debug(f"{humidity=}")
        location = get_from_map(humidity, maps["humidity-to-location map"])
        logger.debug(f"{location=}")
        locations.append(location)

    logger.debug(f"{locations=}")
    return min(locations)


def part_two():
    seed_ranges = list(batched(seeds, 2))
    logger.debug(f"{seed_ranges=}")
    soil = get_ranges_from_map(seed_ranges, maps["seed-to-soil map"])
    logger.debug(f"{soil=}")
    fertilizer = get_ranges_from_map(soil, maps["soil-to-fertilizer map"])
    logger.debug(f"{fertilizer=}")
    water = get_ranges_from_map(fertilizer, maps["fertilizer-to-water map"])
    logger.debug(f"{water=}")
    light = get_ranges_from_map(water, maps["water-to-light map"])
    logger.debug(f"{light=}")
    temp = get_ranges_from_map(light, maps["light-to-temperature map"])
    logger.debug(f"{temp=}")
    humidity = get_ranges_from_map(temp, maps["temperature-to-humidity map"])
    logger.debug(f"{humidity=}")
    locations = get_ranges_from_map(humidity, maps["humidity-to-location map"])
    logger.debug(f"{locations=}")

    return min([x[0] for x in locations])


def main():
    with open(args.filename, "r") as f:
        seeds.extend(int(x) for x in f.readline().split(":")[-1].split())
        logger.debug(seeds)
        f.readline()

        for line in f:
            if line == "\n":
                continue
            if ":" in line:
                current_map = line.split(":")[0]
                logger.debug(current_map)
                maps[current_map] = []
            else:
                maps[current_map].append([int(x) for x in line.split()])

    logger.debug(maps)
    print(f"Part 1: {part_one()}")
    print(f"Part 2: {part_two()}")


if __name__ == "__main__":
    main()
