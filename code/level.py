import pygame
from settings import *
from asset_path import *
from pytmx.util_pygame import load_pygame

from player import Player
from overlay import Overlay
from sprites import Generic, Stone, Tree, Tower

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprites group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.stone_sprites = pygame.sprite.Group()
        self.entity_sprites = pygame.sprite.Group()

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
                groups=[self.all_sprites, self.collision_sprites, self.stone_sprites],
                player_add=self.player_add,
            )

        # Trees
        for obj in tmx_data.get_layer_by_name(LAYER_TREE):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                player_add=self.player_add,
            )

        # create player
        for obj in tmx_data.get_layer_by_name(LAYER_PLAYER):
            if obj.name == "Start":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    stone_sprites=self.stone_sprites,
                    entity_sprites = self.entity_sprites
                )

        # create ground
        Generic(
            pos=(0, 0),
            surf=pygame.image.load(ASSET_PATH_GROUND),
            groups=self.all_sprites,
            z=LAYERS[LAYER_GROUND],
        )

    def player_add(self, item):
        self.player.items_inventory[item] += 1

    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()
        # print(self.player.items_inventory)

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

                    # anaytics
                    if sprite == player:
                        # pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                        hitbox_rect = player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        # pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                        tartget_pos = (
                            offset_rect.center
                            + PLAYER_TOOL_OFFSET[player.direction_state]
                        )
                        # pygame.draw.circle(self.display_surface, 'blue', tartget_pos, 5)
