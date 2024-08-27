# Description: This file contains the configuration for all the towers in the game.
"""
GOLDCOSTS: Vàng để mua tháp/nâng cấp
WOODCOSTS: Gỗ để mua tháp/nâng cấp
STONECOSTS: Đá để mua tháp/nâng cấp
TOKENCOSTS: Token để mua tháp/nâng cấp
HEALTH: Máu của tháp
TOWERRADIUS: Bán kính của tháp
MSBETWEENFIRES: Thời gian giữa các lần bắn của tháp (ms)
DAMAGETOZOMBIES: Sát thương của tháp đối với zombie
GOLDPERSECOND: gold nhận được mỗi giây
PROJECTILENAME: Tên của đạn
PROJECTILEVELOCITY: Vận tốc của đạn
PROJECTILELIFETIME: Thời gian tồn tại của đạn (ms)

MSBEFOREREGEN: Thời gian chờ để tháp bắt đầu hồi máu sau khi bị tấn công (ms = milliseconds)
HEALTHREGENPERSECOND: Máu hồi mỗi giây

DAMAGETOPLAYERS: Sát thương của tháp đối với người chơi
DAMAGETONEUTRALS: Sát thương của tháp đối với neutral
PROJECTILEAOE: Đạn có gây sát thương cho nhiều mục tiêu không
PROJECTILEAOERADIUS: Bán kính của đạn
PROJECTILECOLLISIONRADIUS: Bán kính va chạm của đạn
PROJECTILECOUNT: Số lượng đạn mỗi lần bắn
PROJECTILEIGNORESCOLLISIONS: Đạn có bỏ qua va chạm không
PROJECTILEMAXRANGE: Khoảng cách tối đa mà đạn có thể đi được
"""

