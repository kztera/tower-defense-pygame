import pygame
import math
from settings import *
from game_stats import *
from asset_path import *

from tower_config import *
import random


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
    def __init__(self, pos, surf, groups, player_add, z=LAYERS[LAYER_STONE]):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 3, -self.rect.height // 3)
        )
        # add item player
        self.player_add = player_add

        # handle damage
        self.taking_damage = False
        self.moving_target = False
        self.diection_of_damage = pygame.math.Vector2()
        self.start_pos = pygame.math.Vector2(self.rect.center)
        self.end_pos = pygame.math.Vector2()
        self.timer = 0

    def damage(self, location_of_perpetrator, have_impact):
        if self.taking_damage:
            return False

        self.player_add(ITEM_STONE)

        if have_impact:
            self.diection_of_damage.x = self.start_pos.x - location_of_perpetrator.x
            self.diection_of_damage.y = self.start_pos.y - location_of_perpetrator.y
            self.diection_of_damage = self.diection_of_damage.normalize()
            self.end_pos = pygame.math.Vector2(
                self.start_pos + self.diection_of_damage * 20
            )
            self.timer = 0
            self.moving_target = True
            self.taking_damage = True
        return True

    def update(self, dt):
        if self.taking_damage:
            if self.moving_target:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(
                        self.start_pos, self.end_pos, self.timer / 0.1
                    )
                else:
                    self.rect.center = self.end_pos
                    self.timer = 0
                    self.moving_target = False
            else:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(
                        self.end_pos, self.start_pos, self.timer / 0.1
                    )
                else:
                    self.rect.center = self.start_pos
                    self.taking_damage = False


class Tree(Generic):
    def __init__(self, pos, surf, groups, player_add, z=LAYERS[LAYER_TREE]):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 10, -self.rect.height // 10)
        )
        # add item player
        self.player_add = player_add
        # handle damage
        self.taking_damage = False
        self.moving_target = False
        self.diection_of_damage = pygame.math.Vector2()
        self.start_pos = pygame.math.Vector2(self.rect.center)
        self.end_pos = pygame.math.Vector2()
        self.timer = 0

    def damage(self, location_of_perpetrator, have_impact):
        if self.taking_damage:
            return False

        self.player_add(ITEM_WOOD)

        if have_impact:
            self.diection_of_damage.x = self.start_pos.x - location_of_perpetrator.x
            self.diection_of_damage.y = self.start_pos.y - location_of_perpetrator.y
            self.diection_of_damage = self.diection_of_damage.normalize()
            self.start_pos = pygame.math.Vector2(self.rect.center)
            self.end_pos = pygame.math.Vector2(
                self.start_pos + self.diection_of_damage * 20
            )
            self.timer = 0
            self.moving_target = True
            self.taking_damage = True
        return True

    def update(self, dt):
        if self.taking_damage:
            if self.moving_target:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(
                        self.start_pos, self.end_pos, self.timer / 0.1
                    )
                else:
                    self.rect.center = self.end_pos
                    self.timer = 0
                    self.moving_target = False
            else:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(
                        self.end_pos, self.start_pos, self.timer / 0.1
                    )
                else:
                    self.rect.center = self.start_pos
                    self.taking_damage = False


