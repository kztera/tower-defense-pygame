from typing import Any
import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 5, -self.rect.height // 5)
        )


class Stone(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_STONE]):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 3, -self.rect.height // 3)
        )


class Tree(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_TREE]):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 3, -self.rect.height // 3)
        )
        self.taking_damage = False
        self.diection_of_damage = pygame.math.Vector2()
        self.timer = 0
        self.start_pos = pygame.math.Vector2()
        self.end_pos = pygame.math.Vector2()

        self.moving_target = False
        self.waitting = False

        
    def damage(self, location_of_perpetrator):
        if self.taking_damage:
            return

        self.diection_of_damage.x = self.rect.centerx - location_of_perpetrator.x
        self.diection_of_damage.y = self.rect.centery - location_of_perpetrator.y
        self.diection_of_damage = self.diection_of_damage.normalize() 

        self.start_pos = pygame.math.Vector2(self.rect.center)
        self.end_pos = pygame.math.Vector2(self.rect.center + self.diection_of_damage * 40)

        self.timer = 0
        self.moving_target = True
        self.waitting = False
        self.taking_damage = True

    def update(self, dt):
        if self.taking_damage:
            if self.moving_target:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(self.start_pos, self.end_pos, self.timer / 0.1) 
                else:
                    self.timer = 0
                    self.moving_target = False
                    self.waitting = True
            elif self.waitting:
                self.timer += dt
                if self.timer > 0.08:
                    self.waitting = False
                    self.timer = 0
            else:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(self.end_pos, self.start_pos, self.timer / 0.1) 
                else:
                    self.taking_damage = False



