#!/usr/bin/env python3

from checksum import checksum, find_close

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test_checksum():
    t = """
    abcdef
    bababc
    abbcde
    abcccd
    aabcdd
    abcdee
    ababab
    """
    ids = t.split()
    assertEqual(checksum(ids), 12)
    print("Checksum test passed")

def test_find_close():
    t = """
    abcde
    fghij
    klmno
    pqrst
    fguij
    axcye
    wvxyzt
    """
    ids = t.split()
    assertEqual(find_close(ids), "fgij")
    print("find_close test passed")

test_checksum()
test_find_close()
