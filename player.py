import json
import socket
import action as act
import select
import struct
import game_state as gs
import matplotlib.pyplot as plt
import numpy as np

class tablut_client:
    """
    A class representing the client side of the agent.
    No behavioral code should be put here. 
    Only GUI, basic turnation logic and server communication.
    """
    def __init__(self, player, name, timeout, ip_address):
        """
        Initiates the instance (kind of player, player name, timeout, ip_address, port).
        
        Parameters
        ----------
        player : str
            Either "WHITE" or "BLACK".
        name : str
            Player name.
        timeout : int
            Used in the Java implementation, usage not clear.
        ip_address : str
            Server's ip address.
        """
        self.player = player
        self.name = name + "\n"
        self.timeout = timeout
        self.server_ip = ip_address
        if player == "WHITE":
            self.port = 5800
        elif player == "BLACK":
            self.port = 5801
        self.columns = {
            'a':0,
            'b':1,
            'c':2,
            'd':3,
            'e':4,
            'f':5,
            'g':6,
            'h':7,
            'i':8
        }
        
    def connect(self):
        """
        Creates a socket with the server's ip and port (different for white and black) then creates a connection.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.port))

    def write(self, action):
        """
        Sends an action (action.py) to the server.

        Parameters
        ----------
        action : action
            An action containing starting point and destination point of the piece.
        """
        json_action = json.dumps(action.to_json()).encode("utf-8")
        self.socket.sendall(struct.pack(">I", len(json_action)))
        self.socket.send(json_action)
    
    def recvall(self, n):
        """
        Treates a byte string containing the full message of length n.

        Parameters
        ----------
        n : int
            The message's length in bytes.
        """
        data = b''
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    def read(self, timeout=10000):  
        """
        Waits for a message to be present in the socket and receives it.

        Parameters
        ----------
        timeout : int
            Timeout in seconds (default is 10000).
        
        Returns
        -------
        str
            A decoded string containing the message.
        """
        # timeout in secondi
        # Attendo che il socket sia pronto a leggere
        ready = select.select([self.socket], [], [], timeout)
        
        if ready[0]:  # Se il socket è pronto a leggere
            raw = self.recvall(4)
            if raw is None:
                return None  # Socket chiuso o errore
            
            msglen = struct.unpack('>I', raw)[0]
            return self.recvall(msglen).decode("utf-8")
        else:
            return None  # Timeout, nessun dato ricevuto
    
    def say_hi(self):
        """
        How cute it is saying hi!
        Sends the player name to the server.
        Mandatory after connection (self.connect()).
        """
        self.socket.sendall(struct.pack('>I', len(self.name)))
        self.socket.sendall(self.name.encode("utf-8"))

    def game_loop_player(self):
        """
        A game loop for a human player.
        Reads the board from server,
        updates the GUI,
        reads a move,
        sends it,
        updates the GUI,
        reads the board after the opponent subits it's move
        and loops back.

        Note: no wind condition added (goes on for eternity).
        """
        turn = True
        while True:
            self.state = gs.game_state(self.read())
            print(self.state.board)
            if(turn):
                self.show_board()
                turn = False
            else:
                self.update_chessboard(self.state.board)
                print("update1")
            while True:
                src = input("src:")
                if self.check_piece_present(src):
                    break
                print("no piece present!")
            dst = input("dst:")
            self.write(act.action(src, dst, "WHITE"))
            self.state = gs.game_state(self.read())
            print(self.state.board)
            if(turn):
                self.show_board()
                turn = False
            else:
                print("update2")
                self.update_chessboard(self.state.board)
            
    
    def check_piece_present(self, piece):
        """
        Checks if a piece is present on the specified location in the board.

        Parameters
        ----------
        piece : str
            A string of length of 2 (mandatory), formed by a lowercase character and an integer (1-9).

        Returns
        -------
        bool
            True if the piece is present, False otherwise.
        """
        if self.player == "WHITE":
            return ((self.state.board[int(piece[1])-1][self.columns[piece[0]]] == 2) or
                    (self.state.board[int(piece[1])-1][self.columns[piece[0]]] == 3))
        else:
            return self.state.board[int(piece[1])-1][self.columns[piece[0]]] == 1

    
    def show_board(self):
        """
        Initializes the GUI (use only one time).
        """
        plt.ion()
        matrix = self.state.board
        n = len(matrix)
        # Creazione della griglia vuota
        fig, self.ax = plt.subplots()
        # Creazione della scacchiera
        self.ax.set_xticks(np.arange(0.5, n, 1))
        self.ax.set_yticks(np.arange(0.5, n, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(True) #dim 9x9
        
        for i in range(n):
            for j in range(n):
                if ((i + j == 1) or (i == 0 and j == 2) or (i == 2 and j == 0) or
                    (i == 0 and j == 6) or (i == 0 and j == 7) or (i == 1 and j == 8) or
                    (i == 2 and j == 8) or (i == 6 and j == 0) or (i == 7 and j == 0) or
                    (i == 6 and j == 8) or (i == 7 and j == 8) or (i == 8 and j == 1) or
                    (i == 8 and j == 2) or (i == 8 and j == 6) or (i == 8 and j == 7)):
                    escape = plt.Rectangle((j-0.5, n-i-1.5), 1, 1, color="cyan")
                    self.ax.add_patch(escape)
                if ((i == 0 and j == 3) or (i == 0 and j == 4) or (i == 0 and j == 5) or
                    (i == 1 and j == 4) or (i == 3 and j == 0) or (i == 4 and j == 0) or
                    (i == 5 and j == 0) or (i == 4 and j == 1) or (i == 4 and j == 7) or
                    (i == 3 and j == 8) or (i == 4 and j == 8) or (i == 5 and j == 8) or
                    (i == 7 and j == 4) or (i == 8 and j == 3) or (i == 8 and j == 4) or
                    (i == 8 and j == 5)):
                    camp = plt.Rectangle((j-0.5, n-i-1.5), 1, 1, color="grey")
                    self.ax.add_patch(camp)
                if (i == 4 and j == 4):
                    castle = plt.Rectangle((j-0.5, n-i-1.5), 1, 1, color="gold")
                    self.ax.add_patch(castle)
                
        # _ E E C C C E E _ #
        # E _ _ _ C _ _ _ E #
        # E _ _ _ _ _ _ _ E #
        # C _ _ _ _ _ _ _ C #
        # C C _ _ T _ _ C C #
        # C _ _ _ _ _ _ _ C #
        # E _ _ _ _ _ _ _ E #
        # E _ _ _ C _ _ _ E #
        # _ E E C C C E E _ #


        # Aggiunta dei simboli sulla scacchiera
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    # Disegno un cerchio nero
                    circle = plt.Circle((j, n-i-1), 0.4, color='black')
                    self.ax.add_patch(circle)
                elif matrix[i][j] == 2:
                    # Disegno un cerchio bianco
                    circle = plt.Circle((j, n-i-1), 0.4, color='white', ec='black')
                    self.ax.add_patch(circle)
                elif matrix[i][j] == 3:
                    # Disegno un re (testo "K")
                    self.ax.text(j, n-i-1, 'K', va='center', ha='center', fontsize=20, color='black')

        # Imposto i limiti della scacchiera
        self.ax.set_xlim(-0.5, n - 0.5)
        self.ax.set_ylim(-0.5, n - 0.5)

        # Mostro la scacchiera
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def update_chessboard(self, matrix):
        """
        Updates the GUI.
        """
        self.ax.clear()  # Pulire l'asse senza chiudere la finestra

        n = len(matrix)

        # Creazione della scacchiera
        self.ax.set_xticks(np.arange(0.5, n, 1))
        self.ax.set_yticks(np.arange(0.5, n, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(True)
        for i in range(n):
            for j in range(n):
                if ((i + j == 1) or (i == 0 and j == 2) or (i == 2 and j == 0) or
                    (i == 0 and j == 6) or (i == 0 and j == 7) or (i == 1 and j == 8) or
                    (i == 2 and j == 8) or (i == 6 and j == 0) or (i == 7 and j == 0) or
                    (i == 6 and j == 8) or (i == 7 and j == 8) or (i == 8 and j == 1) or
                    (i == 8 and j == 2) or (i == 8 and j == 6) or (i == 8 and j == 7)):
                    escape = plt.Rectangle((j-0.5, n-i-1.5), 1, 1, color="cyan")
                    self.ax.add_patch(escape)
                if ((i == 0 and j == 3) or (i == 0 and j == 4) or (i == 0 and j == 5) or
                    (i == 1 and j == 4) or (i == 3 and j == 0) or (i == 4 and j == 0) or
                    (i == 5 and j == 0) or (i == 4 and j == 1) or (i == 4 and j == 7) or
                    (i == 3 and j == 8) or (i == 4 and j == 8) or (i == 5 and j == 8) or
                    (i == 7 and j == 4) or (i == 8 and j == 3) or (i == 8 and j == 4) or
                    (i == 8 and j == 5)):
                    camp = plt.Rectangle((j-0.5, n-i-1.5), 1, 1, color="grey")
                    self.ax.add_patch(camp)
                if (i == 4 and j == 4):
                    castle = plt.Rectangle((j-0.5, n-i-1.5), 1, 1, color="gold")
                    self.ax.add_patch(castle)
        # Aggiunta dei simboli sulla scacchiera
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    # Disegno un cerchio nero
                    circle = plt.Circle((j, n-i-1), 0.4, color='black')
                    self.ax.add_patch(circle)
                elif matrix[i][j] == 2:
                    # Disegno un cerchio bianco
                    circle = plt.Circle((j, n-i-1), 0.4, color='white', ec='black')
                    self.ax.add_patch(circle)
                elif matrix[i][j] == 3:
                    # Disegno un re (testo "K")
                    self.ax.text(j, n-i-1, 'K', va='center', ha='center', fontsize=20, color='black')

        # Imposto i limiti della scacchiera
        self.ax.set_xlim(-0.5, n - 0.5)
        self.ax.set_ylim(-0.5, n - 0.5)

        plt.draw()
        plt.pause(0.001)

def conf():
    """
    Used to create a pre configured instance of tablut_client.
    Useful if thesting from python interpreter (CLI).

    Returns
    -------
    tablut_client
        A pre configured tablut_client. 
    """
    return tablut_client("WHITE", "caio", 40, "localhost")

if __name__ == "__main__":
    tab = tablut_client("WHITE", "caio", 30, "localhost")
    tab.connect()
    tab.say_hi()
    tab.game_loop_player()
