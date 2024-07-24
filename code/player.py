import pygame
from settings import *
from support import *

from asset_path import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()

        self.status = ANIM_PLAYER_DOWN_IDLE
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animations = { ANIM_PLAYER_UP:[], ANIM_PLAYER_DOWN:[], ANIM_PLAYER_LEFT:[], ANIM_PLAYER_RIGHT:[],
                            ANIM_PLAYER_UP_IDLE:[], ANIM_PLAYER_DOWN_IDLE:[], ANIM_PLAYER_LEFT_IDLE:[], ANIM_PLAYER_RIGHT_IDLE:[],
                            ANIM_PLAYER_UP_AXE:[], ANIM_PLAYER_DOWN_AXE:[], ANIM_PLAYER_LEFT_AXE:[], ANIM_PLAYER_RIGHT_AXE:[],
                            ANIM_PLAYER_UP_ATTACK:[], }

        for animation in self.animations.keys():
            full_path = ASSET_PATH_PLAYER + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]


    def input(self):
        # keybroad button input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = ANIM_PLAYER_UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = ANIM_PLAYER_DOWN
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = ANIM_PLAYER_RIGHT
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = ANIM_PLAYER_LEFT
        else:
            self.direction.x = 0

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)