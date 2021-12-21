#!/usr/bin/env python3
import argparse
import collections
import re


def part1(template, rules):
    """
    Template:     NNCB
    After step 1: NCNBCHB
    After step 2: NBCCNBBBCBHCB
    After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
    After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
    """
    maps = [(rf"(?=({pattern}))", c) for pattern, c in rules]

    def step(s):
        insertions = []
        for pattern, c in maps:
            for match in re.finditer(pattern, s):
                insertions.append((match.start(), c))
        offset = 1
        ret = list(s)
        for insertion_idx, insertion_char in sorted(insertions):
            ret.insert(insertion_idx + offset, insertion_char)
            offset += 1
        return "".join(ret)

    s = template
    for _ in range(10):
        s = step(s)
    commons = collections.Counter(s).most_common()
    return commons[0][1] - commons[-1][1]


def part2(template, rules):
    # Track pairs instead
    rule_maps = {pattern: (pattern[0] + c, c + pattern[1]) for pattern, c in rules}
    pairs = collections.Counter(["".join(p) for p in zip(template, template[1:])])

    def step(pairs):
        new_pairs = collections.Counter()
        for pair, count in pairs.items():
            if pair in rule_maps:
                left, right = rule_maps[pair]
                new_pairs[left] += count
                new_pairs[right] += count
        return new_pairs

    for _ in range(40):
        pairs = step(pairs)

    # Each pair counts instances of each initial character when summed
    char_count = collections.Counter()
    for pair, count in pairs.items():
        char_count[pair[0]] += count
    # ... except one count of the final character,
    # which luckily is the last character of the initial string
    char_count[template[-1]] += 1
    commons = char_count.most_common()
    return commons[0][1] - commons[-1][1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    template = None
    rules = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            if not template:
                template = line
            elif len(line) == 0:
                continue
            else:
                rules.append(line.split(" -> "))
    if args.part == 1:
        print(part1(template, rules))
    elif args.part == 2:
        print(part2(template, rules))
    else:
        print("illegal part")
