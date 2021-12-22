#!/usr/bin/env python3
from __future__ import annotations
import pdb


import argparse
import json

from typing import Optional, Union


class Pair:
    def __init__(
        self,
        left: Union[int, list],
        right: Union[int, list],
        *,
        depth: int = 0,
        parent: Optional[Pair] = None,
        side: Optional[str] = "root",
    ):
        if isinstance(left, int):
            self.left = Num(left, depth=depth + 1, parent=self, side="left")
        else:
            self.left = Pair(*left, depth=depth + 1, parent=self, side="left")
        if isinstance(right, int):
            self.right = Num(right, depth=depth + 1, parent=self, side="right")
        else:
            self.right = Pair(*right, depth=depth + 1, parent=self, side="right")
        self.depth = depth
        self.parent = parent
        self.side = side

    @property
    def value(self):
        return [self.left, self.right]

    @property
    def magnitude(self):
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def __str__(self):
        return "[" + ",".join([str(val) for val in self.value]) + "]"

    def __iter__(self):
        yield self.left
        yield self.right

    def explode(self):
        if self.depth > 3:
            # Explode
            if self.side == "root" or self.parent is None:
                # Invalid case
                raise RuntimeError("invalid construction")
            if self.side == "left":
                self.parent.right.add_left(self.right.value)
                self.parent.__bubble_left(self.left.value)
                self.parent.__clear_left()
            elif self.side == "right":
                self.parent.left.add_right(self.left.value)
                self.parent.__bubble_right(self.right.value)
                self.parent.__clear_right()
            return True
        if isinstance(self.left, Pair) and self.left.explode():
            return True
        if isinstance(self.right, Pair) and self.right.explode():
            return True
        return False

    def split(self):
        if isinstance(self.left, Pair) and self.left.split():
            return True
        if isinstance(self.right, Pair) and self.right.split():
            return True
        return False

    def add_left(self, val):
        self.left.add_left(val)

    def add_right(self, val):
        self.right.add_right(val)

    def __bubble_left(self, val):
        if self.parent is None:
            return
        if self.side == "left":
            self.parent.__bubble_left(val)
        if self.side == "right":
            self.parent.left.add_right(val)
        return

    def __bubble_right(self, val):
        if self.parent is None:
            return
        if self.side == "left":
            self.parent.right.add_left(val)
        if self.side == "right":
            self.parent.__bubble_right(val)
        return

    def __clear_left(self):
        self.left = Num(0, depth=self.depth + 1, parent=self, side="left")

    def __clear_right(self):
        self.right = Num(0, depth=self.depth + 1, parent=self, side="right")


class Num(Pair):
    def __init__(
        self,
        value: int,
        *,
        depth: int = 0,
        parent: Optional[Pair] = None,
        side: Optional[str] = "root",
    ):
        self.__value = value
        self.depth = depth
        self.parent = parent
        self.side = side

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def magnitude(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def explode(self):
        return False

    def split(self):
        if self.value > 9:
            # Split
            if self.parent is None:
                raise RuntimeError()
            left, r = divmod(self.value, 2)
            right = left + r
            if self.side == "left":
                self.parent.left = Pair(
                    left, right, depth=self.depth, parent=self.parent, side=self.side
                )
            elif self.side == "right":
                self.parent.right = Pair(
                    left, right, depth=self.depth, parent=self.parent, side=self.side
                )
            return True
        return False

    def add_left(self, val):
        self.__value += val

    def add_right(self, val):
        self.__value += val


def part1(*lines):
    joint = lines[0]
    p = None
    for line in lines[1:]:
        joint = [joint, line]
        p = Pair(*joint)
        while True:
            if p.explode():
                continue
            if p.split():
                continue
            break
        joint = json.loads(str(p))
    print(str(p))
    if p is None:
        return 0
    return p.magnitude


def part2(*lines):
    best = 0
    n = len(lines)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            p = Pair(lines[i], lines[j])
            while True:
                if p.explode():
                    continue
                if p.split():
                    continue
                break
            best = max(p.magnitude, best)
    return best


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            lines.append(json.loads(line.strip()))
    if args.part == 1:
        print(part1(*lines))
    elif args.part == 2:
        print(part2(*lines))
    else:
        print("illegal part")
