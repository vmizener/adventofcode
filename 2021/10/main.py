#!/usr/bin/env python3
import argparse


def part1(lines):
    score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    ret = 0
    for line in lines:
        stack = []
        for c in line:
            if c in "([{<":
                stack.append(c)
            elif len(stack) == 0 or pairs[c] != stack[-1]:
                ret += score[c]
                break
            else:
                stack.pop()
    return ret


def part2(lines):
    in_pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }
    out_pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    incomplete_stacks = []
    for line in lines:
        stack = []
        for c in line:
            if c in "([{<":
                stack.append(c)
            elif len(stack) == 0 or out_pairs[c] != stack[-1]:
                break
            else:
                stack.pop()
        else:
            incomplete_stacks.append(stack)

    multiplier = 5
    score_table = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }
    scores = []
    for incomplete_stack in incomplete_stacks:
        score = 0
        for c in reversed(incomplete_stack):
            score *= multiplier
            score += score_table[c]
        scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]


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
