#!/usr/bin/env python3
from __future__ import annotations
from pprint import pprint
import argparse
import collections


class Node:
    def __init__(self, name: str):
        self.name = name
        self.is_big = name == name.upper()
        self.is_terminal = name in ["start", "end"]
        self.connections = set()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"{self.name}:{sorted([n.name for n in self.neighbors])}"

    def __repr__(self):
        return str(self)

    @property
    def neighbors(self):
        return iter(self.connections)

    def add(self, node: Node):
        self.connections.add(node)


class Route:
    def __init__(self, *nodes: Node, has_second_visit=False):
        self.order = list(nodes)
        self.members = set(nodes)
        self.has_second_visit = has_second_visit
        self.end = nodes[-1]

    def __str__(self):
        return ",".join([n.name for n in self.order])

    def __repr__(self):
        return str(self)

    def __lt__(self, other: Route):
        return str(self) < str(other)

    def add(self, node: Node):
        return Route(*list(self.order) + [node], has_second_visit=self.has_second_visit)


def make_grid(lines):
    node_map = {}
    for line in lines:
        left, right = line.strip().split("-")
        if left not in node_map:
            node_map[left] = Node(left)
        left = node_map[left]
        if right not in node_map:
            node_map[right] = Node(right)
        right = node_map[right]
        left.add(right)
        right.add(left)
    return node_map


def part1(lines):
    node_map = make_grid(lines)

    complete_routes = set()
    stack = [Route(node_map["start"])]

    while len(stack) > 0:
        route = stack.pop()
        end_node = route.end
        for neighbor in end_node.neighbors:
            if (not neighbor.is_big) and (neighbor in route.members):
                continue
            new_route = route.add(neighbor)
            if neighbor.name == "end":
                complete_routes.add(new_route)
                continue
            stack.append(new_route)

    pprint(complete_routes)
    return len(complete_routes)


def part2(lines):
    node_map = make_grid(lines)

    complete_routes = set()
    stack = [Route(node_map["start"])]

    while len(stack) > 0:
        route = stack.pop()
        end_node = route.end
        for neighbor in end_node.neighbors:
            new_route = route.add(neighbor)
            if (
                (not neighbor.is_big)
                and (not neighbor.is_terminal)
                and (neighbor in route.members)
            ):
                if route.has_second_visit:
                    continue
                new_route.has_second_visit = True
            if neighbor.name == "end":
                complete_routes.add(new_route)
                continue
            if neighbor.is_terminal:
                continue
            stack.append(new_route)

    pprint(sorted(complete_routes))
    return len(complete_routes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    lines = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            lines.append(line)
    if args.part == 1:
        print(part1(lines))
    elif args.part == 2:
        print(part2(lines))
    else:
        print("illegal part")
