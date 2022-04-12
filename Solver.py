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
        self.Beliefs = {}
        self.__init_beliefs()

    def __init_beliefs(self):
        # TODO: create new data structure to merge coords and belief values. dont need 2 lists
        """
        Initialize belief space for predictions
        :return: None
        """
        for i in range(self.n):
            for j in range(self.n):
                self.Beliefs[(i, j)] = -1.0

    # TODO: Read GridSpace
    def read_grid(self):
        pass

    def find_candidates(self, candidates: list = None) -> [GameTile]:
        """
        Scower the board for potential spaces to reveal on the frontier, and add them to a list

        :return: candidates List[GameTile] containing all potential tiles to play
        """
        if candidates is None:
            candidates = []
        # need to scan board for all revealed tiles with a hidden neighbor
        for i in range(self.n):
            for j in range(self.n):
                tile = self.Board.get_tile(i, j)
                if tile.get_state() is GameTile.REVEALED:
                    neighbors = []
                    zero_count, flag_count = 0, 0
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
                                        neighbors.append(neighbor.get_coords())
                                        # if the neighbor has a zero belief, track it for updating phase
                                        if self.Beliefs[neighbor.get_coords()] == 0.0:
                                            zero_count += 1
                                    elif neighbor.get_state() is GameTile.FLAGGED:
                                        flag_count += 1
                                except IndexError:
                                    pass
                    self.update_beliefs(tile.get_danger()[1], neighbors, zero_count, flag_count)
                    [candidates.append(x) for x in neighbors if x not in candidates]
        return candidates

    # TODO: Assess Candidate Tiles and Update Beliefs
    def update_beliefs(self, threat: int, neighbors: list, null_neighbors: int, flag_neighbors: int):
        # TODO: solve double counting belief values .5 on round 1 updates with .5 on round 2 to be 1, should be .5 total
        for n in neighbors:
            # evaluate the current belief value
            prior_belief = self.Beliefs[n]
            # if it was zero or will be zero, leave it zero
            if not prior_belief or not threat:
                self.Beliefs[n] = 0.0
            else:
                # set prior to zero if we've never been there, then sum
                prior_belief = 0 if prior_belief <= 0 else prior_belief
                self.Beliefs[n] = prior_belief + ((threat-flag_neighbors) / (len(neighbors)-null_neighbors))

    # TODO: Reveal least-likely (most safe) Candidate
    def select_candidate(self, candidates: list) -> (int, int):
        min_belief = 100
        min_candidate = None
        for c in candidates:
            x, y, = c[0], c[1]
            belief = self.Beliefs[c]
            if not belief:
                self.Board.reveal(x, y)
                candidates.remove(c)
                return c
            # flag definite bombs
            elif belief >= 2.0:
                self.Board.toggle_flag(x, y)
                candidates.remove(c)
                return c
            # reveal min probability greater than zero
            elif belief < min_belief:
                min_belief, min_candidate = belief, c
        self.Board.reveal(min_candidate[0], min_candidate[1])
        candidates.remove(min_candidate)
        return min_candidate

    def soften_beliefs(self, candidates: list):
        for c in candidates:
            self.Beliefs[c] = -1

    def play(self):
        candidates = []
        while self.Board.get_state():
            candidates = self.find_candidates(candidates)
            print([(c, self.Beliefs[c]) for c in candidates])
            selection = self.select_candidate(candidates)
            self.soften_beliefs(candidates)
            print(f'{selection[0]+1}, {selection[1]+1}')


if __name__ == "__main__":
    sv = Solver(Grid(5, 6, None))
    sv.play()
