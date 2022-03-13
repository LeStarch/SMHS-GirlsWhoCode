""" juggling.data:

Sets up the data/positions for the ship-based lessons. This is just to remove code duplication and keep the lessons
clean.  Not much has changed here since our original pygame lessons.
"""
from juggling.pygame import SHIP_IMAGE


class Ship(object):
    """ Data package for controlling ships in part 0 - part 3.

    This data contains the basic information for controlling ships, namely the position and the image. It is a class
    (as opposed to variable, or a map) because the '.' operator is more readable (e.g. player.image opposed to
    player["image"]). It also means we don't need to write a bunch of copy calls to build separate ships.

    We can also attach some helpful functions like "draw" to draw the ship and keep the code well organized.
    """
    def __init__(self, y_position):
        """ Builds the object """
        self.ready = True  # Ready to run flag
        self.position = (0, y_position)
        self.image = SHIP_IMAGE
        self.thread = None # Assigned only in the thread lesson (part 2)

    def draw(self, window):
        """ Draw the ship data into the window

        Draws ship into the supplied window. In short: it puts the image at whatever position is set in the class. It
        does this cia pygame and should be called through the program.
        """
        window.blit(self.image, self.position)

