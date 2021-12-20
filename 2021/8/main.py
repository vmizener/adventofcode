#!/usr/bin/env python3
import argparse
import functools


def part1(lines):
    lengths = [2, 4, 3, 7]
    ret = 0
    for _, outputs in lines:
        for output in outputs:
            if len(output) in lengths:
                ret += 1
    return ret


def part2(lines):
    def filter_commons(*entries):
        commons = functools.reduce(
            lambda x, y: x & y, [set(entry) for entry in entries]
        )
        ret = set()
        for entry in entries:
            ret |= set(entry) - commons
        return ret

    def solve(inputs, outputs):
        # Segments of length 2
        one_set = set()
        # Segments of length 4
        four_set = set()
        # Segments of length 3
        seven_set = set()
        # Segments of length 7 are unneeded to solve
        # eight_set = set()
        # Segments of length 5
        two_three_five_set = set()
        # Segments of length 6
        zero_six_nine_set = set()
        for entry in inputs + outputs:
            if len(entry) == 2:
                one_set.add(entry)
            elif len(entry) == 4:
                four_set.add(entry)
            elif len(entry) == 3:
                seven_set.add(entry)
            # elif len(entry) == 7:
            #     eight_set.add(entry)
            elif len(entry) == 5:
                two_three_five_set.add(entry)
            elif len(entry) == 6:
                zero_six_nine_set.add(entry)

        # These have unique sets
        seven_fields = set(seven_set.pop())
        one_fields = set(one_set.pop())
        four_fields = set(four_set.pop())
        # 7-fields should have exactly one more than 1-fields, the top bar 'a'
        a = (seven_fields - one_fields).pop()
        # Uniques among zero_six_nine length entries must be 'c', 'd', and 'e'
        c_d_e = filter_commons(*zero_six_nine_set)
        # 4-fields minus 1-fields must be 'b' and 'd'
        b_d = four_fields - one_fields
        # Get 'b' from 'b_d'-'c_d_e'
        b = (b_d - c_d_e).pop()
        # 5-fields are the only set of length 5 that includes 'b'
        five_fields = [set(f) for f in two_three_five_set if b in f].pop()
        # 0-fields are the only set of length 6 that has 2 unique elements from 5-fields
        zero_fields = [
            set(f) for f in zero_six_nine_set if len(set(f) - five_fields) == 2
        ].pop()
        # 5-fields contain 'f' but not 'c', so we can subtract it from 1-fields to get 'c'
        c = (one_fields - five_fields).pop()
        # Similarly, 0-fields contain 'b' but not 'd', so we can subtract it from the b_d set to get 'd'
        d = (b_d - zero_fields).pop()
        # 1-fields are 'c' and 'f', and we know 'c', so we can get 'f'
        f = (one_fields - {c}).pop()
        # 5-fields now contain only one unknown, 'g', so we can find that too
        g = (five_fields - {a, b, d, f}).pop()
        # Similarly, 0-fields now have only 'e' as an unknown
        e = (zero_fields - {a, b, c, f, g}).pop()

        out_map = {
            a: "a",
            b: "b",
            c: "c",
            d: "d",
            e: "e",
            f: "f",
            g: "g",
        }
        segmap = {
            ("a", "b", "c", "e", "f", "g"): "0",
            ("c", "f"): "1",
            ("a", "c", "d", "e", "g"): "2",
            ("a", "c", "d", "f", "g"): "3",
            ("b", "c", "d", "f"): "4",
            ("a", "b", "d", "f", "g"): "5",
            ("a", "b", "d", "e", "f", "g"): "6",
            ("a", "c", "f"): "7",
            ("a", "b", "c", "d", "e", "f", "g"): "8",
            ("a", "b", "c", "d", "f", "g"): "9",
        }
        num = ""
        for output in outputs:
            mapped_output = []
            for c in output:
                mapped_output.append(out_map[c])
            mapped_output.sort()
            num += segmap[tuple(mapped_output)]
        return int(num)

    ret = 0
    for line in lines:
        num = solve(*line)
        print(num)
        ret += num

    print()
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            io = []
            left, right = line.split("|")
            io.append(left.strip().split(" "))
            io.append(right.strip().split(" "))
            lines.append(io)
    if args.part == 1:
        print(part1(lines))
    elif args.part == 2:
        print(part2(lines))
    else:
        print("illegal part")
