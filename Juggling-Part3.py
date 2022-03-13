""" lesson 3: parallel execution, a complete example

In this lesson we will see how you can use threads (and the OS) to write seemingly completely separate programs that
run at the same time. In this case, you need to write a program to solve a maze. Inside the maze, there is an enemy
player who is not trying to solve the maze, but trying to find your player in the maze and force you to stop slacking
and go back to work.  Can you escape, or will you be forced back to work?

Some things to notice:
1. Put your solution in the "gwc_amazing_solution" function. It is your thread.
2. Keep the "while not game.gameover.is_set():" for your loop. It will stop when a win or lose condition is found.
3. Notice how the enemy player, the screen updating, and the win-condition checking is all done "in parallel".
4. Also notice how you don't know anything about those other program's implementations

Have fun!

CHALLENGE: can you win at VERY_HARD difficulty?
"""
from juggling.pygame import main
from juggling.maze import ExternalControlPlayer, Game, Difficulty, Direction, CellType

# Create a player character, and pass it into the game as your player
PLAYER = ExternalControlPlayer()

# CHALLENGE: can you up the difficulty and win?
GAME = Game(Difficulty.VERY_HARD, PLAYER)


def gwc_amazing_solution(player, game):
    """ ***** TODO: GWC work on you maze solver here ******

    You can fill your maze solving algorithm in here. It will be competing with the computer algorithm running at the
    same time. You do not even need to think about the other program....just write your algorithm here and the other
    algorithm will keep going at the dame time!

    Now let's talk about what is required here!  Two items are required:
    1. You must keep the `while not game.gameover.is_set():` line. This runs your algorithm until the game ends.
    2. To move, you must call player.move(direction), where direction is set to Direction.LEFT, Direction.RIGHT,
        Direction.UP or Direction.DOWN

    You may choose to call `cell, has_enemy = player.look(direction)` to learn about a direction. It returns a pair of
    items: cell_type which describes the type of cell (WALL, PATH, EXIT), and has_enemy which is a boolean whether your
    enemy is immediately in that direction. If has_enemy is ever true.... RUN!!!!!!!

    Now what does the sample algorithm do?  It does this:
    0. Loop until game over
    1. Try every direction (in order LEFT, UP, DOWN, RIGHT)
      a. If that direction is a WALL, or has_enemy check the next
      b. Otherwise choose this direction
    2. Calls move in the chose direction

    """
    while not game.gameover.is_set():
        # EDIT starting here
        for direction in [Direction.LEFT, Direction.UP, Direction.DOWN, Direction.RIGHT]:
            # Look in the curren direction
            cell_type, has_enemy = player.look(direction)
            # If this direction is a wall or has an enemy...keep looking
            if cell_type == CellType.WALL or has_enemy:
                continue
            break  # Stop looking for new directions, effectively choosing this direction
        # EDIT ending here
        player.move(direction)


if __name__ == "__main__":
    PLAYER.set_control(gwc_amazing_solution)
    GAME.start()
    main(GAME.run, GAME)
    GAME.stop()
