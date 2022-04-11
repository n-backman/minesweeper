import Grid
import Solver

size = 6
n_mines = 10
seed = None


def get_input(actions: list, board_size: int) -> (int, int, str):
    while True:
        instr = input(f"Next Move [X][Y][{'/'.join(actions)}]: ")
        try:
            verify(instr, actions, board_size)
        except ValueError as ve:
            print(f"Bad Input: {ve}")
        except IndexError as ie:
            print(f"Bad Input: {ie}")
        except TypeError as te:
            print(f"Bad Input: {te}")
        else:
            # subtract one from x,y to transform from user provided 1-indexing to 0-indexing
            return int(instr[0]) - 1, int(instr[1]) - 1, str(instr[2])


def verify(instr: str, actions: list, board_size: int):
    if len(instr) != 3:
        raise IndexError(f"Command must be 3 characters, got {len(instr)} instead.")
    if instr[0:2].isnumeric():
        x = int(instr[0])
        y = int(instr[1])
    else:
        raise TypeError(f"X and Y arguments must resolve to integers.")
    if instr[2] not in actions:
        raise ValueError(f"Expected one of [{','.join(actions)}] as Action, got '{instr[2]}' instead.")
    if not 1 <= x <= board_size:
        raise ValueError(f"Expect 1 <= X <= {board_size}, got {x} instead.")
    if not 1 <= y <= board_size:
        raise IndexError(f"Expect 1 <= Y <= {board_size}, got {y} instead.")


def info(game_board: Grid):
    print("Welcome to MYNESWEEPER!")
    print("\nYou may interact with this board by typing in X and Y coordinates, followed by an Action.")
    print("Example input [XYA]: 11?\n\t* Reveals tile at X=1, Y=1 (upper-left most tile)")
    print("Possible Actions include:\n\t* '?': Reveal tile\n\t* '!': Flag tile")
    print(f"For this game, your board is {game_board.size}x{game_board.size} with {game_board.mine_count} mines!")


if __name__ == "__main__":
    Board = Grid.Grid(size, n_mines, seed)
    info(Board)
    while Board.get_state() is Board.ACTIVE:
        x, y, action = get_input(Board.actions, Board.size)
        Board.take_action(x, y, action)
    # HMM = Solver.Solver(Board)
    # HMM.play()
