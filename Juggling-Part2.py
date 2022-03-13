""" lesson 3: threaded parallelism

This will establish the basis for the multi-threading lesson. This particular lesson will show what the world is like
before threads.  Students should note that there **is no** move function. Here we creat some threads. Effectively asking
the OS "please juggle these functions for us". Each function is independent.

Students should inspect the "ship1" and "ship2" functions. They can be viewed as entirely separate functions.
"""
import time
import threading

import juggling.pygame
from juggling.data import Ship
from juggling.pygame import main


# Create two ships as global variables. Why use evil globals? It's EASY!
SHIP_1 = Ship(100)
SHIP_2 = Ship(300)


def ship1(ship):
    """
    Control function for ship1. This function is passed the ship as input and is free to update it. Students should
    notice that this function has an infinite while loop to continually updating the ship's data. Since this is
    effectively a separate program, it will run only until it reaches the end of the function.

    CHALLENGE: can you slow ship1 without slowing ship2
    """
    while juggling.pygame.RUN:
        x, y = ship.position
        ship.position = x + 1, y
        time.sleep(0.010)  # No pygame FPS delay (effectively a separate program) so we need our own delay


def ship2(ship):
    """
    Control function for ship2. This function is passed the ship as input and is free to update it. Students should
    notice that this function has an infinite while loop to continually updating the ship's data. Since this is
    effectively a separate program, it will run only until it reaches the end of the function.
    """
    while juggling.pygame.RUN:
        x, y = ship.position
        ship.position = x + 1, y
        time.sleep(0.010)  # No pygame FPS delay (effectively a separate program) so we need our own dela


def start_threads():
    """ Start ships threads

    This is where we ask the operating system to start our threads to run the ships. We assign the threads to out ship
    object such that we can "join" later and ensure that they exit before we exit the program
    """
    # Create the threads
    SHIP_1.thread = threading.Thread(target=ship1, args=(SHIP_1,))
    SHIP_2.thread = threading.Thread(target=ship2, args=(SHIP_2,))
    # Start the threads
    SHIP_1.thread.start()
    SHIP_2.thread.start()


def wait_threads():
    """ Waits for the ship threads before exit

    Waits for threads so that they are not running while we try to exit.
    """
    SHIP_1.thread.join()  # Wait for ship1 thread
    SHIP_2.thread.join()  # Wait for ship2 thread


if __name__ == "__main__":
    # Do nothing move function, just run the drawing loop!
    start_threads()
    main(lambda: None, SHIP_1, SHIP_2)
    wait_threads()
