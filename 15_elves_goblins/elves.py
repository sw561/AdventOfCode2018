#!/usr/bin/env python3

def process_grid(inp):
    # return grid without agents in the way
    # also return list of agents in the form ((x_pos, y_pos), type, hit_points)

    grid = [['#']*len(inp[0]) for _ in inp]
    agents = []

    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if inp[i][j] == '#':
                continue
            elif inp[i][j] in ['G', 'E']:
                agents.append(((i, j), inp[i][j], 200))

            grid[i][j] = '.'

    grid = ["".join(row) for row in grid]

    return grid, agents

def gen_neighbours(i, j):
    yield i-1, j
    yield i, j-1
    yield i, j+1
    yield i+1, j

class Game:
    def __init__(self, grid, agents):
        self.grid = grid
        self.agents = agents
        # set of squares occupied by agents
        self.occupied = {agent[0]: i for i, agent in enumerate(agents)}

    def move(self, agent_id, pos):
        old_pos, t, hit_points = self.agents[agent_id]
        del self.occupied[old_pos]

        self.agents[agent_id] = (pos, t, hit_points)
        self.occupied[pos] = agent_id

    def damage(self, agent_id, attack):
        pos, t, hit_points = self.agents[agent_id]
        self.agents[agent_id] = (pos, t, hit_points - attack)

        if hit_points - attack <= 0:
            # Agent dies
            del self.occupied[pos]

    def targets_remaining(self):
        types = set()
        for agent in self.agents:
            if agent[2] > 0:
                types.add(agent[1])
            if len(types) > 1:
                return True
        return False

    def total_hitpoints(self):
        return sum(agent[2] for agent in self.agents if agent[2] > 0)

    def agent_ids(self):
        # Yield agent_ids in 'read-order' according to position
        ids = sorted(range(len(self.agents)), key=lambda i: self.agents[i][0])
        return ids

    def neighbours(self, i, j):
        for i, j in gen_neighbours(i, j):
            if self.grid[i][j] == '.' and (i, j) not in self.occupied:
                yield i, j

    def enemies(self, agent_id):
        t = self.agents[agent_id][1]
        for agent in self.agents:
            if agent[1] != t and agent[2] > 0:
                yield agent

    def target_squares(self, agent_id):
        for agent in self.enemies(agent_id):
            yield from self.neighbours(*agent[0])

    def nearby_enemies(self, agent_id):
        pos, t, h = self.agents[agent_id]

        for n in gen_neighbours(*pos):
            n_agent_id = self.occupied.get(n, None)
            if n_agent_id is None:
                continue
            if self.agents[n_agent_id][1] != t:
                yield n_agent_id

    def weakest_nearby_enemy(self, agent_id):
        try:
            return min(self.nearby_enemies(agent_id), key=lambda i: self.agents[i][2])
        except ValueError:
            return None

    def in_range(self, agent_id):
        # Return true if agent is in range and can attack
        g = self.nearby_enemies(agent_id)
        try:
            next(g)
        except StopIteration:
            return False
        return True

    def display(self):
        for i in range(len(self.grid)):
            info_required = []

            for j in range(len(self.grid[0])):
                agent_id = self.occupied.get((i, j), None)
                if agent_id is not None:
                    print(self.agents[agent_id][1], end='')
                    info_required.append(agent_id)
                else:
                    print(self.grid[i][j], end='')

            print(' ', end=' ')

            for agent_id in info_required:
                agent = self.agents[agent_id]
                print("{}({})".format(agent[1], agent[2]), end=' ')

            print(" ")

def find_move(game, agent_id):

    targets = set(game.target_squares(agent_id))
    # print("Candidate targets: {}".format(targets))

    if not targets:
        # No target squares available
        return None

    distance = [[-1]*len(game.grid[0]) for _ in game.grid]

    start = game.agents[agent_id][0]
    distance[start[0]][start[1]] = 0
    pos = [start]
    d = 0

    found_targets = set()
    while not found_targets and pos:
        d += 1
        new_pos = []
        for p in pos:
            for n in game.neighbours(*p):
                if distance[n[0]][n[1]] == -1:
                    new_pos.append(n)
                    distance[n[0]][n[1]] = d

                if n in targets and n not in found_targets:
                    found_targets.add(n)

        pos = new_pos

    if not found_targets:
        # Cannot reach any targets
        return None

    # for row in distance:
    #     print(" ".join("{:2d}".format(x) if x >= 0 else '  ' for x in row))
    # print(found_targets)

    target = min(found_targets)
    # print("target: {}".format(target))

    # Now need to search backwards to establish the route
    pos = set([target])

    while d > 1:
        new_pos = set()
        for p in pos:
            for n in gen_neighbours(*p):
                if distance[n[0]][n[1]] == d-1:
                    new_pos.add(n)

        pos = new_pos
        d -= 1

    # pos is now set of good first moves

    destination = min(pos)

    return destination

def play(grid, agents, verbose=False):
    round_counter = 0
    g = Game(grid, agents)

    if verbose:
        print("\nRound: {}".format(round_counter))
        g.display()

    while True:
        for agent_id in g.agent_ids():
            # Check it's alive
            if g.agents[agent_id][2] <= 0:
                continue

            if not g.targets_remaining():
                return round_counter, g

            if not g.in_range(agent_id):
                # print("Moving agent {} at {}".format(agent_id, g.agents[agent_id][0]), end=' ')
                destination = find_move(g, agent_id)
                if destination is not None:
                    # print("to {}".format(destination))
                    g.move(agent_id, destination)
                # else:
                #     print("actually no")

            # Attack a weak enemy
            w = g.weakest_nearby_enemy(agent_id)
            if w is not None:
                g.damage(w, 3)

        round_counter += 1
        if verbose:
            print("\nRound: {}".format(round_counter))
            g.display()

def part1(fname, verbose=False):
    with open(fname, 'r') as f:
        inp = [[x for x in line.strip()] for line in f]

    grid, agents = process_grid(inp)

    round_counter, g = play(grid, agents, verbose=verbose)
    if verbose:
        print("\nRound: {}".format(round_counter))
        g.display()
    return round_counter, g.total_hitpoints()

if __name__=="__main__":
    round_counter, hit_points = part1("15_elves_goblins/input.txt")
    print(round_counter * hit_points)
