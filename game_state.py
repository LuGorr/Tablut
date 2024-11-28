import json
import numpy as np
class game_state:
    """
    A class representing the game state.
    """
    def __init__(self, state):
        """
        Initialises the instance.
        Board is a 2-dimensional 9x9 matrix representing the board and turn is a string either containing \\"WHITE\\" or \\"BLACK\\".
        
        Parameters
        ----------
        state : json
            A json object containing a field for the board and one for the turn.
        """
        piece_map = {'EMPTY': 0, 'BLACK': 1, 'WHITE': 2, 'KING': 3, 'THRONE':0}
        data = json.loads(state)
        self.board = np.array([[piece_map[piece] for piece in row] for row in data['board']], dtype=np.int8)
        self.turn = data['turn']


        