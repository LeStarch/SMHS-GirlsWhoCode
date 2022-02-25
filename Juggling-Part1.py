import copy
import pygame
import juggling.pygame

BASE_DATA = {
    "ready": True,
    "position": (0, 0),
    "image": juggling.pygame.SHIP_IMAGE,
    "function": lambda data: None
}
SHIP_DATA_1 = copy.copy(BASE_DATA)
SHIP_DATA_2 = copy.copy(BASE_DATA)


def ship1(data):
    """ Control function for ship 1 """
    pass


def ship2(data):
    """ Control function for ship 2 """
    pass


SHIP_DATA_1["position"] = (0, 100)
SHIP_DATA_2["position"] = (0, 300)
SHIP_DATA_1["function"] = ship1
SHIP_DATA_2["function"] = ship2


def run(data):
    """ Runs the function with the data, if ready """
    if data["ready"]:
        data["function"](data)


def main():
    """ Main program """
    window, clock = juggling.pygame.setup()

    while juggling.pygame.RUN:
        run(SHIP_DATA_1)
        run(SHIP_DATA_2)

        juggling.pygame.draw(window, SHIP_DATA_1, SHIP_DATA_2)
        juggling.pygame.events()
        clock.tick(juggling.pygame.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()