class Sample_Entity(Generic):
    def __init__(self, pos, surf, groups, player, z=LAYERS[LAYER_MAIN]):
        super().__init__(pos, surf, groups, z)
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = None
        self.player = player

        self.is_colliding = False
        self.original_image = surf.copy()
        self.collision_image = surf.copy()
        self.collision_image.fill(
            (255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT
        )

    def snap_to_grid_on_map(self):
        pos_mouse_on_screen = pygame.math.Vector2(pygame.mouse.get_pos())
        self.offset = pygame.math.Vector2()
        self.offset.x = self.player.rect.centerx - SCREEN_WIDTH_DEFAULT / 2
        self.offset.y = self.player.rect.centery - SCREEN_HEIGHT_DEFAULT / 2
        pos_mouse_on_map = pos_mouse_on_screen + self.offset

        is_small_structure = self.player.selected_entity in [
            ENTITIES_WALL,
            ENTITIES_DOOR,
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

    def update(self, dt):
        self.pos = self.snap_to_grid_on_map()
        self.rect = self.image.get_rect(center=self.pos)

        is_small_structure = self.player.selected_entity in [
            ENTITIES_WALL,
            ENTITIES_DOOR,
        ]
        size = (
            (TILE_SIZE, TILE_SIZE)
            if is_small_structure
            else (TILE_SIZE * 2, TILE_SIZE * 2)
        )

        # Kiểm tra điều kiện đặt tháp
        self.is_colliding = self.player.check_entity_collision(self.pos, size)
        self.is_have_enough_resource = self.player.entity_can_uprade(0)
        # TODO: Cần kiểm tra thêm xem đã đặt căn cứ chưa?
        self.image = (
            self.collision_image
            if self.is_colliding or not self.is_have_enough_resource
            else self.original_image
        )


# ENTITY


class Entity(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        entity_type,
        entity_name,
        zombie_sprites,
        brain_sprites,
        level_map,
        player_add_gold,
        player_reduct_entity_count,
        z=LAYERS[LAYER_ENTITY_BASE],
    ):
        super().__init__(pos, surf, groups, z)
        self.pos = pos
        self.groups = groups
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.zombie_sprites = zombie_sprites
        self.brain_sprites = brain_sprites
        self.level_map = level_map
        # level
        self.level = 1
        self.max_level = 1
        #
        image_path = self.get_image_path()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 5, -self.rect.height // 5)
        )
        # health
        self.max_health = 100
        self.health = self.max_health
        self.health_bar_distance = 0
        self.health_bar_opacity = 128

        if self.entity_type == ENTITY_TYPE_DEFENSE:
            self.health_bar_width = TILE_SIZE - 5
            self.health_bar_height = 5
            self.health_bar_distance = TILE_SIZE // 2
        else:
            self.health_bar_width = TILE_SIZE * 2 - 10
            self.health_bar_height = HEALTH_BAR_HEIGHT
            self.health_bar_distance = TILE_SIZE

        #
        self.player_reduct_entity_count = player_reduct_entity_count
        # recovery
        self.regen_timer = 0.0
        self.before_regen_time = 0.0
        self.health_regen_per_second = 0.0

        # upgrade
        self.object_upgrade = None
        self.is_showing_upgrade = False
        self.is_clicked = False

        # setup data
        formatted_name = self.entity_name.replace("-", "").upper()
        for tower in TOWER_CONFIG:
            if tower["NAME"] == formatted_name:
                self.max_health = tower["HEALTH"][self.level - 1]
                self.health = self.max_health
                self.max_level = len(tower["HEALTH"])
                self.before_regen_time = tower["MSBEFOREREGEN"][self.level - 1] / 1000
                self.health_regen_per_second = tower["HEALTHREGENPERSECOND"][
                    self.level - 1
                ]

        # entity head
        self.entity_head = None
        #
        self.create_entity_head(player_add_gold)
        self.create_health_bar()

    def get_image_path(self):
        path_image = ""
        if self.entity_type == ENTITY_TYPE_DEFENSE:
            path_image = (
                ASSET_PATH_ENTITIES
                + self.entity_name
                + "/"
                + self.entity_name
                + "-t"
                + str(self.level)
                + "-base.png"
            )
        else:
            path_image = (
                ASSET_PATH_ENTITIES
                + self.entity_name
                + "/base/"
                + self.entity_name
                + "-t"
                + str(self.level)
                + "-base.png"
            )

        return path_image

    def create_entity_head(self, player_add_gold):
        if (
            not self.entity_type is ENTITY_TYPE_DEFENSE
            and not self.entity_type is ENTITY_TYPE_BRAIN
        ):
            self.entity_head = Entity_Head(
                pos=self.rect.center,
                surf=pygame.Surface((0, 0)),
                groups=self.groups[0],
                entity_type=self.entity_type,
                entity_name=self.entity_name,
                level=self.level,
                zombie_sprites=self.zombie_sprites,
                player_add_gold=player_add_gold,
            )

    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage
            self.regen_timer = 0.0
        # check dead
        if self.health <= 0:
            self.destroy_self()

    def create_health_bar(self):
        # create health bar
        health_bar_pos = self.calculate_health_bar_position()

        surface_red = pygame.Surface((self.health_bar_width, self.health_bar_height))
        surface_red.fill("red")
        surface_red.set_alpha(self.health_bar_opacity)
        self.healthBar_background = HealthBar(
            health_bar_pos, surface_red, self.groups[0], z=LAYERS[LAYER_MAX_HEALTH]
        )

        surface_green = pygame.Surface((self.health_bar_width, self.health_bar_height))
        surface_green.fill("green")
        surface_green.set_alpha(self.health_bar_opacity)
        self.healthBar = HealthBar(
            health_bar_pos, surface_green, self.groups[0], z=LAYERS[LAYER_HEALTH]
        )

        # Ẩn health bar ban đầu
        self.healthBar_background.image.set_alpha(0)
        self.healthBar.image.set_alpha(0)

    def calculate_health_bar_position(self):
        health_bar_pos = pygame.math.Vector2(self.rect.center)
        health_bar_pos.x -= self.health_bar_width / 2
        health_bar_pos.y -= self.health_bar_height / 2
        if self.health_bar_distance > 0:
            health_bar_pos.y += self.health_bar_distance
        return health_bar_pos

    def update_health_bar(self):
        health_bar_pos = self.calculate_health_bar_position()

        self.healthBar_background.rect.topleft = health_bar_pos
        self.healthBar.rect.topleft = health_bar_pos

        ratio = max(self.health * 1.0 / self.max_health, 0)
        width = max(HEALTH_BAR_WIDTH * ratio, 1)
        surface_green = pygame.Surface((width, HEALTH_BAR_HEIGHT))
        surface_green.fill("green")
        surface_green.set_alpha(self.health_bar_opacity)
        self.healthBar.image = surface_green

        if self.health < self.max_health:
            self.healthBar_background.image.set_alpha(self.health_bar_opacity)
            self.healthBar.image.set_alpha(self.health_bar_opacity)
        else:
            self.healthBar_background.image.set_alpha(0)
            self.healthBar.image.set_alpha(0)

    def show_upgrade(self, request_show_upgrade):
        if self.level >= self.max_level:
            if not self.object_upgrade is None:
                self.object_upgrade.destroy_self()
                self.object_upgrade = None
            return

        if request_show_upgrade:
            if self.is_showing_upgrade == False:
                self.is_showing_upgrade = True
                self.object_upgrade = Upgrade(
                    pos=self.rect.center,
                    groups=self.groups[0],
                    entiry_name=self.entity_name,
                    entity_type=self.entity_type,
                    level=self.level,
                )
            else:
                self.object_upgrade = Upgrade(
                    pos=self.rect.center,
                    groups=self.groups[0],
                    entiry_name=self.entity_name,
                    entity_type=self.entity_type,
                    level=self.level,
                )
        else:
            self.is_showing_upgrade = False
            if not self.object_upgrade is None:
                self.object_upgrade.destroy_self()
                self.object_upgrade = None

    def request_upgrade(self):
        if self.entity_type is ENTITY_TYPE_BRAIN:
            if self.level < self.max_level:
                self.upgrade()
                return True
        else:
            brain = list(self.brain_sprites)
            if self.level < brain[0].level:
                if self.level < self.max_level:
                    self.upgrade()
                    return True
        return False

    def request_sell(self):
        self.destroy_self()

    def upgrade(self):
        self.level += 1
        #
        image_path = self.get_image_path()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.rect.center)
        #
        if not self.object_upgrade is None:
            self.object_upgrade.destroy_self()
            self.object_upgrade = None
        self.show_upgrade(True)
        #
        if not self.object_upgrade is None:
            self.object_upgrade.destroy_self()
            self.object_upgrade = None
        self.show_upgrade(True)
        #
        formatted_name = self.entity_name.replace("-", "").upper()
        for tower in TOWER_CONFIG:
            if tower["NAME"] == formatted_name:
                self.max_health = tower["HEALTH"][self.level - 1]
                self.health = self.max_health

        if not self.entity_head is None:
            self.entity_head.upgrade()

    def destroy_self(self):
        if self.entity_type is ENTITY_TYPE_BRAIN:
            self.level_map.end_game()

        else:
            self.player_reduct_entity_count(self.entity_name)
        #
        self.healthBar_background.kill()
        self.healthBar.kill()
        if not self.entity_head is None:
            self.entity_head.destroy_self()
        if not self.object_upgrade is None:
            self.object_upgrade.destroy_self()
        self.kill()

    def get_object_upgrade(self):
        return self.object_upgrade

    def regen(self, dt):
        self.regen_timer += dt
        if self.regen_timer >= self.before_regen_time:
            if self.health < self.max_health:
                self.health += self.health_regen_per_second
            if self.health > self.max_health:
                self.health = self.max_health
            self.regen_timer = 0.0

    def update(self, dt):
        self.regen(dt)
        self.update_health_bar()


