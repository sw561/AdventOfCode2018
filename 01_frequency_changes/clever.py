#!/usr/bin/env python3

from collections import defaultdict

def get_number_of_loops(accumulate, total):
    # Yield tuples of the form (number of loops, pos_in_loop, repeated_number)
    #
    # If we call this function, we know that none of the numbers in accumulate
    # are repeated. On each loop, the sequence of numbers that we visit is the
    # same, but shifted by total.
    #
    # So after n loops, the ith number in the sequence is just accumulate[i] +
    # total*n. That means a number, accumulate[j], will be repeated if we have
    #   accumulate[i] + n * total = accumulate[j]
    # for some positive integer n.
    #
    # Do count sort. Put all the numbers, x, from accumulate into a dict,
    # visited, at index i s.t. x % total == i. Now we only need to consider
    # pairs of numbers which are in the same element of visited.
    #
    # If two intersections happen after the same number of loops, the winner is
    # determined by the original position of accumulate[i], so we need to keep
    # track of the original positions as a tiebreaker mechanism.

    visited = defaultdict(list)
    for pos, x in enumerate(accumulate):
        visited[x % total].append((x, pos))

    for v in visited.values():
        # Want to loop through pairs (x, y) such that x + n*total = y for
        # positive n. So if total is positive want x<y, else want x>y
        v.sort(reverse = total<0)

        # To find the first intersection, only need to consider neighbouring
        # elements
        for (x, xpos), (y, _) in zip(v, v[1:]):
            n_loops = (y - x) // total

            # print("get from {:4d} to {:4d} after {:4d} loops".format(
            #     x, y, n_loops), end=' ')
            # print("   x position: {}".format(xpos))

            yield (n_loops, xpos, y)

def solve(changes):
    accumulate = [0]*len(changes)
    seen = set([0])
    revisited = None

    for i in range(1, len(changes)):
        accumulate[i] = accumulate[i-1] + changes[i-1]

        if revisited is None:
            if accumulate[i] in seen:
                revisited = accumulate[i]
            else:
                seen.add(accumulate[i])

    # Solution for part 1
    total = accumulate[-1] + changes[-1]

    if revisited is not None:
        return total, revisited
    elif total == 0:
        # If total is zero, we return to zero after exactly one loop
        return total, 0

    # Solution for part 2
    revisited = min(get_number_of_loops(accumulate, total))[2]

    return total, revisited

if __name__=="__main__":
    with open("01_frequency_changes/input.txt", 'r') as f:
        changes = [int(x) for x in f]
    for x in solve(changes):
        print(x)
