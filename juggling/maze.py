""" maze.py

Handling for mazes in the pygame context. This contains algorithms for generating and solving the maze.
"""
import copy
import threading
from enum import Enum
from typing import Tuple, Union
from random import randint
import itertools
import juggling.pygame

import pygame
from .utilities import Direction, CellType, RandomWalk, FloodFill

PLAYER_IMAGE = pygame.image.load("Related/player1.png")
TON_IMAGE = pygame.image.load("Related/ton.png")


class Difficulty(Enum):
    """ Difficultly of the game """
    EASY = RandomWalk()
    HARD = FloodFill(4)
    VERY_HARD = FloodFill(1)


class Cell(object):
    """ A cell class """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.type = CellType.PATH

    def __add__(self, other: Union[Direction, Tuple[int, int]]):
        """ Add a step to this cell to get a new cell"""
        x, y = other.value if isinstance(other, Direction) else other
        new_x = x + self.x
        new_y = y + self.y
        return new_x, new_y

    def __sub__(self, other: "Cell"):
        """ Sub a cell from this to get a step """
        x, y = other.x, other.y
        return self.x - x, self.y - y

    def __eq__(self, other):
        """ Check for equality from coordinates """
        x, y = (other.x, other.y) if isinstance(other, Cell) else other
        return self.x == x and self.y == y

    def __repr__(self):
        return f"({self.x},{self.y}) {self.type.name}"

    def draw(self, window, cell_size, color=None, debug=False):
        """ """
        cell_type = self.type
        color = juggling.pygame.COLORS[cell_type] if color is None else color

        rect = pygame.Rect((self.x + 1) * cell_size, (self.y + 1) * cell_size,
                           cell_size, cell_size)
        # Fill
        pygame.draw.rect(window, color, rect)

        attr = getattr(self, "score", None)
        if attr is not None and debug:
            text = juggling.pygame.FONT.render(str(attr), True, juggling.pygame.COLORS["white"],
                                               juggling.pygame.COLORS["black"])
            window.blit(text, ((self.x + 1) * cell_size, (self.y + 1) * cell_size))

        # Border
        pygame.draw.rect(window, juggling.pygame.COLORS["white"], rect, 2)


class Player(object):
    def __init__(self, image=PLAYER_IMAGE):
        self.x = 0
        self.y = 0
        self.game = None
        self.image = None
        self.original_image = image
        self.waiting = threading.Event()
        self.next_x = None
        self.next_y = None
        self.lock = threading.Lock()

    def set_game(self, game):
        """
        Sets a callback to the game for the player to reference
        :param game: game object
        """
        self.game = game

    def __repr__(self):
        """ """
        return f"{type(self).__name__} @ ({self.x}, {self.y})"

    def start(self, item):
        """ Start the player at the given cell """
        self.x, self.y = (item.x, item.y) if isinstance(item, Cell) else item

    def look(self, direction: Direction):
        """ Retrieve cell in direction """
        next_cell = self.game.maze[self.game.maze[self] + direction]
        return next_cell.type, Player.collided(self.game.ai_player, next_cell)

    def get_scaled_image(self, cell_size):
        """ Get a scaled image """
        if self.image is None or self.image.get_size() != (cell_size, cell_size):
            self.image = pygame.transform.scale(self.original_image, (cell_size, cell_size))
        return self.image

    def move(self, direction):
        """ Wait for the next round, then move """
        # Wait for the next round, as called by the game, them immediately clear waiting state
        current_cell = self.game.maze[self]
        new_cell = self.game.maze[current_cell + direction]
        with self.lock:
            if new_cell.type != CellType.WALL:
                self.next_x, self.next_y = new_cell.x, new_cell.y
            else:
                self.next_x, self.next_y = self.x, self.y
        self.waiting.wait()
        self.waiting.clear()

    def update(self):
        """ Update the position now """
        with self.lock:
            if self.next_x is not None and self.next_y is not None:
                self.x = self.next_x
                self.y = self.next_y

    def unblock(self):
        self.waiting.set()

    def draw(self, window, cell_size):
        """ Draw a player """
        x, y = self.x, self.y
        window.blit(self.get_scaled_image(cell_size), ((x + 1) * cell_size, (y + 1) * cell_size))

    @staticmethod
    def collided(item1, item2):
        """ Check if the two players have collided """
        x1, y1 = item1.x, item1.y if isinstance(item1, (Cell, Player)) else item1
        x2, y2 = item2.x, item2.y if isinstance(item2, (Cell, Player)) else item2
        collided = x1 == x2 and y1 == y2
        return collided


