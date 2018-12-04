#!/usr/bin/env python3

from guard import process, part1, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test():
    with open("test_input.txt", 'r') as f:
        log = [x.strip() for x in f]

    sleep_data = process(log)
    guard_id, minute_max_sleep = part1(sleep_data)
    assertEqual(guard_id, 10)
    assertEqual(minute_max_sleep, 24)

    guard_id, minute, number_of_times_asleep = part2(sleep_data)
    assertEqual(guard_id, 99)
    assertEqual(minute, 45)
    assertEqual(number_of_times_asleep, 3)

test()
