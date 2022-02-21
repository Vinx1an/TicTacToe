from ai import AiNode
import random

DIMENSIONS = 3
CELL_EMPTY = 0
PLAYER1 = 1
PLAYER2 = -1
DRAW_SCORE = 0
PLAYER_VALUE = [PLAYER1, PLAYER2]


def validate_player(player):
    """
    Throws a ValueError if the player is invalid
    :param player: player number to inspect
    :return: None
    """
    if player != PLAYER1 and player != PLAYER2:
        raise ValueError(f'{player} is an invalid player value. Only {PLAYER1} and {PLAYER2} allowed')


class Game(AiNode):
    """
    Game class of tic-tac-toe game
    """

    def __init__(self, board: list[list[int, ...], ...] = None, move: tuple[int, int] = None, player: int = None):
        """
        Create a board as a child of the previous game state
        :param board: Board to enter, raises a ValueError on invalid format
        :param move: Move to make
        :param player: player that makes the move
        """

        # Get the board
        if board is None:
            self._board = [[0 for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]
        else:
            self._validate_board(board)
            self._board = board

        self._last_action = None
        self._current_score = None
        self._game_over = False
        self._last_player = player if player is not None else PLAYER2
        self._valid_moves = self._calculate_valid_moves()
        self._move_private(move, player)
        # Render the board if it's a new board
        if board is None:
            self.render_board()

    @staticmethod
    def _validate_board(board: list[list[int, ...], ...]) -> None:
        """
        Validate board
        :param board: Board to validate
        :return: None
        """
        values = [CELL_EMPTY, PLAYER1, PLAYER2]
        error = f"""Invalid board, required format 
                    {[[0 for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]} given {board}"""
        if len(board) != DIMENSIONS:
            raise ValueError(error)
        for row in board:
            if len(row) != DIMENSIONS:
                raise ValueError(error)
            for cell in row:
                if cell not in values:
                    raise ValueError(f'Only the values {values} are allowed')

    def _calculate_valid_moves(self) -> list[tuple[int, int]]:
        """
        Calculate valid moves from board state
        :return: List of valid moves, move format is (row, column)
        """
        valid_moves = []

        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell == CELL_EMPTY:
                    valid_moves.append((i, j))
        return valid_moves

    def render_board(self) -> None:
        """
        Render the board to the terminal
        :return: None
        """
        translate = {PLAYER2: 'O', 0: ' ', PLAYER1: 'X'}
        skip_row = True

        for row in reversed(self._board):
            if not skip_row:
                print('_' * (DIMENSIONS * 2 - 1))

            skip_row = False
            print('|'.join(translate[cell] for cell in row))

    def _move_private(self, coord: tuple[int, int], player_val: int) -> bool:
        """
        Make a move without printing output to the screen
        :param coord: Coordinate [row, column]
        :param player_val: PLAYER1 or PLAYER2
        :return: True if the move is valid and made, False otherwise
        """
        if coord not in self._valid_moves:
            return False
        row, col = coord
        self._valid_moves.remove(coord)
        self._last_player = player_val
        self._last_action = coord
        self._board[row][col] = player_val
        self._game_over, self._current_score = self._calculate_score()
        return True

    def move(self, coord: tuple[int, int], player_val: int, player_name: str) -> bool:
        """
        Make a move and render the board on success
        :param coord: Coordinate (row, column)
        :param player_val: PLAYER1 or PLAYER2
        :param player_name: Readable player name to write
        :return: True if the move is valid and made, False otherwise
        """
        if not self._move_private(coord, player_val):
            print(f'Error, move{coord} by {player_name} is illegal')
            print(f'valid moves: {self._valid_moves}')
            return False

        print(f'{player_name} made the move {coord}')
        self.render_board()
        return True

    def valid_moves_get(self) -> list[tuple[int, int]]:
        """
        Get a copy of the valid move list
        :return: The list of valid moves. Move format is (row, column)
        """
        return self._valid_moves[:]

    def _calculate_score(self) -> tuple[bool, int]:
        """
        Calculate the current board state
        :return: (game over, winner) true if the game is over, and the winning player in the second element
        """
        def get_columns():
            for i in range(DIMENSIONS):
                yield [rows[i] for rows in self._board]

        def check(cells):
            first_val = 0
            found = False
            for cell in cells:
                found = False
                # Empty cell, no winner
                if cell == 0:
                    break
                # First cell, store the value
                elif first_val == 0:
                    first_val = cell
                # Cells with different values, no winner here
                elif cell != first_val:
                    break
                # Winner found if the for loop is done, continue checking otherwise
                else:
                    found = True

            if found:
                # Winner found! Return the winner
                return True, first_val

        # check row
        for row in self._board:
            val = check(row)
            if val is not None:
                return val

        # check columns
        for col in get_columns():
            val = check(col)
            if val is not None:
                return val

        # check diagonal 1
        val = check([self._board[i][i] for i in range(DIMENSIONS)])
        if val is not None:
            return val

        # check diagonal 2
        val = check([self._board[i][len(self._board) - i - 1] for i in range(DIMENSIONS)])
        if val is not None:
            return val

        # check full (no winner)
        if len(self._valid_moves) == 0:
            return True, CELL_EMPTY
        return False, CELL_EMPTY

    def game_over(self) -> bool:
        """
        Check if the game is over
        :return: True if the game is over
        """
        return self._game_over

    def game_score(self) -> int:
        """
        Get the game score
        :return: PLAYER1, PLAYER2, or DRAW_SCORE. A game that hasn't ended always has a score of DRAW_SCORE
        """
        return self._current_score

    def last_action(self):
        return self._last_action

    def children_get(self):
        # Randomly shuffle moves to have a random child order
        moves = self._valid_moves[:]
        random.shuffle(moves)
        next_player = PLAYER1 if self._last_player == PLAYER2 else PLAYER2
        for _move in moves:
            yield Game(board=[row[:] for row in self._board], move=_move, player=next_player)

    def end_node(self) -> bool:
        return self.game_over()

    def score(self):
        return self.game_score()
