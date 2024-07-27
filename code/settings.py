from pygame.math import Vector2
import pygame

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 48

# overlay
OVERLAY_TOOL = "tool"
OVERLAY_DEFENSE_BASE = "tower"

OVERLAY_TOOL_DISTANCE = 50
OVERLAY_DEFENSE_BASE_DISTANCE = 70

OVERLAY_POSITIONS = {
    OVERLAY_TOOL: (70, SCREEN_HEIGHT - 70),
    OVERLAY_DEFENSE_BASE: (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 70),
}


PLAYER_TOOL_OFFSET = {
    "left": Vector2(-50, 40),
    "right": Vector2(50, 40),
    "up": Vector2(0, -10),
    "down": Vector2(0, 50),
}

LAYER_GROUND = "ground"
LAYER_MAIN = "main"
LAYER_STONE = "stone"
LAYER_TREE = "tree"

LAYERS = {
    LAYER_GROUND: 0,
    LAYER_MAIN: 1,
    LAYER_STONE: 2,
    LAYER_TREE: 3,
}
