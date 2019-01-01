#!/usr/bin/env python3

from collections import defaultdict, deque

def inverse(entry):
    if entry == "N":
        return "S"
    if entry == "S":
        return "N"
    if entry == "E":
        return "W"
    if entry == "W":
        return "E"

def add_direction(pos, direction):
    # print("Calling add_direction, {} {}".format(pos, direction))
    if direction == "N":
        return pos[0] - 1, pos[1]
    elif direction == "S":
        return pos[0] + 1, pos[1]
    elif direction == "E":
        return pos[0], pos[1] + 1
    elif direction == "W":
        return pos[0], pos[1] - 1

def process(regex):
    doors = defaultdict(set)

    stack = []
    pos = (0, 0)

    for entry in regex[1:-1]:
        if entry == "(":
            stack.append(pos)
        elif entry == "|":
            pos = stack[-1]
        elif entry == ")":
            pos = stack.pop()
        else:
            doors[pos].add(entry)
            pos = add_direction(pos, entry)
            doors[pos].add(inverse(entry))

    return doors

def follow_doors(doors):
    # Do BFS through the map
    # A deque of (px, py), distance tuples
    q = deque([((0, 0), 0)])
    distance = dict()
    distance[(0, 0)] = 0
    max_distance = 0
    count_far_rooms = 0

    while q:
        pos, d = q.popleft()

        for direction in doors[pos]:

            new_pos = add_direction(pos, direction)
            if new_pos not in distance:
                distance[new_pos] = d + 1
                if d + 1 > max_distance:
                    max_distance = d + 1
                if d + 1 >= 1000:
                    count_far_rooms += 1
                q.append((new_pos, d+1))

    return max_distance, count_far_rooms

if __name__=="__main__":
    with open("20_doors/input.txt", 'r') as f:
        regex = f.read().strip()

    doors = process(regex)

    for x in follow_doors(doors):
        print(x)
