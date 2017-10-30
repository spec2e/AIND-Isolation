"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

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

        g1 = game.apply_move((2,1))
        g2 = game.apply_move((2,0))

        player1.get_move(g1, 2000.0)

if __name__ == '__main__':
    unittest.main()
