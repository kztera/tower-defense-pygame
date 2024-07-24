import pygame
from settings import *
from support import *
from timeCounter import Timer

from player_stats import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # import asset
        self.import_assets()

        # begin status
        self.status = ANIM_PLAYER_DOWN_IDLE
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = MOVEMENT_SPEED_PLAYER

        # tools
        self.tools = [TOOL_PLAYER_AXE, TOOL_PLAYER_SWORD]
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # defense base
        self.defense_bases = [DEFENSE_BASE_PLAYER_AXE, DEFENSE_BASE_PLAYER_SWORD]
        self.defense_base_index = 0
        self.selected_defense_base = self.defense_bases[self.defense_base_index]

        # timers 
        self.timers = {
            TOOL_USE_TIMER : Timer(TIME_FOR_TOOL, self.use_tool),
            TOOL_SWITCH_TIMER : Timer(TIME_FOR_TOOL_SWITCH),

            DEFENSE_BASE_USE_TIMER : Timer(TIME_FOR_DEFENSE_BASE, self.use_defense_base),
            DEFENSE_BASE_SWITCH_TIMER : Timer(TIME_FOR_DEFENSE_BASE_SWITCH),
        }


    def import_assets(self):
        self.animations = { ANIM_PLAYER_UP:[], ANIM_PLAYER_DOWN:[], ANIM_PLAYER_LEFT:[], ANIM_PLAYER_RIGHT:[],
                            ANIM_PLAYER_UP_IDLE:[], ANIM_PLAYER_DOWN_IDLE:[], ANIM_PLAYER_LEFT_IDLE:[], ANIM_PLAYER_RIGHT_IDLE:[],
                            ANIM_PLAYER_UP_AXE:[], ANIM_PLAYER_DOWN_AXE:[], ANIM_PLAYER_LEFT_AXE:[], ANIM_PLAYER_RIGHT_AXE:[],
                            ANIM_PLAYER_UP_SWORD:[], ANIM_PLAYER_DOWN_SWORD:[], ANIM_PLAYER_LEFT_SWORD:[], ANIM_PLAYER_RIGHT_SWORD:[]}

        for animation in self.animations.keys():
            full_path = ASSET_PATH_PLAYER + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        # keybroad button input
        keys = pygame.key.get_pressed()

        if not self.timers[TOOL_USE_TIMER].active:
            # direction
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = ANIM_PLAYER_UP
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = ANIM_PLAYER_DOWN
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = ANIM_PLAYER_RIGHT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = ANIM_PLAYER_LEFT
            else:
                self.direction.x = 0

        # use tool
        if keys[pygame.K_SPACE]:
            # timer for use tool
            self.timers[TOOL_USE_TIMER].activate()
            self.direction = pygame.math.Vector2()
            self.frame_index = 0

        # change tool
        if keys[pygame.K_q] and not self.timers[TOOL_SWITCH_TIMER].active:
            self.timers[TOOL_SWITCH_TIMER].activate()
            self.tool_index += 1
            self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
            self.selected_tool = self.tools[self.tool_index]

        # use defense base
        if keys[pygame.K_LCTRL]:
            # timer for use defense base
            self.timers[DEFENSE_BASE_USE_TIMER].activate()
            self.direction = pygame.math.Vector2()
            self.frame_index = 0

        # change defense base
        if keys[pygame.K_e] and not self.timers[DEFENSE_BASE_SWITCH_TIMER].active:
            self.timers[DEFENSE_BASE_SWITCH_TIMER].activate()
            self.defense_base_index += 1
            self.defense_base_index = self.defense_base_index if self.defense_base_index < len(self.defense_bases) else 0
            self.selected_defense_base = self.defense_bases[self.defense_base_index]

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # use tool
        if self.timers[TOOL_USE_TIMER].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def use_tool(self):
        print(self.selected_defense_base)

    def use_defense_base(self):
        print(self.selected_tool)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)