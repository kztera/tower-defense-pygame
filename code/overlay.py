import pygame

from settings import *
from asset_path import ASSET_PATH_UI_TOOLS, ASSET_PATH_UI_ENTITIES


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # import asset
        self.tools_surf = {
            tool: pygame.image.load(ASSET_PATH_UI_TOOLS + f"{tool}.png").convert_alpha()
            for tool in player.tools
        }

        self.entities_surf = {
            entity: pygame.image.load(
                ASSET_PATH_UI_ENTITIES + f"{entity}.png"
            ).convert_alpha()
            for entity in player.entities
        }

    def display(self):
        # tool

        total = len(self.player.entities)
        count = int(total / 2)
        first_position = 0
        if total % 2 == 0:
            first_position += (
                count - 1
            ) * OVERLAY_ENTITY_DISTANCE + OVERLAY_ENTITY_DISTANCE
        else:
            first_position += count * OVERLAY_ENTITY_DISTANCE

        i = 0
        font = pygame.font.Font(None, 12)

        for entity in self.player.entities:
            entity_surf = self.entities_surf[entity]
            entity_rect = entity_surf.get_rect(center=OVERLAY_POSITIONS[OVERLAY_ENTITY])
            entity_rect.centerx -= first_position
            entity_rect.centerx += OVERLAY_ENTITY_DISTANCE * i

            outline = pygame.Surface((62, 62), pygame.SRCALPHA)
            pygame.draw.rect(
                outline, (79, 79, 79, 128), outline.get_rect(), border_radius=3
            )
            outline_rect = outline.get_rect(center=OVERLAY_POSITIONS[OVERLAY_ENTITY])
            outline_rect.centerx -= first_position
            outline_rect.centerx += OVERLAY_ENTITY_DISTANCE * i

            number_text = font.render(str(i + 1), True, (255, 255, 255))
            number_offset = 5

            self.display_surface.blit(outline, outline_rect)
            self.display_surface.blit(entity_surf, entity_rect)
            self.display_surface.blit(
                number_text,
                (outline_rect.left + number_offset, outline_rect.top + number_offset),
            )

            if entity != self.player.selected_entity:
                matte = pygame.Surface((62, 62), pygame.SRCALPHA)
                pygame.draw.rect(
                    matte, (181, 181, 181, 64), matte.get_rect(), border_radius=3
                )
                matte_rect = matte.get_rect(center=OVERLAY_POSITIONS[OVERLAY_ENTITY])
                matte_rect.centerx -= first_position
                matte_rect.centerx += OVERLAY_ENTITY_DISTANCE * i
                self.display_surface.blit(matte, matte_rect)

            i += 1
