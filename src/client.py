import sys, pygame, socket, json
from game import *

game_objects = []
ball = Ball()
player_objects = []
player_img = pygame.image.load('img/player.png')
player_img_rect = player_img.get_rect()
ball_img = pygame.image.load('img/ball.png')
ball_img_rect = ball_img.get_rect()
frame = 0

# pygame initialization
pygame.init()
screen = pygame.display.set_mode(WINSIZE)
clock = pygame.time.Clock()

"""
Get currently pressed keys related to the game

Returns
-------
list
    a list of pressed keys in their ASCII uppercase values
"""
def get_pressed_keys():
    keys = pygame.key.get_pressed()
    pressed = []
    if keys[pygame.K_w]:
        pressed.append('W')
    if keys[pygame.K_a]:
        pressed.append('A')
    if keys[pygame.K_s]:
        pressed.append('S')
    if keys[pygame.K_d]:
        pressed.append('D')
    return pressed

"""
Syncs the client data with the server. The client's Player object and keypresses
are sent to the server as JSON, which returns the Player object of all connected
clients, as well as the Ball object.
"""
def update():
    # send client data to server
    send_data = { 'player': player.get_json(), 'keys': get_pressed_keys() }
    s.sendto(bytes(json.dumps(send_data), 'utf-8'), (HOST, PORT))

    recv_data, addr = s.recvfrom(1024)
    if not recv_data: return
    recv_data = json.loads(str(recv_data)[2:-1])

    for d in recv_data['player_objects']:
        player_ids = []
        for p in player_objects:
            player_ids.append(p.id)
            if p.id == d['id']:
                p.client_update(d)
                continue
        if d['id'] not in player_ids:
            player_objects.append(Player(d))
    print(f"{frame} {player_objects}\n")
    print("\n")
    ball.client_update(recv_data['ball'])

"""
Draws the player_objects and Ball to the Pygame window.
"""
def draw():
    screen.fill((0,0,0))
    for p in player_objects:
        player_img_rect.x = p.x
        player_img_rect.y = p.y
        screen.blit(player_img, player_img_rect)

    ball_img_rect.x = ball.x
    ball_img_rect.y = ball.y
    screen.blit(ball_img, ball_img_rect)
    pygame.display.flip()

"""
Initializes connection with the server and obtains a Player object with the
client ID.

Returns
-------
A new Player object using the data received from the surver
"""
def initialize_client(s):
    s.sendto(bytes(CLIENT_CONNECT_MESSAGE, 'utf-8'), (HOST, PORT))
    data, addr = s.recvfrom(1024)
    if not data:
        print("failed to connect to server")
        sys.exit()
    data = json.loads(str(data)[2:-1])
    return Player(data)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    player = initialize_client(s)
    if player == None:
        print('failed to initialize client')
        sys.exit()
    else:
        print('client initialized')
    player_objects.append(player)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        update()
        frame += 1
        draw()
        clock.tick(60)