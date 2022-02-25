import pygame

# Basic constants
SCREEN = (800, 600)
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}
FPS = 60

# Images
SHIP_IMAGE = pygame.image.load("Related/spaceship_red.png")
SHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(SHIP_IMAGE, (100, 100)), 90)


# Global variables
RUN = True


def setup():
    """ Sets up pygame's display etc. """
    pygame.display.set_caption("Part 1: Something 1")
    return pygame.display.set_mode(SCREEN), pygame.time.Clock()


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
    window.fill(COLORS["black"])
    for item in items:
        window.blit(item.get("image"), item.get("position"))
    pygame.display.update()
