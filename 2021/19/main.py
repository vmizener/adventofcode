#!/usr/bin/env python3
import argparse
import math
import re
import pdb


def dist(beacon1, beacon2):
    # Manhattan distance
    return sum([abs(beacon1[dim] - beacon2[dim]) for dim in range(3)])


def create_hash_map(beacons):
    # Create map of unique hashes of each beacon and its 3 nearest neighbors
    hash_map = {}
    for beacon in beacons:
        nearest = []
        d = math.inf
        for peer in beacons:
            if peer == beacon:
                continue
            peer_dist = dist(peer, beacon)
            if peer_dist < d:
                nearest.append((peer_dist, peer))
                nearest.sort()
                d = min([d] + [l[0] for l in nearest[1:]])
            if len(nearest) > 2:
                nearest.sort()
                nearest.pop(-1)
        nearest_dists, nearest_beacons = zip(*nearest)
        # Unique hash of relative distances
        dist_hash = hash((dist(*nearest_beacons), *nearest_dists))
        hash_map[dist_hash] = [beacon] + list(nearest_beacons)
    return hash_map


def find_matching_neighbors(principle_map, scanner_maps):
    # Find first set of neighbors with matching hash to a set in the principle
    for principle_hash in principle_map.keys():
        for scanner, scanner_map in scanner_maps.items():
            for scanner_hash in scanner_map.keys():
                if scanner_hash == principle_hash:
                    principle_neighbors = principle_map[scanner_hash]
                    scanner_neighbors = scanner_map[scanner_hash]
                    return (scanner, principle_neighbors, scanner_neighbors)
    raise RuntimeError()


def get_scanner_offset(principle_neighbors, scanner_neighbors):
    offset, rotation, direction = [None] * 3, [None] * 3, [None] * 3
    for dimension in range(3):
        if offset[dimension] is not None:
            # Solved this dimension
            continue
        for rotation_skew in range(3):
            for direction_skew in [1, -1]:
                offsets = set()
                for idx in range(3):
                    offsets.add(
                        principle_neighbors[idx][dimension]
                        - scanner_neighbors[idx][rotation_skew] * direction_skew
                    )
                if len(offsets) == 1:
                    # All are equal -> found orientation
                    offset[dimension] = offsets.pop()
                    rotation[dimension] = rotation_skew
                    direction[dimension] = direction_skew
    if None in offset:
        pdb.set_trace()
    return offset, rotation, direction


def reorient_scanner(scanner, offset, rotation, direction):
    return tuple(
        [
            tuple(
                [
                    beacon[rotation[idx]] * direction[idx] + offset[idx]
                    for idx in range(3)
                ]
            )
            for beacon in scanner
        ]
    )


def max_dist(positions):
    best = 0
    for pos1 in positions:
        for pos2 in positions:
            best = max(best, dist(pos1, pos2))
    return best


def solve(scanners):
    principle = set(scanners.pop(0))

    scanner_maps = {}
    scanner_positions = {}
    # Create unique hash for each beacon in a scanner against its neighbors
    # This creates a way to identify beacons independent of relative position to scanners
    for scanner in scanners:
        scanner_maps[scanner] = create_hash_map(scanner)

    while len(scanner_maps) > 0:
        # We recalculate the hashes for the principle each loop (as we add beacons to it)
        principle_map = create_hash_map(principle)
        # Finds the first set of 3 matching beacons from a scanner to the principle
        # We're guaranteed at least 3 as by construction we're given 12
        scanner, principle_neighbors, scanner_neighbors = find_matching_neighbors(
            principle_map, scanner_maps
        )
        # Once we have them, we triangulate orientation/position
        scanner_offset, scanner_rotation, scanner_direction = get_scanner_offset(
            principle_neighbors, scanner_neighbors
        )
        # The offset is the position of the scanner
        # Save this for part2
        scanner_positions[scanner] = scanner_offset
        # Re-orient the scanner to align with the principle
        oriented_scanner = reorient_scanner(
            scanner, scanner_offset, scanner_rotation, scanner_direction
        )
        # Remove the scanner from consideration from future loops
        del scanner_maps[scanner]
        # Add the re-oriented beacons from this scanner to the principle
        principle.update(oriented_scanner)
    return principle, scanner_positions


def part1(scanners):
    principle, _ = solve(scanners)
    return len(principle)


def part2(scanners):
    _, scanner_positions = solve(scanners)
    return max_dist(scanner_positions.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    scanners = []
    with open(args.input_file) as fh:
        beacons = []
        for line in fh.readlines():
            line = line.strip()
            if re.match(r"^--- scanner", line):
                continue
            if len(line) == 0:
                scanners.append(tuple(beacons))
                beacons = []
                continue
            beacons.append(tuple([int(c) for c in line.strip().split(",")]))
        scanners.append(tuple(beacons))
    if args.part == 1:
        print(part1(scanners))
    elif args.part == 2:
        print(part2(scanners))
    else:
        print("illegal part")
