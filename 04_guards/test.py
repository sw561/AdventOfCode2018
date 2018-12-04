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
    n_sleep, guard_id, minute = part1(sleep_data)
    assertEqual(n_sleep, 2)
    assertEqual(guard_id, 10)
    assertEqual(minute, 24)

    n_sleep, guard_id, minute = part2(sleep_data)
    assertEqual(n_sleep, 3)
    assertEqual(guard_id, 99)
    assertEqual(minute, 45)

test()
