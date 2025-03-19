import pygame
import math

# Game settings
WIDTH = 800
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
FOV = math.pi / 2
HALF_FOV = FOV / 2
NUM_RAYS = 160
MAX_DEPTH = 1000
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 4 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# Player settings
player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 2

# Colors
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
DARKGRAY = (110, 110, 110)
PURPLE = (120, 0, 120)

# Player
class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.x += cos_a * player_speed
            self.y += sin_a * player_speed
        if keys[pygame.K_s]:
            self.x += -cos_a * player_speed
            self.y += -sin_a * player_speed
        if keys[pygame.K_a]:
            self.x += sin_a * player_speed
            self.y += -cos_a * player_speed
        if keys[pygame.K_d]:
            self.x += -sin_a * player_speed
            self.y += cos_a * player_speed

# Map representation
text_map = [
    'WWWWWWWWWWWWWWW',
    'W...........WWW',
    'W.............W',
    'W....WWWWW....W',
    'W.....WWW.....W',
    'WWW...........W',
    'W...........WWW',
    'W.....WWW.....W',
    'W....WWWWW....W',
    'W.............W',
    'WWW...........W',
    'WWWWWWWWWWWWWWW',
]

world_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * TILE, j * TILE))

def ray_casting(sc, player_pos, player_angle):
    cur_angle = player_angle - HALF_FOV
    xo, yo = player_pos
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        
        # Initialize depth to detect wall collision
        depth = 0
        for depth in range(MAX_DEPTH):
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            
            if (x // TILE * TILE, y // TILE * TILE) in world_map:
                proj_height = PROJ_COEFF / max(depth, 0.1)
                brightness = max(0, 255 - int(depth * 255 / MAX_DEPTH))  # Simple brightness based on depth
                pygame.draw.rect(sc, (brightness, brightness, brightness), (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
                break
        cur_angle += DELTA_ANGLE  

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    mouse_x, mouse_y = pygame.mouse.get_rel()
    player.angle += mouse_x * 0.001
    player.angle = player.angle % (2 * math.pi)

    player.movement()
    sc.fill(BLACK)
    
    ray_casting(sc, player.pos, player.angle)
    
    pygame.display.flip()
    clock.tick(FPS)
