#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re


class MapState:
    def __init__(self, hall, c1, c2, c3, c4):
        self.positions = hall + c1 + c2 + c3 + c4

    @property
    def hall(self):
        return self.positions[:11]

    @property
    def c1(self):
        return self.positions[11:13]

    @property
    def c2(self):
        return self.positions[13:15]

    @property
    def c3(self):
        return self.positions[15:17]

    @property
    def c4(self):
        return self.positions[17:19]

    def __str__(self):
        return "\n".join(
            [
                "#############",
                f"#{''.join(self.hall)}#",
                f"###{self.c1[0]}#{self.c2[0]}#{self.c3[0]}#{self.c4[0]}###",
                f"  #{self.c1[1]}#{self.c2[1]}#{self.c3[1]}#{self.c4[1]}#",
                "  #########",
            ]
        )

    def get_mobile_amphipods(self):
        ret = []
        for idx, value in enumerate(self.positions):
            if value == ".":
                continue
            if idx > 10:
                if (idx % 2) > 0 or self.positions[idx - 1] == ".":
                    ret.append((idx, value))
                continue
            ret.append((idx, value))
        return ret

    def check_amphipod_path(self, pos):
        amphipod = self.positions[pos]
        if amphipod == ".":
            return []
        if pos in [11, 12]:
            hallway_idx = 2
        elif pos in [13, 14]:
            hallway_idx = 4
        elif pos in [15, 16]:
            hallway_idx = 6
        elif pos in [17, 18]:
            hallway_idx = 8
        else:
            hallway_idx = pos
        # Get legal hallway end positions
        open = set()
        for plus_idx in range(hallway_idx + 1, 11):
            if plus_idx in [2, 4, 6, 8]:
                continue
            elif self.positions[plus_idx] == ".":
                open.add(plus_idx)
            else:
                break
        for neg_idx in range(hallway_idx - 1, -1, -1):
            if neg_idx in [2, 4, 6, 8]:
                continue
            elif self.positions[neg_idx] == ".":
                open.add(neg_idx)
            else:
                break
        # Get legal room positions
        if amphipod == "A":
            if self.positions[11] == ".":
                open.add(11)
            if self.positions[12] == ".":
                open.add(12)

    def get_neighbors(self):
        for idx, value in self.get_mobile_amphipods():
            pass

        pass


def part1(hall, c1, c2, c3, c4):
    ms = MapState(hall, c1, c2, c3, c4)
    print(ms.get_mobile_amphipods())
    import pdb

    pdb.set_trace()
    print(ms.check_amphipod_path(11))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    hall = list("...........")
    with open(args.input_file) as fh:
        rows = []
        for line in fh.readlines():
            line = line.strip()
            if match := re.search(r"(\w)#(\w)#(\w)#(\w)", line):
                rows.append(match.groups())
    c1, c2, c3, c4 = zip(*rows)
    if args.part == 1:
        print(part1(hall, list(c1), list(c2), list(c3), list(c4)))
    elif args.part == 2:
        print(part2(hall, list(c1), list(c2), list(c3), list(c4)))
    else:
        print("illegal part")
