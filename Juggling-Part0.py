""" lesson 0: no parallelism

This will establish the basis for the multi-threading lesson. This particular lesson will show what the world is like
before threads.  Students should inspect the "move" function to understand what it does.
"""
import time
from juggling.data import Ship
from juggling.pygame import main

# Create two ships as global variables. Why use evil globals? It's EASY!
SHIP_1 = Ship(100)
SHIP_2 = Ship(300)


def move():
    """ Function to move the ships.

    This is the single thread model. As seen here, the work for both ships is contained within one function. Thus, a
    programmer must juggle the work by-hand. When the work becomes complicated or takes time, the other model is
    affected.

    Things to note:
    1. See the change in position for each ship
    2. Notice the sleep call here to slow ship1
    3. Notice that the slower ship1 causes ship2 to also be slow.
    """
    # Update ship one: sleep 100ms and then move
    time.sleep(0.100)
    # Read ship position into x, y and then update the position to x + 1, y
    x, y = SHIP_1.position
    SHIP_1.position = x + 1, y

    # Now handle the ship two's position. Ship 2 does not want a sleep (to be faster)
    x, y = SHIP_2.position
    SHIP_2.position = x + 1, y
    # Was ship 2 actually faster


if __name__ == "__main__":
    main(move, SHIP_1, SHIP_2)
