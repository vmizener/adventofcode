#!/usr/bin/env python3
import argparse


def part1(depths):
    ret = 0
    for i, val in enumerate(depths[1:]):
        if depths[i] < val:
            ret += 1
    return ret


def part2(depths):
    sums = []
    for i in range(3, len(depths) + 1):
        sums.append(sum(depths[i - 3 : i]))
    return part1(sums)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    depths = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            depths.append(int(line.strip()))

    if args.part == 1:
        print(part1(depths))
    elif args.part == 2:
        print(part2(depths))
    else:
        print("illegal part")
