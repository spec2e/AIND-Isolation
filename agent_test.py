"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""
import timeit
import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)


    def test_minimax(self):

        player1 = game_agent.MinimaxPlayer()
        player2 = game_agent.MinimaxPlayer()
        game = isolation.Board(player1, player2)

        game.apply_move((2,1))
        game.apply_move((2,0))

#        print("min", min(-1, game))

        time_millis = lambda: 1000 * timeit.default_timer()

        move_start = time_millis()
        time_left = lambda: 150 - (time_millis() - move_start)
        player1.get_move(game, time_left)

if __name__ == '__main__':
    unittest.main()
