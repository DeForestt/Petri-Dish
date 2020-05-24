from enum import Enum


# These enums will allow for readability and simplicity when creating and reading genes.
class Stimulants(Enum):
    food = 0
    hunger = 1
    wall = 2
    health = 3
    nearest_cell = 4
    nearest_killer = 5
    energy = 6
    nearest_family = 7
    nearest_stranger = 8


class Reaction(Enum):
    none = 0
    eat_food = 1
    avoid_wall = 2
    attack_nearest_cell = 3
    goto_cell = 4
    avoid_cell = 5
    avoid_killer = 6
    mate = 7
    hide = 8
    selective_mate = 9
    attack_stranger = 10
    family_mate = 11
    goto_family = 12
    slow_down = 13


class Comparison(Enum):
    less_than = 0
    grater_than = 1
    equal_too = 2


# these are the genes that code for stimulating
class StimGene:
    def __init__(self, stimulant, magnitude):
        self.stimulant = stimulant
        self.magnitude = magnitude


# these will bee the basic unit of design for the brain
class Chromosome:
    def __init__(self, stim_gene, reaction, comparison, degree):
        self.stim_gene = stim_gene
        self.reaction = reaction
        self.comparison = comparison
        self.degree = degree
