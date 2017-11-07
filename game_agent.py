"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    return increase_blocking_improved_score(game, player)


def custom_score_2(game, player):
    return decrease_blocking_improved_score(game, player)


def custom_score_3(game, player):
    return blocking_improved_score(game, player)


def increase_blocking_improved_score(game, player):

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    move_count_factor = 0.01 * game.move_count

    return float((len(own_moves) - (len(opp_moves))) + move_count_factor)


def decrease_blocking_improved_score(game, player):

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    move_count_factor = 2 * game.move_count

    return float((len(own_moves) - (2 * len(opp_moves))) - move_count_factor)


def blocking_improved_score(game, player):

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - (2 * opp_moves))


def plain_improved_score(game, player):

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - opp_moves)


def open_move_score(game, player):

    return float(len(game.get_legal_moves(player)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):

        self.time_left = time_left
        best_move = (-1, -1)

        try:
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        current_best = float("-inf")
        current_best_move = (-1, -1)

        for idx, action in enumerate(game.get_legal_moves()):

            v = self.min_value(game.forecast_move(action), depth -1)

            if v >= current_best:
                current_best = v
                current_best_move = action

        return current_best_move

    def cut_off(self, depth, game):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return True

        return False

    def min_value(self, game, depth):

        if self.cut_off(depth, game):
            return self.score(game, self)

        v = float("inf")

        for action in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(action), depth -1))

        return v

    def max_value(self, game, depth):

        if self.cut_off(depth, game):
            return self.score(game, self)

        v = float("-inf")
        for action in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(action), depth -1))

        return v


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):

        self.time_left = time_left
        best_move = (-1, -1)

        try:
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        finally:
            return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        """
        Implementation of the minimax algorithm with alpha-beta pruning with iterative deepening

        :param game: the game predict next move from
        :param depth: current depth
        :param alpha: current alpha - initialized to -inf
        :param beta: current beta - initialized to inf
        :return: best move found using alpha-beta pruning
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        current_best_move = legal_moves[0]
        current_best_score = alpha

        for action in legal_moves:
            v = max(current_best_score, self.min_value(game.forecast_move(action), depth-1, alpha, beta))

            if v > current_best_score:
                current_best_score = v
                current_best_move = action

            alpha = max(v, alpha)

        return current_best_move

    def cut_off(self, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return True

        return False

    def min_value(self, game, depth, alpha, beta):

        v = float("inf")

        if self.cut_off(depth):
            return self.score(game, self)

        for action in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(action), depth -1, alpha, beta))
            if v <= alpha:
                return v

            beta = min(v, beta)

        return v

    def max_value(self, game, depth, alpha, beta):

        v = float("-inf")

        if self.cut_off(depth):
            return self.score(game, self)

        for action in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(action), depth -1, alpha, beta))
            if v >= beta:
                return v

            alpha = max(v, alpha)

        return v

