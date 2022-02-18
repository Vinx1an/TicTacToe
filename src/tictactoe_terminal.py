import game_state
from game_state import Game
from agents import HumanTerminalAgent, RandomAgent


def terminal_main():
    game = Game()
    player1 = HumanTerminalAgent(game_state.PLAYER1)
    player2 = RandomAgent(game_state.PLAYER2)
    while True:
        player1.move(game)
        score = game.game_score()
        if score[0]:
            break;

        player2.move(game)
        score = game.game_score()
        if score[0]:
            break;

    print(f'Game over! {score[2]}')


if __name__ == '__main__':
    terminal_main()
