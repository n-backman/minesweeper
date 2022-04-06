import random

from Grid import Grid
from GameTile import GameTile
import numpy as np


class Solver:
    """
        Given some MineSweeper board, want to reveal the tile least likely to harbor a bomb
        given the current state of the board and it's tiles.
    """

    def __init__(self, game_board: Grid):
        self.Board = game_board
        self.n = game_board.size  # dimension of board (nxn)
        self.Beliefs = [[] for _ in range(self.n)]
        self.__init_beliefs()

    def __init_beliefs(self):
        """
        Initialize belief space for predictions
        :return: None
        """
        for i in range(self.n):
            for j in range(self.n):
                self.Beliefs[i].append(.0)

    # TODO: Read GridSpace
    def read_grid(self):
        pass

    def find_candidates(self, candidates=None) -> [GameTile]:
        """
        Scower the board for potential spaces to reveal, and add them to a list

        :return: candidates List[GameTile] containing all potential tiles to play
        """
        if candidates is None:
            candidates = []

        # need to scan board for all revealed tiles with a hidden neighbor
        for i in range(self.n):
            for j in range(self.n):
                tile = self.Board.get_tile(i, j)
                if tile.get_state() is GameTile.REVEALED:
                    # add neighbors on to the list performing safecheck
                    for x_offset in [-1, 0, 1]:
                        # prevent negative indexing
                        if i + x_offset < 0:
                            continue
                        for y_offset in [-1, 0, 1]:
                            # prevent negative indexing
                            if j + y_offset < 0:
                                continue
                            if x_offset or y_offset:  # never evaluate self
                                try:
                                    neighbor = self.Board.get_tile(i + x_offset, j + y_offset)
                                    if neighbor.get_state() is GameTile.HIDDEN:
                                        candidates.append(neighbor.get_coords())
                                except IndexError:
                                    pass
        return candidates

    # TODO: Assess Candidate Tiles and Update Beliefs

    # TODO: Reveal least-likely (most safe) Candidate

    def play(self):
        while self.Board.get_state():
            x, y = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
            self.Board.reveal(x, y)
            candidates = self.find_candidates()
            for item in candidates:
                print(f'{item[1]+1}, {item[0]+1}\t', end='')
