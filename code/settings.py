from pygame.math import Vector2
import pygame

# screen
SCREEN_WIDTH_DEFAULT = 1280
SCREEN_HEIGHT_DEFAULT = 720
TILE_SIZE = 48

# overlay
OVERLAY_TOOL = "tool"
OVERLAY_ENTITY = "entity"

OVERLAY_TOOL_DISTANCE = 75
OVERLAY_ENTITY_DISTANCE = 75

PLAYER_TOOL_OFFSET = {
    "left": Vector2(-50, 40),
    "right": Vector2(50, 40),
    "up": Vector2(0, -10),
    "down": Vector2(0, 50),
}

LAYER_GROUND = "Ground"
LAYER_TOOL = "Tool"
LAYER_MAIN = "Main"
LAYER_STONE = "Stones"
LAYER_TREE = "Trees"

LAYERS = {
    LAYER_GROUND: 0,
    LAYER_STONE: 1,
    LAYER_TREE: 2,
    LAYER_TOOL: 3,
    LAYER_MAIN: 4,
}
