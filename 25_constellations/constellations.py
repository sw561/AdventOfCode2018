#!/usr/bin/env python3

import re
from collections import defaultdict

def manhattan_distance(p1, p2):
    return sum(abs(p1i - p2i) for p1i, p2i in zip(p1, p2))

def create_graph(positions):
    # Create a graph, g such that g[i] is a list of nodes connected to i

    id_dict = dict()
    sort_0 = defaultdict(list)
    g = [[] for _ in positions]

    for i, pos in enumerate(positions):
        for x in range(pos[0]-3, pos[0]+4):
            for candidate in sort_0[x]:
                j = id_dict[candidate]

                if manhattan_distance(pos, candidate) <= 3:
                    g[i].append(j)
                    g[j].append(i)

        sort_0[pos[0]].append(pos)
        id_dict[pos] = i

    return g

def make_constellations(graph):
    unused = set(range(len(graph)))
    n_constellations = 0

    while unused:
        n_constellations += 1

        node = next(iter(unused))
        unused.remove(node)
        stack = [node]

        while stack:
            node = stack.pop()
            for n in graph[node]:
                if n in unused:
                    stack.append(n)
                    unused.remove(n)

    return n_constellations

def main(fname):
    pos = []
    pattern = re.compile("-?\d+")
    with open(fname, 'r') as f:
        for line in f:
            pos.append(tuple(int(x) for x in re.findall(pattern, line)))

    g = create_graph(pos)
    return make_constellations(g)

if __name__=="__main__":
    print(main("25_constellations/input.txt"))
