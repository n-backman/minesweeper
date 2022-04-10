import Grid
import Solver

size = 5
n_mines = 6
seed = None


def get_input():
    actions = ['?', '!']
    instr = input(f"Next Move [X][Y][{'/'.join(actions)}]: ")
    try:
        x = instr[0]
        y = instr[1]
        action = instr[2]
    except ValueError as ve:
        print(f"Bad Input: {ve}")
        get_input()
    else:
        # subtract one from x,y to transform from user provided 1-indexing to 0-indexing
        return int(x) - 1, int(y) - 1, action


def take_action(game_board: Grid, x_pos: int, y_pos: int, action: str):
    # verify_action()
    if action == '?':
        game_board.reveal(x_pos, y_pos)
    elif action == '!':
        game_board.toggle_flag(x_pos, y_pos)


def info(game: Grid):
    print("Welcome to MYNESWEEPER!")
    print("\nYou may interact with this board by typing in X and Y coordinates, followed by an Action.")
    print("Example input [XYA]: 11?\n\t* Reveals tile at X=1, Y=1 (upper-left most)")
    print("Possible Actions include:\n\t* '?': Reveal tile\n\t* '!': Flag tile")
    print(f"For this game, your board is {game.size}x{game.size} with {game.mine_count} mines!")


if __name__ == "__main__":
    Board = Grid.Grid(size, n_mines, seed)
    info(Board)
    while Board.get_state() is Board.ACTIVE:
        x, y, action = get_input()
        # if verify_action():
        take_action(Board, x, y, action)
    # HMM = Solver.Solver(Board)
    # HMM.play()
