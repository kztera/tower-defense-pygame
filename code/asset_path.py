import os

# Lấy đường dẫn tới thư mục chính
ROOT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# asset path : player body
ASSET_PATH_PLAYER = os.path.join(ROOT_FOLDER_PATH, "../graphics/character/body/player-base.png")

# asset path : player tool
ASSET_PATH_PLAYER_TOOLS = os.path.join(ROOT_FOLDER_PATH, "../graphics/character/tools/player-")

# asset path : ui tool
ASSET_PATH_UI_TOOLS = os.path.join(ROOT_FOLDER_PATH, "../graphics/ui/tools/")

# asset path : overlay
ASSET_PATH_UI_ENTITIES = os.path.join(ROOT_FOLDER_PATH, "../graphics/ui/entities/")

# asset path : ground
ASSET_PATH_GROUND = os.path.join(ROOT_FOLDER_PATH, "../graphics/world/ground.png")

# asset path : map
ASSET_PATH_MAP = os.path.join(ROOT_FOLDER_PATH, "../data/map/map.tmx")
