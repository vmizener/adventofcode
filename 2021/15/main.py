#!/usr/bin/env python3
import argparse
import heapq


def part1(grid):
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]
    m = len(grid)
    n = len(grid[0])

    visited = set()
    d = {}
    for x in range(m):
        for y in range(n):
            d[(x, y)] = float("inf")
    d[(0, 0)] = 0
    p_queue = [(0, 0)]

    while len(p_queue) > 0:
        p_queue.sort(key=lambda n: d[n] * -1)
        x, y = p_queue.pop()
        if (x, y) == (m - 1, n - 1):
            return d[(m - 1, n - 1)]
        visited.add((x, y))
        dist = d[(x, y)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            if (nx, ny) in visited:
                continue
            nval = dist + int(grid[nx][ny])
            if nval < d[(nx, ny)]:
                d[(nx, ny)] = nval
                p_queue.append((nx, ny))


def part2(grid):
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]
    m = len(grid)
    n = len(grid[0])

    visited = set()
    d = {}
    for x in range(m * 5):
        for y in range(n * 5):
            d[(x, y)] = float("inf")
    d[(0, 0)] = 0
    pq = [(0, 0, 0)]

    def get(nx, ny):
        off_x, grd_x = divmod(nx, m)
        off_y, grd_y = divmod(ny, n)
        tile = (int(grid[grd_x][grd_y]) + off_x + off_y) % 9
        if tile == 0:
            tile = 9
        return tile

    while len(pq) > 0:
        _, x, y = heapq.heappop(pq)
        if (x, y) == (m * 5 - 1, n * 5 - 1):
            break
        visited.add((x, y))
        dist = d[(x, y)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < m * 5 and 0 <= ny < n * 5):
                continue
            if (nx, ny) in visited:
                continue
            new_dist = dist + get(nx, ny)
            if new_dist < d[(nx, ny)]:
                d[(nx, ny)] = new_dist
                heapq.heappush(pq, (new_dist, nx, ny))

    return d[(m * 5 - 1, n * 5 - 1)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    grid = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            grid.append(line.strip())
    if args.part == 1:
        print(part1(grid))
    elif args.part == 2:
        print(part2(grid))
    else:
        print("illegal part")
