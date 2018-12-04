#!/usr/bin/env python3

from collections import defaultdict

def read(log_entry):
    minute = int(log_entry[15:17])
    data = log_entry[19:].split()
    return minute, data

def process(log):
    log.sort()

    # sleep_data[guard_id][i] is the number of times the guard was asleep
    # during the ith minute
    sleep_data = defaultdict(lambda: [0]*60)

    guard_id = None
    asleep = False
    for minute, entry in map(read, log):

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
    return guard_id, max(range(60), key=lambda x: data[x])

def part2(sleep_data):
    # For each guard, find the sleepiest minute
    for guard_id in sleep_data.keys():
        sleep_data[guard_id] = max(enumerate(sleep_data[guard_id]), key=lambda x: x[1])

    # Now, sleep_data[guard_id] = (sleepiest_minute, number_of_times_asleep)

    # Find the guard with the sleepiest minute
    guard_id, (minute, number_of_times_asleep) = max(sleep_data.items(), key=lambda x: x[1][1])
    return guard_id, minute, number_of_times_asleep

if __name__=="__main__":
    with open("04_guards/input.txt", 'r') as f:
        log = [x.strip() for x in f]

    sleep_data = process(log)
    guard_id, minute_max_sleep = part1(sleep_data)
    print(guard_id * minute_max_sleep)

    guard_id, minute, number_of_times_asleep = part2(sleep_data)
    print(guard_id * minute)
