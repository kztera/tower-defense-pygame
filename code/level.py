import pygame
from settings import *
from asset_path import *
from pytmx.util_pygame import load_pygame

from player import Player
from overlay import Overlay
from sprites import Generic, Stone, Tree, Zombie, Button, Text
from zombie_config import *
import math
import random
from game_stats import *
from game_data import *

input_rect = pygame.Rect(200, 200, 240, 40)
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("gray15")
color = color_passive


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # started game
        self.game_started = False

        # game name text
        game_text_pos = pygame.Vector2(
            SCREEN_WIDTH_DEFAULT / 2, SCREEN_HEIGHT_DEFAULT / 2
        )
        game_text_pos.y -= 150
        game_font = pygame.font.Font((ASSET_PATH_FONT + FONT_TEXT + ".ttf"), 72)
        self.game_text = game_font.render("TOWER DEFENSE", True, (255, 255, 255))
        self.game_text_rect = self.game_text.get_rect(center=game_text_pos)

        # start button
        pos_button = pygame.Vector2(SCREEN_WIDTH_DEFAULT / 2, SCREEN_HEIGHT_DEFAULT / 2)
        pos_button.y += 50
        self.start_button = pygame.image.load(ASSET_PATH_START_BUTTON)
        self.start_button_rect = self.start_button.get_rect(center=pos_button)

        # user text
        self.activate = False
        self.user_name = ""

        self.pos_text = pygame.Vector2(
            SCREEN_WIDTH_DEFAULT / 2, SCREEN_HEIGHT_DEFAULT / 2
        )
        self.pos_text.y -= 50
        self.base_font = pygame.font.Font((ASSET_PATH_FONT + FONT_TEXT + ".ttf"), 24)
        self.user_text = self.base_font.render(self.user_name, True, (255, 255, 255))
        self.user_text_rect = self.user_text.get_rect(center=self.pos_text)

        # sprites group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.stone_sprites = pygame.sprite.Group()
        self.entity_sprites = pygame.sprite.Group()
        self.zombie_sprites = pygame.sprite.Group()
        self.brain_sprites = pygame.sprite.Group()

        # load data
        self.game_data = GameData()

        # spawn zombie
        self.spawning_zombie = False
        self.timer = 0.0
        self.spawnTime = 2

        # setup
        self.setup()

        # create overlay
        self.overlay = Overlay(player=self.player, game_data=self.game_data)

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
                    path_zombie += (
                        zombie_name
                        + "/"
                        + zombie_name
                        + "-t"
                        + str(sprite_list[0].level)
                        + "-weapon.png"
                    )

            # heath, damage, speed, firerate
            health_zombie = zombie["HEALTH"]
            speed_zombie = float(zombie["SPEED"]) * 10
            firerate_zombie = float(zombie["FIRERATE"]) / 1000
            deals_zombie = float(zombie["DEALS"])

            #
            if can_spawn:
                amount = zombie["AMOUNT"]
                for x in range(0, amount):
                    distance_entity_to_brain = distance
                    distance_entity_to_brain += random.uniform(
                        range_spawn_min, range_spawn_max
                    )
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
                        damage=deals_zombie,
                        add_score_to_player=self.add_score_to_player,
                    )

    def add_score_to_player(self, zombie_max_health):
        self.player.add_score_to_player(zombie_max_health)
        # update game data

    def run(self, dt):
        self.display_surface.fill("black")

        if self.game_started:
            self.all_sprites.custom_draw(self.player)
            self.all_sprites.update(dt)
            self.overlay.display()
        else:
            #
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get(pygame.KEYDOWN)
            if self.activate:
                for event in events:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    else:
                        self.user_name += event.unicode
                    self.user_text = self.base_font.render(
                        self.user_name, True, (255, 255, 255)
                    )
                    self.user_text_rect = self.user_text.get_rect(center=self.pos_text)
            else:
                if input_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.activate = True

            #
            if self.start_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.user_name != "":
                        self.game_started = True
                        # CREATE DATA PLAYER
                        # self.game_data.insert_data(
                        #     self.user_name, self.player.score, self.player.current_wave
                        # )

            #
            self.display_surface.blit(self.game_text, self.game_text_rect)
            self.display_surface.blit(self.user_text, self.user_text_rect)
            self.display_surface.blit(self.start_button, self.start_button_rect)
            if self.activate:
                color = color_active
            else:
                color = color_passive
            input_rect.center = self.user_text_rect.center
            pygame.draw.rect(self.display_surface, color, input_rect, 2)


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


"""
Game: 
- Cho camera góc rộng ra 1 chút
- Thêm số tháp tối đa được đặt là 6, căn cứ chỉ 1, tháp đào vàng là 8

Màn
- Thêm bxh điểm phía góc trên bao gồm: Xếp hạng, Tên, Điểm, Vòng hiện tại
- Thêm màn hình chính vào game: bắt đầu + nhập tên + bxh
- Thêm biểu thị Game over khi căn cứ bị phá + dừng game > hiển thị nút chơi lại hoặc quay về màn hình chính
"""
