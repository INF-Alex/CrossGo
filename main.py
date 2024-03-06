import os
import copy
import random
from queue import Queue
from threading import Thread
import pickle
import pygame
import sys
import time
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
    global origin, path
    node = ask(origin,path)
    a = [node.child[i].value for i in range(len(node.child))]
    x = wander(a,max)
    # x = np.argmax(a)
    path.append(x)
    return node.child[x].root.pos
def f2():
    global origin,path
    node = ask(origin,path)
    a = [node.child[i].value for i in range(len(node.child))]
    x = wander(a,min)
    path.append(x)
    return node.child[x].root.pos
def f_find(current):
    global origin,path
    node = ask(origin,path)
    for i,kid in enumerate(node.child):
        if kid.root.pos == current:
            path.append(i)
            return

def load():
    pygame.init()
    pygame.display.set_caption("Loading......")

    global origin
    if os.path.exists('model.pkl'):
        with open('model.pkl', 'rb') as f:
            origin = pickle.loads(f.read())
    else:
        generate()
        print('ready!')
        with open('model.pkl', 'rb') as f:
            origin = pickle.loads(f.read())

    pygame.quit()

def ask(origin, path):
    if path == []:
        return origin
    p = copy.deepcopy(path)
    x = p.pop(0)
    return ask(origin.child[x], p)

def game_run_1():
    global origin, path
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cross Chess") 
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
        MAP = copy.deepcopy(f1())
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

def game_run_2():
    global origin, path
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cross Chess") 
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
                        MAP[axis[0]][axis[1]] = 1
                        waiting = False

        draw_chess_board(screen)
        draw_cross(screen, MAP)     # 必须放在draw_board之后
        pygame.display.flip()
        clock.tick(30)
        if check(MAP) != None:
            break
        f_find(MAP)
        MAP = copy.deepcopy(f2())
        draw_chess_board(screen)
        draw_cross(screen, MAP)     # 必须放在draw_board之后
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

    return check(MAP)

def main():

    load()
    while True:
        global path
        path = list()
        x = input('请选择1或2：')
        while x != '1' and x != '2':
            x = input('请选择1或2：')
        if x == '1':    
            winner = game_run_1()
        if x == '2':    
            winner = game_run_2()


if __name__ == '__main__':
    main()
