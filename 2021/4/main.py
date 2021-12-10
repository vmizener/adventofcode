#!/usr/bin/env python3
import argparse
import functools
import re


def part1(nums, boards):
    board_maps = []
    for board in boards:
        board_maps.append(
            [set(row) for row in board] + [set(col) for col in zip(*board)]
        )
    for num in nums:
        for board_map in board_maps:
            done = False
            for board_set in board_map:
                if num in board_set:
                    board_set.remove(num)
                if len(board_set) == 0:
                    done = True
            if done:
                joint_set = functools.reduce(lambda s1, s2: s1 | s2, board_map)
                return num * sum(joint_set)


def part2(nums, boards):
    board_maps = {}
    for idx, board in enumerate(boards):
        board_maps[idx] = [set(row) for row in board] + [
            set(col) for col in zip(*board)
        ]
    score_maps = {}
    counter = 1
    for num in nums:
        to_remove = []
        for idx, board_map in board_maps.items():
            done = False
            for board_set in board_map:
                if num in board_set:
                    board_set.remove(num)
                if len(board_set) == 0:
                    done = True
            if done:
                joint_set = functools.reduce(lambda s1, s2: s1 | s2, board_map)
                score_maps[idx] = num * sum(joint_set), counter
                counter += 1
                to_remove.append(idx)
        for idx in to_remove:
            del board_maps[idx]
        if len(board_maps) == 0:
            break
    return sorted(score_maps.values(), key=lambda x: x[-1])[-1][0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    boards = []
    lines = []
    with open(args.input_file) as fh:
        nums = None
        cur_board = []
        for line in fh.readlines():
            line = line.strip()
            if len(line) == 0:
                if cur_board:
                    boards.append(cur_board)
                    cur_board = []
            elif not nums:
                nums = [int(num) for num in line.split(",")]
            else:
                cur_board.append([int(num) for num in re.split(r"\s+", line)])

    if args.part == 1:
        print(part1(nums, boards))
    elif args.part == 2:
        print(part2(nums, boards))
    else:
        print("illegal part")
