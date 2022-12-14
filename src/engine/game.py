import json, getopt, sys, pygame, datetime

# DEFAULTS
HOST = 'localhost'
PORT = 7737
MAX_PACKET_SIZE = 4096
WINSIZE = (640, 480)
debug = False
server_mode = False

CLIENT_CONNECT_MESSAGE = "hello"
CLIENT_DISCONNECT_MESSAGE = "goodbye"
frame = 0
game_objects = []
screen = None
clock = None

class GameObject:
    """
    Base GameObject

    Attributes
    ----------
    id : int
        the unique identifier for the object
    type : str
        name of the type (for deserialization)
    """
    def __init__(self, id, type):
        """
        Initializes the GameObject.

        Parameters
        ----------
        id : int
            unique identifier for the object
        type : str
            string format of the type
        """
        self.id = id
        self.type = "GameObject"

    def get_dict(self):
        """
        Returns a dict of relevant data for transfer between the client and server.

        Returns
        -------
        dict
            relevant data to transfer
        """
        return {'id': self.id, 'type': self.type}

    def client_update(self, data):
        """
        Update the GameObject on the client side (implemented by subclasses).

        Parameters
        ----------
        data : dict
            retrieved data from the server
        """
        pass

    def server_update(self, data, game_objects):
        """
        Update the GameObject on the server side (implemented by subclasses).
        """
        pass

class DrawableObject(GameObject):
    def __init__(self, id, type, sprite, x, y):
        """
        Initialize the DrawableObject

        id : int
            the unique identifier for the object
        type : str
            name of the type (for deserialization)
        sprite : pygame.Surface
            The object's sprite
        x : int
            x-coordinate of the object
        y : int
            y-coordinate of the object
        """
        super(id, "DrawableObject", sprite)
        self.x = x
        self.y = y

    def draw(self, screen, w=None, h=None):
        """
        Draw the object to screen.

        Parameters
        ----------
        screen : pygame.Surface
            the pygame window's surface
        """
        if w == None and h == None:
            to_draw = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        else:
            to_draw = pygame.Rect(self.x, self.y, w, h)
        screen.blit(self.sprite, to_draw)

    def move(self, x, y):
        """
        Change the coordinates of the DrawableObject.

        Parameters
        ----------
        x : int
            new x value
        y : int
            new y value
        """
        self.x = x
        self.y = y

    def client_update(self, data):
        """
        Update the positional values based on data.

        Parameters
        ----------
        data : dict
            new values retrieved from the server
        game_objects : list(GameObject)
            all GameObjects
        """
        super(data)
        self.x = data['x']
        self.y = data['y']

def printd(s):
    """
    Prints to stderr.

    Parameters
    ----------
    s : str
        the string to print
    """
    time = datetime.datetime.now()
    print(time.strftime('%Y-%m-%d %H-%M-%S') + '\t' + s, file=sys.stderr)

def parse_args():
    """
    Parses command line arguments.

    Returns
    -------
    dict
        a dict containing all the arguments passed or their default values.
    """
    opts, args = getopt.getopt(sys.argv[1:], 'si:p:')
    ret = {'server': False, 'debug': False, 'host': HOST, 'port': PORT}
    for o, a in opts:
        if o == '-i':
            ret['host'] = a
        elif o == '-p':
            ret['port'] = a
        elif o == '-s':
            ret['server'] = True
        else:
            print("usage: " + sys.argv[0] + " [-s] [-i IP] [-p PORT]", file=sys.stderr)
            sys.exit(1)
    return ret
