#!/usr/bin/env python3
import argparse


def part1(lines):
    pos = 0
    depth = 0
    for cmd, val in lines:
        if cmd == "forward":
            pos += val
        elif cmd == "down":
            depth += val
        elif cmd == "up":
            depth -= val
    return pos * depth


def part2(lines):
    pos = 0
    depth = 0
    aim = 0
    for cmd, val in lines:
        if cmd == "forward":
            pos += val
            depth += val * aim
        elif cmd == "down":
            aim += val
        elif cmd == "up":
            aim -= val
    return pos * depth


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            cmd, val = line.strip().split(" ")
            lines.append((cmd, int(val)))

    if args.part == 1:
        print(part1(lines))
    elif args.part == 2:
        print(part2(lines))
    else:
        print("illegal part")
