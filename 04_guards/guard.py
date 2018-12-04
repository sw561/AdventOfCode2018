#!/usr/bin/env python3

from collections import defaultdict

def process(log):
    log.sort()

    # sleep_data[guard_id][i] is the number of times the guard was asleep
    # during the ith minute
    sleep_data = defaultdict(lambda: [0]*60)

    guard_id = None
    asleep = False
    for log_entry in log:
        minute = int(log_entry[15:17])
        entry = log_entry[19:].split()

        if entry[0] == "Guard":
            guard_id = int(entry[1][1:])

        elif entry[0] == "falls":
            asleep = minute

        elif entry[0] == "wakes":
            wake = minute
            for m in range(asleep, wake):
                sleep_data[guard_id][m] += 1

    return sleep_data

def part1(sleep_data):
    # Get data for the guard who slept the most
    guard_id, data = max(sleep_data.items(), key=lambda x: sum(x[1]))

    # Find sleepiest minute
    minute, n_sleep = max(enumerate(data), key=lambda x: x[1])
    return n_sleep, guard_id, minute

def loop_through(sleep_data):
    for guard_id, data in sleep_data.items():
        for minute, n_sleep in enumerate(data):
            yield n_sleep, guard_id, minute

def part2(sleep_data):
    # Find the sleepiest minute overall
    return max(loop_through(sleep_data))

if __name__=="__main__":
    with open("04_guards/input.txt", 'r') as f:
        log = [x.strip() for x in f]

    sleep_data = process(log)
    n_sleep, guard_id, minute = part1(sleep_data)
    print(guard_id * minute)

    n_sleep, guard_id, minute = part2(sleep_data)
    print(guard_id * minute)
