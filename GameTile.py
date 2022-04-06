"""
Granular unit to maintain state of the game board.
Each tile may rest in one of three states, HIDDEN being default.

:param x  Denotes the x coordinate of the tile
:param y  Denotes the y coordinate of the tile
"""


class GameTile:
    # constants for tracking tile state
    HIDDEN = 0
    REVEALED = 1
    FLAGGED = 2

    __contains_mine = False  # private field for mine
    __danger_level = 0  # private number of surrounding bombs

    def __init__(self, x_pos: int = None, y_pos: int = None):
        # TODO: x,y pos may be redundant
        self.x = x_pos
        self.y = y_pos
        self.__state = self.HIDDEN  # track if the tile has been clicked

    '''
    Set a mine on this GameTile
    
    :return True on success
    '''
    def set_mine(self) -> bool:
        if not self.__contains_mine:
            self.__contains_mine = True
            self.__danger_level = '!'
            return True
        return False

    '''
    Set threat level of surrounding Tiles
    :returns False if the tile is not dangerous
    '''
    def set_danger(self, danger: int):
        if not self.__contains_mine:
            self.__danger_level = danger
            # auto-reveal blank tiles
            if not danger:
                self.__state = self.REVEALED
                return False
        return True

    '''
    Obtain the coordinates of this GameTile
    
    :return coordinate Tuple (x, y)
    '''
    def get_coords(self):
        return self.x, self.y

    '''
    Get the state of this GameTile
    '''
    def get_state(self):
        return self.__state

    '''
    Check for presence of a mine on this tile
    
    :return True if this GameTile has a mine, False if not
    '''
    def has_mine(self):
        return self.__contains_mine

    '''
    Alter state of GameTile to revealed, check losing condition
    
    :return True if this tile held a mine
    '''
    def reveal(self) -> bool:
        self.__state = self.REVEALED
        return True if self.__contains_mine else False

    '''
    Alter state of GameTile to flagged
    '''
    def flag(self):
        self.__state = self.FLAGGED

    '''
    Alter state of GameTile to Hidden (unflagged) if it is flagged
    '''
    def unflag(self):
        if self.__state is self.FLAGGED:
            self.__state = self.HIDDEN

    '''
    Get point value for this GameTile
    
    :return points The number of points the tile is worth
    '''
    def get_points(self):
        if self.__state is not self.REVEALED:
            return 0
        elif self.__contains_mine:
            return -50
        else:
            return self.__danger_level

    '''
    Print the state of the tile or the threat level
    '''
    def print_tile(self):
        if self.__state is self.HIDDEN:
            print("*", end="  ")
        elif self.__state is self.REVEALED:
            print(self.__danger_level, end="  ")
        elif self.__state is self.FLAGGED:
            print("X", end="  ")
