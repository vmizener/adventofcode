#!/usr/bin/env python3
import argparse


def fold(points, axis, val):
    ret = set()
    for x, y in points:
        if axis == "x" and x > val:
            ret.add((val - abs(val - x), y))
        elif axis == "y" and y > val:
            ret.add((x, val - abs(val - y)))
        else:
            ret.add((x, y))
    return ret


def part1(points: set[tuple[int, int]], folds: list[tuple[str, int]]):
    return len(fold(points, *folds[0]))


def part2(points: set[tuple[int, int]], folds: list[tuple[str, int]]):
    folded_points = points
    for axis, val in folds:
        folded_points = fold(folded_points, axis, val)

    max_x, max_y = max([p[0] for p in folded_points]), max(
        [p[1] for p in folded_points]
    )
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in folded_points:
        grid[y][x] = "█"
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    points = set()
    folds = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            elif "fold" in line:
                axis, val = line[11:].split("=")
                folds.append((axis, int(val)))
            else:
                x, y = line.split(",")
                points.add((int(x), int(y)))
    if args.part == 1:
        print(part1(points, folds))
    elif args.part == 2:
        print(part2(points, folds))
    else:
        print("illegal part")
