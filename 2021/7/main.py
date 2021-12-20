#!/usr/bin/env python3
import argparse


def part1(nums):
    def dist(nums, p):
        ret = 0
        for num in nums:
            ret += abs(num - p)
        return ret

    best = float("inf"), None
    for i in range(min(nums), max(nums)):
        best = min(best, (dist(nums, i), i), key=lambda x: x[0])
    return best


def part2(nums):
    def dist(nums, p):
        ret = 0
        for num in nums:
            n = abs(num - p)
            ret += n * (n + 1) // 2
        return ret

    best = float("inf"), None
    for i in range(min(nums), max(nums)):
        best = min(best, (dist(nums, i), i), key=lambda x: x[0])
    return best


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    start = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            for val in line.split(","):
                start.append(int(val))
    if args.part == 1:
        print(part1(start))
    elif args.part == 2:
        print(part2(start))
    else:
        print("illegal part")
