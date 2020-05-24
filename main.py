from Dish import Dish


def main():
    stage = Dish((1500, 700), 20)
    stage.populate()
    stage.draw()
    stage.run()


main()