class Entity_Head(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        entity_type,
        entity_name,
        level,
        zombie_sprites,
        player_add_gold,
        z=LAYERS[LAYER_ENTITY_HEAD],
    ):
        super().__init__(pos, surf, groups, z)
        self.pos = pos
        self.groups = groups
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.level = level
        self.zombie_sprites = zombie_sprites
        self.player_add_gold = player_add_gold
        #
        image_path = self.get_image_path()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 7, -self.rect.height // 7)
        )
        # rotate
        self.default_image = self.image
        self.current_angle = 0
        self.direction = pygame.math.Vector2()
        self.rotation_angle_timer = 0.0
        #
        self.projectile_surf = None
        self.target = None
        self.current_attack_distance = 0.0

        self.tower_radius = 0
        self.ms_between_fire = 2
        self.timer = 0.0
        self.damage_to_zombie = 0
        self.projectile_velocity = 0
        self.projectile_life_time = 0

        self.gold_per_second = 0
        #
        if entity_type is ENTITY_TYPE_ATTACK:
            self.projectile_surf = pygame.image.load(
                ASSET_PATH_ENTITIES
                + entity_name
                + "/projectile/"
                + entity_name
                + "-projectile.png"
            )

        self.update_data_with_level()

        # # draw tower radius
        # self.range_image = pygame.Surface(
        #     (self.tower_radius * 2, self.tower_radius * 2)
        # )
        # self.range_image.fill((0, 0, 0))
        # self.range_image.set_colorkey((0, 0, 0))
        # pygame.draw.circle(
        #     self.range_image,
        #     "grey100",
        #     (self.tower_radius, self.tower_radius),
        #     self.tower_radius,
        # )
        # self.range_image.set_alpha(100)
        # self.range_rect = self.range_image.get_rect(center=self.rect.center)

        # self.draw_tower_radius = draw_circle(
        #     pos=self.rect.center, surf=self.range_image, groups=groups
        # )

    def get_image_path(self):
        imgae_path = (
            ASSET_PATH_ENTITIES
            + self.entity_name
            + "/head/"
            + self.entity_name
            + "-t"
            + str(self.level)
            + "-head.png"
        )

        return imgae_path

    def calculate_current_angle(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        direction_vector = pygame.math.Vector2(dx, dy)
        if direction_vector.length() > 0:
            self.direction = pygame.math.Vector2(dx, dy).normalize()

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 180) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def update_direction_target(self):
        if not self.target is None:
            # angle
            self.current_angle = self.calculate_current_angle()
            self.image = pygame.transform.rotozoom(
                self.default_image, self.current_angle, 1
            )
            self.rect = self.image.get_rect(center=self.rect.center)

    def update_direction_rotate360(self):
        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def create_entity_projectile(self):
        Entity_Projectile(
            pos=pygame.math.Vector2(self.rect.center),
            surf=self.projectile_surf,
            groups=self.groups,
            angle=self.current_angle,
            direction=self.direction,
            speed=self.projectile_velocity,
            damage=self.damage_to_zombie,
            life_time=self.projectile_life_time,
            zombie_sprites=self.zombie_sprites,
        )

    def pick_tartget(self):
        zombies = []
        first_dash_position = ENTITIES_BOMB_TOWER.find("-")
        entity_bomb = ENTITIES_BOMB_TOWER[first_dash_position + 1 :]

        has_target = False
        self.current_attack_distance = 0.0
        for zombie in self.zombie_sprites:
            distance_x = zombie.rect.centerx - self.rect.centerx
            distance_y = zombie.rect.centery - self.rect.centery
            distance = math.sqrt(distance_x**2 + distance_y**2)
            if distance < self.tower_radius:
                if self.entity_name == entity_bomb:
                    zombies.append(zombie)
                else:
                    if self.current_attack_distance == 0.0:
                        self.current_attack_distance = distance
                        self.target = zombie
                        has_target = True
                    else:
                        if distance < self.current_attack_distance:
                            self.current_attack_distance = distance
                            self.target = zombie
                            has_target = True

        if self.entity_name == entity_bomb:
            if len(zombies) > 0:
                self.target = random.choice(zombies)
                has_target = True

        if not has_target:
            self.target = None

    def upgrade(self):
        self.level += 1
        #
        image_path = self.get_image_path()
        self.default_image = pygame.image.load(image_path)
        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)
        #
        self.update_data_with_level()

    def update_data_with_level(self):
        formatted_name = self.entity_name.replace("-", "").upper()
        for tower in TOWER_CONFIG:
            if tower["NAME"] == formatted_name:
                if self.entity_type is ENTITY_TYPE_ATTACK:
                    self.tower_radius = tower["TOWERRADIUS"][self.level - 1]
                    self.ms_between_fire = tower["MSBETWEENFIRES"][self.level - 1] / 400
                    self.damage_to_zombie = tower["DAMAGETOZOMBIES"][self.level - 1]
                    self.projectile_velocity = tower["PROJECTILEVELOCITY"][
                        self.level - 1
                    ] * (self.level + 3)
                    self.projectile_life_time = (
                        tower["PROJECTILELIFETIME"][self.level - 1] / 100
                    )
                if self.entity_type is ENTITY_TYPE_PRODUCE:
                    self.gold_per_second = tower["GOLDPERSECOND"][self.level - 1]

    def destroy_self(self):
        # self.draw_tower_radius.kill()
        self.kill()

    def update(self, dt):
        if self.entity_type == ENTITY_TYPE_ATTACK:
            self.pick_tartget()
            self.update_direction_target()
            if not self.target is None:
                self.timer += dt
                if self.timer >= self.ms_between_fire:
                    self.create_entity_projectile()
                    self.timer = 0
        elif self.entity_type == ENTITY_TYPE_PRODUCE:
            base_rotation_speed = 0.005
            speed_multiplier = 1 + (self.level - 1) * 0.5  # Tăng 50% tốc độ mỗi cấp
            rotation_speed = base_rotation_speed / speed_multiplier

            self.rotation_angle_timer += dt
            if self.rotation_angle_timer >= rotation_speed:
                rotation_amount = int(1 * speed_multiplier)
                self.current_angle += rotation_amount
                if self.current_angle >= 360:
                    self.current_angle %= 360
                self.update_direction_rotate360()
                self.rotation_angle_timer = 0

            self.timer += dt
            if self.timer >= 1:
                self.player_add_gold(self.gold_per_second)
                self.timer = 0


