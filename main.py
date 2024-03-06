import os
import copy
import random
from queue import Queue
from threading import Thread
import pickle
import pygame
import sys
import numpy as np
import tkinter as tk
import tkinter.messagebox

from generate_model import generate, Board, TreeNode
from game_UI import draw_chess_board, draw_cross, get_mouse_cell, check
from game_UI import WIDTH, HEIGHT, BOARD_SIZE, SQUARE_SIZE, TICK, CROSS, EMPTY, WHITE, BLACK, C1, C2

def wander(a,f=max):
    m = f(a)
    i = random.randint(0,len(a)-1)
    while a[i] != m:
        i = random.randint(0,len(a)-1)
    return i
def f1():
    global origin
    a = [origin.child[i].value for i in range(len(origin.child))]
    x = wander(a,max)
    origin = origin.child[x]
    return origin.root.pos
def f2():
    global origin
    a = [origin.child[i].value for i in range(len(origin.child))]
    x = wander(a,min)
    origin = origin.child[np.argmin(a)]
    return origin.root.pos
def f_find(current):
    global origin
    for kid in origin.child:
        if kid.root.pos == current:
            origin = kid
            return
    print("can't find kid!")

def load():
    global origin
    if os.path.exists('model.pkl'):
        with open('model.pkl', 'rb') as f:
            origin = pickle.loads(f.read())
    else:
        generate()
        print('ready!')
        with open('model.pkl', 'rb') as f:
            origin = pickle.loads(f.read())

def game_run():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cross Chess Board") 
    clock = pygame.time.Clock()

    MAP = [[0,0,0],[0,0,0],[0,0,0]]

    draw_chess_board(screen)
    draw_cross(screen, MAP)     # 必须放在draw_board之后
    pygame.display.flip()
    clock.tick(30)

    running = True
    while running:
        if check(MAP) != None:
            break
        f_find(MAP)
        MAP = f1()
        draw_chess_board(screen)
        draw_cross(screen, MAP)     # 必须放在draw_board之后
        pygame.display.flip()
        clock.tick(30)
        if check(MAP) != None:
            break
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    axis = get_mouse_cell(event.pos)
                    print('axis',axis)
                    if MAP[axis[0]][axis[1]] == 0:
                        MAP[axis[0]][axis[1]] = -1
                        waiting = False

        draw_chess_board(screen)
        draw_cross(screen, MAP)     # 必须放在draw_board之后
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

    return check(MAP)

origin = None
i, j = 0,0
def main():

    
    while True:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Loading......")

        clock = pygame.time.Clock()
        global origin
        load()
        pygame.quit()
        winner = game_run()



if __name__ == '__main__':
    main()
