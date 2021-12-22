#!/usr/bin/env python3
import argparse
import re
import math


def sim(min_x, max_x, min_y, max_y, vx, vy):
    best_y = float("-inf")
    cur_x, cur_y = 0, 0
    while cur_y >= min_y and cur_x <= max_x:
        best_y = max(best_y, cur_y)
        if (min_x <= cur_x <= max_x) and (min_y <= cur_y <= max_y):
            return best_y
        if vx == 0 and not (min_x <= cur_x <= max_x):
            break
        cur_x += vx
        cur_y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return None


def part1(min_x, max_x, min_y, max_y):

    # Needs at least x steps for sqrt(x) to reach min_x, but x will be zero by then
    vx_min = int(math.sqrt(min_x))
    # Single step into max bound
    vx_max = max_x
    # If min_y>0, y must be >=min_y otherwise will never reach
    # If min_y<0, y again must be >=min_y otherwise will overshoot
    vy_min = min_y
    # If min_y>0, y-position will mirror on way up vs way down
    #   To ensure no overshoot on the way down, want the initial y-position to be at min_y (which is furthest possible)
    # If min_y<0, vy on way down will be -min_y when back to 0-position, which will barely overshoot
    #   This makes it a good max speed as larger will overshoot further
    vy_max = abs(min_y)

    best = float("-inf")
    for vx in range(vx_min, vx_max + 1):
        for vy in range(vy_min, vy_max + 1):
            s = sim(min_x, max_x, min_y, max_y, vx, vy)
            if s is None:
                continue
            best = max(best, s)
    return best


def part2(min_x, max_x, min_y, max_y):
    count = 0
    for vx in range(int(math.sqrt(min_x)), max_x + 1):
        for vy in range(min_y, abs(min_y) + 1):
            if sim(min_x, max_x, min_y, max_y, vx, vy) is None:
                continue
            count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    template = None
    tgt_x_range = []
    tgt_y_range = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            tgt_x_range = [
                int(group)
                for group in re.search(r"x=([-0-9]+)..([-0-9]+)", line).groups()
            ]
            tgt_y_range = [
                int(group)
                for group in re.search(r"y=([-0-9]+)..([-0-9]+)", line).groups()
            ]
    if args.part == 1:
        print(part1(*tgt_x_range, *tgt_y_range))
    elif args.part == 2:
        print(part2(*tgt_x_range, *tgt_y_range))
    else:
        print("illegal part")
