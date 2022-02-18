DIMENSIONS = 3
CELL_EMPTY = 0
PLAYER1 = 1
PLAYER2 = -1


def validate_player(player):
    """
    Throws a ValueError if the player is invalid

    :param player: player number to inspect
    :return: None
    """
    if player != PLAYER1 and player != PLAYER2:
        raise ValueError(f'{player} is an invalid player value. Only {PLAYER1} and {PLAYER2} allowed')


class Game:

    def __init__(self):
        self._board = [[0 for i in range(DIMENSIONS)] for i in range(DIMENSIONS)]
        self._valid_moves = self._calculate_valid_moves()
        self._last_action = None
        self._render_board()

    def _calculate_valid_moves(self):
        valid_moves = []

        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell == CELL_EMPTY:
                    valid_moves.append((i, j))
        return valid_moves

    def _render_board(self):
        translate = {PLAYER2: 'O', 0: ' ', PLAYER1: 'X'}
        skip_row = True

        for row in reversed(self._board):
            if not skip_row:
                print('_' * (DIMENSIONS * 2 - 1))

            skip_row = False
            print('|'.join(translate[cell] for cell in row))

    def move(self, coord, player_val, player_name):
        if coord not in self._valid_moves:
            print(f'Error, move{coord} by {player_name} is illegal')
            print(f'valid moves: {self._valid_moves}')
            return False
        else:
            row, col = coord
            self._valid_moves.remove(coord)
            self._board[row][col] = player_val
            print(f'{player_name} made the move {coord}')
            self._render_board()
            return True

    def valid_moves_get(self):
        return self._valid_moves[:]

    def game_score(self):

        translate = {PLAYER1: 'player 1 wins', PLAYER2: 'player 2 wins', 0: 'Draw'}

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
                else:
                    if first_val == 0:
                        first_val = cell
                    # Cells with different values, skip
                    elif cell != first_val:
                        break
                    else:
                        found = True

            if found:
                # Winner found! Return the winner
                return True, first_val, translate[first_val]

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
        val = check([self._board[i][len(self._board)-i-1] for i in range(DIMENSIONS)])
        if val is not None:
            return val

        # check full (no winner)
        if len(self._valid_moves) == 0:
            return True, 0, translate[0]
        return False, 0, translate[0]
