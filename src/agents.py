from abc import ABCMeta, abstractmethod
import game_state
from game_state import Game
import random
import time
from ai import alpha_beta


class Agent(metaclass=ABCMeta):
    """
    Abstract agent class that contains all the moves it should

    Methods
    ----------
    move(state: Game)
        let the agent make a move depending on the game state
    """
    @abstractmethod
    def __init__(self, player, player_name):
        """
        Init the player
        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        :param player_name: Name of the agent
        """
        game_state.validate_player(player)
        self.player = player
        self.player_name = f'{player_name} {1 if self.player == game_state.PLAYER1 else 2}'
        pass

    @abstractmethod
    def move(self, state: Game):
        pass

    @abstractmethod
    def win_message(self):
        print(f'{self.player_name} won!')
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
        super().__init__(player, "Human")

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

    def win_message(self):
        super().win_message()


class RandomAgent(Agent):
    """
    Random agent makes a random move from the available move pool

    Implements the abstract class Agent
    """
    def __init__(self, player):
        """

        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        """
        super().__init__(player, "Random")

    def move(self, state: Game):
        """
        Make a random move

        :param state: Current game state
        :return: None
        """
        moves = state.valid_moves_get()
        state.move(random.choice(moves), self.player, self.player_name)

    def win_message(self):
        super().win_message()


class AiAgent(Agent):
    def __init__(self, player, name, depth):
        """

        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        :param depth: maximum search depth
        """
        super().__init__(player, name)
        self.depth = depth

    def move(self, state: Game) -> None:
        """

        :param state: Current game state
        :return: None
        """
        maximizing = self.player > 0
        print(f'{self.player_name} starts exploring all nodes (this might take a while)')
        time_start = time.time()
        score, node, explored = alpha_beta(state, self.depth, maximizing)
        time_end = time.time()
        print(f'{self.player_name} explored {explored} nodes in {time_end - time_start} seconds')
        state.move(node.last_action(), self.player, self.player_name)

    def win_message(self):
        super().win_message()


class EasyAgent(AiAgent):
    def __init__(self, player):
        """

        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        """
        super().__init__(player, "Easy AI", 2)

    def move(self, state: Game) -> None:
        super().move(state)

    def win_message(self):
        super().win_message()


class PerfectAgent(AiAgent):
    def __init__(self, player):
        """

        :param player: integer value, valid input is game_state.PLAYER1 or game_state.PLAYER2
        """
        super().__init__(player, "Impossible AI", 9)

    def move(self, state: Game) -> None:
        super().move(state)

    def win_message(self):
        super().win_message()