class Entity_Projectile(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        angle,
        direction,
        speed,
        damage,
        life_time,
        zombie_sprites,
        z=LAYERS[LAYER_ENTITY_PROJECTILE],
    ):
        super().__init__(pos, surf, groups, z)
        self.pos = pos
        self.image = pygame.transform.rotozoom(surf, angle, 1)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-self.rect.width, -self.rect.height))

        self.current_angle = angle
        self.direction = direction

        self.speed = speed
        self.damage = damage
        self.life_time = life_time
        self.timer = 0.0

        self.zombie_sprites = zombie_sprites
        #
        self.default_image = self.image

    def movement(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def cause_damage(self):
        for zombie in self.zombie_sprites:
            if not zombie.dead:
                if self.rect.collidepoint(zombie.rect.center):
                    zombie.take_damage(self.damage)
                    self.destroy_self()

    def destroy_self(self):
        self.kill()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.life_time:
            self.destroy_self()

        self.movement(dt)
        self.cause_damage()


#


class draw_circle(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 1, -self.rect.height // 1)
        )


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


# ZOMBIE
class Zombie(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        entity_sprites,
        brain_sprites,
        max_heath,
        speed,
        firerate,
        damage,
        add_score_to_player,
        z=LAYERS[LAYER_ZOMBIE],
    ):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 3, -self.rect.height // 3)
        )
        self.pos = pygame.math.Vector2(self.rect.center)
        self.target = None
        self.brain_sprites = brain_sprites

        # movement
        self.direction = pygame.math.Vector2()
        self.default_image = surf
        self.current_angle = 0
        self.speed = speed

        # damage
        self.attacking = False
        self.swing = False
        self.min_angle = 0
        self.max_angle = 0
        self.attack_distance = 100
        self.entity_sprites = entity_sprites
        self.timer = 0
        self.firerate = firerate
        self.direction_attack = DIRECTION_DOWN
        self.attack_pos = USE_TOOL_OFFSET[DIRECTION_DOWN]
        self.has_caused_damage = False
        self.damage = damage

        self.add_score_to_player = add_score_to_player

        # health
        self.dead = False
        self.max_health = max_heath
        self.health = self.max_health

        self.health_bar_distance = 50

        health_bar_pos = pygame.math.Vector2(self.rect.center)
        health_bar_pos.x -= HEALTH_BAR_WIDTH_ZOMBIE / 2
        health_bar_pos.y += self.health_bar_distance

        surface_red = pygame.Surface((HEALTH_BAR_WIDTH_ZOMBIE, HEALTH_BAR_HEIGHT))
        surface_red.fill("red")
        self.healthBar_background = HealthBar(
            health_bar_pos, surface_red, groups[0], z=LAYERS[LAYER_MAX_HEALTH]
        )

        ratio = self.health / self.max_health
        surface_green = pygame.Surface(
            (HEALTH_BAR_WIDTH_ZOMBIE * ratio, HEALTH_BAR_HEIGHT)
        )
        surface_green.fill("green")
        self.healthBar = HealthBar(
            health_bar_pos, surface_green, groups[0], z=LAYERS[LAYER_HEALTH]
        )

    def calculate_angle(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        self.direction = pygame.math.Vector2(dx, dy).normalize()

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 90) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def update_direction(self, dt):
        if self.attacking:
            if self.swing:
                self.current_angle += 8
                if self.current_angle >= self.max_angle:
                    self.swing = False
            else:
                if self.current_angle > self.min_angle:
                    self.current_angle -= 8
                    self.timer = 0
                else:
                    self.timer += dt
                    if self.timer >= self.firerate:
                        self.attacking = False
        else:
            self.current_angle = self.calculate_angle()

        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def movement(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def take_damage(self, damage):
        if not self.dead:
            self.health -= damage

            if self.health <= 0:
                # ad score to player
                self.add_score_to_player(self.max_health)
                # dead
                self.dead = True
                self.healthBar_background.kill()
                self.healthBar.kill()
                self.kill()

    def update_health_bar(self):
        health_bar_pos = pygame.math.Vector2(self.rect.center)
        health_bar_pos.x -= HEALTH_BAR_WIDTH_ZOMBIE / 2
        health_bar_pos.y += self.health_bar_distance

        self.healthBar_background.rect.topleft = health_bar_pos
        self.healthBar.rect.topleft = health_bar_pos

        ratio = self.health / self.max_health
        surface_green = pygame.Surface(
            (HEALTH_BAR_WIDTH_ZOMBIE * ratio, HEALTH_BAR_HEIGHT)
        )
        surface_green.fill("green")
        self.healthBar.image = surface_green

    def request_attack(self):
        self.attacking = True
        self.swing = True
        self.has_caused_damage = False
        self.current_angle = self.calculate_angle()
        self.min_angle = self.current_angle
        self.max_angle = self.current_angle + ANGLE_OF_TOOL_USE
        self.get_attack_pos()

    def attack(self):
        if self.attacking:
            if (
                self.target.rect.collidepoint(self.target_pos)
                and not self.has_caused_damage
            ):
                self.target.take_damage(self.damage)
                self.has_caused_damage = True

    def update_status(self, dt):
        for entity in self.entity_sprites:
            self_pos = pygame.math.Vector2(self.rect.center)
            target_pos = pygame.math.Vector2(entity.rect.center)
            distance = self_pos.distance_to(target_pos)
            if distance < self.attack_distance:
                self.target = entity
                break
            else:
                self.target = None

        if self.target is None:
            sprite_list = list(self.brain_sprites)
            if len(sprite_list) > 0:
                self.target = sprite_list[0]
            else:
                self.attacking = False
                self.target = None
                return

        if self.target is None:
            self.attacking = False
        else:
            self_pos = pygame.math.Vector2(self.rect.center)
            target_pos = pygame.math.Vector2(self.target.rect.center)
            distance = self_pos.distance_to(target_pos)

            if self.target.entity_type is ENTITY_TYPE_DEFENSE:
                self.attack_distance = 55
            else:
                self.attack_distance = 85

            if distance > self.attack_distance:
                self.movement(dt)
            else:
                if not self.attacking:
                    self.request_attack()

    def get_attack_pos(self):
        if self.current_angle <= 22.5 or self.current_angle > 337.5:
            self.direction_attack = DIRECTION_UP
        elif self.current_angle <= 67.5:
            self.direction_attack = DIRECTION_DIAGONAL_LEFT_UP
        elif self.current_angle <= 112.5:
            self.direction_attack = DIRECTION_LEFT
        elif self.current_angle <= 157.5:
            self.direction_attack = DIRECTION_DIAGONAL_LEFT_DOWN
        elif self.current_angle <= 202.5:
            self.direction_attack = DIRECTION_DOWN
        elif self.current_angle <= 247.5:
            self.direction_attack = DIRECTION_DIAGONAL_RIGHT_DOWN
        elif self.current_angle <= 292.5:
            self.direction_attack = DIRECTION_RIGHT
        elif self.current_angle <= 337.5:
            self.direction_attack = DIRECTION_DIAGONAL_RIGHT_UP

        self.target_pos = self.rect.center + USE_TOOL_OFFSET[self.direction_attack]

    def update(self, dt):
        self.update_status(dt)
        self.update_health_bar()

        if not self.target is None:
            self.update_direction(dt)
            if self.attacking:
                self.attack()


# UPGRADE


class Upgrade(pygame.sprite.Sprite):
    def __init__(
        self, pos, groups, entiry_name, entity_type, level, z=LAYERS[LAYER_UPGRADE]
    ):
        super().__init__(groups)
        self.width = 400
        self.height = 300
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.set_alpha(80)
        self.rect = self.image.get_rect(center=pos)
        self.z = z

        self.groups = groups
        self.entiry_name = entiry_name
        self.entity_type = entity_type
        self.level = level

        self.tower_current = None
        self.tower_upgrade = None

        self.text_name = None
        self.text_level = None
        self.text_health_current = None
        self.text_health_upgrade = None
        self.text_damage_current = None
        self.text_damage_upgrade = None
        self.text_range_current = None
        self.text_range_upgrade = None

        self.text_arrow = None

        self.text_gold_current = None
        self.text_gold_upgrade = None

        self.button_upgrade = None
        self.button_sell = None

        self.tower_current = TowerInformation(entiry_name, entity_type, level)
        self.tower_upgrade = TowerInformation(entiry_name, entity_type, level + 1)

        self.create_name_level(groups, entiry_name, level)
        self.create_config(groups, entity_type)
        self.create_button(groups)

    def create_name_level(self, groups, entiry_name, level):
        # text entity_name
        str_text_name = entiry_name.replace("-", " ").upper()
        pos_text_name = pygame.math.Vector2(self.rect.center)
        pos_text_name.y -= 120

        self.text_name = Text(
            pos=pos_text_name, groups=groups, text=str_text_name, text_size=40
        )

        # text level
        str_text_level = "LEVEL " + str(level).upper()
        pos_text_level = pygame.math.Vector2(self.rect.center)
        pos_text_level.y -= 80

        self.text_level = Text(
            pos=pos_text_level, groups=groups, text=str_text_level, text_size=30
        )

    def create_config(self, groups, entity_type):
        # Config
        if entity_type is ENTITY_TYPE_ATTACK:
            # health
            str_text_health_current = (
                "Health: " + str(self.tower_current.HEALTH).upper()
            )
            pos_text_health_current = pygame.math.Vector2(self.rect.center)
            pos_text_health_current.x -= 110
            pos_text_health_current.y -= 40
            self.text_health_current = Text(
                pos=pos_text_health_current,
                groups=groups,
                text=str_text_health_current,
                text_size=30,
            )

            str_text_health_upgrade = (
                "Health: " + str(self.tower_upgrade.HEALTH).upper()
            )
            pos_text_health_upgrade = pygame.math.Vector2(self.rect.center)
            pos_text_health_upgrade.x += 110
            pos_text_health_upgrade.y -= 40
            self.text_health_upgrade = Text(
                pos=pos_text_health_upgrade,
                groups=groups,
                text=str_text_health_upgrade,
                text_size=30,
            )

            # damage
            str_text_damage_current = (
                "Damage: " + str(self.tower_current.DAMAGETOZOMBIES).upper()
            )
            pos_text_damage_current = pygame.math.Vector2(self.rect.center)
            pos_text_damage_current.x -= 110
            self.text_damage_current = Text(
                pos=pos_text_damage_current,
                groups=groups,
                text=str_text_damage_current,
                text_size=30,
            )

            #
            pos_text_arrow = pygame.math.Vector2(self.rect.center)
            self.text_arrow = Text(
                pos=pos_text_arrow, groups=groups, text=">", text_size=60
            )

            #
            str_text_damage_upgrade = (
                "Damage: " + str(self.tower_current.DAMAGETOZOMBIES).upper()
            )
            pos_text_damage_upgrade = pygame.math.Vector2(self.rect.center)
            pos_text_damage_upgrade.x += 110
            self.text_damage_upgrade = Text(
                pos=pos_text_damage_upgrade,
                groups=groups,
                text=str_text_damage_upgrade,
                text_size=30,
            )

            # range
            str_text_range_current = (
                "Range: " + str(self.tower_current.TOWERRADIUS).upper()
            )
            pos_text_range_current = pygame.math.Vector2(self.rect.center)
            pos_text_range_current.x -= 110
            pos_text_range_current.y += 40
            self.text_range_current = Text(
                pos=pos_text_range_current,
                groups=groups,
                text=str_text_range_current,
                text_size=30,
            )

            str_text_range_upgrade = (
                "Range: " + str(self.tower_current.TOWERRADIUS).upper()
            )
            pos_text_range_upgrade = pygame.math.Vector2(self.rect.center)
            pos_text_range_upgrade.x += 110
            pos_text_range_upgrade.y += 40
            self.text_range_upgrade = Text(
                pos=pos_text_range_upgrade,
                groups=groups,
                text=str_text_range_upgrade,
                text_size=30,
            )

        elif entity_type is ENTITY_TYPE_PRODUCE:
            str_text_health_current = (
                "Health: " + str(self.tower_current.HEALTH).upper()
            )
            pos_text_health_current = pygame.math.Vector2(self.rect.center)
            pos_text_health_current.x -= 110
            pos_text_health_current.y -= 20
            self.text_health_current = Text(
                pos=pos_text_health_current,
                groups=groups,
                text=str_text_health_current,
                text_size=30,
            )

            str_text_health_upgrade = (
                "Health: " + str(self.tower_upgrade.HEALTH).upper()
            )
            pos_text_health_upgrade = pygame.math.Vector2(self.rect.center)
            pos_text_health_upgrade.x += 110
            pos_text_health_upgrade.y -= 20
            self.text_health_upgrade = Text(
                pos=pos_text_health_upgrade,
                groups=groups,
                text=str_text_health_upgrade,
                text_size=30,
            )

            # arrow
            pos_text_arrow = pygame.math.Vector2(self.rect.center)
            self.text_arrow = Text(
                pos=pos_text_arrow, groups=groups, text=">", text_size=60
            )

            # gold
            str_text_gold_current = (
                "Gold/Sec: " + str(self.tower_current.GOLDPERSECOND).upper()
            )
            pos_text_gold_current = pygame.math.Vector2(self.rect.center)
            pos_text_gold_current.x -= 110
            pos_text_gold_current.y += 20
            self.text_gold_current = Text(
                pos=pos_text_gold_current,
                groups=groups,
                text=str_text_gold_current,
                text_size=30,
            )

            str_text_gold_upgrade = (
                "Gold/Sec: " + str(self.tower_upgrade.GOLDPERSECOND).upper()
            )
            pos_text_gold_upgrade = pygame.math.Vector2(self.rect.center)
            pos_text_gold_upgrade.x += 110
            pos_text_gold_upgrade.y += 20
            self.text_gold_upgrade = Text(
                pos=pos_text_gold_upgrade,
                groups=groups,
                text=str_text_gold_upgrade,
                text_size=30,
            )

        else:
            str_text_health_current = (
                "Health: " + str(self.tower_current.HEALTH).upper()
            )
            pos_text_health_current = pygame.math.Vector2(self.rect.center)
            pos_text_health_current.x -= 110
            self.text_health_current = Text(
                pos=pos_text_health_current,
                groups=groups,
                text=str_text_health_current,
                text_size=30,
            )

            #
            pos_text_arrow = pygame.math.Vector2(self.rect.center)
            self.text_arrow = Text(
                pos=pos_text_arrow, groups=groups, text=">", text_size=60
            )

            str_text_health_upgrade = (
                "Health: " + str(self.tower_upgrade.HEALTH).upper()
            )
            pos_text_health_upgrade = pygame.math.Vector2(self.rect.center)
            pos_text_health_upgrade.x += 110
            self.text_health_upgrade = Text(
                pos=pos_text_health_upgrade,
                groups=groups,
                text=str_text_health_upgrade,
                text_size=30,
            )

    def create_button(self, groups):
        # BUTTON
        str_gold = str(self.tower_upgrade.GOLDCOSTS) + " gold, "
        str_wood = str(self.tower_upgrade.WOODCOSTS) + " wood, "
        str_stone = str(self.tower_upgrade.STONECOSTS) + " stone, "

        pos_button_upgrade = pygame.math.Vector2(self.rect.center)
        pos_button_upgrade.y += 80
        self.button_upgrade = Button(
            pos=pos_button_upgrade,
            groups=groups,
            width=350,
            height=30,
            text="Upgrade",
            text_item=str_gold + str_wood + str_stone,
        )
        self.button_upgrade.text.rect.left = pos_button_upgrade.x - 350 / 2 + 20
        self.button_upgrade.text_item.rect.left = (
            self.button_upgrade.text.rect.right + 10
        )

        pos_button_sell = pygame.math.Vector2(self.rect.center)
        pos_button_sell.y += 120
        self.button_sell = Button(
            pos=pos_button_sell,
            groups=groups,
            width=350,
            height=30,
            text="Sell",
            text_item="destroy",
        )
        self.button_sell.text.rect.left = pos_button_sell.x - 350 / 2 + 20
        self.button_sell.text_item.rect.left = self.button_sell.text.rect.right + 10

    def destroy_self(self):
        self.text_name.destroy_self()
        self.text_level.destroy_self()
        self.text_health_current.destroy_self()
        self.text_health_upgrade.destroy_self()

        if self.entity_type is ENTITY_TYPE_ATTACK:
            self.text_damage_current.destroy_self()
            self.text_damage_upgrade.destroy_self()
            self.text_range_current.destroy_self()
            self.text_range_upgrade.destroy_self()
        elif self.entity_type is ENTITY_TYPE_PRODUCE:
            self.text_gold_current.destroy_self()
            self.text_gold_upgrade.destroy_self()

        self.text_arrow.destroy_self()
        self.button_upgrade.destroy_self()
        self.button_sell.destroy_self()

        self.kill()


class TowerInformation:
    def __init__(self, entiry_name, entity_type, level):
        self.NAME = None
        self.GOLDCOSTS = None
        self.WOODCOSTS = None
        self.STONECOSTS = None
        self.HEALTH = None
        #
        self.GOLDPERSECOND = None
        #
        self.DAMAGETOZOMBIES = None
        self.TOWERRADIUS = None
        self.MSBETWEENFIRES = None
        self.PROJECTILEVELOCITY = None
        self.PROJECTILELIFETIME = None

        formatted_name = entiry_name.replace("-", "").upper()
        for tower in TOWER_CONFIG:
            if tower["NAME"] == formatted_name:
                self.NAME = tower["NAME"]
                self.GOLDCOSTS = tower["GOLDCOSTS"][level - 1]
                self.WOODCOSTS = tower["WOODCOSTS"][level - 1]
                self.STONECOSTS = tower["STONECOSTS"][level - 1]
                self.HEALTH = tower["HEALTH"][level - 1]

                if entity_type is ENTITY_TYPE_PRODUCE:
                    self.GOLDPERSECOND = tower["GOLDPERSECOND"][level - 1]

                elif entity_type is ENTITY_TYPE_ATTACK:
                    self.DAMAGETOZOMBIES = tower["DAMAGETOZOMBIES"][level - 1]
                    self.TOWERRADIUS = tower["TOWERRADIUS"][level - 1]
                    self.MSBETWEENFIRES = tower["MSBETWEENFIRES"][level - 1]
                    self.PROJECTILEVELOCITY = tower["PROJECTILEVELOCITY"][level - 1]
                    self.PROJECTILELIFETIME = tower["PROJECTILELIFETIME"][level - 1]


class Button(pygame.sprite.Sprite):
    def __init__(
        self, pos, groups, width, height, text, text_item, z=LAYERS[LAYER_BUTTON]
    ):
        super().__init__(groups)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.set_alpha(80)
        self.rect = self.image.get_rect(center=pos)
        self.z = z

        self.text = Text(pos=pos, groups=groups, text=text, text_size=25)
        self.text_item = Text(pos=pos, groups=groups, text=text_item, text_size=20)

    def destroy_self(self):
        self.text.destroy_self()
        self.text_item.destroy_self()
        self.kill()


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, groups, text, text_size, z=LAYERS[LAYER_TEXT]):
        super().__init__(groups)
        font = pygame.font.Font(None, text_size)
        self.image = font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.z = z

    def destroy_self(self):
        self.kill()


""" 
    MSBEFOREREGEN: Thời gian chờ để tháp bắt đầu hồi máu sau khi bị tấn công (ms = milliseconds)
    HEALTHREGENPERSECOND: Máu hồi mỗi giây
    DAMAGETOPLAYERS: Sát thương của tháp đối với người chơi
    DAMAGETONEUTRALS: Sát thương của tháp đối với neutral
    PROJECTILELIFETIME: Thời gian tồn tại của đạn (ms)
    PROJECTILEVELOCITY: Vận tốc của đạn
    PROJECTILENAME: Tên của đạn
    PROJECTILEAOE: Đạn có gây sát thương cho nhiều mục tiêu không
    PROJECTILEAOERADIUS: Bán kính của đạn
    PROJECTILECOLLISIONRADIUS: Bán kính va chạm của đạn
    PROJECTILECOUNT: Số lượng đạn mỗi lần bắn
    PROJECTILEIGNORESCOLLISIONS: Đạn có bỏ qua va chạm không
    PROJECTILEMAXRANGE: Khoảng cách tối đa mà đạn có thể đi được"""
