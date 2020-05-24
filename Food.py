from Dish import *
import math


# Food for the cell to eat
class Food:

    def __init__(self, position, dish):
        self.position = position
        self.food = Circle(Point(self.position[0], self.position[1]), 2)
        self.dish = dish

    def draw(self, win):
        self.food.setFill(color_rgb(102, 255, 102))
        self.food.draw(win)
        for spot in self.dish.hiding_spots:
            if self.distance(spot.position) < 100:
                self.eat()

    # calculates the distance from the food to any object
    def distance(self, position):
        return math.sqrt(((position[0] - self.position[0])**2) + ((position[1] - self.position[1])**2))

    # when the food gets eaten.
    def eat(self):
        self.food.undraw()
