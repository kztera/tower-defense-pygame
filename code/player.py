import pygame
import math
from settings import *
from support import *
from timeCounter import Timer
from asset_path import *
from game_stats import *
from sprites import Entity, Sample_Entity


class Player(pygame.sprite.Sprite):
    def __init__(
        self, pos, group, collision_sprites, tree_sprites, stone_sprites, entity_sprites, zombie_sprites
    ):
        super().__init__(group)

        self.screen_width = pygame.display.get_surface().get_width()
        self.screen_height = pygame.display.get_surface().get_height()

        self.all_sprites = group
        self.collision_sprites = collision_sprites
        self.current_wave = 0

        # general setup
        self.image = pygame.image.load(
            ASSET_PATH_PLAYER + PLAYER_AXE + ".png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS[LAYER_PLAYER]

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.tool_pos = pygame.math.Vector2(self.rect.center)
        self.speed = MOVEMENT_SPEED_PLAYER
        self.direction_state = DIRECTION_DOWN

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

        self.auto_using_tool = False

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

        # interaction
        self.tree_sprites = tree_sprites
        self.stone_sprites = stone_sprites
        self.has_interacted_tree = pygame.sprite.Group()
        self.has_interacted_stone = pygame.sprite.Group()

        # inventory
        self.items_inventory = {
            ITEM_WOOD: 0,
            ITEM_STONE: 0,
            ITEM_GOLD: 0,
            ITEM_TOKEN: 0,
        }

        # handle create entities
        self.entity_sprites = entity_sprites
        self.is_creating_entity = False
        self.sample_entity_image = None

        #
        self.zombie_sprites = zombie_sprites

    def input(self):
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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.auto_using_tool = False
                    self.using_tool = True
                    self.current_angle = self.calculate_current_angle()
                    self.min_angle = self.current_angle
                    self.max_angle = self.current_angle + ANGLE_OF_TOOL_USE
                    self.swing = True
                    self.get_target_pos()
                    self.has_interacted_tree.empty()
                    self.has_interacted_stone.empty()
                    self.timers[TOOL_USE_TIMER].activate()

                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                    and not self.auto_using_tool
                ):
                    self.auto_using_tool = True
                    self.using_tool = True
                    self.current_angle = self.calculate_current_angle()
                    self.min_angle = self.current_angle
                    self.max_angle = self.current_angle + ANGLE_OF_TOOL_USE
                    self.swing = True
                    self.get_target_pos()
                    self.has_interacted_tree.empty()
                    self.has_interacted_stone.empty()
                    self.timers[TOOL_USE_TIMER].activate()
        else:
            if self.auto_using_tool:
                for event in events:
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    ):
                        self.auto_using_tool = False

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
            self.is_creating_entity = False
            self.all_sprites.remove(self.sample_entity_image)
            self.sample_entity_image = None

        # use entity
        if self.is_creating_entity:
            if self.sample_entity_image is None:
                pos_mouse_on_map = self.snap_to_grid_on_map()
                first_dash_position = self.selected_entity.find("-")
                entity_name = self.selected_entity[first_dash_position + 1 :]
                path_base = ""

                # entity type
                entity_type = self.get_entity_type()

                if entity_type == ENTITY_TYPE_DEFENSE:
                    path_base = (
                        ASSET_PATH_ENTITIES
                        + entity_name
                        + "/"
                        + entity_name
                        + "-t1-base.png"
                    )
                else:
                    path_base = (
                        ASSET_PATH_ENTITIES
                        + entity_name
                        + "/base/"
                        + entity_name
                        + "-t1-base.png"
                    )

                sample_entity_surf = pygame.image.load(path_base).convert_alpha()
                sample_entity_surf.set_alpha(100)

                self.sample_entity_image = Sample_Entity(
                    pos=pos_mouse_on_map,
                    surf=sample_entity_surf,
                    groups=self.all_sprites,
                    player=self,
                )

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.timers[ENTITY_USE_TIMER].activate()
                    self.create_entity()
        else:
            self.sample_entity_image = None

        # change entity
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
            else:
                change = False

            if change:
                self.timers[ENTITY_SWITCH_TIMER].activate()
                self.selected_entity = self.entities[self.entity_index]
                self.all_sprites.remove(self.sample_entity_image)
                self.sample_entity_image = None
                self.is_creating_entity = True

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
        self.hitbox.centerx = math.floor(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = math.floor(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def rotate(self):
        player_image = pygame.image.load(
            ASSET_PATH_PLAYER_TOOLS + self.selected_tool + ".png"
        ).convert_alpha()

        if self.using_tool:
            if self.swing:
                self.current_angle += 8
                if self.current_angle >= self.max_angle:
                    self.swing = False
            else:
                self.current_angle -= 8
                if self.current_angle <= self.min_angle:
                    self.using_tool = False
        else:
            self.current_angle = self.calculate_current_angle()

        self.image = pygame.transform.rotozoom(player_image, self.current_angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.auto_using_tool and not self.using_tool:
            self.using_tool = True
            self.current_angle = self.calculate_current_angle()
            self.min_angle = self.current_angle
            self.max_angle = self.current_angle + ANGLE_OF_TOOL_USE
            self.swing = True
            self.get_target_pos()
            self.has_interacted_tree.empty()
            self.has_interacted_stone.empty()
            self.timers[TOOL_USE_TIMER].activate()

    def calculate_current_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        center_x, center_y = self.screen_width / 2, self.screen_height / 2
        dx = mouse_x - center_x
        dy = mouse_y - center_y

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 90) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def use_tool(self):
        if self.using_tool:
            have_impact = False
            if self.selected_tool == TOOL_AXE:
                have_impact = True

            for tree in self.tree_sprites:
                if (
                    tree.rect.collidepoint(self.target_pos)
                    and not tree in self.has_interacted_tree
                ):
                    tree.damage(self.pos, have_impact)
                    self.has_interacted_tree.add(tree)

            for stone in self.stone_sprites:
                if (
                    stone.rect.collidepoint(self.target_pos)
                    and not stone in self.has_interacted_stone
                ):
                    stone.damage(self.pos, have_impact)
                    self.has_interacted_stone.add(stone)

    def use_entity(self):
        # print(self.selected_entity)
        return

    def create_entity(self):
        pos_mouse_on_map = self.snap_to_grid_on_map()

        first_dash_position = self.selected_entity.find("-")
        entity_name = self.selected_entity[first_dash_position + 1 :]
        path_base = ""

        # entity type
        entity_type = self.get_entity_type()

        if entity_type == ENTITY_TYPE_DEFENSE:
            path_base = (
                ASSET_PATH_ENTITIES + entity_name + "/" + entity_name + "-t1-base.png"
            )
        else:
            path_base = (
                ASSET_PATH_ENTITIES
                + entity_name
                + "/base/"
                + entity_name
                + "-t1-base.png"
            )

        # create
        new_entity = Entity(
            pos=pos_mouse_on_map,
            surf=pygame.image.load(path_base),
            groups=[self.all_sprites, self.collision_sprites, self.entity_sprites],
            entity_type=entity_type,
            entity_name=entity_name,
            zombie_sprites=self.zombie_sprites
        )

    def snap_to_grid_on_map(self):
        pos_mouse_on_screen = pygame.math.Vector2(pygame.mouse.get_pos())
        self.offset = pygame.math.Vector2()


        self.offset.x = self.rect.centerx - SCREEN_WIDTH_DEFAULT / 2
        self.offset.y = self.rect.centery - SCREEN_HEIGHT_DEFAULT / 2
        pos_mouse_on_map = pos_mouse_on_screen + self.offset

        is_small_structure = self.selected_entity in [
            ENTITIES_WALL,
            ENTITIES_DOOR,
            ENTITIES_SLOW_TRAP,
        ]

        if is_small_structure:
            snapped_x = (
                math.floor(pos_mouse_on_map.x / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
            )
            snapped_y = (
                math.floor(pos_mouse_on_map.y / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
            )
        else:
            snapped_x = round(pos_mouse_on_map.x / TILE_SIZE) * TILE_SIZE
            snapped_y = round(pos_mouse_on_map.y / TILE_SIZE) * TILE_SIZE

        pos_mouse_on_map = pygame.math.Vector2(snapped_x, snapped_y)

        return pos_mouse_on_map

    def get_entity_type(self):
        entity_type = ENTITY_TYPE_ATTACK
        if (
            self.selected_entity == ENTITIES_WALL
            or self.selected_entity == ENTITIES_DOOR
            or self.selected_entity == ENTITIES_SLOW_TRAP
        ):
            entity_type = ENTITY_TYPE_DEFENSE
        elif (
            self.selected_entity == ENTITIES_GOLD_MINE
            or self.selected_entity == ENTITIES_GOLD_STASH
        ):
            entity_type = ENTITY_TYPE_PRODUCE
        else:
            entity_type = ENTITY_TYPE_ATTACK
        return entity_type

    def get_target_pos(self):
        mouse_direction = self.calculate_current_angle()

        if mouse_direction <= 22.5 or mouse_direction > 337.5:
            self.direction_state = DIRECTION_UP
        elif mouse_direction <= 67.5:
            self.direction_state = DIRECTION_DIAGONAL_LEFT_UP
        elif mouse_direction <= 112.5:
            self.direction_state = DIRECTION_LEFT
        elif mouse_direction <= 157.5:
            self.direction_state = DIRECTION_DIAGONAL_LEFT_DOWN
        elif mouse_direction <= 202.5:
            self.direction_state = DIRECTION_DOWN
        elif mouse_direction <= 247.5:
            self.direction_state = DIRECTION_DIAGONAL_RIGHT_DOWN
        elif mouse_direction <= 292.5:
            self.direction_state = DIRECTION_RIGHT
        elif mouse_direction <= 337.5:
            self.direction_state = DIRECTION_DIAGONAL_RIGHT_UP

        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.direction_state]

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.screen_height = pygame.display.get_surface().get_height()
        self.screen_width = pygame.display.get_surface().get_width()
        self.input()
        self.update_timers()

        self.move(dt)
        self.rotate()
