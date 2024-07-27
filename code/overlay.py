import pygame

from settings import *
from asset_path import ASSET_PATH_OVERLAYS, ASSET_PATH_DEFENSE_BASES


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # import asset
        self.tools_surf = {
            tool: pygame.image.load(ASSET_PATH_OVERLAYS + f"{tool}.png").convert_alpha()
            for tool in player.tools
        }

        self.defense_bases_surf = {
            defense_base: pygame.image.load(
                ASSET_PATH_DEFENSE_BASES + f"{defense_base}.png"
            ).convert_alpha()
            for defense_base in player.defense_bases
        }

    def display(self):
        # tool
        i = 0
        for tool in self.player.tools:
            tool_surf = self.tools_surf[tool]
            tool_rect = tool_surf.get_rect(center=OVERLAY_POSITIONS[OVERLAY_TOOL])
            tool_rect.centerx += OVERLAY_TOOL_DISTANCE * i
            self.display_surface.blit(tool_surf, tool_rect)
            i += 1

        # defense base

        k = 0
        index = len(self.player.defense_bases) - 1
        for defense_base in self.player.defense_bases:
            defense_base_surf = self.defense_bases_surf[
                self.player.defense_bases[index]
            ]
            defense_base_rect = defense_base_surf.get_rect(
                center=OVERLAY_POSITIONS[OVERLAY_DEFENSE_BASE]
            )
            defense_base_rect.centerx -= OVERLAY_DEFENSE_BASE_DISTANCE * k

            boder = pygame.Surface((60, 60))
            boder.fill("pink")
            boder_rect = boder.get_rect(center=OVERLAY_POSITIONS[OVERLAY_DEFENSE_BASE])
            boder_rect.centerx -= OVERLAY_DEFENSE_BASE_DISTANCE * k

            self.display_surface.blit(boder, boder_rect)
            self.display_surface.blit(defense_base_surf, defense_base_rect)

            k += 1
            index -= 1
