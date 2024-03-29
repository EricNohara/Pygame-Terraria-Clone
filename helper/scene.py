import pygame as pg, random
from helper.myconstants import *
from helper.sprite import Entity, Mob
from helper.player import Player
from helper.texturedata import *
from helper.camera import Camera
from opensimplex import OpenSimplex
from inventory.inventory import Inventory
from helper.items import *
from helper.button import Button
from helper.events import EventHandler

class Scene:
    def __init__(self, app) -> None:
        """Do construct Scene with app as argument."""
        self.app = app
        self.textures = self.gen_solo_textures()
        self.textures.update(self.gen_atlas_textures('assets/texture-atlas.png'))

        self.sprites = Camera()
        self.enemy_group = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.group_list: dict[str, pg.sprite.Group] = {
            'sprites': self.sprites,
            'block_group': self.blocks,
            'enemy_group': self.enemy_group,
            'wall_group': self.walls
        }

        # Inventory:
        self.inventory = Inventory(self.app, self.textures)

        self.player = Player([self.sprites], self.textures['player_static_right'], (WIDTH / 2, HEIGHT / 2), {'group_list': self.group_list, 'textures': self.textures, 'inventory': self.inventory, 'health': 5})
        Mob([self.sprites, self.enemy_group], self.textures['slime_static_right'], (800, -500), parameters={'block_group': self.blocks, 'player': self.player, 'textures': self.textures, 'damage': 1, 'health': 3})

        self.chunks: dict[tuple[int, int], Chunk] = {}
        self.active_chunks: dict[tuple[int, int], Chunk] = {}

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
        pass      

    def update(self):
        player_chunk_pos = Chunk.get_chunk_pos(self.player.rect.center)
        positions = [player_chunk_pos, 
                     (player_chunk_pos[0] - 1, player_chunk_pos[1]),
                     (player_chunk_pos[0] + 1, player_chunk_pos[1]),

                     (player_chunk_pos[0] - 1, player_chunk_pos[1] - 1),
                     (player_chunk_pos[0] + 1, player_chunk_pos[1] - 1),
                     (player_chunk_pos[0], player_chunk_pos[1] - 1),
                     
                     (player_chunk_pos[0] - 1, player_chunk_pos[1] + 1),
                     (player_chunk_pos[0] + 1, player_chunk_pos[1] + 1),
                     (player_chunk_pos[0], player_chunk_pos[1] + 1),
                     ]
        for position in positions:
            if position not in self.active_chunks:
                if position in self.chunks:
                    self.chunks[position].load_chunk()
                    self.active_chunks[position] = self.chunks[position]
                else:
                    self.chunks[position] = Chunk(position, self.group_list, self.textures, self.sprites)
                    self.active_chunks[position] = self.chunks[position]
        target = None
        for pos, chunk in self.active_chunks.items():
            if pos not in positions:
                target = pos
        if target != None:
            self.active_chunks[target].unload_chunk()
            self.active_chunks.pop(target)

        self.sprites.update()
        self.inventory.update()

        if self.player not in self.sprites:
            self.reset_screen()

    def reset_screen(self):
        mouse_pos = pg.mouse.get_pos()
        game_over_screen = pg.Surface((WIDTH, HEIGHT))
        game_over_screen.fill('black')
        game_over_screen.set_alpha(180)
        self.app.screen.blit(game_over_screen, (0,0))

        respawn_button = pg.Surface(RESPAWN_BTN)
        respawn_button.fill('grey')
        respawn_btn = Button(image=respawn_button, pos=(WIDTH/2, HEIGHT/2), text_input="Respawn", font=HEADER_FONT, base_color="black", hovering_color="white")       
        respawn_btn.changeColor(mouse_pos)
        respawn_btn.update(self.app.screen)

        if EventHandler.clicked():
            if respawn_btn.checkForInput(mouse_pos):
                self.reset()

    def reset(self):
        self.player = Player([self.sprites], self.textures['player_static_right'], (WIDTH / 2, HEIGHT / 2), {'group_list': self.group_list, 'textures': self.textures, 'inventory': self.inventory, 'health': 5})
        for enemy in self.enemy_group:
            enemy.kill()

    def draw(self):
        self.app.screen.fill("lightblue")
        self.sprites.draw(self.player, self.app.screen)
        self.inventory.draw()


