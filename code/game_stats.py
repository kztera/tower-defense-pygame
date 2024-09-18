# movement
MOVEMENT_SPEED_PLAYER = 400

# player tool
PLAYER_AXE = "player-pickaxe-t2"
PLAYER_SPEAR = "player-spear-t2"

# tool
TOOL_AXE = "pickaxe-t2"
TOOL_SPEAR = "spear-t2"

TOOL_USE_TIMER = "tool use"
TOOL_SWITCH_TIMER = "tool switch"

TIME_FOR_TOOL = 350
TIME_FOR_TOOL_SWITCH = 200

ANGLE_OF_TOOL_USE = 120

# entities
ENTITIES_ARROW_TOWER = "entities-arrow-tower"
ENTITIES_BOMB_TOWER = "entities-bomb-tower"
ENTITIES_CANNON_TOWER = "entities-cannon-tower"
ENTITIES_MAGE_TOWER = "entities-mage-tower"
ENTITIES_GOLD_MINE = "entities-gold-mine"
ENTITIES_GOLD_STASH = "entities-gold-stash"
ENTITIES_WALL = "entities-wall"
ENTITIES_DOOR = "entities-door"

ENTITY_USE_TIMER = "entity use"
ENTITY_SWITCH_TIMER = "entity switch"

TIME_FOR_ENTITY = 350
TIME_FOR_ENTITY_SWITCH = 200

ENTITY_TYPE_ATTACK = "attack"
ENTITY_TYPE_DEFENSE = "defense"
ENTITY_TYPE_PRODUCE = "produce"
ENTITY_TYPE_BRAIN = "brain"

# inventory
ITEM_WOOD = "wood"
ITEM_STONE = "stone"
ITEM_GOLD = "gold"
ITEM_TOKEN = "token"

# font
FONT_TEXT = "SVN-New Athletic M54"
FONT_LUCKIEST_GUY = "LuckiestGuy-Regular"

#
HEALTH_BAR_WIDTH = 45
HEALTH_BAR_HEIGHT = 5

# zombie
ZOMBIE_BLUE = "zombie-blue"
ZOMBIE_GREEN = "zombie-green"
ZOMBIE_ORANGE = "zombie-orange"
ZOMBIE_PURPLE = "zombie-purple"
ZOMBIE_RED = "zombie-red"
ZOMBIE_YELLOW = "zombie-yellow"
ZOMBIE_BOSS = "zombie-boss"

ZOMBIE_ARRAYS = {
    ZOMBIE_BLUE,
    ZOMBIE_GREEN,
    ZOMBIE_ORANGE,
    ZOMBIE_PURPLE,
    ZOMBIE_RED,
    ZOMBIE_YELLOW,
    ZOMBIE_BOSS,
}


"""
# Description: This file contains the configuration for all the towers in the game.

GOLDCOSTS: Vàng để mua tháp/nâng cấp
WOODCOSTS: Gỗ để mua tháp/nâng cấp
STONECOSTS: Đá để mua tháp/nâng cấp
TOKENCOSTS: Token để mua tháp/nâng cấp
HEALTH: Máu của tháp
MSBEFOREREGEN: Thời gian chờ để tháp bắt đầu hồi máu sau khi bị tấn công (ms = milliseconds)
HEALTHREGENPERSECOND: Máu hồi mỗi giây
TOWERRADIUS: Bán kính của tháp
MSBETWEENFIRES: Thời gian giữa các lần bắn của tháp (ms)
DAMAGETOZOMBIES: Sát thương của tháp đối với zombie
DAMAGETOPLAYERS: Sát thương của tháp đối với người chơi
DAMAGETONEUTRALS: Sát thương của tháp đối với neutral
PROJECTILELIFETIME: Thời gian tồn tại của đạn (ms)
PROJECTILEVELOCITY: Vận tốc của đạn
PROJECTILENAME: Tên của đạn
PROJECTILEAOE: Đạn có gây sát thương cho nhiều mục tiêu không
PROJECTILEAOERADIUS: Bán kính của đạn
PROJECTILECOLLISIONRADIUS: Bán kính va chạm của đạn
PROJECTILECOUNT: Số lượng đạn mỗi lần bắn
PROJECTILEIGNORESCOLLISIONS: Đạn có bỏ qua va chạm không
PROJECTILEMAXRANGE: Khoảng cách tối đa mà đạn có thể đi được
"""
