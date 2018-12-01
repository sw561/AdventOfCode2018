#!/usr/bin/env python3

def get_number_of_loops(accumulate, total):
    # Yield tuples of the form (number of loops, pos_in_loop, repeated_number)
    #
    # If we call this function, we know that none of the numbers in accumulate
    # are repeated. On each loop, the sequence of numbers that we visit is the
    # same, but shifted by total.
    #
    # So after n loops, the ith number in the sequence is just accumulate[i] +
    # total*n. That means a number, accumulate[j], will be repeated if we have
    #   accumulate[i] = accumulate[j] + n * total
    # for some positive integer n.
    #
    # Do count sort. Put all the numbers from accumulate, x, into an array,
    # visited, at index i s.t. x % total == i.
    #
    # Now we only need to consider pairs of numbers which are in the same
    # element of visited.
    #
    # If two intersections happen after the same number of loops, the winner is
    # determined by the original position of accumulate[i], so we need to keep
    # track of the original positions as a tiebreaker mechanism.

    visited = [[] for _ in range(abs(total))]
    for pos, x in enumerate(accumulate):
        # We need pos as a tiebreaker
        visited[x % total].append((x, pos))

    for v in visited:
        # Want to loop through pairs (x, y) such that x + n*total = y for
        # positive n
        v.sort(reverse = total<0)

        for i in range(len(v)):
            for j in range(i+1, len(v)):

                n_loops = (v[j][0] - v[i][0]) // total

                # print("get from {:4d} to {:4d} after {:4d} loops".format(
                #     v[i][0], v[j][0], n_loops), end=' ')
                # print("\t\ttiebreaker: {}".format(v[i][1]))

                yield (n_loops, v[i][1], v[j][0])

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

    # print("accumulate:", accumulate)

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
