""" lesson 1: cooperative parallelism

This will establish the basis for the multi-threading lesson. This particular lesson will show what the world is like
before threads.  Students should inspect the "move" function to understand what it does. Then students should inspect
the "ship1" and "ship2" functions that are called from "move".
"""
import time

from juggling.data import Ship
from juggling.pygame import main


def ship1(ship):
    """ Control function for ship 1 """
    # Update ship one: sleep 100ms and then move
    time.sleep(0.100)
    # Read ship position into x, y and then update the position to x + 1, y
    x, y = ship.position
    ship.position = x + 1, y


def ship2(ship):
    """ Control function for ship 2 """
    x, y = ship.position
    ship.position = x + 1, y


# Create two ships as global variables. Why use evil globals? It's EASY!
SHIP_1 = Ship(100)
SHIP_2 = Ship(300)


def move():
    """ Move the ships using two functions

    This version of move is a form of cooperative multithreading. In essence, function writes agree that each call to
    their function does a small (one)  unit of work. Calling the functions in an interleaving fashion virtualizes
    multiple programs operating at once. This does imply:

    1. Function implementors must behave, don't do long amounts of work in the function (sleeps, big calculations)
    2. Functions still affect one another, however; in this case the code is separated
    3. Our "ship1" function is poorly behaved (it sleeps) and delays ship2 still

    CHALLENGE: can you fix ship1 to be slow while keeping ship2 fast? Hint: time.time() gets the current time.
    """
    ship1(SHIP_1)
    ship2(SHIP_2)


if __name__ == "__main__":
    main(move, SHIP_1, SHIP_2)
