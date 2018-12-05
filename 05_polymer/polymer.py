#!/usr/bin/env python3

from string import ascii_uppercase

def reacted(polymer, ignore=[]):

    stack = []
    for c in polymer:
        if c in ignore:
            continue

        if stack and abs(stack[-1] - c) == 32:
            stack.pop()
        else:
            stack.append(c)

    return stack

def part2(polymer):
    return min(len(reacted(polymer, ignore=(ord(x), ord(x)+32))) for x in ascii_uppercase)

if __name__=="__main__":
    with open("05_polymer/input.txt", 'r') as f:
        polymer = f.read().strip()

    r = reacted(map(ord, polymer))
    print(len(r))
    print(part2(r))
