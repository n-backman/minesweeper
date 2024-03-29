from GameTile import GameTile
import random
from typing import Tuple


class Grid:
    """
        Game board to play minesweeper on comprised of NxN GameTiles

        :param size         Dimensions of game board size^2
        :param mine_count   Number of mines on game board
        :param seed         Seed for RNG
    """
    INACTIVE = 0
    ACTIVE = 1
    actions = ['?', '!']

    def __init__(self, size: int, mine_count: int, seed: int = None):
        self.size = size
        self.corners = [(0,0),(size-1,size-1),(0,size-1),(size-1,0)]
        self.mine_count = mine_count
        self.seed = seed
        self.reveal_total = 0
        self.__state = self.ACTIVE

        # build board and tiles
        self.grid = [[] for _ in range(size)]
        self.__init_grid()
        self.__init_mines()
        self.__init_danger()
        self.print_board()

    def __init_grid(self):
        """
            Populate the game board with GameTiles
        """
        # populate board with tiles
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i].append(GameTile(i, j))

    def __init_mines(self):
        """
            Populate GameTile board with n mines
        """
        # place mines
        random.seed(self.seed)
        mines_placed = 0
        while mines_placed < self.mine_count:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if((x,y) in self.corners):
                continue # don't allow mines in the corner.
            if self.grid[x][y].set_mine():
                mines_placed += 1

    def __init_danger(self):
        """
            Calculate and set neighbor bomb count and set danger level
        """
        for i in range(self.size):
            for j in range(self.size):
                danger_level = 0
                # check each of the 8 surrounding GameTiles for bombs and add count to self
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
                                danger_level += self.grid[i + x_offset][j + y_offset].has_mine()
                            except IndexError:
                                pass
                # increment reveal total if the danger is zero
                if not self.grid[i][j].set_danger(danger_level):
                    self.reveal_total += 1

    def get_tile(self, i: int, j: int) -> GameTile:
        """
            Grab specified GameTile object from board

            :return: GameTile object
        """
        return self.grid[i][j]

    def get_state(self):
        """
            Grab state of board
        """
        return self.__state

    def reveal(self, i: int, j: int):
        """
           Take action on board by revealing a tile **checks lose condition**
        """
        # returns true if the tile had a Mine
        if not self.grid[i][j].reveal():
            self.reveal_total += 1
            self.print_board()
            if self.size ** 2 - (self.mine_count + self.reveal_total) == 0:
                self.__game_over(won=True)
        else:
            self.__game_over(won=False)

    def toggle_flag(self, i: int, j: int):
        """
            Take action on board by marking a tile with a bomb stake
        """
        state = self.get_tile(i, j).get_state()
        if state is GameTile.HIDDEN:
            self.grid[i][j].flag()
        elif state is GameTile.FLAGGED:
            self.grid[i][j].unflag()
        self.print_board()

    def print_board(self):
        """
            Neatly print the current state of the board to console
        """
        print()
        for j in range(self.size):
            for i in range(self.size):
                self.grid[i][j].print_tile()
            print()

    def print_full_board(self):
        """
            Neatly print the fully revealed board to console
        """
        print()
        for j in range(self.size):
            for i in range(self.size):
                self.grid[i][j].reveal()
                self.grid[i][j].print_tile()
            print()

    def __game_over(self, won: bool):
        """
           Handles the end of the game conditionally
        """
        # turn off the game and get the player's score
        self.__state = self.INACTIVE
        score = self.get_score()
        if not won:
            self.print_full_board()
            print("You lose!")
        else:
            print("You win!")
        print(f'Your score is: {score} points!')

    def get_score(self) -> int:
        """
           Calculate end of game score
        """
        total_score = 0
        for i in range(self.size):
            for j in range(self.size):
                total_score += self.get_tile(i, j).get_points()
        return total_score

    def take_action(self, x_pos: int, y_pos: int, action: str):
        if action == '?':
            self.reveal(x_pos, y_pos)
        elif action == '!':
            self.toggle_flag(x_pos, y_pos)


if __name__ == "__main__":
    Board = Grid(5, 4, 11)
    for i in range(Board.size):
        for j in range(Board.size):
            Board.reveal(i, j)
