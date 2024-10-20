import json

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
        data = json.loads(state)
        self.board = data['board']
        self.turn = data['turn']


        