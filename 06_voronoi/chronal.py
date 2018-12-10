#!/usr/bin/env python3

from string import ascii_lowercase
from collections import deque

def manhattan_distance(p1, p2):
    return sum(abs(p1i - p2i) for p1i, p2i in zip(p1, p2))

def quadrant(p, p2):
    # Return 0 for North, 1 for East, 2 for South, 3 for West
    # The direction indicates quadrant of p2 with respect to p
    #
    # If a point is on the boundary, it counts as being in both quadrants

    dx = [p2i - pi for pi, p2i in zip(p, p2)]

    if abs(dx[0]) >= abs(dx[1]):
        if dx[0] > 0:
            yield 1
        else:
            yield 3

    if abs(dx[0]) <= abs(dx[1]):
        if dx[1] > 0:
            yield 0
        else:
            yield 2

def has_infinite_area(p, points):
    quad = [False] * 4
    n_quad_occupied = 0

    for pi in points:
        if pi == p:
            continue
        for q in quadrant(p, pi):
            if not quad[q]:
                quad[q] = True
                n_quad_occupied += 1
        if n_quad_occupied == 4:
            return False

    return True

def neighbours(p):
    yield (p[0] + 1, p[1])
    yield (p[0] - 1, p[1])
    yield (p[0], p[1] + 1)
    yield (p[0], p[1] - 1)

def good(ref, c, dp):
    # Check if c is closest to ref, in which case return True
    # if c is closest to some other point in dp, return False

    distance = manhattan_distance(ref, c)

    for d, p in dp:
        if d > 2*distance:
            # Don't need to consider more points
            break
        if manhattan_distance(c, p) <= distance:
            return False

    return True

def area(i, points, DATA=None):

    # Return number of squares for which points[i] is nearest point.
    # If there are infinite such squares return 0

    if has_infinite_area(points[i], points):
        return 0

    dp = sorted((manhattan_distance(p, points[i]), p) for p in points if p != points[i])

    num_squares = 0
    q = deque([points[i]])
    visited = set([points[i]])
    while q:
        c = q.popleft()

        if good(points[i], c, dp):
            if DATA is not None and c != points[i]:
                DATA[c[1]][c[0]] = ascii_lowercase[i]
            num_squares += 1
            for new in neighbours(c):
                if new not in visited:
                    q.append(new)
                    visited.add(new)

    return num_squares

def part1(points, DATA=None):
    # For each p in points, find number of closest squares or infinity
    return max(area(i, points, DATA) for i in range(len(points)))

def update(location, total_distance, index, points, direction=0):
    # Requires that points is sorted using coordinate corresponding to direction
    while index < len(points) and points[index][direction] < location[direction]:
        index += 1

    total_distance += index - (len(points) - index)
    return total_distance, index

def get_total_distances(points_x, threshold=10000):
    location = [0, 0]
    points_x.sort()
    points_y = sorted(points_x, key=lambda x: x[1])

    x_index = 0
    y_index = 0

    total_distance = sum(manhattan_distance(p, location) for p in points_x)

    found_any_squares = False
    while y_index < len(points_x):

        # Search in x direction
        loc, dist = location[:], total_distance
        x_index = 0
        found_some_squares = False

        while True:
            loc[0] += 1
            ret = update(loc, dist, x_index, points_x)
            if ret[0] > dist and ret[0] > threshold:
                break
            dist, x_index = ret
            if dist < threshold:
                found_some_squares = True
                found_any_squares = True
                yield loc, dist

        if found_any_squares and not found_some_squares:
            return

        location[1] += 1
        total_distance, y_index = update(
            location, total_distance, y_index, points_y, direction=1
            )

def part2(points):
    return sum(1 for _ in get_total_distances(points))

if __name__=="__main__":
    with open("06_voronoi/input.txt", 'r') as f:
        points = [tuple(int(x) for x in line.split(',')) for line in f]

    print(part1(points))
    print(part2(points))
