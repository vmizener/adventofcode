#!/usr/bin/env python3
import argparse
import operator
import math


def expand_hex(s):
    ret = bin(int(s, base=16))[2:]
    offset = (4 - (len(ret) % 4)) % 4
    return "0" * offset + ret


class Packet:
    def __init__(self, s):
        self.version = int(s[0:3], base=2)
        self.type_id = int(s[3:6], base=2)
        self.content = []
        if self.is_literal:
            idx = 6
            bin_lit = ""
            while True:
                group_tag = s[idx]
                bin_lit += s[idx + 1 : idx + 5]
                if group_tag == "0":
                    break
                idx += 5
            self.content.append(int(bin_lit, base=2))
            self.terminal_idx = idx + 5
        else:
            length_type = s[6]
            if length_type == "0":
                # Next 15 bits are total subpacket length
                subpacket_length = int(s[7:22], base=2)
                substring = s[22 : 22 + subpacket_length]
                idx = 0
                while idx < subpacket_length:
                    subpacket = Packet(substring[idx:])
                    idx += subpacket.terminal_idx
                    self.content.append(subpacket)
                self.terminal_idx = 22 + idx
            else:
                # Next 11 bits are the number of subpackets
                subpacket_count = int(s[7:18], base=2)
                substring = s[18:]
                idx = 0
                for _ in range(subpacket_count):
                    subpacket = Packet(substring[idx:])
                    idx += subpacket.terminal_idx
                    self.content.append(subpacket)
                self.terminal_idx = 18 + idx
        self.raw = s[: self.terminal_idx]

    @property
    def is_literal(self):
        return self.type_id == 4

    @property
    def type_str(self):
        return {
            0: "SUM",
            1: "PRD",
            2: "MIN",
            3: "MAX",
            4: "LIT",
            5: "GT",
            6: "LT",
            7: "EQ",
        }[self.type_id]

    @property
    def operator(self):
        return {
            0: lambda *x: sum(x),
            1: lambda *x: math.prod(x),
            2: lambda *x: min(x),
            3: lambda *x: max(x),
            4: lambda x: x,
            5: operator.gt,
            6: operator.lt,
            7: operator.eq,
        }[self.type_id]

    def __str__(self):
        count = len(self.content)
        count_str = f"({count})" if count > 1 else ""
        content = f"[{','.join([str(c) for c in self.content])}]"
        return f"{self.type_str}v{self.version}:{count_str}{content}"

    def sum_version(self):
        ret = self.version
        for subcontent in self.content:
            if isinstance(subcontent, Packet):
                ret += subcontent.sum_version()
        return ret

    def value(self):
        content = []
        for subcontent in self.content:
            if isinstance(subcontent, Packet):
                content.append(subcontent.value())
            else:
                content.append(subcontent)
        return self.operator(*content)


def part1(lines):
    for line in lines:
        print("#######")
        print(line)
        p = Packet(expand_hex(line))
        print(p)
        print(p.sum_version())


def part2(lines):
    for line in lines:
        print("#######")
        print(line)
        p = Packet(expand_hex(line))
        print(p)
        print(p.value())


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
        part1(lines)
    elif args.part == 2:
        part2(lines)
    else:
        print("illegal part")
