
import operator
from uuid import *
from Brain import *
from Food import *
from random import *
from numpy import *


# these are the cells that populate the dish
class Cell:

    # declarations
    health = 10.00
    hunger = 0.00
    energy = 200
    can_mate = 100
    step = False  # lets us know if we need to move on the next step.
    velocity = [0, 0]
    acc = [0, 0]
    sleep = False
    sleepcounter = 0

    def __init__(self, position, color, tail_length, radius, brain, family, max_acc, max_speed):
        self.position = position
        self.color = color
        self.tail_length = tail_length
        self.radius = radius
        self.body = Circle(Point(self.position[0], self.position[1]), self.radius)
        self.tail = []
        self.brain = brain
        self.maturity = 0
        self.build()
        self.family = family
        self.id = uuid4()
        self.last_thought = Reaction.none
        self.highlighted = False
        self.highlightc = Circle(Point(self.position[0], self.position[1]), 10)
        self.highlightc.setOutline("Green")
        self.killer = False
        self.can_attack = 51
        self.hiding = False
        self.max_acc = max_acc
        self.max_speed = max_speed

    # the following will build the body and tail of he Cell
    def build(self):
        self.body = Circle(Point(self.position[0], self.position[1]), self.radius)
        self.body.setFill(color_rgb(self.color[0], self.color[1], self.color[2]))
        for i in range(0, self.tail_length):
            self.tail.append(Point(self.position[0] - (self.radius*i/2), self.position[1] - (self.radius*i/2)))

    # draws the cell
    def i_draw(self, win):
        self.body.draw(win)
        # for point in self.tail:
        #    point.draw(win)

    # this method will find the nearest food and move towards it
    def eat_food(self, dish):

        closest_food = Food((1000000, 1000000), dish)
        go = False
        for food in dish.food:
            if food.distance(self.position) < closest_food.distance(self.position):
                closest_food = food
                go = True
        if go:
            if closest_food.distance(self.position) <= self.radius:
                self.hunger = 0
                dish.food.remove(closest_food)
                closest_food.eat()
            self.move_towards(closest_food.position, closest_food.distance(self.position))

    # The most important function
    def mate(self, dish):
        closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
        go = False
        for cell in dish.cells:
            if cell.id == self.id or cell.maturity < dish.age_of_maturity or cell.hiding:
                go = go
            elif self.can_mate >= 100 and cell.distance(self.position) < closest_cell.distance(self.position) \
                    and closest_cell.id != self.id:
                closest_cell = cell

                go = True

        if go:
            if closest_cell.distance(self.position) < self.radius:
                chroms = []
                for i in range(0, len(self.brain.chromosomes)):
                    new_chrom = choice([self.brain.chromosomes[i], closest_cell.brain.chromosomes[i]])
                    chroms.append(new_chrom)
                brain = Brain(chroms)
                if self.maturity > dish.age_of_maturity:
                    mycolor = self.color
                    baby = Cell([self.position[0] + 10, self.position[1] + 5],
                                mycolor,
                                choice([self.tail_length, closest_cell.tail_length]),
                                choice([self.radius, closest_cell.radius]), brain,
                                self.family, random.uniform(self.max_acc - 0.3, closest_cell.max_acc + 0.3),
                                random.uniform(self.max_acc - 0.3, closest_cell.max_acc + 0.3))
                    baby.i_draw(dish.win)
                    dish.cells.append(baby)
                    self.health -= 1
                    closest_cell.health -= 3
            if closest_cell.distance(self.position) > 0:
                self.move_towards(closest_cell.position, closest_cell.distance(self.position))

    # Mate but only with a cell from the same family
    def family_mate(self, dish):
        closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
        go = False
        for cell in dish.cells:
            if cell.id == self.id or cell.maturity < dish.age_of_maturity or cell.hiding or not\
                    cell.family == self.family:
                go = go
            elif self.can_mate >= 100 and cell.distance(self.position) < closest_cell.distance(self.position) \
                    and closest_cell.id != self.id:
                closest_cell = cell
                go = True

        if go:
            if closest_cell.distance(self.position) < self.radius:
                chroms = []
                mycolor = self.color
                for i in range(0, len(self.brain.chromosomes)):
                    new_chrom = choice([self.brain.chromosomes[i], closest_cell.brain.chromosomes[i]])
                    chroms.append(new_chrom)
                brain = Brain(chroms)
                if self.maturity > dish.age_of_maturity:
                    baby = Cell([self.position[0] + 10, self.position[1] + 5],
                                mycolor,
                                choice([self.tail_length, closest_cell.tail_length]),
                                choice([self.radius, closest_cell.radius]), brain,
                                self.family, random.uniform(self.max_acc - 0.3, closest_cell.max_acc + 0.3),
                                random.uniform(self.max_acc - 0.3, closest_cell.max_acc + 0.3))
                    baby.i_draw(dish.win)
                    dish.cells.append(baby)
                    self.health -= 1
                    closest_cell.health -= 3
            if closest_cell.distance(self.position) > 0:
                self.move_towards(closest_cell.position, closest_cell.distance(self.position))

    # Mate only with someone who is older than you
    def selective_mate(self, dish):
        closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
        go = False
        for cell in dish.cells:
            if cell.id == self.id or cell.maturity < dish.age_of_maturity or cell.hiding or \
                    cell.maturity < self.maturity:
                go = go
            elif self.can_mate >= 100 and cell.distance(self.position) < closest_cell.distance(self.position) \
                    and closest_cell.id != self.id:
                closest_cell = cell
                go = True

        if go:
            if closest_cell.distance(self.position) < self.radius:
                chroms = []
                mycolor = self.color
                for i in range(0, len(self.brain.chromosomes)):
                    new_chrom = choice([self.brain.chromosomes[i], closest_cell.brain.chromosomes[i]])
                    chroms.append(new_chrom)
                brain = Brain(chroms)
                if self.maturity > 5:
                    baby = Cell([self.position[0] + 10, self.position[1] + 5],
                                mycolor,
                                choice([self.tail_length, closest_cell.tail_length]),
                                choice([self.radius, closest_cell.radius]), brain,
                                self.family, random.uniform(self.max_acc - 0.3, closest_cell.max_acc + 0.3),
                                random.uniform(self.max_acc - 0.3, closest_cell.max_acc + 0.3))
                    dish.cells.append(baby)
                    baby.i_draw(dish.win)
                    self.health -= 1
                    closest_cell.health -= 3
            if closest_cell.distance(self.position) > 0:
                self.move_towards(closest_cell.position, closest_cell.distance(self.position))

    # Hide
    def hide(self, dish):
        i = 0
        close = None
        for spot in dish.hiding_spots:
            if i == 0:
                close = spot
            elif self.distance(spot.position) < self.distance(close.position):
                close = spot

        if self.distance(close.position) < 10:
            self.hiding = True
        else:
            self.move_towards(close.position, self.distance(close.position))

    # this allows the cell to avoid the wall
    def avoid_wall(self, dish):
        to_center = self.distance([dish.size[0] / 2, dish.size[1] / 2])
        self.move_towards((dish.size[0] / 2, dish.size[1] / 2), to_center)

    # this function moves towards any given point
    def move_towards(self, position, magnitude):
        # vector subtraction
        difference = list(map(operator.__sub__, position, self.position))
        # normalisation and assignment
        if magnitude > 0:
            self.acc[0] = (difference[0] / magnitude) * self.max_acc
            self.acc[1] = (difference[1] / magnitude) * self.max_acc
            self.step = True
        # print(self.x_acc)
        # print(self.y_acc)

    # avoid killer
    def avoid(self, position, magnitude):
        # vector subtraction
        difference = list(map(operator.__sub__, position, self.position))
        # normalisation and assignment
        if magnitude > 0:
            self.acc[0] = -(difference[0] / magnitude) * self.max_acc
            self.acc[1] = -(difference[1] / magnitude) * self.max_acc
            self.step = True
        # print(self.x_acc)
        # print(self.y_acc)

    # attack the nearest cell
    def attack(self, dish):
        if self.can_attack > 50:
            closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
            go = False
            for cell in dish.cells:
                if cell.id == self.id or cell.hiding:
                    go = go
                elif cell.distance(self.position) < closest_cell.distance(self.position)\
                        and closest_cell.distance(self.position) > 0:
                    closest_cell = cell
                    go = True
            if go:
                if closest_cell.distance(self.position) <= self.radius:
                    self.hunger = 0
                    if self.hunger < 0:
                        self.hunger = 0
                    closest_cell.health -= 5
                    self.killer = True
                    self.body.setOutline("Red")
                    self.can_attack = 0
                if closest_cell.distance(self.position) > 0:
                    self.move_towards(closest_cell.position, closest_cell.distance(self.position))

    # attack the nearest cell
    def attack_stranger(self, dish):
        if self.can_attack > 50:
            closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
            go = False
            for cell in dish.cells:
                if cell.id == self.id or cell.hiding or cell.family == self.family:
                    go = go
                elif cell.distance(self.position) < closest_cell.distance(self.position)\
                        and closest_cell.distance(self.position) > 0:
                    closest_cell = cell
                    go = True
            if go:
                if closest_cell.distance(self.position) <= self.radius:
                    self.hunger = 0
                    if self.hunger < 0:
                        self.hunger = 0
                    closest_cell.health -= 5
                    self.killer = True
                    self.body.setOutline("Red")
                    self.can_attack = 0
                if closest_cell.distance(self.position) > 0:
                    self.move_towards(closest_cell.position, closest_cell.distance(self.position))

    # avoid the nearest Cell
    def avoid_killer(self, dish):
        closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
        go = False
        for cell in dish.cells:
            if cell.id == self.id or not cell.killer or cell.hiding:
                go = go
            elif cell.distance(self.position) < closest_cell.distance(self.position) \
                    and closest_cell.distance(self.position) > 0:
                closest_cell = cell
                go = True
        if go:
            if closest_cell.distance(self.position) > 0:
                self.avoid(closest_cell.position, closest_cell.distance(self.position))

    # goto Family
    def goto_family(self, dish):
        if self.can_attack > 50:
            closest_cell = Cell([10000, 10000], [0, 0, 0], 2, 2, Brain([]), -1, 0, 0)
            go = False
            for cell in dish.cells:
                if cell.id == self.id or cell.hiding or not cell.family == self.family:
                    go = go
                elif cell.distance(self.position) < closest_cell.distance(self.position)\
                        and closest_cell.distance(self.position) > 0:
                    closest_cell = cell
                    go = True
            if go:
                if closest_cell.distance(self.position) <= self.radius + closest_cell.radius + 4:
                    self.stop()
                if closest_cell.distance(self.position) > 0:
                    self.move_towards(closest_cell.position, closest_cell.distance(self.position))

    # allows the cell to stop moving when needed
    def stop(self):
        if mag(self.velocity) > 0:
            if mag(self.velocity) > 0:
                self.acc[0] = -(self.velocity[0] / mag(self.velocity)) * (mag(self.velocity) / 30)
                self.acc[1] = -(self.velocity[1] / mag(self.velocity)) * (mag(self.velocity) / 30)

    # this function will plan the next thing that the cell will do and then do it
    def plan(self, dish):
        thought = self.brain.think(self, dish)
        if thought == Reaction.eat_food:
            if not self.sleep:
                self.eat_food(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.avoid_wall:
            if not self.sleep:
                self.avoid_wall(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.attack_nearest_cell:
            if not self.sleep:
                self.attack(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.mate:
            if not self.sleep:
                self.mate(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.avoid_killer:
            if not self.sleep:
                self.avoid_killer(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.selective_mate:
            if not self.sleep:
                self.selective_mate(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.family_mate:
            if not self.sleep:
                self.family_mate(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.goto_family:
            if not self.sleep:
                self.goto_family(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.attack_stranger:
            if not self.sleep:
                self.attack_stranger(dish)
            else:
                thought = Reaction.none
        elif thought == Reaction.slow_down:
            if not self.sleep:
                self.stop()
            else:
                thought = Reaction.none
        if thought == Reaction.none:
            self.stop()
        elif thought == Reaction.hide:
            self.hide(dish)
            if self.sleep:
                thought = Reaction.none
        self.last_thought = thought

    # adds the highlight to the cell so that it can be tracked
    def highlight(self, win):
        self.highlightc.draw(win)
        self.highlighted = True

    # removes the highlight from the cell
    def unhighlight(self):
        self.highlighted = False
        self.highlightc.undraw()

    # this is the function that will actually move the cell
    def go(self, dish):
        if self.health <= 0:
            self.body.undraw()
            dish.cells.remove(self)
            food = Food(self.position, dish)
            food.draw(dish.win)
            dish.food.append(food)
            self.highlightc.undraw()
            del self
            return
        self.velocity = list(map(operator.__add__, self.velocity, self.acc))
        if mag(self.velocity) >= self.\
                max_speed:
            self.velocity[0] = (self.velocity[0] / (self.velocity[0]**2 + self.velocity[1]**2)) * self.max_speed
            self.velocity[1] = (self.velocity[1] / (self.velocity[0]**2 + self.velocity[1]**2)) * self.max_speed
        self.body.move(self.velocity[0], self.velocity[1])
        self.highlightc.move(self.velocity[0], self.velocity[1])
        # self.position[0] = self.body.getCenter().getX()
        # self.position[1] = self.body.getCenter().getY()
        self.position = list(map(operator.__add__, self.velocity, self.position))
        if self.energy > 0:
            self.energy -= .1
        else:
            self.sleep = True

        if self.sleep:
            self.sleepcounter += .1
            if self.sleepcounter >= 20:
                self.sleep = False
                self.sleepcounter = 0
                self.energy = 200

        if self.hunger <= 10 and not self.sleep:
            self.hunger += 0.1
        elif self.sleep and self.hunger <= 10:
            self.hunger += 0.05
        self.maturity += 0.01
        self.acc[0] = 0
        self.acc[1] = 0
        if self.can_attack <= 100:
            self.can_attack += 1
        if self.can_mate <= 100:
            self.can_mate += 1
        if self.hunger >= 10:
            self.health -= .02
        elif self.hunger < 10:
            self.hunger += .001 * mag(self.velocity) + 0.002 * mag(self.acc)
            if self.hunger <= 5 and self.health < 10:
                self.health += .02

        if self.position[0] < 0 or self.position[0] > dish.size[0] or self.position[1] < 0 or self.position[1]\
                > dish.size[1]:
            self.body.undraw()
            self.highlightc.undraw()
            dish.cells.remove(self)
            del self
            return

        x = randint(1, 2500)
        if x == 1:
            cbrain = self.brain
            cbrain.chromosomes[randint(0, len(cbrain.chromosomes)) - 1].degree = random.random() * 10
            self.brain = cbrain

        x = randint(1, 5000)
        if x == 1:
            cbrain = self.brain
            cbrain.chromosomes[randint(0, len(cbrain.chromosomes)) - 1] = build_random_chrom()
            self.brain = cbrain
            y = randint(1, 2)
            if y == 1:
                color = [randint(0, 225), randint(0, 225), randint(0, 225)]
                self.color = color
                self.family = uuid4()
                self.body.setFill(color_rgb(self.color[0], self.color[1], self.color[2]))
        self.hiding = False
        for spot in dish.hiding_spots:
            if self.distance(spot.position) < 20:
                self.hiding = True

    # calculates the distance from the cell to any object
    def distance(self, position):
        return math.sqrt(((position[0] - self.position[0]) ** 2) + ((position[1] - self.position[1]) ** 2))


# static methods
def mag(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)

# build a random chromosome
def build_random_chrom():
    stimulants = [Stimulants.nearest_cell, Stimulants.health, Stimulants.wall, Stimulants.food, Stimulants.hunger,
                  Stimulants.nearest_killer, Stimulants.energy, Stimulants.nearest_family, Stimulants.nearest_stranger]
    reactants = [Reaction.attack_nearest_cell, Reaction.avoid_wall, Reaction.eat_food, Reaction.mate,
                 Reaction.avoid_killer, Reaction.hide, Reaction.selective_mate, Reaction.attack_stranger,
                 Reaction.family_mate, Reaction.goto_family, Reaction.slow_down]
    comparison = [Comparison.less_than, Comparison.grater_than]
    return Chromosome(choice(stimulants), choice(reactants), choice(comparison), random.random() * 10)
