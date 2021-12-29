#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re


def part1(lines):
    def strip_lines(lines):
        stripped_lines = []
        for instruction, x1, x2, y1, y2, z1, z2 in lines:
            stripped_line = [instruction, x1, x2, y1, y2, z1, z2]
            discard = False
            for idx, val in enumerate(stripped_line):
                if idx == 0:
                    continue
                if idx % 2 == 1:
                    if val > 50:
                        discard = True
                        break
                    if val < -50:
                        stripped_line[idx] = -50
                elif idx % 2 == 0:
                    if val < -50:
                        discard = True
                        break
                    if val > 50:
                        stripped_line[idx] = 50
            if not discard:
                stripped_lines.append(stripped_line)
        return stripped_lines

    s = set()
    for instruction, x1, x2, y1, y2, z1, z2 in strip_lines(lines):
        for x in range(x1, x2 + 1):
            if x < -50 or x > 50:
                continue
            for y in range(y1, y2 + 1):
                if y < -50 or y > 50:
                    continue
                for z in range(z1, z2 + 1):
                    if z < -50 or z > 50:
                        continue
                    coord = (x, y, z)
                    if instruction == "on":
                        s.add(coord)
                    elif coord in s:
                        s.remove(coord)
    return len(s)


def part2(lines):
    class Cuboid:
        def __init__(self, is_on, x1, x2, y1, y2, z1, z2):
            self.is_on = is_on
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2
            self.z1 = z1
            self.z2 = z2

        def __str__(self):
            return f"<{'on' if self.is_on else 'off'} x={self.x1},{self.x2} y={self.y1},{self.y2} z={self.z1},{self.z2}>"

        def __repr__(self):
            return str(self)

        def __hash__(self):
            return hash((self.x1, self.x2, self.y1, self.y2, self.z1, self.z2))

        def is_empty(self):
            return self.x1 > self.x2 or self.y1 > self.y2 or self.z1 > self.z2

        def count(self):
            return (
                (1 + self.x2 - self.x1)
                * (1 + self.y2 - self.y1)
                * (1 + self.z2 - self.z1)
            )

        def overlaps(self, c: Cuboid):
            if (
                self.x1 > c.x2
                or self.x2 < c.x1
                or self.y1 > c.y2
                or self.y2 < c.y1
                or self.z1 > c.z2
                or self.z2 < c.z1
            ):
                return False
            return True

    def subtract(c: Cuboid, d: Cuboid):
        if not c.overlaps(d):
            return set([c])
        i = Cuboid(
            c.is_on,
            max(c.x1, d.x1),
            min(c.x2, d.x2),
            max(c.y1, d.y1),
            min(c.y2, d.y2),
            max(c.z1, d.z1),
            min(c.z2, d.z2),
        )
        new = [
            Cuboid(c.is_on, *coords)
            for coords in [
                (c.x1, c.x2, c.y1, c.y2, i.z2 + 1, c.z2),  # Top face
                (c.x1, c.x2, c.y1, c.y2, c.z1, i.z1 - 1),  # Bottom face
                (i.x2 + 1, c.x2, i.y1, i.y2, i.z1, i.z2),  # Right face
                (c.x1, i.x1 - 1, i.y1, i.y2, i.z1, i.z2),  # Left face
                (c.x1, c.x2, c.y1, i.y1 - 1, i.z1, i.z2),  # Front face
                (c.x1, c.x2, i.y2 + 1, c.y2, i.z1, i.z2),  # Back face
            ]
        ]
        ret = set()
        hashes = set()
        for cuboid in new:
            h = hash(cuboid)
            if cuboid.is_empty() or h in hashes:
                continue
            ret.add(cuboid)
            hashes.add(h)
        return ret

    cuboids = set()
    for line in lines:
        instruction, coords = line[0], line[1:]
        entry = Cuboid(instruction == "on", *coords)
        field = set()
        for cuboid in cuboids:
            slices = subtract(cuboid, entry)
            field |= slices
        if entry.is_on:
            field.add(entry)
        cuboids = field

    return sum([cuboid.count() for cuboid in cuboids])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            instruction, cuboid = line.split(" ")
            x, y, z = cuboid.split(",")
            line = [instruction]
            for dim in [x, y, z]:
                if match := re.search(r"=([-0-9]+)..([-0-9]+)", dim):
                    line.extend([int(el) for el in match.groups()])
            lines.append(line)
    if args.part == 1:
        print(part1(lines))
    elif args.part == 2:
        print(part2(lines))
    else:
        print("illegal part")
