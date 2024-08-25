import pygame
import math
from settings import *
from game_stats import *
from asset_path import *


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
            self.diection_of_damage.x = self.rect.centerx - location_of_perpetrator.x
            self.diection_of_damage.y = self.rect.centery - location_of_perpetrator.y
            self.diection_of_damage = self.diection_of_damage.normalize()
            self.start_pos = pygame.math.Vector2(self.rect.center)
            self.end_pos = pygame.math.Vector2(
                self.rect.center + self.diection_of_damage * 20
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
                    self.timer = 0
                    self.moving_target = False
            else:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(
                        self.end_pos, self.start_pos, self.timer / 0.1
                    )
                else:
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
        self.start_pos = pygame.math.Vector2()
        self.end_pos = pygame.math.Vector2()
        self.timer = 0

    def damage(self, location_of_perpetrator, have_impact):
        if self.taking_damage:
            return False

        self.player_add(ITEM_WOOD)

        if have_impact:
            self.diection_of_damage.x = self.rect.centerx - location_of_perpetrator.x
            self.diection_of_damage.y = self.rect.centery - location_of_perpetrator.y
            self.diection_of_damage = self.diection_of_damage.normalize()
            self.start_pos = pygame.math.Vector2(self.rect.center)
            self.end_pos = pygame.math.Vector2(
                self.rect.center + self.diection_of_damage * 20
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
                    self.timer = 0
                    self.moving_target = False
            else:
                self.timer += dt
                if self.timer <= 0.1:
                    self.rect.center = Vector2.lerp(
                        self.end_pos, self.start_pos, self.timer / 0.1
                    )
                else:
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

    def update(self, dt):
        self.pos = self.snap_to_grid_on_map()
        self.rect = self.image.get_rect(center=self.pos)

        is_small_structure = self.player.selected_entity in [
            ENTITIES_WALL,
            ENTITIES_DOOR,
            ENTITIES_SLOW_TRAP,
        ]
        size = (
            (TILE_SIZE, TILE_SIZE)
            if is_small_structure
            else (TILE_SIZE * 2, TILE_SIZE * 2)
        )

        # Kiểm tra va chạm và cập nhật hình ảnh
        self.is_colliding = self.player.check_entity_collision(self.pos, size)
        self.image = self.collision_image if self.is_colliding else self.original_image


class Entity(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        entity_type,
        entity_name,
        zombie_sprites,
        z=LAYERS[LAYER_ENTITY_BASE],
    ):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 5, -self.rect.height // 5)
        )

        #
        self.pos = pos
        self.entity_head = None

        self.entity_type = entity_type

        # health
        self.max_health = 100
        self.health = self.max_health
        self.health_bar_distance = 40

        # create entity head
        if not entity_type is ENTITY_TYPE_DEFENSE:
            head_surf = pygame.image.load(
                ASSET_PATH_ENTITIES
                + entity_name
                + "/head/"
                + entity_name
                + "-t1-head.png"
            )

            self.entity_head = Entity_Head(
                pos=pos,
                surf=head_surf,
                groups=[groups[0]],
                entity_type=entity_type,
                entity_name=entity_name,
                zombie_sprites=zombie_sprites,
            )

        # create health bar
        healthBar_pos = pygame.math.Vector2(self.rect.center)
        healthBar_pos.x -= HEALTH_BAR_WIDTH / 2
        healthBar_pos.y += self.health_bar_distance

        surface_red = pygame.Surface((HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        surface_red.fill("red")
        self.healthBar_background = HealthBar(
            healthBar_pos, surface_red, groups[0], z=LAYERS[LAYER_MAX_HEALTH]
        )

        ratio = self.health / self.max_health
        surface_green = pygame.Surface((HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))
        surface_green.fill("green")
        self.healthBar = HealthBar(
            healthBar_pos, surface_green, groups[0], z=LAYERS[LAYER_HEATH]
        )

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.healthBar_background.kill()
            self.healthBar.kill()
            if not self.entity_head is None:
                self.entity_head.kill()
            self.kill()

    def update_heathBar(self):
        healthBar_pos = pygame.math.Vector2(self.rect.center)
        healthBar_pos.x -= HEALTH_BAR_WIDTH / 2
        healthBar_pos.y += self.health_bar_distance

        self.healthBar_background.rect.topleft = healthBar_pos
        self.healthBar.rect.topleft = healthBar_pos

        ratio = self.health / self.max_health
        surface_green = pygame.Surface((HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))
        surface_green.fill("green")
        self.healthBar.image = surface_green

    def update(self, dt):
        self.update_heathBar()


class Entity_Head(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        entity_type,
        entity_name,
        zombie_sprites,
        z=LAYERS[LAYER_ENTITY_HEAD],
    ):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 7, -self.rect.height // 7)
        )
        self.default_image = surf
        self.pos = pos
        self.groups = groups
        self.current_angle = 0
        self.zombie_sprites = zombie_sprites
        self.direction = pygame.math.Vector2()

        #
        self.can_attack = entity_type == ENTITY_TYPE_ATTACK
        self.creating_entity_projectile = False
        self.attack_cooldown = 2
        self.timer = 0.0
        self.range = 360
        self.last_shot = pygame.time.get_ticks()
        self.target = None

        #
        self.projectile_surf = None

        #
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(
            self.range_image, "grey100", (self.range, self.range), self.range
        )
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect(center=self.rect.center)

        draw_circle(pos=self.rect.center, surf=self.range_image, groups=groups)

        #

        if self.can_attack:
            self.projectile_surf = pygame.image.load(
                ASSET_PATH_ENTITIES
                + entity_name
                + "/projectile/"
                + entity_name
                + "-projectile.png"
            )

    def calculate_current_angle(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        if not self.direction is pygame.math.Vector2():
            self.direction = pygame.math.Vector2(dx, dy).normalize()

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 180) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def update_direction(self):
        if not self.target is None:
            # angle
            self.current_angle = self.calculate_current_angle()
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
            zombie_sprites=self.zombie_sprites,
        )

    def pick_tartget(self):
        has_target = False
        for zombie in self.zombie_sprites:
            distance_x = zombie.rect.centerx - self.rect.centerx
            distance_y = zombie.rect.centery - self.rect.centery
            distance = math.sqrt(distance_x**2 + distance_y**2)
            if distance < self.range:
                self.target = zombie
                has_target = True

        if not has_target:
            self.target = None

    def update(self, dt):
        self.pick_tartget()
        self.update_direction()

        if self.can_attack and not self.target is None:
            self.timer += dt
            if self.timer >= self.attack_cooldown:
                self.create_entity_projectile()
                self.timer = 0


class Entity_Projectile(Generic):
    def __init__(
        self,
        pos,
        surf,
        groups,
        angle,
        direction,
        zombie_sprites,
        z=LAYERS[LAYER_ENTITY_PROJECTILE],
    ):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-self.rect.width, -self.rect.height))

        # movement
        self.pos = pos
        self.direction = direction
        self.speed = 200

        # rotation
        self.default_image = surf
        self.current_angle = angle
        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)
        self.zombie_sprites = zombie_sprites

        # damage
        self.damage = 20

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
                    self.kill()

    def update(self, dt):
        self.movement(dt)
        self.cause_damage()


