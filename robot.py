# import json
# import os
import numpy as np
import copy
from queue import Queue

TICK = 1
CROSS = -1
EMPTY = 0

# if os.path.exists('model.json'):
#     with open('model.json','r',encoding='utf-8') as f :
#         model = json.load(f)
# else:
#     model = dict()


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
    
# 对于先手的树
class TreeNode:
    def __init__(self, root, child=None):
        self.root = root
        self.child = child
        self.value = None
    def add_child(self, child):
        self.child.append(child)
    def cal_val(self):
        if self.value == None:
            v = sum([kid.cal_val() for kid in self.child])
            self.value = v
            return v
        else:
            return self.value
    def count(self):
        if self.child == None:
            return 1
        return sum([kid.count() for kid in self.child])

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

print(origin.cal_val())
model = origin


# with open('model.json', 'w') as f:
#     json.dump(model, f)
