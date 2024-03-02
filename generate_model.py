import os
import copy
from queue import Queue
import pickle
import time

TICK = 1
CROSS = -1
EMPTY = 0
start_time = time.time()

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
        self.choice = None
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

if os.path.exists('model.pkl'):
    with open('model.pkl', 'rb') as f:
        origin = pickle.loads(f.read())
else:
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

    with open('model.pkl','wb') as f:
        model_str = pickle.dumps(origin)
        f.write(model_str)

# print('OriginVal:',origin.cal_val())

# tree = copy.deepcopy(origin)
# def f1():
#     global tree
#     a = [tree.child[i].value for i in range(len(tree.child))]
#     tree = tree.child[np.argmax(a)]
#     print(np.argmax(a))
#     return np.argmax(a)
# def f2():
#     global tree
#     a = [tree.child[i].value for i in range(len(tree.child))]
#     tree = tree.child[np.argmin(a)]
#     print(np.argmin(a))
#     return np.argmin(a)


end_time = time.time()
print('running time:',end_time-start_time,'s')