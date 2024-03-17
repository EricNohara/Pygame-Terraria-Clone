from helper.myconstants import *

atlas_texture_data = {
    'grass': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (0,0)},
    'stone': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (1,0)},
    'dirt': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (2,0)},
    'grassdirt': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (3,0)},
}

solo_texture_data = {
    'player_static_right': {'type': 'player', 'file_path': 'assets/Player-right.png', 'size': (TILESIZE*1.5, TILESIZE*2)},
    'player_static_left': {'type': 'player', 'file_path': 'assets/Player-left.png', 'size': (TILESIZE*1.5, TILESIZE*2)},
    'slime_static_right': {'type': 'enemy', 'file_path': 'assets/slime-right.png', 'size': (TILESIZE*1.5, TILESIZE)},
    'slime_static_left': {'type': 'enemy', 'file_path': 'assets/slime-left.png', 'size': (TILESIZE*1.5, TILESIZE)},
    'shortsword': {'type': 'weapon', 'file_path': 'assets/shortsword.png', 'size': (TILESIZE, TILESIZE)}
}