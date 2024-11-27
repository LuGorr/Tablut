
import random 
import node
import numpy as np
import time
class move_tree:
    def __init__(self, value, move=None):
        self.value = value
        self.childs = []
        self.count = 0
        self.move = move
        self.node = None

class minimax_base:
    def __init__(self, node, depth, heuristics, weight_engine):
        self.node = node
        self.depth = depth
        self.heuristics = heuristics
        self.weight_engine = weight_engine
        self.tree = move_tree(None)
        self.count = 0
    
    def search(self, node=None, depth=None, max_player=True, path=[], tree_src=None, start=float("-inf"), alpha=float('-inf'), beta=float('+inf')):
        if (time.time() - start) > 50:
            raise Exception
        self.count+=1
        if node is None:
            node = self.node
        if path == []:
            path = [node.board]
        if depth is None:
            depth = self.depth
        if (depth == 0):
            tree_src.value = self.heuristics.get(node.board)
            tree_src.node = node
            tree_src.path = path
            return tree_src.value
        if tree_src == None:
            tree_src = self.tree
        if isinstance(node, str) and tree_src.childs == []:
            node = tree_src.node
            path = tree_src.path
        if max_player:
            tree_src.value = float('-inf')
            if tree_src.childs != []:
                for c in tree_src.childs:
                    tree_src.value = max(tree_src.value, self.search("", depth - 1, True, "", c, start=start, alpha=alpha, beta=beta))
            else:
                while True:
                    child = node.expand(path)
                    if child == None:
                        break
                    tree_src.childs.append(move_tree(None, child.move))
                    i = tree_src.childs.index(tree_src.childs[-1])
                    tree_src.value = max(tree_src.value, self.search(child, depth - 1, False, path+[child.board], tree_src.childs[i], start=start, alpha=alpha, beta=beta))
                    alpha = max(alpha, tree_src.value)
                    if beta <= alpha:
                        return alpha

        else:
            tree_src.value = float('inf')
            if tree_src.childs != []:
                for c in tree_src.childs:
                    tree_src.value = min(tree_src.value, self.search("", depth - 1, True, "", c, start=start, alpha=alpha, beta=beta))
            else:
                while True:
                    child = node.expand(path)
                    if child == None:
                        break
                    tree_src.childs.append(move_tree(None, child.move))
                    i = tree_src.childs.index(tree_src.childs[-1])
                    tree_src.value = min(tree_src.value, self.search(child, depth -  1, True, path+[child.board], tree_src.childs[i], start=start, alpha=alpha, beta=beta))
                    beta = min(beta, tree_src.value)
                    if beta <= alpha:
                        return beta
        return tree_src.value
    def get_move(self):
        best = max(self.tree.childs, key=lambda t : t.value)
        self.node = best
        return best.move
class tmp:
    def get(self, a):
        return random.randint(0,10)

if __name__ == "__main__":
    test_node = node.node(np.array([[0,0,0,1,1,1,0,0,0],
                   [0,0,0,0,1,0,0,0,0],
                   [0,0,0,0,2,0,0,0,0],
                   [1,0,0,0,2,0,0,0,1],
                   [1,1,2,2,3,2,2,1,1],
                   [1,0,0,0,2,0,0,0,1],
                   [0,0,0,0,2,0,0,0,0],
                   [0,0,0,0,1,0,0,0,0],
                   [0,0,0,1,1,1,0,0,0]]), 0)
    src = minimax_base(test_node, 3, tmp(), None)
    src.search()
    print(src.count)
    src.tree.save_graph("tree.png")