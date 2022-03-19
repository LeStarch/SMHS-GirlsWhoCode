
import pygame
from .utilities import CellType

from random import randint

# Basic constants
SCREEN = (1900, 1080)
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    CellType.WALL: (120, 50, 0),
    CellType.PATH: (0, 0, 0),
    CellType.EXIT: (0, 255, 0)
}
IMAGES = {
    CellType.WALL: pygame.image.load("Related/wall.png"),
    CellType.PATH: pygame.image.load("Related/path.png"),
    CellType.EXIT: pygame.image.load("Related/exit.png")
}


FPS = 60
# Images
SHIP_IMAGE = pygame.image.load("Related/spaceship_red.png")
SHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(SHIP_IMAGE, (100, 100)), 90)

FONT, FONT_END = None, None

# Global variables
RUN = True


def setup(caption="You Forgot to Set A Caption, Michael..."):
    """ Sets up pygame's display etc. """
    global FONT, FONT_END
    pygame.init()
    FONT = pygame.font.SysFont("ariel.ttf", 32)
    FONT_END = pygame.font.SysFont("ariel.ttf", 256)
    pygame.display.set_caption(caption)
    return pygame.display.set_mode((1400, 900), pygame.RESIZABLE), pygame.time.Clock()


def events():
    """ Check the current events and exit """
    global RUN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False


def draw(window, *items):
    """ Update the scene from two positions

    Compose the scene into the given window and a list of positions of ships that you want to draw.

    :param window: window to draw the scene into
    :param items: any number of data items used to draw ships
    """
    #window.fill(COLORS["black"])
    for item in items:
        item.draw(window)
    pygame.display.update()


def main(move, *items):
    """ Main program """
    window, clock = setup()

    while RUN:
        move()
        draw(window, *items)
        events()
        clock.tick(FPS)
    pygame.quit()
