#!/usr/bin/env python3
import argparse
import math


def get_risk(grid):
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]
    risk = 0
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            for direction in directions:
                try:
                    check_x, check_y = [sum(tup) for tup in zip((x, y), direction)]
                    if check_x < 0 or check_y < 0:
                        continue
                    if grid[check_y][check_x] <= val:
                        break
                except IndexError:
                    continue
            else:
                risk += val + 1
    return risk


def get_basins(grid):
    seen = set()
    basins = []

    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]

    def explore(x, y, basin):
        if (x, y) in seen:
            return
        seen.add((x, y))
        basin.add((x, y))
        for direction in directions:
            try:
                check_x, check_y = [sum(tup) for tup in zip((x, y), direction)]
                if check_x < 0 or check_y < 0:
                    continue
                if grid[check_y][check_x] != 9:
                    explore(check_x, check_y, basin)
            except IndexError:
                continue

    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if (x, y) in seen:
                continue
            if val == 9:
                continue
            basin = set()
            explore(x, y, basin)
            basins.append(basin)
    basins.sort(key=lambda x: len(x))
    return math.prod([len(basin) for basin in basins[-3:]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "part", type=int, help="Which part to run.  1: get_risk.  2: get_basins"
    )
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    grid = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            grid.append([int(el) for el in line.strip()])

    if args.part == 1:
        print(get_risk(grid))
    elif args.part == 2:
        print(get_basins(grid))
    else:
        print("illegal part")
