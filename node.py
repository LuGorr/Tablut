import numpy as np
BOARD_SIDE = 9
cols = {
            0:'a',
            1:'b',
            2:'c',
            3:'d',
            4:'e',
            5:'f',
            6:'g',
            7:'h',
            8:'i'
        }
class node:
    def __init__(self, board, player):
        self.value = None
        self.board = board
        self.player = player
        self.already_gen = 0
        self.leaf=None
        self.move = None

    def expand(self, path, stop=False):
        try:
            nums_for_player = [1] if self.player == 1 else [2, 3]
            idxs = np.where(np.isin(self.board, nums_for_player))
            pieces = np.array(list(zip(idxs[0], idxs[1]))).astype(np.int8)
            skipped = 0
            for piece in pieces:
                col_left = [i for i in range(piece[0] - 1, -1, -1)]
                col_right = [i for i in range(piece[0] + 1, BOARD_SIDE)]
                row_left = [i for i in range(piece[1] - 1, -1, -1)]
                row_right = [i for i in range(piece[1] + 1, BOARD_SIDE)]
                for i in col_left:
                    check = self.check_rules(piece, (i,piece[1]))
                    if check and skipped >= self.already_gen:
                        if not stop:
                            self.already_gen += 1
                        new_board = self.board.copy()
                        new_board[piece[0], piece[1]] = 0
                        new_board[i,piece[1]] = self.board[piece[0], piece[1]]
                        kill = self.check_kill(new_board,(i,piece[1]))
                        if kill != None:
                            self.kill = kill
                            new_board[kill[0], kill[1]] = 0
                        ret = node(new_board, (self.player + 1) % 2)
                        ret.check_leaf(path, stop)
                        ret.move = str(piece[0]+1)+cols[piece[1]]+'-'+str(i+1)+cols[piece[1]]
                        return ret
                    elif check and skipped < self.already_gen:
                        skipped += 1
                    else:
                        break
                for i in col_right:
                    check = self.check_rules(piece, (i,piece[1]))
                    if check and skipped >= self.already_gen:
                        if not stop:
                            self.already_gen += 1
                        new_board = self.board.copy()
                        new_board[piece[0], piece[1]] = 0
                        new_board[i, piece[1]] = self.board[piece[0], piece[1]]
                        kill = self.check_kill(new_board,(i,piece[1]))
                        if kill != None:
                            self.kill = kill
                            new_board[kill[0], kill[1]] = 0
                        ret = node(new_board, (self.player + 1) % 2)
                        ret.check_leaf(path, stop)
                        ret.move = str(piece[0]+1)+cols[piece[1]]+'-'+str(i+1)+cols[piece[1]]
                        return ret
                    elif check and skipped < self.already_gen:
                        skipped += 1
                    else:
                        break
                for i in row_left:
                    check = self.check_rules(piece, (piece[0],i))
                    if check and skipped >= self.already_gen:
                        if not stop:
                            self.already_gen += 1
                        new_board = self.board.copy()
                        new_board[piece[0], piece[1]] = 0
                        new_board[piece[0], i] = self.board[piece[0], piece[1]]
                        kill = self.check_kill(new_board,(piece[0],i))
                        if kill != None:
                            self.kill = kill
                            new_board[kill[0], kill[1]] = 0
                        ret = node(new_board, (self.player + 1) % 2)
                        ret.check_leaf(path, stop)
                        ret.move = str(piece[0]+1)+cols[piece[1]]+'-'+str(piece[0]+1)+cols[i]
                        return ret
                    elif check and skipped < self.already_gen:
                        skipped += 1
                    else:
                        break
                for i in row_right:
                    check = self.check_rules(piece, (piece[0],i))
                    if check and skipped >= self.already_gen:
                        if not stop:
                            self.already_gen += 1
                        new_board = self.board.copy()
                        new_board[piece[0], piece[1]] = 0
                        new_board[piece[0], i] = self.board[piece[0], piece[1]]
                        kill = self.check_kill(new_board,(piece[0],i))
                        if kill != None:
                            self.kill = kill
                            new_board[kill[0], kill[1]] = 0
                        ret = node(new_board, (self.player + 1) % 2)
                        ret.check_leaf(path, stop)
                        ret.move = str(piece[0]+1)+cols[piece[1]]+'-'+str(piece[0]+1)+cols[i]
                        return ret
                    elif check and skipped < self.already_gen:
                        skipped += 1
                    else:
                        break
        except:
            pass
        return None

    def check_rules(self, prev, piece):
        try:
            fortress = [(0,3),(0,4),(0,5),(1,4),(3,0),(4,0),(5,0),(4,1),
                    (3,8),(4,8),(5,8),(4,7),(8,3),(8,4),(8,5),(7,4),(4,4)]
            if self.board[piece] != 0:
                return False
            if (self.player == 0) and piece in fortress:
                return False
            if (self.player == 1) and (prev[0], prev[1]) not in fortress and piece in fortress[0:-1]:
                return False
            if (self.player == 1) and piece in fortress[-1]:
                return False
        except:
            pass
        return True
    #TODO ancora semplicistico, non tiene in conto se è il re o se la casella adiacente è una fortezza,
    #attento alle eccezioni!
    def check_kill(self, board, piece):
        board = board.tolist()
        p1 = int(piece[0])
        p2 = int(piece[1])
        piece = (p1, p2)
        fortress = [(0,3),(0,4),(0,5),(1,4),(3,0),(4,0),(5,0),(4,1),
                    (3,8),(4,8),(5,8),(4,7),(8,3),(8,4),(8,5),(7,4),(4,4)]
        opponent = 2 if self.player == 1 else 1
        for i in [0, 2]:
            j = -1 if i == 0 else 1
            row_index = piece[0] - 1 + i
            col_index = piece[1] - 1 + i
    
            # Verifica se gli indici sono fuori limiti prima di procedere
            if row_index < 0 or row_index > 8:
                continue
            if col_index < 0 or col_index > 8:
                continue

            # Calcola l'indice con j (aggiunta di j)
            row_index_with_j = piece[0] - 1 + i + j
            col_index_with_j = piece[1] - 1 + i + j

         # Verifica se l'indice con j è fuori limiti
            if col_index_with_j < 0 or col_index_with_j > 8:
                continue
            if row_index_with_j < 0 or row_index_with_j > 8:
                continue

            #TOFIX white checkers don't kill blacks adjacent to camps
            try:
                if (((board[piece[0]-1+i][piece[1]] == opponent) or 
                     (self.player == 1 and board[piece[0]-1+i][piece[1]] == 3))):
                    if (((board[piece[0]-1+i][piece[1]] != 3) and 
                         (self.player == 0 and board[piece[0]-1+i+j][piece[1]] in [2, 3]) or 
                         (self.player == 1 and board[piece[0]-1+i+j][piece[1]] == 1) or 
                         (piece[0]-1+i+j,piece[1]) in fortress) or ((board[piece[0]-1+i][piece[1]] == 3) and 
                         (self.player == 1) and (board[piece[0]-1+i][piece[1]-1] == 1) and 
                         (board[piece[0]-1+i][piece[1]+1] == 1) and 
                         (((piece[0]-1+i+j, piece[1]) == fortress[-1]) or 
                          ((board[piece[0]-1+i+j][piece[1]]== 1) and 
                           (piece[0]-1+i, piece[1]) == fortress[-1])))):
                            return (piece[0]-1+i, piece[1])
            except Exception:
                continue
        for i in [0, 2]:
            j = -1 if i == 0 else 1
            row_index = piece[0] - 1 + i
            col_index = piece[1] - 1 + i
    
            # Verifica se gli indici sono fuori limiti prima di procedere
            if row_index < 0 or row_index > 8:
                continue
            if col_index < 0 or col_index > 8:
                continue

            # Calcola l'indice con j (aggiunta di j)
            row_index_with_j = piece[0] - 1 + i + j
            col_index_with_j = piece[1] - 1 + i + j

         # Verifica se l'indice con j è fuori limiti
            if col_index_with_j < 0 or col_index_with_j > 8:
                continue
            if row_index_with_j < 0 or row_index_with_j > 8:
                continue

            try:
                if ((board[piece[0]][piece[1]-1+i] == opponent) or 
                    (self.player == 1 and board[piece[0]][piece[1]-1+i] == 3)):
                    if (((board[piece[0]][piece[1]-1+i] != 3) and 
                        (self.player == 0 and board[piece[0]][piece[1]-1+i+j] in [2, 3]) or
                        (self.player == 1 and board[piece[0]][piece[1]-1+i+j] == 1) or
                        (piece[0],piece[1]-1+i+j) in fortress) or ((board[piece[0]][piece[1]-1+i] == 3) and
                        (self.player == 1) and (board[piece[0]-1][piece[1]-1+i] == 1) and 
                        (board[piece[0]+1][piece[1]-1+i] == 1) and (((piece[0], piece[1]-1+i+j) == fortress[-1]) or
                        ((board[piece[0]][piece[1]-1+i+j]== 1) and (piece[0],piece[1]-1+i) == fortress[-1])))):
                            return (piece[0], piece[1]-1+i)
            except Exception as e:
                continue
        return None

        
    def check_leaf(self, path, stop):
        try:
            escapes = [(0,1),(0,2),(0,6),(0,7),(8,1),(8,2),(8,6),(8,7),
                   (1,0),(2,0),(6,0),(7,0),(1,8),(2,8),(6,8),(7,8)]
            if 3 not in self.board:
                self.leaf = 2 - self.player
            if list(zip(np.where(self.board == 3))) in escapes:
                self.leaf = 1 + self.player
            if any(np.array_equal(self.board, arr) for arr in path):
                self.leaf = 3
            if (not stop) and self.already_gen == 0 and self.expand(path, stop=True) == None:
                self.leaf = 2
        except:
            pass



if __name__=="__main__":
    a = node(np.array([[0, 0, 0, 1, 0, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 2, 0, 0, 0, 0, 0],
                       [1, 0, 0, 0, 2, 0, 0, 0, 1],
                       [1, 1, 2, 2, 3, 2, 2, 1, 1],
                       [1, 0, 0, 0, 2, 0, 0, 0, 1],
                       [0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0, 0]]), 0)
    a.check_kill(a, (2,3))

