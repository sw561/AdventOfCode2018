#!/usr/bin/env python3

from subprocess import check_call
from datetime import datetime, timedelta

def run_and_time(command):
    start = datetime.now()
    check_call(command, shell=True)
    end = datetime.now()
    return end - start

day = 0
total = timedelta()
for line in open("run_tests.sh", 'r'):
    if line[0] == '#':
        continue
    day += 1
    duration = run_and_time(line.strip())
    print("Day {:2d} takes {}".format(day, duration))
    total += duration

print("------------------------------")
print("Total time:  {}".format(total))
