from graphics import *
from random import *
from numpy import *
from uuid import *
from Cell import Cell
from Food import *
from Brain import Brain
from Chrom import *
from Food import Food


class Dish:
    def __init__(self, size, min_pop):
        # set window attributes
        self.size = size
        self.win = GraphWin("Dish", size[0], size[1])

        # Init list properties
        self.cells = []
        self.food = []
        self.seeds = []
        self.seedlings = []
        self.hiding_spots = []

        # init other properties
        self.cell_count = 0
        self.min_pop = min_pop
        self.food_rate = 100
        self.age_of_maturity = 7

        # init draw info menu
        self.brain_of_oldest = Text(Point(self.win.getWidth() * .75, 90), "")
        self.brain_of_oldest.setFill("White")
        self.oldest = Text(Point(self.win.getWidth() * .75, 50), "")
        self.oldest.setFill("White")
        self.population = Text(Point(self.win.getWidth() * .75, 30), "")
        self.population.setFill("White")
        self.average_age = Text(Point(self.win.getWidth() * .75, 70), "Click Mouse to Continue")
        self.average_age.setFill("White")
        self.vbrain = Text(Point(self.win.getWidth() * .20, 110), "")
        self.vbrain.setFill("White")
        self.vbrain.setSize(10)
        self.stats = Text(Point(self.win.getWidth() * .50, 50), "")
        self.stats.setSize(10)
        self.stats.setFill("White")
        self.families = Text(Point(self.win.getWidth() * .75, 10), "")
        self.families.setFill("White")

        # these properties allow the user to follow a particular cell
        self.hid = 0
        self.index_of_h = 0

    # Set the starting conditions for the dish
    def populate(self):
        # generate the hiding spots
        for i in range(0, 5):
            self.hiding_spots.append(HidingSpot([randrange(self.size[0]),
                                                 randrange(self.size[1])]))

        # Populate the dish with a starting number of cells
        for i in range(0, self.min_pop):
            new_cell = Cell([randrange(self.size[0]), randrange(self.size[1])],
                            [randrange(225), randrange(225),
                             randrange(225)], randrange(10), randint(3, 5), build_random_brain(10), uuid4(),
                            random.uniform(3, 5), random.uniform(3, 5))
            self.cells.append(new_cell)
            self.cell_count += 1

    # draw an updated image to the screen
    def draw(self):
        self.win.setBackground("Black")

        # draw hiding spots
        for spot in self.hiding_spots:
            spot.draw(self.win)

        # draw all cells
        for cell in self.cells:
            cell.i_draw(self.win)

        # draw food
        for food in self.food:
            food.draw(self.win)

        # draw info menu
        self.population.setText(len(self.cells))
        self.population.draw(self.win)
        self.oldest.setText(self.cells[0].maturity)
        self.oldest.draw(self.win)
        self.average_age.draw(self.win)
        self.brain_of_oldest.draw(self.win)
        self.vbrain.draw(self.win)
        self.stats.draw(self.win)
        self.families.draw(self.win)

        self.win.getMouse()  # wait to start

    # the run loop for the dish
    def run(self):
        while 1 == 1:
            aage = 0  # the average age
            i = 0

            # count up the number of cell families
            fams = set()
            reset = True
            for cell in self.cells:
                if cell.family not in fams:
                    fams.add(cell.family)
                if cell.highlighted:
                    self.index_of_h = i
                    self.hid = cell.id
                    reset = False
                cell.plan(self)

                aage += cell.maturity  # add cell age to the average
                cell.go(self)  # run each cell
                i += 1
            aage = aage / len(self.cells)  # calculate average age

            # find the index of the highlighted cell
            if reset:
                if len(self.cells) <= self.index_of_h:
                    self.hid = self.cells[self.index_of_h].id
                    self.cells[self.index_of_h].highlight(self.win)
                else:  # default to the oldest cell
                    self.index_of_h = 0
                    self.hid = self.cells[self.index_of_h].id
                    self.cells[self.index_of_h].highlight(self.win)

            # place food based on the probability input by the user
            x = randrange(0, 100)
            if x <= self.food_rate:
                new_food = Food([randrange(0, self.size[0]),
                                 randrange(0, self.size[1])], self)
                self.food.append(new_food)
                new_food.draw(self.win)

            # repopulate if population is too low
            while len(self.cells) < self.min_pop:
                new_cell = Cell([randrange(self.size[0]), randrange(self.size[1])],
                                [randrange(225), randrange(225),
                                 randrange(225)], randrange(10), randint(5, 7),
                                build_random_brain(10), uuid4(), random.uniform(3, 5), random.uniform(3, 5))
                self.cells.append(new_cell)
                new_cell.i_draw(self.win)

            # update info menu
            self.population.setText("Population: " + str(len(self.cells)))
            try:
                self.oldest.setText("Age of highlight: " + str(int(self.cells[self.index_of_h].maturity)))
                self.average_age.setText("Average Age: " + str(int(aage)))
                self.brain_of_oldest.setText("Thought of highlight: " + str(self.cells[self.index_of_h].last_thought))
                text = ""
                for chrom in self.cells[self.index_of_h].brain.chromosomes:
                    text = text + "\n if " + str(chrom.stim_gene) + " " + str(chrom.comparison) + " " + \
                           str(round(chrom.degree, 4)) + " then " + str(chrom.reaction)
                self.vbrain.setText("highlight brain: " + text)
                self.stats.setText("Stats: " + "Health: " + str(round(self.cells[self.index_of_h].health, 2)) +
                                   "\nHunger: " + str(round(self.cells[self.index_of_h].hunger, 2)) + "\nEnergy: " +
                                   str(round((self.cells[self.index_of_h].energy / 200) * 10, 2)) + "\n Family: " +
                                   str(self.cells[self.index_of_h].family))
                self.families.setText("Families: " + str(len(fams)))
            except IndexError:
                print("Error")

            # poor man's event handling to check if the p key is pressed this will allow the simulation to
            # paused and a new highlight to be selected
            net = self.win.checkKey()
            if net == 'p':
                position = self.win.getMouse()
                print(position)
                i = 0
                for cell in self.cells:
                    if cell.body.getCenter().x + cell.radius > position.x > cell.body.getCenter().x - cell.radius and \
                            cell.body.getCenter().y + cell.radius > position.y > cell.body.getCenter().y - cell.radius:
                        for cell2 in self.cells:
                            cell2.unhighlight()
                        cell.highlight(self.win)
                        self.index_of_h = i
                        self.hid = cell.id
                        self.population.setText("Population: " + str(len(self.cells)))
                        self.oldest.setText("Age of highlight: " + str(int(self.cells[self.index_of_h].maturity)))
                        self.average_age.setText("Average Age: " + str(int(aage)))
                        self.brain_of_oldest.setText(
                            "Thought of highlight: " + str(self.cells[self.index_of_h].last_thought))
                        text = ""
                        for chrom in self.cells[self.index_of_h].brain.chromosomes:
                            text = text + "\n if " + str(chrom.stim_gene) + " " + str(chrom.comparison) + " " + str(
                                round(chrom.degree, 4)) + " then " + str(chrom.reaction)
                        self.vbrain.setText("highlight brain: " + text)
                    i += 1
            # same for settings
            elif net == 's':
                prompt1 = Text(Point(self.size[0] / 2 - 10, self.size[1] / 2), "Food Spawn Rate: ")
                prompt1.setTextColor("White")
                mfood = Entry(Point(self.size[0] / 2 + 100, self.size[1] / 2), 10)
                mfood.setText(str(self.food_rate))
                prompt1.draw(self.win)
                mfood.draw(self.win)
                prompt2 = Text(Point(self.size[0] / 2 - 10, self.size[1] / 2 - 20), "Minimum Population: ")
                prompt2.setTextColor("White")
                mpop = Entry(Point(self.size[0] / 2 + 100, self.size[1] / 2 - 20), 10)
                mpop.setText(str(self.min_pop))
                mpop.draw(self.win)
                prompt2.draw(self.win)
                prompt3 = Text(Point(self.size[0] / 2 - 10, self.size[1] / 2 + 20), "Age of adulthood: ")
                prompt3.setTextColor("White")
                adult = Entry(Point(self.size[0] / 2 + 100, self.size[1] / 2 + 20), 10)
                adult.setText(str(self.age_of_maturity))
                adult.draw(self.win)
                prompt3.draw(self.win)

                self.win.getMouse()

                if mfood.getText().isdigit():
                    self.food_rate = int(mfood.getText())
                if mpop.getText().isdigit():
                    self.min_pop = int(mpop.getText())
                if adult.getText().isdigit():
                    self.age_of_maturity = int(adult.getText())

                mfood.undraw()
                prompt3.undraw()
                prompt2.undraw()
                prompt1.undraw()
                mpop.undraw()
                adult.undraw()
                del mfood
                del mpop
                del adult
                del prompt1
                del prompt2
                del prompt3


# makes brains for the cells to hace
def build_random_brain(size):
    chroms = []
    for i in range(0, size):
        chroms.append(build_random_chrom())
    return Brain(chroms)


# builds chromosomes for the brain
def build_random_chrom():
    stimulants = [Stimulants.nearest_cell, Stimulants.health, Stimulants.wall, Stimulants.food, Stimulants.hunger,
                  Stimulants.nearest_killer, Stimulants.energy, Stimulants.nearest_family, Stimulants.nearest_stranger]
    reactants = [Reaction.attack_nearest_cell, Reaction.avoid_wall, Reaction.eat_food, Reaction.mate,
                 Reaction.avoid_killer, Reaction.hide, Reaction.selective_mate, Reaction.attack_stranger,
                 Reaction.family_mate, Reaction.goto_family, Reaction.slow_down]
    comparison = [Comparison.less_than, Comparison.grater_than]

    return Chromosome(choice(stimulants), choice(reactants), choice(comparison), random.random() * 10)


class HidingSpot:

    def __init__(self, position):
        self.position = position
        self.spot = Circle(Point(self.position[0], self.position[1]), 20)

    def draw(self, win):
        self.spot.setFill(color_rgb(135, 206, 250))
        self.spot.draw(win)