class Chunk:
    def __init__(self, position: tuple[int, int], group_list: dict[str, pg.sprite.Group], textures: dict[str, pg.Surface], sprites):
        self.position = position
        self.group_list = group_list
        self.textures = textures
        self.sprites = sprites
        self.blocks = []
        self.gen_chunk()

    def gen_chunk(self):
        noise_generator = OpenSimplex(seed=3284329854)
        height_map = []
        for i in range(CHUNKSIZE * self.position[0], CHUNKSIZE * self.position[0] + CHUNKSIZE):
            noise_value = noise_generator.noise2(i * TERRAIN_VOLATILITY, 0)
            height = int((noise_value + 1) * 4 + 5)
            height_map.append(height)
        
        for x in range(len(height_map)):
            if self.position[1] > 0:
                height_val = CHUNKSIZE
            elif self.position[1] < 0:
                height_val = 0
            else:
                height_val = height_map[x]

            # testing
            if x % TREE_SCARCITY == 0:
                for i in range(5):
                    block_type = 'wood'
                    use_type = items[block_type].use_type
                    groups = [self.group_list[group] for group in items[block_type].groups]
                    wood_block = use_type(groups, self.textures[block_type], (x * TILESIZE + (CHUNKPIXELSIZE * self.position[0]), (CHUNKSIZE-height_map[x])*TILESIZE - (TILESIZE*i)), block_type)
                    self.blocks.append(wood_block)

                for i in range(5):
                    for j in range(2):
                        block_type = 'leaf'
                        use_type = items[block_type].use_type
                        groups = [self.group_list[group] for group in items[block_type].groups]
                        self.blocks.append(use_type(groups, 
                                                self.textures[block_type], 
                                                (x * TILESIZE + (CHUNKPIXELSIZE * self.position[0]) - i*TILESIZE + 2*TILESIZE,
                                                (CHUNKSIZE-height_map[x]-5)*TILESIZE - (TILESIZE*j)), 
                                                block_type))
                        
                for i in range(3):
                    block_type = 'leaf'
                    use_type = items[block_type].use_type
                    groups = [self.group_list[group] for group in items[block_type].groups]
                    self.blocks.append(use_type(groups, 
                                                self.textures[block_type], 
                                                (x * TILESIZE + (CHUNKPIXELSIZE * self.position[0]) - i*TILESIZE + TILESIZE,
                                                (CHUNKSIZE-height_map[x]-5)*TILESIZE - (TILESIZE*2)), 
                                                block_type))

            for y in range(height_val):
                self.generate_random_ore()
                block_type = 'dirt'
                if y == height_map[x] - 1:
                    block_type = 'grassdirt'
                if y < height_map[x] - 5:
                    block_type = 'stone'
                if self.position[1] > 0:
                    block_type = self.generate_random_ore()

                use_type = items[block_type].use_type
                groups = [self.group_list[group] for group in items[block_type].groups]
                self.blocks.append(use_type(groups, 
                                            self.textures[block_type], 
                                            (x * TILESIZE + (CHUNKPIXELSIZE * self.position[0]),
                                             (CHUNKSIZE - y) * TILESIZE + (CHUNKPIXELSIZE * self.position[1])), 
                                             block_type))
                
    def generate_random_ore(self):
        num = random.randint(1, 1000)
        if num >= 765 and num < 865:
            return 'cobblestone'
        elif num >= 865 and num < 940:
            return 'crackedstone'
        elif num >= 940 and num < 960:
            return 'copperore'
        elif num >= 960 and num < 980:
            return 'coalore'
        elif num >= 980 and num < 987.5:
            return 'silverore'
        elif num >= 987.5 and num < 992.5:
            return 'platinumore'
        elif num >= 992.5 and num < 995:
            return 'saphireore'
        elif num >= 995 and num < 997.5:
            return 'rubyore'
        elif num >= 997.5 and num < 1000:
            return 'emeraldore'
        else:
            return 'stone'
            
                    
    def load_chunk(self):
        for block in self.blocks:
            groups = [self.group_list[group] for group in items[block.name].groups]
            for group in groups:
                group.add(block)

    def unload_chunk(self):
        for block in self.blocks:
            block.kill()

    @staticmethod
    def get_chunk_pos(position):
        return (position[0] // CHUNKPIXELSIZE, position[1] // CHUNKPIXELSIZE)
