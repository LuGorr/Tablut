
import random 
import node
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pydot
class move_tree:
    def __init__(self, value):
        self.value = value
        self.childs = []
        self.count = 0
    def limited_depth_dfs(self, node=None, max_depth=0, current_depth=0, parent_child_relations=None):
        if node is None:
            node = self
        if node is None or current_depth > max_depth:
            return parent_child_relations
    

        if parent_child_relations is None:
            parent_child_relations = {}
    

        parent_child_relations[node.value] = [child.value for child in node.childs]
    

        for child in node.childs:
            self.limited_depth_dfs(child, max_depth, current_depth + 1, parent_child_relations)
    
        return parent_child_relations
    def create_graph(self, node=None, graph=None):
        self.count+=1
        if (self.count%10000) == 0:
            print(self.count)
        if graph is None:
            graph = nx.DiGraph()

        if node is None:
            node = self
        

        for child in node.childs:
            graph.add_edge(f"{id(node)} -> {node.value}", f"{id(child)} -> {child.value}")
            graph = self.create_graph(child, graph)
        
        return graph
    
    def save_graph(self, filename="tree_graph.png"):
        graph = self.create_graph()
        print("done")
        pydot_graph = nx.nx_pydot.to_pydot(graph)
        print(1)
        pydot_graph.set_graph_defaults(dpi=300)  # Migliora la qualità dell'immagine
        pydot_graph.set_edge_defaults(minlen="2")  # Aumenta la lunghezza minima degli archi
        pydot_graph.set_graph_defaults(splines="true")  # Usa spline curve per evitare sovrapposizioni
        pydot_graph.set_graph_defaults(sep="+4")  # Distanza tra i nodi
        pydot_graph.set_graph_defaults(overlap="scale")  # Evita sovrapposizioni
        print(2)
        pydot_graph.write_png(filename, prog="sfdp")

class minimax_base:
    def __init__(self, node, depth, heuristics, weight_engine):
        self.node = node
        self.depth = depth
        self.heuristics = heuristics
        self.weight_engine = weight_engine
        self.tree = move_tree(None)
        self.count = 0
    
    def search(self, node=None, depth=None, max_player=True, path=[], tree_src=None):
        self.count+=1
        if node is None:
            node = self.node
        if path == []:
            path = [node.board]
        if depth is None:
            depth = self.depth
        if (depth == 0):
            tree_src.value = self.heuristics.get(node.board)
            return tree_src.value
        if tree_src == None:
            tree_src = self.tree
        if max_player:
            tree_src.value = float('-inf')
            while True:
                child = node.expand(path)
                if child == None:
                    break
                tree_src.childs.append(move_tree(None))
                i = tree_src.childs.index(tree_src.childs[-1])
                tree_src.value = max(tree_src.value, self.search(child, depth - 1, False, path+[child.board], tree_src.childs[i]))

        else:
            tree_src.value = float('inf')
            while True:
                child = node.expand(path)
                if child == None:
                    break
                tree_src.childs.append(move_tree(None))
                i = tree_src.childs.index(tree_src.childs[-1])
                tree_src.value = min(tree_src.value, self.search(child, depth - 1, True, path+[child.board], tree_src.childs[i]))
        return tree_src.value
        
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