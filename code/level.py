import pygame
from settings import *
from asset_path import *
from pytmx.util_pygame import load_pygame

from player import Player
from overlay import Overlay
from sprites import Generic, Stone, Tree, Zombie
from zombie_config import *
import math
import random
from game_stats import *
from game_data import *


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
        self.zombie_sprites = pygame.sprite.Group()
        self.brain_sprites = pygame.sprite.Group()

        #
        self.game_data = GameData()

        #
        self.spawning_zombie = False
        self.timer = 0.0
        self.spawnTime = 2

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
                    entity_sprites=self.entity_sprites,
                    zombie_sprites=self.zombie_sprites,
                    brain_sprites=self.brain_sprites,
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

    def request_upgrade_wave(self):
        if self.player.is_started:
            self.upgrade_wave()

    def upgrade_wave(self):
        self.player.upgrade_wave()
        self.spawn_zombie()

    def spawn_zombie(self):
        sprite_list = list(self.brain_sprites)
        if len(sprite_list) < 1:
            return

        brain_pos = pygame.math.Vector2(sprite_list[0].rect.center)
        range_spawn_min = 400
        range_spawn_max = 1000
        distance_entity_to_brain = 0
        for entity in self.entity_sprites:
            target_pos = pygame.math.Vector2(entity.rect.center)
            distance = brain_pos.distance_to(target_pos)
            if distance > distance_entity_to_brain:
                distance_entity_to_brain = distance
        #
        for zombie in ZOMBIE_CONFIG:
            waves = zombie["WAVES"]
            can_spawn = False
            wave_start, wave_end = waves.split("-")
            wave_start = int(wave_start)
            if wave_end == "":
                if wave_start <= self.player.current_wave:
                    can_spawn = True
            else:
                wave_end = int(wave_end)
                if wave_start <= self.player.current_wave <= wave_end:
                    can_spawn = True
            #
            path_zombie = ASSET_PATH_ZOMBIES
            model_name = ((zombie["MODEL"]).split("Tier")[0]).upper()
            for zombie_name in ZOMBIE_ARRAYS:
                if (zombie_name.replace("-", "")).upper() == model_name:
                    path_zombie += zombie_name + "/" + zombie_name + "-t" + str(sprite_list[0].level) + "-weapon.png"
                    
            # heath, damage, speed, firerate
            health_zombie = zombie["HEALTH"]
            speed_zombie = float(zombie["SPEED"]) * 10
            firerate_zombie = float(zombie["FIRERATE"]) / 1000
            deals_zombie = float(zombie["DEALS"]) / 1000

            #
            if can_spawn:
                amount = zombie["AMOUNT"]
                for x in range(0, amount):
                    distance_entity_to_brain = distance
                    distance_entity_to_brain += random.uniform(range_spawn_min, range_spawn_max)
                    angle = random.uniform(0, 360)
                    radian = math.radians(angle)
                    new_x = brain_pos.x + distance_entity_to_brain * math.cos(radian)
                    new_y = brain_pos.y + distance_entity_to_brain * math.sin(radian)
                    zombie_spawnpos = pygame.Vector2(new_x, new_y)
                    # spawn
                    Zombie(
                        pos=zombie_spawnpos,
                        surf=pygame.image.load(path_zombie),
                        groups=[
                            self.all_sprites,
                            self.collision_sprites,
                            self.zombie_sprites,
                        ],
                        entity_sprites=self.entity_sprites,
                        brain_sprites=self.brain_sprites,
                        max_heath=health_zombie,
                        speed=speed_zombie,
                        firerate=firerate_zombie,
                        damage=deals_zombie
                    )
                    print("Spawn Zombie")

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
                            offset_rect.center + USE_TOOL_OFFSET[player.direction_state]
                        )
                        # pygame.draw.circle(self.display_surface, 'blue', tartget_pos, 5)
