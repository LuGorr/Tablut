class Strategy:
    def __init__(self, search_strategy, weight_engine, heuristics, depth):
        self.search_strategy = search_strategy
        self.weight_engine = weight_engine
        self.heuristics = heuristics
        self.depth = depth
    
    def get_move(self, node):
        boards = self.search_strategy.get_leaves(node)
        boards_with_scores = [[] for _ in range(len(boards))]
        for heuristic in self.heuristics:
            for index, board in enumerate(boards):
             boards_with_scores[index].append(heuristic.approximate(board))
        boards_reduced = []
        for weights in boards_with_scores:
           boards_reduced.append(self.weight_engine.reduce(weights))
        return self.search_strategy.search(boards_reduced, node)
        