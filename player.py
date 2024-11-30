import json
import socket
import action as act
import select
import struct
import game_state as gs
import numpy as np
from minimax_base import minimax_base
from minimax_base import TimeException
from minimax_base import move_tree
from node import node
import time
import copy
import argparse
import evaluation


class tablut_client:
    """
    A class representing the client side of the agent.
    No behavioral code should be put here. 
    Only GUI, basic turnation logic and server communication.
    """
    def __init__(self, player, name, timeout, ip_address, heuristics, port=None):
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
        if port == None:
            if player == "WHITE":
                self.port = 5800
            elif player == "BLACK":
                self.port = 5801
        else:
            self.port = port
        self.state = None
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
        self.minimax = minimax_base(node(np.array([[0,0,0,1,1,1,0,0,0],
                   [0,0,0,0,1,0,0,0,0],
                   [0,0,0,0,2,0,0,0,0],
                   [1,0,0,0,2,0,0,0,1],
                   [1,1,2,2,3,2,2,1,1],
                   [1,0,0,0,2,0,0,0,1],
                   [0,0,0,0,2,0,0,0,0],
                   [0,0,0,0,1,0,0,0,0],
                   [0,0,0,1,1,1,0,0,0]]), 0), 2, heuristics, self.timeout, playing_player= (0 if player == "WHITE" else 1))
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
    
    def read(self, turn, timeout=10000):  
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
        while True:
            ready = select.select([self.socket], [], [], timeout)
        
            if ready[0]:  # Se il socket è pronto a leggere
                raw = self.recvall(4)
                if raw is None:
                    return None  # Socket chiuso o errore
            
                msglen = struct.unpack('>I', raw)[0]
                ret =  gs.game_state(self.recvall(msglen).decode("utf-8"))
            else:
                ret = None  # Timeout, nessun dato ricevuto
            if ret!= None:
                break
        return ret
    
    def say_hi(self):
        """
        How cute it is saying hi!
        Sends the player name to the server.
        Mandatory after connection (self.connect()).
        """
        self.socket.sendall(struct.pack('>I', len(self.name)))
        self.socket.sendall(self.name.encode("utf-8"))
    
    def game_loop_agent(self):
        turn = 0
        t = True
        d = False
        already = 0
        tmp_tree = None
        opponent = "BLACK" if self.player == "WHITE" else "WHITE"
        self.state = self.read("WHITE")
        if self.player == "BLACK":
                self.state = self.read("BLACK")
                
        while True:
            start = time.time()
            i = 1
            try:
                while True:
                    if self.state is None:
                        self.minimax.search(None, depth=i, start=start)
                        tmp_tree = copy.deepcopy(self.minimax.tree)
                    else:
                        self.minimax.search(node(self.state.board, 0 if self.player == "WHITE" else 1), 
                                            depth=i, start=start)
                        tmp_tree = copy.deepcopy(self.minimax.tree)
                    i+=1
            except TimeException:
                pass
            except Exception:
                pass
            self.minimax.tree = tmp_tree
            src, dst = self.minimax.get_move().split("-", 1)
            self.minimax.tree = next((c for c in self.minimax.tree.childs if c.move == src+"-"+dst), None) 
            src = src[::-1]
            dst = dst[::-1]
            
            self.write(act.action(src, dst, self.player))
            turn+=1
            self.state = self.read(opponent)
            if self.state.turn in ["WHITEWIN", "BLACKWIN", "DRAW"]:
                return (turn, self.state.turn)
            tmp = self.read(self.player)

            if tmp.turn in ["WHITEWIN", "BLACKWIN", "DRAW"]:
                return (turn, tmp.turn)
            move = self.get_move(self.state, tmp)
            mv1, mv2 = (move.split("-", 1))
            move = str(int(mv1[1]) + 1) + mv1[0] +"-"+ str(int(mv2[1]) + 1) + mv2[0]
            self.state = tmp   
            self.minimax.tree = next((c for c in self.minimax.tree.childs if c.move == move), None) 
            if self.minimax.tree is None:
                self.minimax.tree = move_tree(None, move)

    def get_move(self, before, after):
        if self.player == "WHITE":
            src = np.argwhere((before.board==1) & (after.board==0))
            dst = np.argwhere((before.board==0) & (after.board==1))
        else:
            src = np.argwhere(((before.board==2) | (before.board==3)) & (after.board==0))
            dst = np.argwhere((before.board==0) & ((after.board==2) | (after.board==3)))
        src_lett = next((k for k, v in self.columns.items() if v == src[0][1]), None)
        dst_lett = next((k for k, v in self.columns.items() if v == dst[0][1]), None)
        return src_lett + str(src[0][0]) + '-' + dst_lett + str(dst[0][0])
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--player', type=str, required=True, help="WHITE or BLACK")
    parser.add_argument('--timeout', type=int, required=True)
    parser.add_argument('--server_ip', type=str, required=True)
    args = parser.parse_args()
    player = args.player.upper()
    heu = [0.15 , 0.24, 1 , 0.25] if player == "BLACK" else [0.20, 0.15, 1, 1 , 0.9]
    tab = tablut_client(player, "Tree_Planters", args.timeout, args.server_ip, evaluation.heuristic(heu))
    tab.connect()
    tab.say_hi()
    tab.game_loop_agent()