TOWER_CONFIG = [
    {
        "NAME": "WALL",
        "CLASS": "WALL",
        "GOLDCOSTS": [0, 5, 30, 60, 80, 100, 250, 800, 1000],
        "WOODCOSTS": [2, 0, 0, 0, 0, 0, 0, 0, 0],
        "STONECOSTS": [0, 2, 0, 0, 0, 0, 0, 0, 0],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "HEALTH": [150, 200, 300, 400, 600, 800, 1500, 2500, 5000],
        "MSBEFOREREGEN": [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 1000],
        "HEALTHREGENPERSECOND": [5, 7, 12, 17, 25, 40, 80, 250, 500],
    },
    {
        "NAME": "GOLDSTASH",
        "CLASS": "GOLDSTASH",
        "GOLDCOSTS": [0, 5000, 10000, 16000, 20000, 32000, 100000, 400000, 1000000],
        "WOODCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "STONECOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "HEALTH": [1500, 1800, 2300, 3000, 5000, 8000, 12000, 20000, 40000],
        "MSBEFOREREGEN": [
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
        ],
        "HEALTHREGENPERSECOND": [50, 60, 70, 90, 110, 150, 400, 700, 2000],
    },
    {
        "NAME": "GOLDMINE",
        "CLASS": "GOLDMINE",
        "GOLDCOSTS": [0, 200, 300, 600, 800, 1200, 8000, 30000, 80000],
        "WOODCOSTS": [5, 15, 25, 35, 45, 55, 700, 1600, 2000],
        "STONECOSTS": [5, 15, 25, 35, 45, 55, 700, 1600, 2000],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "HEALTH": [150, 250, 350, 500, 800, 1400, 1800, 2800, 4000],
        "GOLDPERSECOND": [4, 6, 7, 10, 12, 15, 25, 35, 60],
        "MSBEFOREREGEN": [
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
        ],
        "HEALTHREGENPERSECOND": [5, 7, 12, 17, 25, 40, 70, 120, 150],
    },
    {
        "NAME": "DOOR",
        "CLASS": "DOOR",
        "GOLDCOSTS": [0, 10, 50, 70, 150, 200, 400, 800, 1000],
        "WOODCOSTS": [5, 5, 0, 0, 0, 0, 0, 0, 0],
        "STONECOSTS": [5, 5, 0, 0, 0, 0, 0, 0, 0],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "HEALTH": [150, 200, 300, 500, 700, 1000, 1500, 2000, 4000],
        "MSBEFOREREGEN": [10000, 10000, 10000, 10000, 10000, 10000, 10000, 1000, 1000],
        "HEALTHREGENPERSECOND": [5, 7, 12, 17, 25, 40, 70, 100, 150],
    },
    {
        "NAME": "CANNONTOWER",
        "CLASS": "TOWER",
        "GOLDCOSTS": [0, 100, 200, 600, 1200, 2000, 8000, 35000, 100000],
        "WOODCOSTS": [15, 25, 30, 40, 60, 80, 300, 800, 2000],
        "STONECOSTS": [15, 25, 40, 50, 80, 120, 300, 800, 2000],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "TOWERRADIUS": [500, 500, 500, 500, 600, 600, 600, 600, 700],
        "MSBETWEENFIRES": [1000, 769, 625, 500, 400, 350, 250, 250, 200],
        "HEALTH": [150, 200, 400, 800, 1200, 1600, 2200, 3600, 5000],
        "MSBEFOREREGEN": [
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
        ],
        "HEALTHREGENPERSECOND": [2, 5, 10, 20, 40, 80, 110, 150, 200],
        "DAMAGETOZOMBIES": [20, 30, 50, 70, 120, 150, 200, 300, 500],
        "DAMAGETOPLAYERS": [5, 5, 5, 5, 5, 5, 6, 8, 8],
        "DAMAGETONEUTRALS": [250, 350, 450, 550, 650, 750, 850, 1000, 2000],
        "PROJECTILELIFETIME": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        "PROJECTILEVELOCITY": [60, 65, 70, 70, 75, 80, 100, 140, 170],
        "PROJECTILENAME": "cannon-tower-projectile",
        "PROJECTILEAOE": [True, True, True, True, True, True, True, True, True],
        "PROJECTILEAOERADIUS": [250, 250, 250, 250, 250, 250, 250, 250, 250],
        "PROJECTILECOLLISIONRADIUS": [10, 10, 10, 10, 10, 10, 10, 10, 10],
        "PROJECTILECOUNT": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    {
        "NAME": "ARROWTOWER",
        "CLASS": "TOWER",
        "GOLDCOSTS": [0, 100, 200, 600, 1200, 2000, 8000, 35000, 100000],
        "WOODCOSTS": [5, 25, 30, 40, 50, 70, 300, 800, 2000],
        "STONECOSTS": [5, 20, 30, 40, 60, 80, 300, 800, 2000],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "TOWERRADIUS": [600, 650, 700, 750, 800, 850, 900, 1000, 2000],
        "MSBETWEENFIRES": [400, 333, 285, 250, 250, 250, 250, 250, 200],
        "HEALTH": [150, 200, 400, 800, 1200, 1600, 2200, 3600, 5000],
        "MSBEFOREREGEN": [
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
        ],
        "HEALTHREGENPERSECOND": [2, 5, 10, 20, 40, 80, 110, 150, 200],
        "DAMAGETOZOMBIES": [20, 40, 70, 120, 180, 250, 400, 500, 700],
        "DAMAGETOPLAYERS": [5, 5, 5, 5, 5, 5, 6, 6, 7],
        "DAMAGETONEUTRALS": [250, 350, 450, 550, 650, 750, 850, 1000, 2000],
        "PROJECTILELIFETIME": [1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300],
        "PROJECTILEVELOCITY": [60, 65, 70, 70, 75, 80, 120, 140, 150],
        "PROJECTILENAME": "arrow-tower-projectile",
        "PROJECTILEAOE": [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
        "PROJECTILECOLLISIONRADIUS": [10, 10, 10, 10, 10, 10, 10, 10, 10],
        "PROJECTILECOUNT": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    {
        "NAME": "BOMBTOWER",
        "CLASS": "TOWER",
        "GOLDCOSTS": [0, 100, 200, 600, 1200, 2000, 8000, 35000, 100000],
        "WOODCOSTS": [10, 25, 40, 50, 80, 120, 300, 800, 2000],
        "STONECOSTS": [10, 25, 40, 50, 80, 120, 300, 800, 2000],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "TOWERRADIUS": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        "MSBETWEENFIRES": [1000, 1000, 1000, 1000, 1000, 1000, 900, 900, 800],
        "HEALTH": [150, 200, 400, 800, 1200, 1600, 2200, 3600, 5000],
        "MSBEFOREREGEN": [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000],
        "HEALTHREGENPERSECOND": [2, 5, 10, 20, 40, 80, 110, 150, 200],
        "DAMAGETOZOMBIES": [30, 60, 100, 140, 200, 600, 1200, 1600, 2000],
        "DAMAGETOPLAYERS": [10, 10, 10, 10, 10, 10, 10, 10, 10],
        "DAMAGETONEUTRALS": [250, 350, 450, 550, 650, 750, 850, 1000, 2000],
        "PROJECTILELIFETIME": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        "PROJECTILEVELOCITY": [20, 20, 20, 20, 20, 20, 20, 20, 20],
        "PROJECTILENAME": "bomb-tower-projectile",
        "PROJECTILEAOE": [True, True, True, True, True, True, True, True, True],
        "PROJECTILEIGNORESCOLLISIONS": [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ],
        "PROJECTILEAOERADIUS": [250, 250, 250, 250, 250, 250, 250, 250, 250],
        "PROJECTILECOLLISIONRADIUS": [10, 10, 10, 10, 10, 10, 10, 10, 10],
        "PROJECTILEMAXRANGE": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        "PROJECTILECOUNT": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    {
        "NAME": "MAGICTOWER",
        "CLASS": "MAGICTOWER",
        "GOLDCOSTS": [0, 100, 200, 600, 1200, 2000, 8000, 35000, 100000],
        "WOODCOSTS": [15, 25, 40, 50, 70, 100, 300, 800, 2000],
        "STONECOSTS": [15, 25, 40, 50, 70, 100, 300, 800, 2000],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "TOWERRADIUS": [400, 400, 400, 400, 400, 400, 400, 400, 400],
        "MSBETWEENFIRES": [800, 800, 700, 600, 500, 400, 300, 300, 200],
        "HEALTH": [150, 200, 400, 800, 1200, 1600, 2200, 3600, 5000],
        "MSBEFOREREGEN": [
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
        ],
        "HEALTHREGENPERSECOND": [2, 5, 10, 20, 40, 80, 110, 150, 200],
        "DAMAGETOZOMBIES": [10, 20, 40, 50, 70, 80, 120, 160, 300],
        "DAMAGETOPLAYERS": [5, 5, 5, 5, 5, 5, 5, 5, 5],
        "DAMAGETONEUTRALS": [250, 350, 450, 550, 650, 750, 850, 1000, 2000],
        "PROJECTILELIFETIME": [500, 500, 500, 500, 500, 500, 500, 500, 500],
        "PROJECTILEVELOCITY": [45, 45, 45, 45, 45, 45, 45, 45, 45],
        "PROJECTILENAME": "magic-tower-projectile",
        "PROJECTILEAOE": [True, True, True, True, True, True, True, True, True],
        "PROJECTILEAOERADIUS": [100, 100, 100, 100, 100, 100, 100, 100, 100],
        "PROJECTILECOLLISIONRADIUS": [10, 10, 10, 10, 10, 10, 10, 10, 10],
        "PROJECTILECOUNT": [3, 3, 3, 3, 3, 3, 3, 3, 3],
    },
    {
        "NAME": "SLOWTRAP",
        "CLASS": "TRAP",
        "GOLDCOSTS": [0, 100, 200, 400, 600, 800, 1000, 1500, 2000],
        "WOODCOSTS": [5, 25, 30, 40, 50, 70, 300, 800, 2000],
        "STONECOSTS": [5, 20, 30, 40, 60, 80, 300, 800, 2000],
        "TOKENCOSTS": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "HEALTH": [150, 200, 400, 800, 1200, 1600, 2200, 3000, 5000],
        "MSBEFOREREGEN": [
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
            10000,
        ],
        "HEALTHREGENPERSECOND": [2, 5, 10, 20, 40, 80, 110, 150, 200],
        "SLOWDURATION": [2500, 2500, 2500, 3000, 3000, 3250, 3500, 4000, 5000],
        "SLOWAMOUNT": [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.7, 1],
    },
]

'''
            FIX 
- Cần sửa lại thời gian bắn của các tháp
- Khoảng cách tấn công của các tháp
'''
