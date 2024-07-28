import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class Stone(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_STONE]):
        super().__init__(pos, surf, groups, z)


class Tree(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_TREE]):
        super().__init__(pos, surf, groups, z)


class Tool(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_TOOL]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
