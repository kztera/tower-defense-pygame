from pygame.math import Vector2

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# overlay
OVERLAY_TOOL = "tool"
OVERLAY_DEFENSE_BASE = "defense base"

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

# layer
LAYER_WATER = "water"
LAYER_GROUND = "ground"
LAYER_SOIL = "soil"
LAYER_SOIL_WATER = "soil water"
LAYER_RAIN_FLOOR = "rain floor"
LAYER_HOUSE_BOTTOM = "house bottom"
LAYER_GROUND_PLANT = "ground plant"
LAYER_MAIN = "main"
LAYER_HOUSE_TOP = "house top"
LAYER_FRUIT = "fruit"
LAYER_RAIN_DROPS = "rain drops"

LAYERS = {
    LAYER_WATER: 0,
    LAYER_GROUND: 1,
    LAYER_SOIL: 2,
    LAYER_SOIL_WATER: 3,
    LAYER_RAIN_FLOOR: 4,
    LAYER_HOUSE_BOTTOM: 5,
    LAYER_GROUND_PLANT: 6,
    LAYER_MAIN: 7,
    LAYER_HOUSE_TOP: 8,
    LAYER_FRUIT: 9,
    LAYER_RAIN_DROPS: 10,
}

APPLE_POS = {
    "Small": [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    "Large": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
}

GROW_SPEED = {"corn": 1, "tomato": 0.7}

SALE_PRICES = {"wood": 4, "apple": 2, "corn": 10, "tomato": 20}

PURCHASE_PRICES = {"corn": 4, "tomato": 5}
