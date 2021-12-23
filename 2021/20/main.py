#!/usr/bin/env python3
import argparse
import collections
import pdb


def dump_map(map, field):
    print(f"(field: {field})")
    for row in map:
        print(row)
    print("\n%%%%%%\n")


def count_lit(map):
    c = collections.Counter()
    for row in map:
        c += collections.Counter(row)
    return c["#"]


def translate(alg, s):
    s = s.replace(".", "0").replace("#", "1")
    return alg[int(s, base=2)]


def map_get(map, x, y, field="."):
    m, n = len(map), len(map[0])
    if x < 0 or x >= m or y < 0 or y >= n:
        return field
    return map[y][x]


def enhance(alg, map, field):
    if field == "." and alg[0] == "#":
        new_field = "#"
    elif field == "#" and alg[511] == ".":
        new_field = "."
    else:
        new_field = field
    new_map = []
    n, m = len(map), len(map[0])
    for y in range(-1, n + 1, 1):
        new_row = ""
        for x in range(-1, m + 1, 1):
            s = ""
            for y_offset in [-1, 0, 1]:
                for x_offset in [-1, 0, 1]:
                    s += map_get(map, x + x_offset, y + y_offset, field=field)
            new_row += translate(alg, s)
        new_map.append(new_row)

    return new_map, new_field


def part1(alg, map, steps=2):
    field = "."
    for _ in range(steps):
        map, field = enhance(alg, map, field)
    dump_map(map, field)

    return count_lit(map)


def part2(alg, map):
    return part1(alg, map, steps=50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    alg = None
    map = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            if alg is None:
                alg = line
            elif len(line) != 0:
                map.append(line)
    if args.part == 1:
        print(part1(alg, map))
    elif args.part == 2:
        print(part2(alg, map))
    elif args.part == 3:
        pdb.set_trace()
    else:
        print("illegal part")
