#!/usr/bin/env python3

from string import ascii_lowercase

def reacted(polymer, ignore=None):

    stack = []
    for c in polymer:
        if c.lower() == ignore:
            continue
        if stack and stack[-1].lower() == c.lower()\
                and (stack[-1].islower() is not c.islower()):
            stack.pop()
        else:
            stack.append(c)

    return stack

def part2(polymer):
    return min(len(reacted(polymer, ignore=x)) for x in ascii_lowercase)

if __name__=="__main__":
    with open("05_polymer/input.txt", 'r') as f:
        polymer = f.read().strip()

    r = reacted(polymer)
    print(len(r))
    print(part2(r))
