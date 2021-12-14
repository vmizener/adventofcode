#!/usr/bin/env python3
import argparse
import collections


def part1(lines):
    def get_points(start, end):
        ret = []
        x, y = start[0], start[1]
        if start[0] == end[0]:
            y_diff = end[1] - start[1]
            if y_diff > 0:
                for n in range(y_diff + 1):
                    ret.append((x, y + n))
            else:
                for n in range(0, y_diff - 1, -1):
                    ret.append((x, y + n))
        elif start[1] == end[1]:
            x_diff = end[0] - start[0]
            if x_diff > 0:
                for n in range(x_diff + 1):
                    ret.append((x + n, y))
            else:
                for n in range(0, x_diff - 1, -1):
                    ret.append((x + n, y))
        return ret

    c = collections.Counter()
    for start, end in lines:
        points = get_points(start, end)
        c += collections.Counter(points)

    return len([v for v in c.values() if v > 1])


def part2(lines):
    def get_points(start, end):
        ret = []
        x, y = start[0], start[1]
        if start[0] == end[0]:
            y_diff = end[1] - start[1]
            y_range = range(y_diff + 1) if y_diff > 0 else range(0, y_diff - 1, -1)
            for n in y_range:
                ret.append((x, y + n))
        elif start[1] == end[1]:
            x_diff = end[0] - start[0]
            x_range = range(x_diff + 1) if x_diff > 0 else range(0, x_diff - 1, -1)
            for n in x_range:
                ret.append((x + n, y))
        else:
            x_diff = end[0] - start[0]
            y_diff = end[1] - start[1]
            x_range = range(x_diff + 1) if x_diff > 0 else range(0, x_diff - 1, -1)
            y_range = range(y_diff + 1) if y_diff > 0 else range(0, y_diff - 1, -1)
            for nx, ny in zip(x_range, y_range):
                ret.append((x + nx, y + ny))

        return ret

    c = collections.Counter()
    for start, end in lines:
        points = get_points(start, end)
        c += collections.Counter(points)

    return len([v for v in c.values() if v > 1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            left, right = [
                [int(val) for val in s.split(",")] for s in line.split(" -> ")
            ]
            lines.append((left, right))
    if args.part == 1:
        print(part1(lines))
    elif args.part == 2:
        print(part2(lines))
    else:
        print("illegal part")
