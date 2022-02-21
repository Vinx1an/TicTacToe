import game_state
from game_state import Game
from agents import HumanTerminalAgent, RandomAgent, PerfectAgent


def terminal_main():
    agents = {0: [HumanTerminalAgent, "Human player"],
              1: [RandomAgent, "Very easy AI"],
              2: [PerfectAgent, "Impossible AI"]}
    players = []

    while (length := len(players)) < 2:
        print(f'Select player {length + 1}:')
        [print('\t', key, ':', value[1]) for key, value in agents.items()]
        try:
            index = int(input('Enter your selection: '))
            players.append(agents[index][0](game_state.PLAYER_VALUE[length]))
        except (ValueError, KeyError):
            print('Invalid Input!')

    game = Game()

    while not game.game_over():
        for player in players:
            player.move(game)
            if game.game_over():
                if game.score() == game_state.DRAW_SCORE:
                    print('Game draw')
                else:
                    player.win_message()
                break


if __name__ == '__main__':
    terminal_main()
