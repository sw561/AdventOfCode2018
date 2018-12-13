#!/usr/bin/env python3

from itertools import chain

translate = {">": "-", "<": "-", "v": "|", "^": "|"}

def process(track):
    # Return position and direction of carts,
    # and track but without carts in the way

    # list of (position, direction, number_of_intersections_passed) tuples
    carts = []
    occupied = set()
    new_track = [[" "]*len(track[0]) for _ in range(len(track))]
    for i, line in enumerate(track):
        for j, piece in enumerate(line):

            if piece not in translate:
                new_track[i][j] = piece
            else:
                carts.append(((i, j), piece, 0))
                occupied.add((i, j))
                new_track[i][j] = translate[piece]

    return new_track, carts, occupied

def new_position(i, j, direction):
    if direction == ">":
        return i, j+1
    elif direction == "<":
        return i, j-1
    elif direction == "v":
        return i+1, j
    elif direction == "^":
        return i-1, j

u = ["^", ">", "v", "<"]
def turn_right(direction):
    i = (u.index(direction) + 1) % 4
    return u[i]

def turn_left(direction):
    i = (u.index(direction) - 1) % 4
    return u[i]

def remove(pos, carts, new_carts):
    for search_list in [carts, new_carts]:
        for i, x in enumerate(search_list):
            if x[0] == pos:
                search_list.pop(i)
                return

    raise Exception("remove function did not find the cart")

first_crash = True

def move(track, carts, occupied):
    global first_crash
    new_carts = []
    # sort in reverse, since it's more efficient to pop from the end
    carts.sort(reverse=True)

    while carts:
        ((i, j), direction, n) = carts.pop()
        occupied.remove((i, j))

        i, j = new_position(i, j, direction)

        if (i, j) in occupied:
            if first_crash:
                print("{},{}".format(j, i))
                first_crash = False

            occupied.remove((i, j))
            # Need to remove cart that was crashed into. This cart could be in
            # carts or new_carts.
            remove((i, j), carts, new_carts)

        else:
            # No crash, update details and add to new_carts
            if track[i][j] == "/":
                if translate[direction] == "|":
                    direction = turn_right(direction)
                else:
                    direction = turn_left(direction)

            elif track[i][j] == "\\":
                if translate[direction] == "|":
                    direction = turn_left(direction)
                else:
                    direction = turn_right(direction)

            elif track[i][j] == "+":
                if n%3 == 0:
                    direction = turn_left(direction)
                elif n%3 == 2:
                    direction = turn_right(direction)

                n += 1

            occupied.add((i, j))
            new_carts.append(((i, j), direction, n))

    return new_carts

if __name__=="__main__":
    with open("13_mine_cart/input.txt", 'r') as f:
        track = [[x for x in line if x!="\n"] for line in f]

    track, carts, occupied = process(track)

    while carts is not None:
        carts = move(track, carts, occupied)

        if len(carts) == 1:
            print("{},{}".format(carts[0][0][1], carts[0][0][0]))
            break
