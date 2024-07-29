import pygame
import math
from settings import *
from support import *
from timeCounter import Timer
from asset_path import *
from game_stats import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        # general setup
        self.image = pygame.image.load(
            ASSET_PATH_PLAYER + PLAYER_AXE + ".png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS[LAYER_MAIN]

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.tool_pos = pygame.math.Vector2(self.rect.center)
        self.speed = MOVEMENT_SPEED_PLAYER

        # collision
        self.hitbox = self.rect.copy().inflate((-130, -130))
        self.collision_sprites = collision_sprites

        # tools
        self.tools = [TOOL_AXE, TOOL_SPEAR]
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.using_tool = False
        self.current_angle = 0
        self.swing = False
        self.max_angle = 0
        self.min_angle = 0

        # entities
        self.entities = [
            ENTITIES_WALL,
            ENTITIES_DOOR,
            ENTITIES_SLOW_TRAP,
            ENTITIES_ARROW_TOWER,
            ENTITIES_BOMB_TOWER,
            ENTITIES_CANNON_TOWER,
            ENTITIES_MAGE_TOWER,
            ENTITIES_MELEE_TOWER,
            ENTITIES_HARVESTER,
            ENTITIES_GOLD_MINE,
            ENTITIES_GOLD_STASH,
        ]
        self.entity_index = 0
        self.selected_entity = self.entities[self.entity_index]

        # timers
        self.timers = {
            TOOL_USE_TIMER: Timer(TIME_FOR_TOOL, self.use_tool),
            TOOL_SWITCH_TIMER: Timer(TIME_FOR_TOOL_SWITCH),
            ENTITY_USE_TIMER: Timer(TIME_FOR_ENTITY, self.use_entity),
            ENTITY_SWITCH_TIMER: Timer(TIME_FOR_ENTITY_SWITCH),
        }

    def input(self):
        # keybroad button input
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        # direction
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # use tool
        if not self.using_tool:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.using_tool = True
                        self.current_angle = self.calculate_current_angle()
                        self.min_angle = self.current_angle
                        self.max_angle = self.current_angle + ANGLE_OF_TOOL_USE
                        self.swing = True
                        # timer for use tool
                        self.timers[TOOL_USE_TIMER].activate()
                        self.direction = pygame.math.Vector2()
                        print("attack")

        # change tool
        changing_tool = False
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                changing_tool = True

        if (keys[pygame.K_q] or changing_tool) and not self.timers[
            TOOL_SWITCH_TIMER
        ].active:
            self.timers[TOOL_SWITCH_TIMER].activate()
            self.tool_index += 1
            self.tool_index = (
                self.tool_index if self.tool_index < len(self.tools) else 0
            )
            self.selected_tool = self.tools[self.tool_index]
            changing_tool = False

        # use entities
        if keys[pygame.K_LCTRL]:
            # timer for use defense base
            self.timers[ENTITY_USE_TIMER].activate()
            self.direction = pygame.math.Vector2()

        # change entities
        if not self.timers[ENTITY_SWITCH_TIMER].active:
            change = True
            if keys[pygame.K_1]:
                self.entity_index = 0
            elif keys[pygame.K_2]:
                self.entity_index = 1
            elif keys[pygame.K_3]:
                self.entity_index = 2
            elif keys[pygame.K_4]:
                self.entity_index = 3
            elif keys[pygame.K_5]:
                self.entity_index = 4
            elif keys[pygame.K_6]:
                self.entity_index = 5
            elif keys[pygame.K_7]:
                self.entity_index = 6
            elif keys[pygame.K_8]:
                self.entity_index = 7
            elif keys[pygame.K_9]:
                self.entity_index = 8
            elif keys[pygame.K_0]:
                self.entity_index = 9
            else:
                change = False

            if change:
                self.timers[ENTITY_SWITCH_TIMER].activate()
                self.selected_entity = self.entities[self.entity_index]
            """
            self.timers[ENTITY_SWITCH_TIMER].activate()
            self.entity_index += 1
            self.entity_index = (
                self.entity_index if self.entity_index < len(self.entities) else 0
            )
            self.selected_entity = self.entities[self.entity_index]
            """

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == "vertical":
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def rotate(self):
        player_image = pygame.image.load(
            ASSET_PATH_PLAYER_TOOLS + self.selected_tool + ".png"
        ).convert_alpha()

        if self.using_tool:
            if self.swing:
                self.current_angle += 10
                if self.current_angle >= self.max_angle:
                    self.swing = False
            else:
                self.current_angle -= 10
                if self.current_angle <= self.min_angle:
                    self.using_tool = False
        else:
            self.current_angle = self.calculate_current_angle()

        self.image = pygame.transform.rotozoom(player_image, self.current_angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def calculate_current_angle(self):
        # Lấy vị trí chuột
        mouse_x, mouse_y = pygame.mouse.get_pos()

        center_x, center_y = SCREEN_WIDTH_DEFAULT / 2, SCREEN_HEIGHT_DEFAULT / 2
        # Tính vector từ tâm đến vị trí chuột
        dx = mouse_x - center_x
        dy = mouse_y - center_y

        # Tính góc giữa vector đó và trục y dương
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        # Chuyển đổi góc để hướng lên trên (0, 1) là 0 độ và góc tính theo chiều kim đồng hồ
        angle_degrees = (-angle_degrees - 90) % 360

        # Đảm bảo góc trong khoảng 0 - 360 độ
        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def use_tool(self):
        # print(self.selected_entity)
        return

    def use_entity(self):
        # print(self.selected_tool)
        return

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.update_timers()
        self.move(dt)
        self.rotate()
