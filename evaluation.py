import numpy as np
import traceback
############### maybe too expensive, could modify-remove parameters

def no_obstacles_between(board,coordinations_1, coordinations_2):
    v=0
    if (coordinations_1[0]!=coordinations_2[0]) and  (coordinations_1[1]!=coordinations_2[1]):
        return False
    elif coordinations_1[0]==coordinations_2[0]:
        i=coordinations_1[0]
        for j in (min(coordinations_1[1],coordinations_2[1])+1, max(coordinations_1[1],coordinations_2[1])):
            if i in range(0,9) and j in range(0,9) and board[i][j]!=0:
                v+=1
    elif coordinations_1[1]==coordinations_2[1]:
        j=coordinations_1[1]
        for i in (min(coordinations_1[0],coordinations_2[0])+1, max(coordinations_1[0],coordinations_2[0])):
            if i in range(0,9) and j in range(0,9) and board[i][j]!=0:
                v+=1
    if v==0:
        return True
    else:
        return False

def could_reach(board, coordinations_1, coordinations_2): #if pieces in coordinations1 could reach king in coordinations2
    i=coordinations_2[0] #συντεταγμένες βασιλιά 
    j=coordinations_2[1]
    if (coordinations_1[0] in range(i-1,i+2 )) or (coordinations_1[1] in range(j-1, j+2)): #πρέπει να αποκλείσω τα καμπς 
        if (i-1 in range(0,9) and j in range(0,9)):
            if no_obstacles_between(board, coordinations_1, (i-1,j)):
                return True
        if (i+1 in range(0,9) and j in range(0,9)):
            if no_obstacles_between(board, coordinations_1, (i+1,j)):
                return True
        if (j+1 in range(0,9) and i in range(0,9)):
            if no_obstacles_between(board, coordinations_1, (i,j+1)):
                return True
        if (j-1 in range(0,9) and i in range(0,9)):
            if no_obstacles_between(board, coordinations_1, (i,j-1)):
                #isws na raise exemption gia otan kapoio synoro toy vasilia einai camp
                #μπορεί και να μην χρειαζεται να τα αποκλείσουμε, απλώς κανει πιο ισχυρή την περιπτωση ο βασιλιας να είναι δίπλα σε καμπ..
                return True
    else:
        return False
        
      
    #####need to check if its a camp, 

class heuristic:
    
    def __init__ (self, listOfweights):
        self.weights=listOfweights #4 for black, 5 for white

    

    def get(self, board,player):
        if player==1:
            #runs for black player:
            evaluation=0
            #take into consideration 4 parameters :
            # number  of black pawns  
            # number  of white pawns 
            # number of black pawns and towers adjacent to the king 
            # and finally # of unobstructed paths to the king
        
            #for the first parameter:
            black_pieces = np.count_nonzero(board == 1)

            #for the second parameter:
            white_pieces = np.count_nonzero(board == 2)

            #for the third:
            count=0
            attack=0 #number of unobstracted paths to the king
            fortress=[(0,3),(0,4),(0,5),(1,4),(3,0),(4,0),(5,0),(4,1),(4,4),
                      (3,8),(4,8),(5,8),(4,7),(8,3),(8,4),(8,5),(7,4)]
            try:
                king= (np.where(board==3)[0][0], np.where(board==3)[1][0]) #coordunations of the king
                i,j= king[0], king[1] 
                if (i-1 >= 0) and (board[i-1][j]==1) or ((i-1,j) in fortress):
                    count+=1
                if (i+1 < 9) and board[i+1][j]==1 or ((i+1,j) in fortress):
                    count+=1
                if (j-1 >= 0) and board[i][j-1]==1 or ((i,j-1) in fortress):
                    count+=1
                if (j+1 < 9) and board[i][j+1]==1 or ((i,j+1) in fortress):
                    count+=1
            
                #for the forth parameter
               
                bl= np.where(board==1) #επιστρεφει (array([0, 0, 0, 1, 3, 3, 4, 4, 4, 4, 5, 5, 7, 8, 8, 8]), array([3, 4, 5, 4, 0, 8, 0, 1, 7, 8, 0, 8, 4, 3, 4, 5]))
            
                for k in range(len(bl[0])): 
                    a=(bl[0][k],bl[1][k]) #μαύρα πούλια
                    if could_reach(board, a, king)==True:
                        attack+=1
            except:
                pass
        
            try:
                evaluation = self.weights[0]*black_pieces - self.weights[1]*white_pieces + self.weights[2]*count + self.weights[3]*attack
            except:
                pass
            return evaluation





        elif player==0:
        # evaluation_white 
            #take into consinderation 
        #  of black pawns  
        # # of white pawns 
        # # unobstructed paths from the king to the border *****
        # # towers or black pawns adj to the king (state of the king)
        # #freePaths to the king (same as black's IV)

        
            #for the first parameter:
            black_pieces = np.count_nonzero(board == 1)

            #for the second parameter:
            white_pieces = np.count_nonzero(board == 2)

            #for the third parameter:
            paths=0
            count=0
            danger=0
            try:
                king= (np.where(board==3)[0][0],np.where(board==3)[1][0])
                border = [(0,1), (0,2), (0,6), (0,7), (1,0), (1,8), (2,0), (2,8), (6,0), (6,8), (7,0), (7,8), (8,1), (8,2), (8,6), (8,7)] #removed the corner pieces, as they are useless
                for a in border:
                    if no_obstacles_between(board,king,a) == True:
                        paths+=1
        

            #for the forth parameter:
            
                fortress=[(0,3),(0,4),(0,5),(1,4),(3,0),(4,0),(5,0),(4,1),(4,4),
                        (3,8),(4,8),(5,8),(4,7),(8,3),(8,4),(8,5),(7,4)]
        
                i,j =king[0],king[1]
                #i,j= int(np.where(board==3)[0]) , int(np.where(board==3)[1]) #coordunations of the king
                if (i-1 >= 0) and (board[i-1][j]==1) or ((i-1,j) in fortress):
                    count+=1
                if (i+1 < 9) and board[i+1][j]==1 or ((i+1,j) in fortress):
                    count+=1
                if (j-1 >= 0) and board[i][j-1]==1 or ((i,j-1) in fortress):
                    count+=1
                if (j+1 < 9) and board[i][j+1]==1 or ((i,j+1) in fortress):
                    count+=1

            #for the fifth parameter:
                 #number of unobstracted paths to the king
                bl= np.where(board==1) 
            
                for k in range(len(bl[0])): 
                    a=(bl[0][k],bl[1][k]) #μαύρα πούλια
                    if could_reach(board, a, king)==True:
                        danger+=1
            except:
                pass
            try:
                fitness_of_the_board = -self.weights[0]*black_pieces + self.weights[1]*white_pieces + self.weights[2]*paths - self.weights[3]*count - self.weights[4]*danger
            except:
                pass
        
            return fitness_of_the_board
        


if __name__=="__main__":
    heu = heuristic([1, 1, 1, 1, 1])
    board = np.array([[0,0,1,0,1,1,0,0,0],
             [0,0,0,0,1,0,0,0,0],
             [0,0,0,0,2,0,0,0,0],
             [1,0,0,2,3,0,0,0,1],
             [1,1,2,2,0,2,2,1,1],
             [1,0,0,0,2,0,0,0,1],
             [0,0,0,1,2,0,0,0,0],
             [0,0,0,0,1,0,0,0,0],
             [0,0,0,0,1,1,0,0,0]])
    heu.get(board, 1)
    