class AiPlayer(Player):
    """ An automated player that knows how to solve the maze """

    def __init__(self, difficulty):
        """"""
        super().__init__(image=TON_IMAGE)
        self.difficulty = difficulty
        self.thread = threading.Thread(target=self.hunter_thread)

    def hunter_thread(self):
        """ Hunt the player until we are told to stop """
        while not self.game.gameover.is_set():
            position, maze, goal = self.game.maze[self], self.game.maze, self.game.player
            move = self.difficulty.value.next(position, maze, goal)
            self.move(move)

    def start(self, item):
        """ Start this player """
        super().start(item)
        self.thread.start()


class ExternalControlPlayer(Player):

    def __init__(self):
        """ Externally controlled player """
        super().__init__(PLAYER_IMAGE)
        self.thread = None

    def set_control(self, function):
        """ Set control function """
        self.thread = threading.Thread(target=function, args=(self, self.game))

    def start(self, item):
        """ Set start location """
        super().start(item)
        self.thread.start()


class Maze(object):
    """ A Maze object used for storing the maze information

    The maze class consists of a 2D array of cells as shown above. These cells represent the type of the maze, where
    PATHs can be walked, WALLs cannot, and the EXIT (singular) is the goal

    """
    def __init__(self, width, height):
        """ """
        self.width = width
        self.height = height
        self.full_width = width + 2
        self.full_height = height + 2
        self._map = None
        self.exit = None
        self.randomize()

    def __getitem__(self, item: Union[Cell, Tuple[int, int]]):
        """ Get the map cell at given coordinates """
        x, y = (item.x, item.y) if isinstance(item, (Cell, Player)) else item
        # Clamp values onto map's range
        x = max(0, min(x, self.full_width - 1))
        y = max(0, min(y, self.full_height - 1))
        return self._map[y][x]

    def __iter__(self):
        """ Iterate this object """
        def gen_maker():
            for x in range(0, self.full_width):
                for y in range(0, self.full_height):
                    yield self[x, y]
        return gen_maker()

    def __len__(self):
        """ Calculates the length of this range"""
        return int(self.full_width * self.full_height)

    def randomize(self):
        """ Randomize the map using some algorithm """
        self._map = [[Cell(x, y) for x in range(0, self.full_width)] for y in range(0, self.full_height)]
        self._borders()
        self.exit = self._make_exit()
        self._walls()

    def _borders(self):
        """ Draw boarders on the map """
        for x in range(0, self.full_width):
            self[x, 0].type = CellType.WALL
            self[x, self.full_height - 1].type = CellType.WALL
        for y in range(0, self.full_height):
            self[0, y].type = CellType.WALL
            self[self.full_width - 1, y].type = CellType.WALL

    def _make_exit(self):
        """ Choose randomize exit """
        random_x = randint(1, self.width)
        random_y = randint(1, self.height)

        dist_x = random_x - (self.width/2)
        dist_y = random_y - (self.height/2)

        cell = self[0 if dist_x < 0 else self.width + 1, random_y]
        if abs(dist_x) > abs(dist_y):
            cell.type = self[random_x, 0 if dist_y < 0 else self.height + 1].type
        cell.type = CellType.EXIT
        return cell

    def _test_wall(self, coord):
        """ """
        test_cell = self[coord]
        # Don't double up a wall
        if test_cell.type != CellType.PATH:
            return False
        # Count the number of neighbor walls and avoid more than
        neighbor_steps = itertools.product((-1, 0, 1), (-1, 0, 1))
        nearby_count = len([step for step in neighbor_steps if self[test_cell + step].type == CellType.WALL])
        if nearby_count > 3:
            return False
        # Finally, set the wall and test that it is solvable
        annotated_maze = copy.deepcopy(self)
        annotated_maze[test_cell].type = CellType.WALL
        annotated_maze = FloodFill.cache(annotated_maze, False)
        for cell in annotated_maze:
            output = FloodFill.recursive_walker(annotated_maze, annotated_maze[cell])
            if cell.type == CellType.PATH and output is None:
                return False
        return True

    def _walls(self):
        """ Randomize walls """
        for _ in range(0, len(self)):
            coord = (randint(1, self.width), randint(1, self.height))
            if self._test_wall(coord):
                self[coord].type = CellType.WALL


