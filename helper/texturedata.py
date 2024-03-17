from helper.myconstants import *

atlas_texture_data = {
    'grass': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (0,0)},
    'stone': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (1,0)},
    'dirt': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (2,0)},
    'grassdirt': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (3,0)},
    'cobblestone': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (0,1)},
    'crackedstone': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (1,1)},
    'copperore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (0,2)},
    'silverore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (1,2)},
    'coalore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (2,2)},
    'platinumore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (2,3)},
    'rubyore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (3,3)},
    'saphireore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (0,10)},
    'emeraldore': {'type': 'block', 'size': (TILESIZE, TILESIZE), 'position': (11,10)},
}

solo_texture_data = {
    'player_static_right': {'type': 'player', 'file_path': 'assets/Player-right.png', 'size': (TILESIZE*1.5, TILESIZE*2)},
    'player_static_left': {'type': 'player', 'file_path': 'assets/Player-left.png', 'size': (TILESIZE*1.5, TILESIZE*2)},
    'slime_static_right': {'type': 'enemy', 'file_path': 'assets/slime-right.png', 'size': (TILESIZE*1.5, TILESIZE)},
    'slime_static_left': {'type': 'enemy', 'file_path': 'assets/slime-left.png', 'size': (TILESIZE*1.5, TILESIZE)},
    'shortsword': {'type': 'weapon', 'file_path': 'assets/shortsword.png', 'size': (TILESIZE, TILESIZE)}
}