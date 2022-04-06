import Grid

size = 5
n_mines = 6
seed = None


def get_input():
    instr = input("Next Move [X][Y][?/!]: ")
    return int(instr[1])-1, int(instr[0])-1, instr[2]


def take_action(game_board: Grid, x_pos: int, y_pos: int, action: str):
    if action == '?':
        game_board.reveal(x_pos, y_pos)
    elif action == '!':
        game_board.toggle_flag(x_pos, y_pos)


if __name__ == "__main__":
    Board = Grid.Grid(size, n_mines, seed)
    while Board.get_state():
        x, y, action = get_input()
        take_action(Board, x, y, action)
