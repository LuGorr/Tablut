import json

class action:
    """
    A class representing an in game move.
    """
    def __init__(self, src, dst, turn):
        """
        Initialises the instance with piece orgin, destination and turn.

        Parameters
        ----------
        src : str
            Piece's origin, must be of length 2, the first charcter must be from \\'a\\' to \\'i\\' and the second a number from 0 to 9.
        dst : str
            Piece's destination, formatted like src.
        turn : str
            A string representing the player (either \\"WHITE\\" or \\"BLACK\\").
        """
        if(len(src) != 2 or len(dst) != 2):
            raise ValueError("SRC or DST != 2")
        else:
            self.dst = dst
            self.src = src
            self.turn = turn
    
    def to_json(self):
        """
        Converts the action to a json.

        Returns
        -------
        json
            a json version of the action.
        """
        return {
            "from": self.src,
            "to": self.dst,
            "turn": self.turn
        }

