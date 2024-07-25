import pygame
from settings import *
from asset_path import ASSET_PATH_OVERLAYS, ASSET_PATH_DEFENSE_BASES

class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # import asset
        self.tools_surf = {tool:pygame.image.load(ASSET_PATH_OVERLAYS + f'{tool}.png').convert_alpha() for tool in player.tools}
        self.defense_bases_surf = {defense_base:pygame.image.load(ASSET_PATH_DEFENSE_BASES + f'{defense_base}.png').convert_alpha() for defense_base in player.defense_bases}

    def display(self):
        # tool
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # defense base
        defense_base_surf = self.defense_bases_surf[self.player.selected_defense_base]
        defense_base_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['defense base'])
        self.display_surface.blit(defense_base_surf, defense_base_rect)