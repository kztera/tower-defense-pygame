import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class Stone(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


class Tree(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


class Tool(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_TOOL]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
