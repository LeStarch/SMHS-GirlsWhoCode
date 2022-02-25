import copy
import time
import threading


import pygame
import juggling.pygame

BASE_DATA = {
    "position": (0, 0),
    "image": juggling.pygame.SHIP_IMAGE,
    "function": lambda data: None,
    "thread": None
}
SHIP_DATA_1 = copy.copy(BASE_DATA)
SHIP_DATA_2 = copy.copy(BASE_DATA)


def ship1(data):
    """ Control function for ship 1 """
    while juggling.pygame.RUN:
        pass


def ship2(data):
    """ Control function for ship 2 """
    while juggling.pygame.RUN:
        pass


SHIP_DATA_1["position"] = (0, 100)
SHIP_DATA_2["position"] = (0, 300)
SHIP_DATA_1["function"] = ship1
SHIP_DATA_2["function"] = ship2


def start_threads(*items):
    """ Setup threads for the run """
    for item in items:
        item["thread"] = threading.Thread(target=item.get("function"), args=(item,))
        item["thread"].start()


def main():
    """ Main program """
    window, clock = juggling.pygame.setup()
    start_threads(SHIP_DATA_1, SHIP_DATA_2)

    while juggling.pygame.RUN:
        juggling.pygame.draw(window, SHIP_DATA_1, SHIP_DATA_2)
        juggling.pygame.events()
        clock.tick(juggling.pygame.FPS)

    for item in [SHIP_DATA_1, SHIP_DATA_2]:
        item.get("thread").join()
    pygame.quit()


if __name__ == "__main__":
    main()