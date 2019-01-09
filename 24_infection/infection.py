#!/usr/bin/env python3

import re
from itertools import chain

class Group:
    def __init__(self, n, hitpoints, weaknesses, immunities, attack, attack_type, initiative, army, id_n):
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
        self.n -= damage // self.hitpoints
        self.n = max(0, self.n)

    def gen_props(self):
        if self.immunities:
            yield "immune to " + ", ".join(x for x in self.immunities)
        if self.weaknesses:
            yield "weak to " + ", ".join(x for x in self.weaknesses)

    def props(self):
        s = "; ".join(self.gen_props())
        if s:
            s = " ({}) ".format(s)
        else:
            s = " "
        return s

    def hypothetical_damage(self, other_group):
        if self.attack_type in other_group.immunities:
            return 0
        if self.attack_type in other_group.weaknesses:
            return 2 * self.n * self.attack
        return self.n * self.attack

    def __str__(self):
        return "{} units each with {} hit points{}with an attack that does {} {} damage at initiative {}".format(
            self.n, self.hitpoints, self.props(), self.attack, self.attack_type, self.initiative
            )

    def str_short(self):
        def army_str(x):
            if x:
                return "Infection"
            else:
                return "Immune System"
        return "{}: group {} contains {} units".format(army_str(self.army), self.id_n+1, self.n)

class Game:
    def __init__(self, groups):
        self.groups = groups

    def iter_groups(self, army):
        yield from (x for x in self.groups if x.army == army)

    def stopping_condition(self):
        army_ids = set()
        for group in self.groups:
            if group.n > 0:
                army_ids.add(group.army)
                if len(army_ids) >= 2:
                    return False

        return True

    def __str__(self):
        return "\n".join(g.str_short() for g in self.groups)

def play_round(game):
    # target selection

    choose_targets = sorted(range(len(game.groups)),
        key=lambda i: (game.groups[i].effective_power(), game.groups[i].initiative),
        reverse=True)
    target = dict()
    targeted = set()

    for index in choose_targets:
        attacker = game.groups[index]
        best_target = max((i for i in range(len(game.groups)) if i not in targeted and game.groups[i].army != attacker.army),
            default = None,
            key = lambda i: (attacker.hypothetical_damage(game.groups[i]), game.groups[i].effective_power(), game.groups[i].initiative)
            )

        if best_target is None:
            continue

        if attacker.hypothetical_damage(game.groups[best_target]) == 0:
            continue

        target[index] = best_target
        targeted.add(best_target)

    # print("target:", target)

    # Attacking phase

    attack_order = sorted(range(len(game.groups)), key=lambda i: game.groups[i].initiative,
        reverse=True)

    for attacker_index in attack_order:

        t = target.get(attacker_index, None)
        if t is None:
            continue

        attacker = game.groups[attacker_index]
        defender = game.groups[t]
        damage = attacker.hypothetical_damage(defender)

        # print(attacker.str_short(), "dealing {} damage to".format(damage), defender.str_short())
        defender.take_damage(damage)

    # Remove dead groups

    i = 0
    while i < len(game.groups):
        if game.groups[i].n:
            i += 1
        else:
            game.groups.pop(i)

def play_game(game):
    # print(game)

    while True:
        play_round(game)
        # print("--------------------")
        # print(game)
        # print("--------------------")
        if game.stopping_condition():
            break
        # else:
        #     input()

    return sum(g.n for g in game.groups)

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
    numbers = re.compile("\d+")
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

if __name__=="__main__":
    groups = read_file("24_infection/input.txt")

    g = Game(groups)
    print(play_game(g))
