import socket, json
from engine.game import *

class GameServer:
    """
    Game Server class.

    Attributes
    ----------
    addr : str
        address of the server socket
    port : int
        port of the server socket
    game_objects : list(GameObject)
        list of GameObjects
    clients : arr(tuple(str, int))
        address and port of each client
    running : bool
        if the server is running or not
    """

    def __init__(self, addr, port):
        """
        """
        self.addr = addr
        self.port = port
        self.game_objects = []
        self.clients = []
        self.running = False

    def add_client(self, addr):
        """
        Add a client to the server.

        Parameters
        ----------
        addr : tuple(str, int)
            address and port of the new client

        Returns
        -------
        int
            the amount of clients connected.
        """
        self.clients.append(addr)
        return len(self.clients)

    def game_loop(self):
        """
        The main server loop.
        """
        self.running = True
        while self.running:
            data, addr = self.sock.recvfrom(1024)
            game_objects_json = []
            for o in self.game_objects:
                game_objects_json.append(o.get_dict())

            if data == None: break
            data = str(data)[2:-1]
            if data == CLIENT_CONNECT_MESSAGE:
                client_id = self.add_client(addr)
                response = bytes(json.dumps({'id': client_id, 'game_objects': game_objects_json}), encoding='utf-8')
                self.sock.sendto(bytes(json.dumps({'id': client_id, 'game_objects': game_objects_json}), encoding='utf-8'), addr)
                continue

            try:
                data_dict = json.loads(data)
                client_id = data_dict['id']
                for o in self.game_objects:
                    o.server_update(data_dict, self.game_objects)
            except ValueError as e:
                printd('Malformed packet received.')
            self.sock.sendto(bytes(json.dumps({'id': client_id, 'game_objects': game_objects_json}), encoding='utf-8'), addr)
        self.halt()

    def halt(self):
        """
        Stop the server.
        """
        self.running = False
        self.sock.close()

    def start(self):
        """
        Start the server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as self.sock:
            self.sock.bind((self.addr, self.port))
            self.game_loop()
