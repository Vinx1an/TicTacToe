from abc import ABCMeta, abstractmethod
import game_state
from game_state import Game
import random


class Agent(metaclass=ABCMeta):
    """
    Abstract agent class that contains all the moves it should

    Methods
    ----------
    move(state: Game)
        let the agent make a move depending on the game state
    """
    @abstractmethod
    def __init__(self, player):
        game_state.validate_player(player)
        pass

    @abstractmethod
    def move(self, state: Game):
        pass


class HumanTerminalAgent(Agent):
    """
    Human agent for running entering coordinates in the terminal

    Implements the abstract class Agent

    """
    def __init__(self, player: int):
        """

        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        """
        super().__init__(player)
        self.player = player
        self.player_name = f'Human {1 if player == game_state.PLAYER1 else 2}'

    def move(self, state: Game):
        """
        Let the player make a move, asks for input until a valid input is given
        :param state: Current game state
        :return: None
        """
        move_made = False
        while not move_made:
            try:
                row, col = [int(x) for x in input('Enter a coordinate in the format {row} {col}: ').split()]
                move_made = state.move((row, col), self.player, self.player_name)
            except ValueError:
                print('Given input was not given in the format {row} {col}')
                move_made = False
                pass


class RandomAgent(Agent):
    """
    Random agent makes a random move from the available move pool

    Implements the abstract class Agent
    """
    def __init__(self, player):
        """

        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        """
        super().__init__(player)
        self.player = player
        self.player_name = f'Random Agent {1 if player == game_state.PLAYER1 else 2}'

    def move(self, state: Game):
        """
        Make a random move

        :param state: Current game state
        :return: None
        """
        moves = state.valid_moves_get()
        state.move(random.choice(moves), self.player, self.player_name)
