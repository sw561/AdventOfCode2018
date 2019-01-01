#!/usr/bin/env python3

from doors import process, follow_doors

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

tests = [
("^ENWWW(NEEE|SSE(EE|N))$", 10),
("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
]

for regex, i in tests:
    doors = process(regex)
    x, _ = follow_doors(doors)
    assertEqual(x, i)
