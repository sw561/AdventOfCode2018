#!/usr/bin/env python3

class Node:
    __slots__ = 'x', 'n', 'p'
    def __init__(self, x, n=None, p=None):
        self.x = x
        self.n = n
        self.p = p

    def __str__(self):
        return str(self.x)

class Circular_List:
    def __init__(self, x):
        self.head = Node(x)
        self.head.n = self.head
        self.head.p = self.head

    def rotate(self, i):
        if self.head is None:
            raise Exception("Can't rotate empty list")
        if i > 0:
            for _ in range(i):
                self.head = self.head.n
        else:
            for _ in range(-i):
                self.head = self.head.p

    def insert(self, x):
        # Insert new node with data x after head
        after = self.head.n
        new = Node(x, after, self.head)
        after.p = new
        self.head.n = new
        self.head = new

    def pop(self):
        # Remove head and return the data corresponding to head
        before, data, after = self.head.p, self.head.x, self.head.n
        before.n = after
        after.p = before
        self.head = after
        return data

    def __iter__(self):
        node = self.head
        yield node
        while node.n != self.head:
            node = node.n
            yield node

    def __str__(self):
        return " ".join(map(str, iter(self)))

def play(last):
    game = Circular_List(0)

    for i in range(1, last+1):
        if i%23:
            game.rotate(1)
            game.insert(i)
            # game.rotate(1)
        else:
            game.rotate(-7)
            yield i, game.pop()

    # print(game)

def solve(players, last):
    points = [0]*players

    for i, x in play(last):
        points[i % players] += i + x

    return max(points)

def process(line):
    u = line.split()
    return int(u[0]), int(u[-2])

if __name__=="__main__":
    with open("09_marble/input.txt", 'r') as f:
       players, last  = process(f.read())

    # Part 1
    print(solve(players, last))

    # Part 2
    print(solve(players, last*100))
