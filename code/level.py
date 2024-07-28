import pygame
from settings import *
from asset_path import *
from pytmx.util_pygame import load_pygame

from player import Player
from overlay import Overlay
from sprites import Generic, Stone, Tree


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprites group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # setup
        self.setup()

        # create overlay
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame(ASSET_PATH_MAP)

        # Stones
        for obj in tmx_data.get_layer_by_name(LAYER_STONE):
            Stone(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites],
            )

        # Trees
        for obj in tmx_data.get_layer_by_name(LAYER_TREE):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites],
            )

        # create player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player(
                    (obj.x, obj.y), self.all_sprites, self.collision_sprites
                )

        # create ground
        Generic(
            pos=(0, 0),
            surf=pygame.image.load(ASSET_PATH_GROUND),
            groups=self.all_sprites,
            z=LAYERS[LAYER_GROUND],
        )

    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH_DEFAULT / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT_DEFAULT / 2

        for layer in LAYERS.values():
            for sprite in sorted(
                self.sprites(), key=lambda sprite: sprite.rect.centery
            ):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
