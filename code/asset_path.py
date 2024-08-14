import os

# Lấy đường dẫn tới thư mục chính
ROOT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# asset path : player body
ASSET_PATH_PLAYER = os.path.join(ROOT_FOLDER_PATH, "../graphics/character/body/")

# asset path : player tool
ASSET_PATH_PLAYER_TOOLS = os.path.join(
    ROOT_FOLDER_PATH, "../graphics/character/body/player-"
)

# asset path : ui tool
ASSET_PATH_UI_TOOLS = os.path.join(ROOT_FOLDER_PATH, "../graphics/ui/tools/")

# asset path : ui entities
ASSET_PATH_UI_ENTITIES = os.path.join(ROOT_FOLDER_PATH, "../graphics/ui/entities/")

# asset path : ground
ASSET_PATH_GROUND = os.path.join(ROOT_FOLDER_PATH, "../graphics/world/ground.png")

# asset path : map
ASSET_PATH_MAP = os.path.join(ROOT_FOLDER_PATH, "../data/map/map.tmx")

# asset path : font
ASSET_PATH_FONT = os.path.join(ROOT_FOLDER_PATH, "../font/")

# asset path : entities
ASSET_PATH_ENTITIES = os.path.join(ROOT_FOLDER_PATH, "../graphics/entities/")

# asset path : zombie
ASSET_PATH_ZOMBIES = os.path.join(
    ROOT_FOLDER_PATH, "../graphics/zombies/zombie-boss.png"
)

ASSET_MUSIC_DAY = os.path.join(ROOT_FOLDER_PATH, "../audio/day/")

ASSET_MUSIC_NIGHT = os.path.join(ROOT_FOLDER_PATH, "../audio/night/")