class draw_circle(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(pos, surf, groups[0], z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 1, -self.rect.height // 1)
        )


# ZOMBIE
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class Zombie(Generic):
    def __init__(self, pos, surf, groups, entity_sprites, z=LAYERS[LAYER_ZOMBIE]):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 3, -self.rect.height // 3)
        )
        self.pos = pygame.math.Vector2(self.rect.center)
        self.target = None

        # movement
        self.direction = pygame.math.Vector2()
        self.default_image = surf
        self.current_angle = 0
        self.speed = 100

        # damage
        self.attacking = False
        self.swing = False
        self.min_angle = 0
        self.max_angle = 0
        self.range = 480
        self.entity_sprites = entity_sprites
        self.timer = 0
        self.cooldown = 1
        self.direction_attack = DIRECTION_DOWN
        self.attack_pos = USE_TOOL_OFFSET[DIRECTION_DOWN]
        self.has_caused_damage = False
        self.damage = 50

        # health
        self.dead = False
        self.max_health = 100
        self.health = self.max_health

        self.health_bar_distance = 50

        healthBar_pos = pygame.math.Vector2(self.rect.center)
        healthBar_pos.x -= HEALTH_BAR_WIDTH / 2
        healthBar_pos.y += self.health_bar_distance

        surface_red = pygame.Surface((HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        surface_red.fill("red")
        self.healthBar_background = HealthBar(
            healthBar_pos, surface_red, groups[0], z=LAYERS[LAYER_MAX_HEALTH]
        )

        ratio = self.health / self.max_health
        surface_green = pygame.Surface((HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))
        surface_green.fill("green")
        self.healthBar = HealthBar(
            healthBar_pos, surface_green, groups[0], z=LAYERS[LAYER_HEATH]
        )

    def pick_target(self):
        has_target = False
        for entity in self.entity_sprites:
            distance_x = entity.rect.centerx - self.rect.centerx
            distance_y = entity.rect.centery - self.rect.centery
            distance = math.sqrt(distance_x**2 + distance_y**2)
            if distance < self.range:
                self.target = entity
                has_target = True

        if has_target is False:
            self.target = None

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
                    if self.timer >= self.cooldown:
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
                self.dead = True
                self.healthBar_background.kill()
                self.healthBar.kill()
                self.kill()

    def update_heathBar(self):
        healthBar_pos = pygame.math.Vector2(self.rect.center)
        healthBar_pos.x -= HEALTH_BAR_WIDTH / 2
        healthBar_pos.y += self.health_bar_distance

        self.healthBar_background.rect.topleft = healthBar_pos
        self.healthBar.rect.topleft = healthBar_pos

        ratio = self.health / self.max_health
        surface_green = pygame.Surface((HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))
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
        if self.target is None:
            self.attacking = False
        else:
            self_pos = pygame.math.Vector2(self.rect.center)
            target_pos = pygame.math.Vector2(self.target.rect.center)

            distance = self_pos.distance_to(target_pos)

            attack_distance = 0
            if self.target.entity_type == ENTITY_TYPE_DEFENSE:
                attack_distance = 70
            else:
                attack_distance = 100

            if distance > attack_distance:
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
        self.pick_target()
        self.update_status(dt)
        self.update_heathBar()

        if not self.target is None:
            self.update_direction(dt)
            if self.attacking:
                self.attack()
