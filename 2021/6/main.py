#!/usr/bin/env python3
import argparse


def part1(fish_list, days=80):
    prev_list = fish_list
    next_list = []
    while days > 0:
        new = 0
        for fish in prev_list:
            if fish == 0:
                next_list.append(6)
                new += 1
            else:
                next_list.append(fish - 1)
        next_list.extend([8] * new)
        days -= 1
        prev_list, next_list = next_list, []
    return len(prev_list)


# 00 -5 | 6
# 01 -4 | 5
# 02 -3 | 4
# 03 -2 | 3
# 04 -1 | 2
# 05 00 | 1
# 06 01 | 0
# 07 02 | 68
# 08 03 | 57
# 09 04 | 46
# 10 05 | 35
# 11 06 | 24
# 12 07 | 13
# 13 08 | 02
# 14 09 | 618
# 15 10 | 507
# 16 11 | 4668
# 17 12 | 3557
# 18 13 | 2446
# 19 14 | 1335
# 20 15 | 0224
# 21 16 | 61138
# 22 17 | 50027
# 23 18 | 4661688


def part2(fish_list, days=256):
    d = {}

    def count_descendents(days):
        if days in d:
            return d[days]
        if days < 7:
            return 0
        num_children = days // 7
        ret = num_children
        for i in range(num_children):
            ret += count_descendents(days - 2 - 7 * (i + 1))
        d[days] = ret
        return ret

    ret = 0
    for f in fish_list:
        ret += 1 + count_descendents(days + 6 - f)
    return ret


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
