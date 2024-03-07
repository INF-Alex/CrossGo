import time
import pygame

from generate_model import load
from game_engine import game_run_1, game_run_2
from home_page import home


def main():

    origin = load()

    winner = 'EMPTY'
    running = True
    while running:
        global path
        path = list()
        x = home()
        if x == '1':    
            winner = game_run_1(origin, path)
        elif x == '2':    
            winner = game_run_2(origin, path)
        else:
            running = False
        if winner == '1':
            winner = 'RED'
        elif winner == '-1':
            winner = 'BLUE'
        print('winner:',winner)


if __name__ == '__main__':
    main()