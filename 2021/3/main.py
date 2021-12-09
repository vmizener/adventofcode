#!/usr/bin/env python3
import argparse
import collections
import operator


def part1(lines):
    cols = zip(*lines)
    gamma_rate = ""
    epsilon_rate = ""
    for col in cols:
        counter = collections.Counter(col)
        (gamma, _), (epsilon, _) = counter.most_common()
        gamma_rate += str(gamma)
        epsilon_rate += str(epsilon)
    return int(gamma_rate, base=2) * int(epsilon_rate, base=2)


def part2(lines):
    def loop(lines, pos, check):
        if len(lines) == 1:
            return lines
        cols = list(zip(*lines))
        critical_column = cols[pos]
        counter = collections.Counter(critical_column).most_common()
        (most_key, most_cnt), (least_key, least_cnt) = counter
        key = None
        if check == "o2":
            if most_cnt == least_cnt:
                key = "1"
            else:
                key = most_key
        elif check == "co2":
            if most_cnt == least_cnt:
                key = "0"
            else:
                key = least_key
        new_lines = operator.itemgetter(
            *[idx for idx, val in enumerate(critical_column) if val == key]
        )(lines)
        if isinstance(new_lines, str):
            return new_lines
        return loop(
            new_lines,
            pos=pos + 1,
            check=check,
        )

    o2_rating = int(loop(lines, 0, "o2"), base=2)
    co2_rating = int(loop(lines, 0, "co2"), base=2)
    return o2_rating * co2_rating


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            lines.append(line.strip())

    if args.part == 1:
        print(part1(lines))
    elif args.part == 2:
        print(part2(lines))
    else:
        print("illegal part")
