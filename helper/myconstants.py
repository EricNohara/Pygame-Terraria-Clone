import pygame as pg

pg.init()

# SCREEN SETTINGS
SIZE = (WIDTH, HEIGHT) = (1280, 720)
FPS = 60
TILESIZE = 32
SLOTSIZE = TILESIZE * 2
RESPAWN_BTN = (350, 125)
FONT = pg.font.Font('assets/fonts/pixel.ttf', 20)
HEADER_FONT = pg.font.Font('assets/fonts/pixel.ttf', 50)

# Physics Constants
GRAVITY = 0.1
TERMINAL_VELOCITY = 2
KNOCKBACK = 7
FRICTION_CONSTANT = 0.2

# Player Stat Constants
DEFAULT_MASS = 5
PLAYER_SPEED = 5
PLAYER_DASH_SPEED = 15
PLAYER_JUMP_POWER = 10
INVENTORY_SIZE = 10

# Enemy Stats
ENEMY_AGGRO_RANGE = 17.5

# World Gen Constants
TERRAIN_VOLATILITY = 0.08
CHUNKSIZE = 30
CHUNKPIXELSIZE = CHUNKSIZE * TILESIZE
DASH_DOUBLE_CLICK = 250
TREE_SCARCITY = CHUNKSIZE/2