#!/usr/bin/env python3

from copy import deepcopy
from itertools import count

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
                agents.append(Agent((i, j), inp[i][j]))

            grid[i][j] = ' '

    grid = ["".join(row) for row in grid]

    return grid, agents

def neighbours(i, j):
    yield i-1, j
    yield i, j-1
    yield i, j+1
    yield i+1, j

class Agent:
    def __init__(self, pos, t, hit_points=200):
        self.pos = pos
        self.t = t
        self.hit_points = hit_points

    def live(self):
        return self.hit_points > 0

    def __str__(self):
        return "{}({})".format(self.t, self.hit_points)

class Game:
    def __init__(self, grid, agents):
        self.grid = grid
        self.agents = deepcopy(agents)
        # set of squares occupied by agents
        self.occupied = {agent.pos: i for i, agent in enumerate(agents)}

    def move(self, agent_id, pos):
        old_pos = self.agents[agent_id].pos
        del self.occupied[old_pos]

        self.agents[agent_id].pos = pos
        self.occupied[pos] = agent_id

    def damage(self, agent_id, attack):
        self.agents[agent_id].hit_points -= attack

        if not self.agents[agent_id].live():
            # Agent dies
            del self.occupied[self.agents[agent_id].pos]

    def targets_remaining(self, t):
        # Find an agent with type not equal to t
        return any(agent.live() and agent.t != t for agent in self.agents)

    def total_hitpoints(self):
        return sum(agent.hit_points for agent in self.agents if agent.live())

    def agent_ids(self):
        # Yield agent_ids in 'read-order' according to position
        ids = sorted(range(len(self.agents)), key=lambda i: self.agents[i].pos)
        return ids

    def neighbouring_spaces(self, i, j):
        for i, j in neighbours(i, j):
            if self.grid[i][j] == ' ' and (i, j) not in self.occupied:
                yield i, j

    def target_squares(self, agent_id):
        t = self.agents[agent_id].t
        for agent in self.agents:
            if agent.t != t and agent.live():
                yield from self.neighbouring_spaces(*agent.pos)

    def nearby_enemies(self, agent_id):
        pos, t = self.agents[agent_id].pos, self.agents[agent_id].t

        for n in neighbours(*pos):
            n_agent_id = self.occupied.get(n, None)
            if n_agent_id is not None and self.agents[n_agent_id].t != t:
                yield n_agent_id

    def weakest_nearby_enemy(self, agent_id):
        return min(self.nearby_enemies(agent_id),
            key=lambda i: (self.agents[i].hit_points, self.agents[i].pos),
            default=None)

    def in_range(self, agent_id):
        # Return true if agent is in range and can attack
        g = self.nearby_enemies(agent_id)
        try:
            next(g)
        except StopIteration:
            return False
        return True

    def display_row(self, i):
        info_required = []

        for j in range(len(self.grid[0])):
            agent_id = self.occupied.get((i, j), None)
            if agent_id is not None:
                yield self.agents[agent_id].t
                info_required.append(agent_id)
            else:
                yield self.grid[i][j]

        for agent_id in info_required:
            yield " "
            yield str(self.agents[agent_id])

    def __str__(self):
        return "\n".join("".join(self.display_row(i)) for i in range(len(self.grid)))

def find_move(game, agent_id):

    targets = set(game.target_squares(agent_id))
    # print("Candidate targets: {}".format(targets))

    if not targets:
        # No target squares available
        return None

    distance = [[-1]*len(game.grid[0]) for _ in game.grid]

    start = game.agents[agent_id].pos
    distance[start[0]][start[1]] = 0
    pos = [start]
    d = 0

    found_targets = set()
    while not found_targets and pos:
        d += 1
        new_pos = []
        for p in pos:
            for n in game.neighbouring_spaces(*p):
                if distance[n[0]][n[1]] == -1:
                    new_pos.append(n)
                    distance[n[0]][n[1]] = d

                if n in targets:
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
            for n in neighbours(*p):
                if distance[n[0]][n[1]] == d-1:
                    new_pos.add(n)

        pos = new_pos
        d -= 1

    # pos is now set of good first moves
    destination = min(pos)

    return destination

def play(grid, agents, elf_attack=3, verbose=False):
    g = Game(grid, agents)

    for round_counter in count():
        if verbose:
            print("\nRound: {}".format(round_counter))
            print(g)

        for agent_id in g.agent_ids():
            # Check it's alive
            if not g.agents[agent_id].live():
                continue

            if not g.targets_remaining(g.agents[agent_id].t):
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
                g.damage(w, elf_attack if g.agents[agent_id].t=='E' else 3)

def n_elf_survivors(grid, agents, elf_attack):
    r, g = play(grid, agents, elf_attack=elf_attack)

    n_alive = sum(agent.t == 'E' for agent in g.agents if agent.live())
    return n_alive

def bisection(f, left, right):
    # Find smallest value i s.t. f(i) = True

    assert f(left) is False
    assert f(right) is True

    while right - left > 1:
        m = (left + right) // 2
        if f(m):
            right = m
        else:
            left = m

    return right

if __name__=="__main__":
    with open("15_elves_goblins/input.txt", 'r') as f:
        inp = [line.strip() for line in f]

    grid, agents = process_grid(inp)

    # Part 1
    round_counter, game = play(grid, agents)
    # print("\nRound: {}".format(round_counter))
    # print(game)
    print(round_counter * game.total_hitpoints())

    # Part 2
    n_elves = sum(agent.t == 'E' for agent in agents)

    elf_attack = bisection(
        lambda x: n_elf_survivors(grid, agents, x) == n_elves, 3, 50
        )

    round_counter, game = play(grid, agents, elf_attack=elf_attack)
    # print("\nelf_attack = {} Round: {}".format(elf_attack, round_counter))
    # print(game)
    print(round_counter * game.total_hitpoints())
