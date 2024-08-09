import pygame
import math
from settings import *
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

    def get_pos_mouse_on_map(self):
        pos_mouse_on_screen = pygame.math.Vector2(pygame.mouse.get_pos())
        self.offset = pygame.math.Vector2()
        self.offset.x = self.player.rect.centerx - SCREEN_WIDTH_DEFAULT / 2
        self.offset.y = self.player.rect.centery - SCREEN_HEIGHT_DEFAULT / 2
        pos_mouse_on_map = pos_mouse_on_screen + self.offset
        return pos_mouse_on_map

    def update(self, dt):
        self.pos = self.get_pos_mouse_on_map()
        self.rect = self.image.get_rect(center=self.pos)


class Entity(Generic):
    def __init__(
        self, pos, surf, groups, entity_type, entity_name, z=LAYERS[LAYER_ENTITY_BASE]
    ):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 7, -self.rect.height // 7)
        )
        self.entity_head = None

        if entity_type == ENTITY_TYPE_DEFENSE:
            return
        else:
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
                groups=groups,
                entity_type=entity_type,
                entity_name=entity_name,
            )


class Entity_Head(Generic):
    def __init__(
        self, pos, surf, groups, entity_type, entity_name, z=LAYERS[LAYER_ENTITY_HEAD]
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
        #
        self.can_attack = entity_type == ENTITY_TYPE_ATTACK
        self.creating_entity_projectile = False
        self.direction = pygame.math.Vector2()
        self.attack_cooldown = 1
        self.timer = 0.0

        self.projectile_surf = None

        if self.can_attack:
            self.projectile_surf = pygame.image.load(
                ASSET_PATH_ENTITIES
                + entity_name
                + "/projectile/"
                + entity_name
                + "-projectile.png"
            )

    def calculate_current_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        center_x, center_y = SCREEN_WIDTH_DEFAULT / 2, SCREEN_HEIGHT_DEFAULT / 2

        dx = mouse_x - center_x
        dy = mouse_y - center_y

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 180) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def update_angle(self):
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
        )

    def update(self, dt):
        self.update_angle()

        if self.can_attack:
            self.timer += dt
            if self.timer >= self.attack_cooldown:
                self.create_entity_projectile()
                self.timer = 0
                print("Attack")


class Entity_Projectile(Generic):
    def __init__(self, pos, surf, groups, angle, z=LAYERS[LAYER_ENTITY_PROJECTILE]):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 7, -self.rect.height // 7)
        )
        self.default_image = surf
        self.pos = pos
        self.current_angle = angle
        self.direction = pygame.math.Vector2()
        self.speed = 50

        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

        # test
        self.direction.x = -1

    def movement(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.movement(dt)

        """self.current_angle = self.calculate_current_angle()
        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def calculate_current_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        center_x, center_y = SCREEN_WIDTH_DEFAULT / 2, SCREEN_HEIGHT_DEFAULT / 2

        dx = mouse_x - center_x
        dy = mouse_y - center_y

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 180) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees"""


# ZOMBIE


class Zombie(Generic):
    def __init__(self, pos, surf, groups, player, z=LAYERS[LAYER_ZOMBIE]):
        super().__init__(pos, surf, groups, z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 7, -self.rect.height // 7)
        )

        self.player = player
        self.default_image = surf
        self.pos = pos
        self.current_angle = 0

    def calculate_current_angle(self):
        dx = self.player.pos.x - self.pos.x
        dy = self.player.pos.y - self.pos.y

        print(self.player.pos)
        print(self.rect.center)

        angle_radians = math.atan2(dy, dx)

        angle_degrees = math.degrees(angle_radians)

        angle_degrees = (-angle_degrees - 180) % 360

        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees

    def update_angle(self):
        self.current_angle = self.calculate_current_angle()
        print(self.current_angle)
        self.image = pygame.transform.rotozoom(
            self.default_image, self.current_angle, 1
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        self.update_angle()
