# This is a separate class for the thinking of the cell, this is just to make it easier to handle
# The brain is made up of a collection of 10 "chromosomes" which will control the cell's behavior

from Chrom import *
import math


class Brain:

    def __init__(self, chromosomes):
        self.chromosomes = chromosomes

    def think(self, cell, dish):
        # cycle through each chromosome in the brain
        for chrom in self.chromosomes:
            # Distance of Food
            if chrom.stim_gene == Stimulants.food:
                if chrom.comparison == Comparison.grater_than:
                    for food in dish.food:
                        if food.distance(cell.position) >= (chrom.degree/10) * mag(dish.size):
                            return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    for food in dish.food:
                        if food.distance(cell.position) < (chrom.degree/10) * mag(dish.size):
                            return chrom.reaction
            # How hungary you are.
            elif chrom.stim_gene == Stimulants.hunger:
                if chrom.comparison == Comparison.grater_than:
                    if cell.hunger >= chrom.degree:
                        return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    if cell.hunger < chrom.degree:
                        return chrom.reaction
            # How far is the wall
            elif chrom.stim_gene == Stimulants.wall:
                if chrom.comparison == Comparison.grater_than:
                    if abs(cell.position[0] - dish.size[0]/2) >= (chrom.degree/10) * (mag(dish.size) / 2):
                        return chrom.reaction
                    if abs(cell.position[1] - dish.size[1]/2) >= (chrom.degree/10) * (mag(dish.size) / 2):
                        return chrom.reaction
                if chrom.comparison == Comparison.less_than:
                    if abs(cell.position[0] - dish.size[0]/2) < (chrom.degree/10) * (mag(dish.size) / 2):
                        return chrom.reaction
                    if abs(cell.position[1] - dish.size[1]/2) < (chrom.degree/10) * (mag(dish.size) / 2):
                        return chrom.reaction
            # How healthy am I
            elif chrom.stim_gene == Stimulants.health:
                if chrom.comparison == Comparison.grater_than:
                    if cell.health >= chrom.degree:
                        return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    if cell.health < chrom.degree:
                        return chrom.reaction
            # Distance of nearest Cell
            elif chrom.stim_gene == Stimulants.nearest_cell:
                if chrom.comparison == Comparison.grater_than:
                    for cello in dish.cells:
                        if cell.distance(cello.position) >= (chrom.degree / 10) * mag(dish.size)\
                                and cell.id != cello.id:
                            return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    for cello in dish.cells:
                        if cello.id == cell.id:
                            chrom.comparison = chrom.comparison
                        elif cell.distance(cello.position) < (chrom.degree / 10) * mag(dish.size):
                            return chrom.reaction
            # Distance to nearest killer
            elif chrom.stim_gene == Stimulants.nearest_killer:
                if chrom.comparison == Comparison.grater_than:
                    for cello in dish.cells:
                        if cello.id == cell.id or not cello.killer:
                            chrom.comparison = chrom.comparison
                        elif cell.distance(cello.position) >= (chrom.degree / 10) * mag(dish.size):
                            return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    for cello in dish.cells:
                        if cello.id == cell.id or not cello.killer:
                            chrom.comparison = chrom.comparison
                        elif cell.distance(cello.position) < (chrom.degree / 10) * mag(dish.size):
                            return chrom.reaction
            # How tiered am I
            elif chrom.stim_gene == Stimulants.energy:
                if chrom.comparison == Comparison.grater_than:
                    if cell.energy >= (chrom.degree / 10) * 200:
                        return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    if cell.energy < (chrom.degree / 10) * 200:
                        return chrom.reaction
            # Distance of nearest Family
            elif chrom.stim_gene == Stimulants.nearest_family:
                if chrom.comparison == Comparison.grater_than:
                    for cello in dish.cells:
                        if cello.id == cell.id:
                            chrom.comparison = chrom.comparison
                        elif cello.family == cell.family and cell.distance(cello.position) >= (chrom.degree / 10) * \
                                mag(dish.size) and cell.distance(cello.position) > 0:
                            return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    for cello in dish.cells:
                        if cello.id == cell.id:
                            chrom.comparison = chrom.comparison
                        elif cello.family == cell.family and cell.distance(cello.position) < (chrom.degree / 10) * \
                                mag(dish.size) > 0:
                            return chrom.reaction
            # Distance of nearest stranger
            elif chrom.stim_gene == Stimulants.nearest_stranger:
                if chrom.comparison == Comparison.grater_than:
                    for cello in dish.cells:
                        if cello.id == cell.id:
                            chrom.comparison = chrom.comparison
                        elif not cello.family == cell.family and cell.distance(cello.position) >= (chrom.degree / 10) \
                                * mag(dish.size):
                            return chrom.reaction
                elif chrom.comparison == Comparison.less_than:
                    for cello in dish.cells:
                        if cello.id == cell.id:
                            chrom.comparison = chrom.comparison
                        elif not cello.family == cell.family and cell.distance(cello.position) < (chrom.degree / 10) * \
                                mag(dish.size):
                            return chrom.reaction
        return Reaction.none


def mag(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)
