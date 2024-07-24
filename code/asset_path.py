import os

# Lấy đường dẫn tới thư mục chính
ROOT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# Player
ASSET_PATH_PLAYER = os.path.join(ROOT_FOLDER_PATH, "../graphics/player/")

ANIM_PLAYER_UP = 'up'
ANIM_PLAYER_DOWN = 'down'
ANIM_PLAYER_LEFT = 'left'
ANIM_PLAYER_RIGHT = 'right'

ANIM_PLAYER_UP_IDLE = 'up_idle'
ANIM_PLAYER_DOWN_IDLE = 'down_idle'
ANIM_PLAYER_LEFT_IDLE = 'left_idle'
ANIM_PLAYER_RIGHT_IDLE = 'right_idle'

ANIM_PLAYER_UP_AXE = 'up_axe'
ANIM_PLAYER_DOWN_AXE = 'down_axe'
ANIM_PLAYER_LEFT_AXE = 'left_axe'
ANIM_PLAYER_RIGHT_AXE = 'right_axe'

ANIM_PLAYER_UP_ATTACK = 'up_attack'
ANIM_PLAYER_DOWN_ATTACK = 'down_attack'
ANIM_PLAYER_LEFT_ATTACK = 'left_attack'
ANIM_PLAYER_RIGHT_ATTACK = 'right_attack'
