#!/usr/bin/env python3
import argparse
import collections
import re


def part1(positions):
    def sim(positions):
        p1, p2 = positions
        s1, s2 = 0, 0
        step = 0
        die = 1
        while s1 < 1000 and s2 < 1000:
            # print(f"{step:03}: ({p1}, {s1:03}) ({p2}, {s2:03})")
            step += 1
            p1 = (p1 + 3 + die * 3) % 10
            if p1 == 0:
                s1 += 10
            else:
                s1 += p1
            die += 3
            p2 = (p2 + 3 + die * 3) % 10
            if p2 == 0:
                s2 += 10
            else:
                s2 += p2
            die += 3
        return step, (s1, s2), (p1, p2)

    step, (s1, s2), (p1, p2) = sim(positions)
    if s1 < s2:
        # Player 2 wins
        rolls = step * 6
        return s1 * rolls
    else:
        rolls = step * 6 - 3
        return (s2 - p2) * rolls


def part2(positions, winning_score=21):
    rolls = {
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1,
    }
    games = collections.defaultdict(int)
    games[((*positions,), (0, 0))] = 1
    p1_wins, p2_wins = 0, 0

    while len(games) > 0:
        new_games = collections.defaultdict(int)
        for ((p1, p2), (s1, s2)), universes in games.items():
            # Do p1 first
            for roll1, count1 in rolls.items():
                p1_universes = universes * count1
                new_p1 = (p1 + roll1 - 1) % 10 + 1
                new_s1 = s1 + new_p1
                if new_s1 >= winning_score:
                    p1_wins += p1_universes
                    continue
                # Do p2 next if game isn't over
                for roll2, count2 in rolls.items():
                    p2_universes = universes * count1 * count2
                    new_p2 = (p2 + roll2 - 1) % 10 + 1
                    new_s2 = s2 + new_p2
                    if new_s2 >= winning_score:
                        p2_wins += p2_universes
                        continue
                    # Game continues; include its state for next iteration
                    new_games[((new_p1, new_p2), (new_s1, new_s2))] += p2_universes
        games = new_games

    player_wins = sorted([(p1_wins, 1), (p2_wins, 2)])
    winner_wins, winner_num = player_wins[-1]
    return f"Player {winner_num} wins in {winner_wins} universes"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, help="Which part to run.")
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    positions = []
    with open(args.input_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            if match := re.search(r": (\d)", line):
                positions.append(int(match.group(1)))
    if args.part == 1:
        print(part1(positions))
    elif args.part == 2:
        print(part2(positions))
    else:
        print("illegal part")
