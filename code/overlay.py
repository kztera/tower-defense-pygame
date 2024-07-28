import pygame

from settings import *
from asset_path import ASSET_PATH_UI_TOOLS, ASSET_PATH_UI_ENTITIES


class Overlay:
    def __init__(self, player):
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

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
        self.display_surface = pygame.display.get_surface()
        current_width, current_height = self.display_surface.get_size()

        overlay_positions = {
            OVERLAY_TOOL: (current_width / 2, current_height - 150),
            OVERLAY_ENTITY: (current_width / 2, current_height - 70),
        }

        self._display_items(
            self.player.tools,
            self.tools_surf,
            self.player.selected_tool,
            overlay_positions[OVERLAY_TOOL],
            OVERLAY_TOOL_DISTANCE,
        )
        self._display_items(
            self.player.entities,
            self.entities_surf,
            self.player.selected_entity,
            overlay_positions[OVERLAY_ENTITY],
            OVERLAY_ENTITY_DISTANCE,
            True,
        )

    def _display_items(
        self, items, surfaces, selected_item, position, distance, show_numbers=False
    ):
        total = len(items)
        count = int(total / 2)
        first_position = 0
        if total % 2 == 0:
            first_position += (count - 1) * distance + distance / 2
        else:
            first_position += count * distance

        font = pygame.font.Font(None, 12) if show_numbers else None
        number_offset = 5

        for i, item in enumerate(items):
            item_surf = surfaces[item]
            item_rect = item_surf.get_rect(center=position)
            item_rect.centerx -= first_position
            item_rect.centerx += distance * i

            outline = pygame.Surface((62, 62), pygame.SRCALPHA)
            pygame.draw.rect(
                outline, (79, 79, 79, 128), outline.get_rect(), border_radius=3
            )
            outline_rect = outline.get_rect(center=position)
            outline_rect.centerx -= first_position
            outline_rect.centerx += distance * i

            self.display_surface.blit(outline, outline_rect)
            self.display_surface.blit(item_surf, item_rect)

            if show_numbers:
                number_text = font.render(str(i + 1), True, (255, 255, 255))
                self.display_surface.blit(
                    number_text,
                    (
                        outline_rect.left + number_offset,
                        outline_rect.top + number_offset,
                    ),
                )

            if item != selected_item:
                matte = pygame.Surface((62, 62), pygame.SRCALPHA)
                pygame.draw.rect(
                    matte, (181, 181, 181, 64), matte.get_rect(), border_radius=3
                )
                matte_rect = matte.get_rect(center=position)
                matte_rect.centerx -= first_position
                matte_rect.centerx += distance * i
                self.display_surface.blit(matte, matte_rect)