class Game(object):
    """ Create the GAME in all its glory """
    def __init__(self, difficulty: Difficulty, player, turn_time=500):
        self.won = False
        self.gameover = threading.Event()
        self.maze = FloodFill.cache(Maze(12, 12), False)
        self.last = None
        self.turn_time = turn_time
        self.player = player
        self.ai_player = AiPlayer(difficulty)
        for player in self.players():
            player.set_game(self)

    def players(self):
        """ Returns list of players """
        return [self.player, self.ai_player]

    def choose_start(self, avoid, fairness=5):
        """ Choose a start location """
        for _ in range(0, 10000):
            x, y = randint(1, self.maze.width), randint(1, self.maze.height)
            cell = self.maze[x, y]
            if cell.type == CellType.WALL or abs(cell.score - avoid) < fairness:
                continue
            return x, y
        else:
            raise Exception("Failed to find fair start location in 10000 iterations.")

    def start(self):
        """ Start all players """
        self.player.start(self.choose_start(0))
        self.ai_player.start(self.choose_start(self.maze[self.player].score))
        self.last = pygame.time.get_ticks()

    def stop(self):
        """ Stop the game """
        self.gameover.set()
        for player in self.players():
            player.unblock()
        for player in self.players():
            player.thread.join()

    def run(self):
        """ Run the game """
        # Check if it is time for a step
        now = pygame.time.get_ticks()
        if (now - self.last) < self.turn_time:
            return
        self.last = now
        for player in self.players():
            player.update()
            if Player.collided(self.player, self.maze.exit):
                self.won = True
                self.gameover.set()
                break
            if Player.collided(self.player, self.ai_player):
                self.gameover.set()
                break
        for player in self.players():
            player.unblock()

    def get_cell_size(self, window):
        """ """
        # 2 hidden cells, so we don't bump up against the window edge
        cell_counts_horizontal = self.maze.full_width + 2
        cell_counts_vertical = self.maze.full_height + 2

        width, height = window.get_size()
        return min(width // cell_counts_horizontal, height // cell_counts_vertical)

    def draw(self, window):
        """ Draw the maze """
        window.fill(juggling.pygame.COLORS["black"])
        cell_size = self.get_cell_size(window)
        for cell in self.maze:
            cell.draw(window, cell_size)
        for player in self.players():
            player.draw(window, cell_size)

        if self.gameover.is_set() and self.won:
            text = juggling.pygame.FONT_END.render("You WON!!!!", True, juggling.pygame.COLORS["white"],
                                                   juggling.pygame.COLORS["black"])
            window.blit(text, (300, 300))
        elif self.gameover.is_set():
            text = juggling.pygame.FONT_END.render("You LOST!!!!", True, juggling.pygame.COLORS["white"],
                                                   juggling.pygame.COLORS["black"])
            window.blit(text, (300, 300))
