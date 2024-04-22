from generate_model import load
from game_engine import game_run_1, game_run_2
from home_page import home


def main():

    origin = load()

    winner = ''
    running = True
    while running:
        global path
        path = list()
        x = home(winner)
        if x == '2':    
            x = '1'
            winner = game_run_1(origin, path)
        elif x == '1':    
            x = '2'
            winner = game_run_2(origin, path)
        else:
            running = False
        if not winner:
            winner = '平局'
        elif winner == x:
            winner = '玩家胜利'
        else:
            winner = '电脑胜利'
        print('winner:',winner)


if __name__ == '__main__':
    main()