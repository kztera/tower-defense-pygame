import pygame

from settings import *
from asset_path import *
from game_stats import *


class Overlay:
    def __init__(self, player, game_data):
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.font_text = pygame.font.Font((ASSET_PATH_FONT + FONT_TEXT + ".ttf"), 16)

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
        # data
        self.game_data = game_data
        self.top_10_data = self.game_data.get_data()

    def display(self):
        self.display_surface = pygame.display.get_surface()
        current_width, current_height = self.display_surface.get_size()

        overlay_positions = {
            OVERLAY_TOOL: (current_width / 2, current_height - 150),
            OVERLAY_ENTITY: (current_width / 2, current_height - 70),
            ITEM_INVENTORY: (current_width - 200, current_height - 200),
            OVERLAY_LEADERBOARD: (current_width / 2, current_height + 100),
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

        self.display_item_inventory(overlay_positions[ITEM_INVENTORY])

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

    def display_item_inventory(self, pos):
        background_width = 150
        background_height = 170
        padding = 10
        item_height = 30
        font_color = (200, 200, 200)
        background_color = (0, 0, 0, 120)
        background = pygame.Surface(
            (background_width, background_height), pygame.SRCALPHA
        )

        pygame.draw.rect(
            background, background_color, background.get_rect(), border_radius=10
        )

        background_rect = background.get_rect(topleft=pos)
        self.display_surface.blit(background, background_rect)

        for i, (item_name, item_value) in enumerate(
            self.player.items_inventory.items()
        ):
            item_text = f"{item_name.upper()}"
            value_text = f"{item_value}"

            item_surf = self.font_text.render(item_text, True, font_color)
            value_surf = self.font_text.render(value_text, True, font_color)

            item_rect = item_surf.get_rect(
                topleft=(pos[0] + padding, pos[1] + padding + i * item_height)
            )
            value_rect = value_surf.get_rect(
                topright=(
                    pos[0] + background_width - padding,
                    pos[1] + padding + i * item_height,
                )
            )

            self.display_surface.blit(item_surf, item_rect)
            self.display_surface.blit(value_surf, value_rect)

        wave_text = "WAVE"
        wave_number = f"{self.player.current_wave}"
        wave_surf = self.font_text.render(wave_text, True, font_color)
        number_surf = self.font_text.render(wave_number, True, font_color)

        wave_rect = wave_surf.get_rect(
            bottomleft=(pos[0] + padding, pos[1] + background_height - padding)
        )
        number_rect = number_surf.get_rect(
            bottomright=(
                pos[0] + background_width - padding,
                pos[1] + background_height - padding,
            )
        )

        self.display_surface.blit(wave_surf, wave_rect)
        self.display_surface.blit(number_surf, number_rect)

        line_y = pos[1] + background_height - item_height - padding // 2
        pygame.draw.line(
            self.display_surface,
            font_color,
            (pos[0], line_y),
            (pos[0] + background_width, line_y),
            1,
        )
