#!/usr/bin/env python3

from copy import deepcopy

class Group:
    def __init__(self, n, hitpoints, weaknesses, immunities, attack,
            attack_type, initiative, army, id_n):
        self.n = n
        self.hitpoints = hitpoints
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.army = army
        self.id_n = id_n

    def effective_power(self):
        return self.n * self.attack

    def take_damage(self, damage):
        casualties = damage // self.hitpoints
        self.n = max(0, self.n - casualties)
        return casualties

    def hypothetical_damage(self, other_group):
        if self.attack_type in other_group.immunities:
            return 0
        if self.attack_type in other_group.weaknesses:
            return 2 * self.n * self.attack
        return self.n * self.attack

    def __str__(self):
        def army_str(x):
            if x:
                return "Infection"
            else:
                return "Immune System"
        return "{}: group {} contains {} units".format(
            army_str(self.army), self.id_n+1, self.n
            )

def stopping_condition(groups):
    army_ids = set()
    for group in groups:
        if group.n > 0:
            army_ids.add(group.army)
            if len(army_ids) >= 2:
                return False

    return True

class Stalemate(Exception):
    pass

def play_round(groups):
    # target selection

    order = sorted(range(len(groups)),
        key=lambda i: (groups[i].effective_power(), groups[i].initiative),
        reverse=True)
    target = dict()
    targeted = set()

    for index in order:
        attacker = groups[index]
        best_target = max(
            (i for i in range(len(groups)) if\
                i not in targeted and groups[i].army != attacker.army),
            default = None,
            key = lambda i: (
                attacker.hypothetical_damage(groups[i]),
                groups[i].effective_power(),
                groups[i].initiative
                )
            )

        if best_target is None or\
                attacker.hypothetical_damage(groups[best_target]) == 0:
            continue

        target[index] = best_target
        targeted.add(best_target)

    # Attacking phase

    order = sorted(target.keys(),
        key=lambda i: groups[i].initiative,
        reverse=True)
    damage_done = False

    for index in order:

        attacker = groups[index]
        defender = groups[target[index]]
        damage = attacker.hypothetical_damage(defender)

        # print(str(attacker), "dealing {} damage to".format(damage), str(defender))
        casualties = defender.take_damage(damage)
        if casualties:
            damage_done = True

    if not damage_done:
        raise Stalemate()

    # Remove dead groups

    i = 0
    while i < len(groups):
        if groups[i].n:
            i += 1
        else:
            groups.pop(i)

def play_game(groups, boost=0, cache=dict()):
    if boost in cache:
        return cache[boost]
    # print("Evaluating with boost = {}".format(boost))
    groups = deepcopy(groups)

    # boost for immune system
    for g in groups:
        if g.army == 0:
            g.attack += boost
    # print("\n".join(map(str, groups)))

    while not stopping_condition(groups):
        play_round(groups)
        # print("--------------------")
        # print("\n".join(map(str, groups)))
        # print("--------------------")
        # input()

    ret = sum(g.n for g in groups), groups[0].army
    cache[boost] = ret
    return ret

def read_group(group, army, id_n):

    words = group.split()

    n = int(words[0])
    hitpoints = int(words[4])
    attack = int(words[-6])
    attack_type = words[-5]
    initiative = int(words[-1])

    wi = [[], []]
    try:
        t = group.index('(')
        c = group.index(')')
        s = group[t+1:c].split()
    except ValueError:
        s = []

    w = 0

    for i in s:
        if i == "weak":
            w = 0
        elif i == "immune":
            w = 1
        elif i == "to":
            continue
        else:
            wi[w].append("".join(x for x in i if ord('a') <= ord(x.lower()) <= ord('z')))

    return Group(n, hitpoints, wi[0], wi[1], attack, attack_type, initiative, army, id_n)

def read_file(fname):
    groups = []
    ids = [0, 0]
    army = 0
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith("Immune"):
                continue

            elif line.startswith("Infection"):
                army = 1
                continue

            elif not line.strip():
                continue

            groups.append(read_group(line, army, ids[army]))
            ids[army] += 1

    return groups

def bisection(groups, left, right):
    # Find smallest value i s.t. f(i) = True

    def f(boost):
        try:
            remaining, army = play_game(groups, boost)
        except Stalemate:
            return False
        return army == 0

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
    groups = read_file("24_infection/input.txt")

    # part 1
    remaining, army = play_game(groups)
    print(remaining)

    # part 2
    required_boost = bisection(groups, 0, 200)
    # print(required_boost)
    remaining, army = play_game(groups, boost=required_boost)
    print(remaining)
