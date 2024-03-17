import pygame as pg, math
from helper.myconstants import *

class Entity(pg.sprite.Sprite):
    def __init__(self, groups, image = pg.Surface((TILESIZE, TILESIZE)), pos = (0,0), name: str = "default"):
        super().__init__(groups)
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.in_groups = groups

    def update(self):
        pass

class Mob(Entity):
    def __init__(self, groups, image=pg.Surface((TILESIZE, TILESIZE)), pos=(0, 0), parameters={}):
        super().__init__(groups, image, pos)

        if parameters:
            self.block_group = parameters['block_group']
            self.player = parameters['player']
            self.textures = parameters['textures']
            self.damage = parameters['damage']

        self.velocity = pg.math.Vector2()
        self.mass = 5
        self.speed = 2
        self.jump_power = 10
        self.terminal_velocity = TERMINAL_VELOCITY * self.mass

        # States:
        self.attacking = True
        self.attacked = False
        self.grounded = False
        self.attack_cooldown = 60
        self.counter = self.attack_cooldown

    def move(self):         
        # handling gravity
        self.velocity.y += GRAVITY * self.mass
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        # Check if within player range
        if abs(math.sqrt((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2)) < TILESIZE * ENEMY_AGGRO_RANGE:
            # handle moving to player
            if self.rect.x > self.player.rect.x:
                self.velocity.x = -self.speed
                self.image = self.textures['slime_static_left']
            elif self.rect.x < self.player.rect.x:
                self.velocity.x = self.speed
                self.image = self.textures['slime_static_right']
            self.attacking = True
        else:
            self.attacking = False
            self.velocity.x = 0

        self.rect.x += self.velocity.x
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

        if self.grounded and self.attacking and abs(self.velocity.x) < 0.1:
            self.velocity.y = -self.jump_power

    def check_collisions(self, direction):
        if direction == 'horizontal':
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0:     # right
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0:     # left
                        self.rect.left = block.rect.right
                    self.velocity.x = 0
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

    def check_player_collision(self):
        if not self.attacked and self.attacking and self.rect.colliderect(self.player.rect):
            self.player.health -= self.damage
            self.attacked = True
            self.counter = self.attack_cooldown
            if self.player.rect.centerx > self.rect.centerx:
                self.player.velocity.x = KNOCKBACK
            elif self.player.rect.centerx < self.rect.centerx:
                self.player.velocity.x = -KNOCKBACK

    def update(self):
        self.move()
        self.check_player_collision()

        if self.attacked:
            self.counter -= 1
            if self.counter < 0: 
                self.counter = self.attack_cooldown
                self.attacked = False