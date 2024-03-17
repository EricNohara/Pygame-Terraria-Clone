import pygame as pg
from helper.myconstants import *
from helper.sprite import Entity, Mob
from helper.player import Player
from helper.texturedata import *
from helper.camera import Camera
from opensimplex import OpenSimplex
from inventory.inventory import Inventory

class Scene:
    def __init__(self, app) -> None:
        """Do construct Scene with app as argument."""
        self.app = app
        self.solo_textures = self.gen_solo_textures()
        self.atlas_textures = self.gen_atlas_textures('assets/texture-atlas.png')

        self.sprites = Camera()
        self.blocks = pg.sprite.Group()
        self.group_list: dict[str, pg.sprite.Group] = {
            'sprites': self.sprites,
            'block_group': self.blocks
        }

        # Inventory:
        self.inventory = Inventory(self.app, self.atlas_textures)

        self.player = Player([self.sprites], self.solo_textures['player_static_right'], (600,300), {'group_list': self.group_list, 'textures': self.atlas_textures, 'solo_textures': self.solo_textures, 'inventory': self.inventory})
        Mob([self.sprites], self.solo_textures['slime_static_right'], (800, -500), parameters={'block_group': self.blocks, 'player': self.player, 'solo_textures': self.solo_textures})

        self.gen_world()

    def gen_solo_textures(self) -> dict:
        """
        Do generate dictionary of all solo_textures specified in texturedata.py file.
        Do scale all solo_textures by specified size, and convert alpha.
        """
        textures = {}
        for name, data in solo_texture_data.items():
            textures[name] = pg.transform.scale(pg.image.load(data['file_path']).convert_alpha(), (data['size']))
        return textures

    def gen_atlas_textures(self, filepath) -> dict:
        """
        Do generate dictionary from texturedata.py containing all atlas textures specified.
        Do store textures as a scaled and converted subsurface.
        """
        textures = {}
        atlas_img = pg.transform.scale(pg.image.load(filepath).convert_alpha(), (TILESIZE*16,TILESIZE*16))
        for name, data in atlas_texture_data.items():
            textures[name] = pg.Surface.subsurface(atlas_img, pg.Rect((data['position'][0]*TILESIZE, data['position'][1]*TILESIZE), data['size']))
        return textures

    def gen_world(self):
        noise_generator = OpenSimplex(seed=3284329854)
        height_map = []
        for i in range(WIDTH//TILESIZE):
            noise_value = noise_generator.noise2(i * TERRAIN_VOLATILITY, 0)
            height = int((noise_value + 1) * 4 + 5)
            height_map.append(height)
        
        for x in range(len(height_map)):
            for y in range(height_map[x]):
                y_offset = 5 - y + 6
                block_type = 'dirt'
                if y == height_map[x] - 1:
                    block_type = 'grassdirt'
                if y < height_map[x] - 5:
                    block_type = 'stone'
                Entity([self.sprites, self.blocks], self.atlas_textures[block_type], (x*TILESIZE, y_offset*TILESIZE), name = block_type)

    def update(self):
        self.sprites.update()
        self.inventory.update()

    def draw(self):
        self.app.screen.fill("lightblue")
        self.inventory.draw()
        self.sprites.draw(self.player, self.app.screen)