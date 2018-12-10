#!/usr/bin/env python3

def consume_node(g):
    # g generates the entries of data, consume a node and yield the metadata

    n_children = next(g)
    n_meta = next(g)
    for _ in range(n_children):
        yield from consume_node(g)
    for _ in range(n_meta):
        yield next(g)

def part1(data):
    return sum(consume_node(iter(data)))

def value(g):

    n_children = next(g)
    n_meta = next(g)

    if n_children == 0:
        v = sum(next(g) for _ in range(n_meta))
        return v

    value_children = [value(g) for _ in range(n_children)]

    v = 0
    for _ in range(n_meta):
        index = next(g)-1
        if index in range(n_children):
            v += value_children[index]

    return v

def part2(data):
    return value(iter(data))

if __name__=="__main__":
    with open("08_metadata/input.txt", 'r') as f:
        data = [int(x) for x in f.read().split()]

    print(part1(data))
    print(part2(data))
