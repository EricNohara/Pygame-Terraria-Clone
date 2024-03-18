import pygame as pg
from helper.myconstants import *
from helper.events import EventHandler
from helper.texturedata import *
from helper.sprite import Entity

class Player(pg.sprite.Sprite):
    def __init__(self, groups, image: pg.Surface, pos: tuple, parameters: dict):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.velocity = pg.math.Vector2()
        self.mass = DEFAULT_MASS
        self.terminal_velocity = self.mass * TERMINAL_VELOCITY
        self.grounded = True
        self.dashed = False
        # parameters
        self.group_list = parameters['group_list']
        self.enemy_group = self.group_list['enemy_group']
        self.block_group = self.group_list['block_group']
        self.textures = parameters['textures']
        # inventory:
        self.inventory = parameters['inventory']
        self.health = parameters['health']
        self.last_a_click = 0
        self.last_d_click = 0

    def input(self):
        direction, self.last_a_click, self.last_d_click = EventHandler.double_clicked(self.last_a_click, self.last_d_click)

        keys = pg.key.get_pressed()
        if keys[pg.K_a] and not self.dashed:
            self.velocity.x = -PLAYER_SPEED
            self.image = self.textures['player_static_left']
        if keys[pg.K_d] and not self.dashed:
            self.velocity.x = PLAYER_SPEED
            self.image = self.textures['player_static_right']
        if not keys[pg.K_a] and not keys[pg.K_d]:
            if self.velocity.x > 0:
                self.velocity.x -= FRICTION_CONSTANT
            elif self.velocity.x < 0:
                self.velocity.x += FRICTION_CONSTANT
            if abs(self.velocity.x) < PLAYER_SPEED/2:
                self.velocity.x = 0
        elif self.dashed:
            if self.velocity.x > 0:
                self.velocity.x -= FRICTION_CONSTANT
            elif self.velocity.x < 0:
                self.velocity.x += FRICTION_CONSTANT
            if abs(self.velocity.x) < PLAYER_SPEED/2:
                self.velocity.x = 0
            if abs(self.velocity.x) < PLAYER_SPEED:
                self.dashed = False

        if self.grounded and EventHandler.keydown(pg.K_SPACE):
            self.velocity.y = -PLAYER_JUMP_POWER

        if EventHandler.clicked(1):
            for enemy in self.enemy_group:
                if enemy.rect.collidepoint(self.transform_mouse_pos()):
                    self.inventory.slots[self.inventory.active_slot].attack(self, enemy)

        if direction != 'None' and not self.dashed:
            self.dashed = True
            if direction == 'left':
                self.velocity.x = -PLAYER_DASH_SPEED
                self.image = self.textures['player_static_left']
            elif direction == 'right':
                self.velocity.x = PLAYER_DASH_SPEED
                self.image = self.textures['player_static_right']
            
    def move(self):
        # handling gravity
        self.velocity.y += GRAVITY * self.mass
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity
        self.rect.x += self.velocity.x
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

    def check_collisions(self, direction):
        if direction == 'horizontal':
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0:     # right
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0:     # left
                        self.rect.left = block.rect.right
        elif direction == 'vertical':
            collisions = 0
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.y > 0:     # down
                        collisions += 1
                        self.rect.bottom = block.rect.top
                    if self.velocity.y < 0:     # up
                        self.rect.top = block.rect.bottom
            if collisions > 0:
                self.grounded = True
            else:
                self.grounded = False

    def block_handling(self):
        placed = False
        collision = False
        mouse_pos = self.transform_mouse_pos()

        if EventHandler.clicked_any():
            for block in self.block_group:
                if block.rect.collidepoint(mouse_pos):
                    collision = True
                    if EventHandler.clicked(1): # breaking the block
                        self.inventory.add_item(block)
                        block.kill()
                if EventHandler.clicked(3) and not collision:
                    mouse_rect = pg.rect.Rect((mouse_pos[0]//TILESIZE)*TILESIZE, (mouse_pos[1]//TILESIZE)*TILESIZE, TILESIZE, TILESIZE)
                    if not mouse_rect.colliderect(self.rect):
                        placed = True
        if placed and not collision:
            self.inventory.use(self, self.get_block_pos(mouse_pos))

    def transform_mouse_pos(self) -> tuple:
        mouse_pos = pg.mouse.get_pos()
        player_offset = pg.math.Vector2()
        player_offset.x = WIDTH / 2 - self.rect.centerx
        player_offset.y = HEIGHT / 2 - self.rect.centery
        return (mouse_pos[0] - player_offset.x, mouse_pos[1] - player_offset.y)
    
    def get_block_pos(self, mouse_pos: tuple):
        return (int((mouse_pos[0]//TILESIZE)*TILESIZE), int((mouse_pos[1]//TILESIZE)*TILESIZE))

    def update(self):
        self.input()
        self.move()
        self.block_handling()
        if self.health <= 0:
            self.kill()