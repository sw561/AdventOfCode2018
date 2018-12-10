#!/usr/bin/env python3

from string import ascii_lowercase

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

def gen_points(p, d):
    # Generate points at distance d from point p

    yield p[0] - d, p[1]
    for dx in range(-d+1, d):
        yield p[0] + dx, p[1] + (d - abs(dx))
        yield p[0] + dx, p[1] - (d - abs(dx))
    yield p[0] + d, p[1]

def area(i, points, DATA=None):

    # Return number of squares for which points[i] is nearest point.
    # If there are infinite such squares return 0

    if has_infinite_area(points[i], points):
        return 0

    # Create a sorted list dp, s.t. dp[i] = (distance to points[i], points[i])
    dp = sorted((manhattan_distance(p, points[i]), p) for p in points if p != points[i])

    num_squares_old = None
    num_squares = 1 # Include square at points[i] itself
    distance = 0
    while num_squares_old is None or num_squares > num_squares_old:
        num_squares_old = num_squares
        distance += 1

        for s in gen_points(points[i], distance):
            found_square = True
            for d, p in dp:
                if d > 2*distance:
                    break
                if manhattan_distance(p, s) <= distance:
                    found_square = False
                    break

            if found_square:
                if DATA is not None:
                    DATA[s[1]][s[0]] = ascii_lowercase[i]
                num_squares += 1

    return num_squares

def part1(points, DATA=None):
    # For each p in points, find number of closest squares or infinity
    return max(area(i, points, DATA) for i in range(len(points)))

def update_x(location, total_distance, x_index, points):
    # Requires that points is sorted using x-coordinate
    location = (location[0] + 1, location[1])
    while x_index < len(points) and points[x_index][0] < location[0]:
        x_index += 1

    total_distance += x_index - (len(points) - x_index)
    return location, total_distance, x_index

def update_y(location, total_distance, y_index, points):
    # Requires that points is sorted using y-coordinate
    location = (location[0], location[1]+1)
    while y_index < len(points) and points[y_index][1] < location[1]:
        y_index += 1

    total_distance += y_index - (len(points) - y_index)
    return location, total_distance, y_index

# The region will be contiguous, so find centre of mass and search outwards

def get_total_distances(points_x, threshold=10000):
    location = 0, 0
    points_x.sort()
    points_y = sorted(points_x, key=lambda x: x[1])

    x_index = 0
    y_index = 0

    total_distance = sum(manhattan_distance(p, location) for p in points_x)

    found_any_squares = False
    while y_index < len(points_x):

        # Search in x direction
        loc, dist = location, total_distance
        x_index = 0
        found_some_squares = False

        while True:
            ret = update_x(loc, dist, x_index, points_x)
            if ret[1] > dist and ret[1] > threshold:
                break
            loc, dist, x_index = ret
            if dist < threshold:
                found_some_squares = True
                found_any_squares = True
                yield loc, dist

        if found_any_squares and not found_some_squares:
            return

        location, total_distance, y_index = update_y(location, total_distance, y_index, points_y)

def part2(points):
    return sum(1 for _ in get_total_distances(points))

if __name__=="__main__":
    with open("06_voronoi/input.txt", 'r') as f:
        points = [[int(x) for x in line.split(',')] for line in f]

    print(part1(points))
    print(part2(points))
