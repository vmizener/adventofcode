#!/usr/bin/env python3
import argparse


def step(grid):
    flash_set = set()
    new = []
    for i, row in enumerate(grid):
        new_row = []
        for j, c in enumerate(row):
            if c == 9:
                flash_set.add((i, j))
                new_row.append(0)
            else:
                new_row.append(c + 1)
        new.append(new_row)

    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    n = len(grid)
    flashes = len(flash_set)
    seen = set()
    while len(flash_set) > 0:
        x, y = flash_set.pop()
        for dir_x, dir_y in directions:
            adj_x, adj_y = x + dir_x, y + dir_y
            if not ((0 <= adj_x < n) and (0 <= adj_y < n)):
                continue
            if (adj_x, adj_y) in seen:
                continue
            adj_val = new[adj_x][adj_y]
            if adj_val == 0:
                continue
            if adj_val == 9:
                flash_set.add((adj_x, adj_y))
                new[adj_x][adj_y] = 0
                flashes += 1
            else:
                new[adj_x][adj_y] = adj_val + 1
        seen.add((x, y))

    return new, flashes


def part1(grid):
    net_flashes = 0
    for _ in range(100):
        grid, flashes = step(grid)
        net_flashes += flashes
    return net_flashes


def part2(grid):
    n = 1
    while True:
        grid, flashes = step(grid)
        if flashes == 100:
            break
        n += 1
    return n


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    grid = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            grid.append([int(c) for c in line.strip()])
    if args.part == 1:
        print(part1(grid))
    elif args.part == 2:
        print(part2(grid))
    else:
        print("illegal part")
