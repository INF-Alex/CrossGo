import os
import copy
from queue import Queue
import pickle
import pygame
import sys
import numpy as np
import tkinter as tk
import tkinter.messagebox

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE
TICK = 1
CROSS = -1
EMPTY = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
C1 = (255, 0, 0)
C2 = (0, 0, 255)

class Board:
    def __init__(self, playerA:list=None, playerB:list=None, A=TICK, B=CROSS, turn=TICK):
        self.pos = [[0,0,0],[0,0,0],[0,0,0]]
        self.avai = [[x,y] for x in range(3) for y in range(3)]
        self.A = A
        self.B = B
        self.turn = turn    # 轮到的玩家
        if playerA:
            for x,y in playerA:
                self.pos[x][y] = self.A
        if playerB:
            for x,y in playerB:
                self.pos[x][y] = self.B
    def place(self, position):
        self.pos[position[0]][position[1]] = self.turn
        self.turn = -self.turn
        self.avai.pop(self.avai.index(position))
    def check(self):
        for player in [self.A, self.B]:
            if (any([all([self.pos[x][y] == player for y in range(3)]) for x in range(3)]) 
             or any([all([self.pos[x][y] == player for x in range(3)]) for y in range(3)])):
                return player
            if all([self.pos[x][x] == player for x in range(3)]) or all([self.pos[x][2-x] == player for x in range(3)]):
                return player
        if self.avai == []:
            return 0    # 平局
        return None
    def next(self):
        posibilities = list()
        for p in self.avai:
            tmp = copy.deepcopy(self)
            tmp.place(p)
            posibilities.append(TreeNode(tmp))
        return posibilities
    
class TreeNode:
    def __init__(self, root, child=None):
        self.root = root
        self.child = child
        self.value = None
    def add_child(self, child):
        self.child.append(child)
    def cal_val(self):
        if self.value == None:
            if any([kid.cal_val() == self.root.turn for kid in self.child]):
                self.value = self.root.turn
            elif any([kid.cal_val() == 0 for kid in self.child]):
                self.value = 0
            else:
                self.value = -self.root.turn
        return self.value
    def count(self):
        if self.child == None:
            return 1
        return sum([kid.count() for kid in self.child])
    
    
def generate():
    print('generating model...')
    game = Board()
    origin = TreeNode(game)
    origin.child = game.next()
    workplace = Queue()

    for kid in origin.child:
        workplace.put(kid)

    while not workplace.empty():
        item = workplace.get()
        if item.root.check() != None:
            item.value = item.root.check()
        else:
            item.child = item.root.next()
            for kid in item.child:
                workplace.put(kid)

    origin.cal_val()
    with open('model.pkl','wb') as f:
        model_str = pickle.dumps(origin)
        print(origin.child[0].value)
        assert(origin.child[0].child[0].child[0].child[1].child[3].child[0].child[0].child[1].value == 0)
        print('assert1 ok')
        f.write(model_str)
    
def f1():
    global origin
    a = [origin.child[i].value for i in range(len(origin.child))]
    origin = origin.child[np.argmax(a)]
    return origin.root.pos
def f2():
    global origin
    a = [origin.child[i].value for i in range(len(origin.child))]
    origin = origin.child[np.argmin(a)]
    return origin.root.pos
def f_find(current):
    global origin
    for kid in origin.child:
        if kid.root.pos == current:
            origin = kid
            return
    print("can't find kid!")


def draw_chess_board(screen):
    screen.fill(WHITE)
    for x in [HEIGHT/3,HEIGHT*2/3]:
        pygame.draw.line(screen, BLACK, (x, 0), (x, WIDTH), 2)
    for y in [WIDTH/3,WIDTH*2/3]:
        pygame.draw.line(screen, BLACK, (0, y), (HEIGHT, y), 2)

def draw_cross(screen, MAP):
    for row in range(3):
        for col in range(3):
            if MAP[row][col]:
                x = row * SQUARE_SIZE + SQUARE_SIZE // 2
                y = col * SQUARE_SIZE + SQUARE_SIZE // 2
                if MAP[row][col] == 1:
                    pygame.draw.circle(screen, C1, (x, y), SQUARE_SIZE // 5)
                else:
                    pygame.draw.circle(screen, C2, (x, y), SQUARE_SIZE // 5)

def get_mouse_cell(position):
    return [position[0] // SQUARE_SIZE, position[1] // SQUARE_SIZE]

def check(MAP):
    for player in [TICK,CROSS]:
        if (any([all([MAP[x][y] == player for y in range(3)]) for x in range(3)]) 
            or any([all([MAP[x][y] == player for x in range(3)]) for y in range(3)])):
            return player
        if all([MAP[x][x] == player for x in range(3)]) or all([MAP[x][2-x] == player for x in range(3)]):
            return player
    if all([MAP[x][y] != 0 for x in range(3) for y in range(3)]):
        return 0    # 平局
    return None



def game_run(screen,clock):
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
    return check(MAP)

origin = None
def main():

    while True:
        pygame.init()

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Loading......")

        clock = pygame.time.Clock()
        global origin
        if os.path.exists('model.pkl'):
            with open('model.pkl', 'rb') as f:
                origin = pickle.loads(f.read())
        else:
            generate()
            print('ready!')
            with open('model.pkl', 'rb') as f:
                origin = pickle.loads(f.read())

        pygame.display.set_caption("Cross Chess Board")
        winner = game_run(screen, clock)
        pygame.quit()



if __name__ == '__main__':
    main()
