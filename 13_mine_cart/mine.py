#!/usr/bin/env python3

orientation = {">": "-", "<": "-", "v": "|", "^": "|"}

def process(track):
    # Return position and direction of carts,
    # and track but without carts in the way

    # list of (position, direction, number_of_intersections_passed) tuples
    carts = []
    new_track = [[" "]*len(track[0]) for _ in range(len(track))]
    for i, line in enumerate(track):
        for j, piece in enumerate(line):

            if piece not in orientation:
                new_track[i][j] = piece
            else:
                carts.append(((i, j), piece, 0))
                new_track[i][j] = orientation[piece]

    return new_track, carts

new_position_func_dict = {
    ">": lambda x: (x[0], x[1]+1),
    "<": lambda x: (x[0], x[1]-1),
    "v": lambda x: (x[0]+1, x[1]),
    "^": lambda x: (x[0]-1, x[1]),
}

u = ["^", ">", "v", "<"]
turn_right_dict = {u[i]: u[(i+1)%4] for i in range(4)}
turn_left_dict = {u[i]: u[(i-1)%4] for i in range(4)}

def update_dn(track, direction, n):
    if track == "/":
        if orientation[direction] == "|":
            direction = turn_right_dict[direction]
        else:
            direction = turn_left_dict[direction]

    elif track == "\\":
        if orientation[direction] == "|":
            direction = turn_left_dict[direction]
        else:
            direction = turn_right_dict[direction]

    elif track == "+":
        if n%3 == 0:
            direction = turn_left_dict[direction]
        elif n%3 == 2:
            direction = turn_right_dict[direction]

        n += 1
    return direction, n

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
        (pos, direction, n) = carts.pop()
        occupied.remove(pos)

        pos = new_position_func_dict[direction](pos)

        if pos in occupied:
            if first_crash:
                print("{},{}".format(pos[1], pos[0]))
                first_crash = False

            occupied.remove(pos)
            # Need to remove cart that was crashed into. This cart could be in
            # carts or new_carts.
            remove(pos, carts, new_carts)

        else:
            # No crash, update details and add to new_carts
            direction, n = update_dn(track[pos[0]][pos[1]], direction, n)

            occupied.add(pos)
            new_carts.append((pos, direction, n))

    return new_carts

if __name__=="__main__":
    with open("13_mine_cart/input.txt", 'r') as f:
        track = [[x for x in line if x!="\n"] for line in f]

    track, carts = process(track)
    occupied = set(cart[0] for cart in carts)

    while len(carts) > 1:
        carts = move(track, carts, occupied)

    print("{},{}".format(carts[0][0][1], carts[0][0][0]))
