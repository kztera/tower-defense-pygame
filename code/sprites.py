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


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, entity_type, entity_name, z=LAYERS[LAYER_ENTITY]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(
            (-self.rect.width // 7, -self.rect.height // 7)
        )

        self.entity_type = entity_type
        self.entity_head = None

        if self.entity_type == ENTITY_TYPE_ATTACK or self.entity_type == ENTITY_TYPE_PRODUCE:
            head_surf = pygame.image.load(
                ASSET_PATH_ENTITIES + entity_name + "/head/" + entity_name + "-t1-head.png"
            )

            self.entity_head = Entity_Head(
                pos=pos,
                surf= head_surf,
                groups=groups)
        
    def update(self, dt):
        if not self.entity_head is None:
            self.entity_head.update(dt) 
    
    

class Entity_Head(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.default_image = surf
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        #
        self.current_angle = 0

    def update(self, dt):
        self.current_angle = self.calculate_current_angle()
        self.image = pygame.transform.rotozoom(self.default_image, self.current_angle, 1)
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
        return angle_degrees
    
class Entity_Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS[LAYER_MAIN]):
        super().__init__(groups)
        self.default_image = surf
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z

        # attack, defend, produce
        self.current_angle = 0

    def update(self, dt):
        self.current_angle = self.calculate_current_angle()
        self.image = pygame.transform.rotozoom(self.default_image, self.current_angle, 1)
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
        return angle_degrees