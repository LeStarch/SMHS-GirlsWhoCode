""" utilities.py

Things that help with the maze game. Definitions n' such..
"""
from enum import Enum
import copy
from random import choice, sample


class Direction(Enum):
    """ Direction up down left or right """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STAY = (0, 0)


class CellType(Enum):
    """ Cell Type for maze cells """
    EXIT = 0
    PATH = 1
    WALL = 2


class RandomWalk(object):
    """ Randomly walk the maze """

    def next(self, position, maze, goal):
        """ Get a next step """
        return choice(list(Direction))


class FloodFill(object):
    def __init__(self, thinking):
        self.thinking = thinking
        self.current = 0

    def next(self, position, maze, goal):
        """ Next call """
        move = Direction.STAY
        if self.current == 0:
            path = FloodFill.solve(maze, position, goal)
            difference = path[1] - position
            move = Direction.STAY if len(path) < 2 else Direction(difference)
        self.current = (self.current + 1) % self.thinking
        return move

    @classmethod
    def recursive_scorer(cls, maze, current, score, end):
        """ Score each cell recursively from curren to end """
        # Walls and tiles already scored lower do not continue
        if current.type == CellType.WALL or current.score <= score:
            return
        # Update current score and break if we have reach the end tile
        current.score = score
        if end is not None and current == end:
            return
        # Otherwise, score each tile in the cardinal directions and find the minimum score sofar
        randomized_directions = sample(list(Direction), k=len(list(Direction)))
        [cls.recursive_scorer(maze, maze[current + step], score + 1, end) for step in randomized_directions]
        return

    @classmethod
    def recursive_walker(cls, maze, current, score=None):
        """ Walk the maze recursively back to a score of zero """
        score = score if score is not None else current.score
        assert current.score <= score, f"Scoring failure. Algorithm score {score} != cell.score {current.score}"
        if score >= len(maze):
            return None
        elif score == 0:
            return [current]
        possible_steps = [maze[current + step] for step in Direction if maze[current + step].score < score]
        return [current] + cls.recursive_walker(maze, possible_steps[0], score - 1)

    @classmethod
    def solve(cls, maze, position, goal, need_copy=True):
        """ Solve the flood fill returning path """
        maze = copy.deepcopy(maze) if need_copy else maze
        position = maze[position] if position is not None else None
        goal = maze[goal]
        # Initialize scores, if not already initialized
        for cell in maze:
            if cell.type == CellType.WALL or need_copy:
                cell.score = len(maze) + 1
            else:
                setattr(cell, "score", getattr(cell, "score", len(maze) + 1))
        cls.recursive_scorer(maze, goal, 0, position)
        if position is not None:
            path = cls.recursive_walker(maze, position, position.score)
            assert not path or not list(filter(lambda x: x is None, path)), f"None steps discovered in path: {path}"
            return path
        return None

    @classmethod
    def cache(cls, maze, copy_needed=True):
        """ Precache the solutions for every cell """
        maze_copy = copy.deepcopy(maze) if copy_needed else maze
        cls.solve(maze_copy, None, maze_copy.exit, False)
        return maze_copy
