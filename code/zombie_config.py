"""
Zombie Configuration
--------------------
Each zombie has the following attributes:
- MODEL: Tên zombie.
- AMOUNT: Số lượng xuất hiện trong mỗi wave.
- HEALTH: Máu của zombie.
- FIRERATE: Tốc độ tấn công của zombie.
- SPEED: Tốc độ di chuyển của zombie.
- RADIUS: Bán kính (hitbox) của zombie.
- WAVES: Các wave mà zombie xuất hiện.
- DEALS: Điểm số mà người chơi nhận được khi tiêu diệt zombie.
"""

ZOMBIE_CONFIG = [
    {
        "MODEL": "ZombieGreenTier1",
        "AMOUNT": 10,
        "HEALTH": 110,
        "FIRERATE": 785,
        "SPEED": 10,
        "RADIUS": 15,
        "WAVES": "1-5",
        "DEALS": 10,
    },
    {
        "MODEL": "ZombieGreenTier2",
        "AMOUNT": 15,
        "HEALTH": 130,
        "FIRERATE": 780,
        "SPEED": 9,
        "RADIUS": 16,
        "WAVES": "4-8",
        "DEALS": 13,
    },
    {
        "MODEL": "ZombieGreenTier3",
        "AMOUNT": 25,
        "HEALTH": 150,
        "FIRERATE": 775,
        "SPEED": 8,
        "RADIUS": 18,
        "WAVES": "6-10",
        "DEALS": 15,
    },
    {
        "MODEL": "ZombieGreenTier4",
        "AMOUNT": 30,
        "HEALTH": 165,
        "FIRERATE": 760,
        "SPEED": 7,
        "RADIUS": 20,
        "WAVES": "10-13",
        "DEALS": 20,
    },
    {
        "MODEL": "ZombieGreenTier5",
        "AMOUNT": 34,
        "HEALTH": 176.5,
        "FIRERATE": 747,
        "SPEED": 6,
        "RADIUS": 23,
        "WAVES": "12-14",
        "DEALS": 23,
    },
    {
        "MODEL": "ZombieGreenTier6",
        "AMOUNT": 25,
        "HEALTH": 182.3,
        "FIRERATE": 738,
        "SPEED": 5,
        "RADIUS": 27,
        "WAVES": "13-16",
        "DEALS": 25,
    },
    {
        "MODEL": "ZombieGreenTier7",
        "AMOUNT": 26,
        "HEALTH": 192,
        "FIRERATE": 700,
        "SPEED": 4,
        "RADIUS": 30,
        "WAVES": "14-17",
        "DEALS": 28,
    },
    {
        "MODEL": "ZombieGreenTier8",
        "AMOUNT": 26,
        "HEALTH": 200,
        "FIRERATE": 682,
        "SPEED": 3.4,
        "RADIUS": 33,
        "WAVES": "16-18",
        "DEALS": 33,
    },
    {
        "MODEL": "ZombieGreenTier9",
        "AMOUNT": 21,
        "HEALTH": 212,
        "FIRERATE": 666,
        "SPEED": 3.01,
        "RADIUS": 35,
        "WAVES": "17-20",
        "DEALS": 36,
    },
    {
        "MODEL": "ZombieBlueTier1",
        "AMOUNT": 26,
        "HEALTH": 780,
        "FIRERATE": 589,
        "SPEED": 6,
        "RADIUS": 15,
        "WAVES": "17-19",
        "DEALS": 47,
    },
    {
        "MODEL": "ZombieBlueTier2",
        "AMOUNT": 31,
        "HEALTH": 860,
        "FIRERATE": 632,
        "SPEED": 5.2,
        "RADIUS": 16,
        "WAVES": "20-24",
        "DEALS": 67,
    },
    {
        "MODEL": "ZombieBlueTier3",
        "AMOUNT": 34,
        "HEALTH": 998,
        "FIRERATE": 678,
        "SPEED": 4.8,
        "RADIUS": 19,
        "WAVES": "23-28",
        "DEALS": 78,
    },
    {
        "MODEL": "ZombieBlueTier4",
        "AMOUNT": 34,
        "HEALTH": 1024,
        "FIRERATE": 723,
        "SPEED": 4.1,
        "RADIUS": 21,
        "WAVES": "26-32",
        "DEALS": 102,
    },
    {
        "MODEL": "ZombieBlueTier5",
        "AMOUNT": 37,
        "HEALTH": 1203,
        "FIRERATE": 748,
        "SPEED": 3.8,
        "RADIUS": 23,
        "WAVES": "30-38",
        "DEALS": 124,
    },
    {
        "MODEL": "ZombieBlueTier6",
        "AMOUNT": 29,
        "HEALTH": 1561,
        "FIRERATE": 732,
        "SPEED": 3.1,
        "RADIUS": 26,
        "WAVES": "33-39",
        "DEALS": 157,
    },
    {
        "MODEL": "ZombieBlueTier7",
        "AMOUNT": 32,
        "HEALTH": 1784,
        "FIRERATE": 723,
        "SPEED": 2.3,
        "RADIUS": 29,
        "WAVES": "35-39",
        "DEALS": 184,
    },
    {
        "MODEL": "ZombieBlueTier8",
        "AMOUNT": 34,
        "HEALTH": 1889,
        "FIRERATE": 711,
        "SPEED": 2,
        "RADIUS": 32,
        "WAVES": "37-39",
        "DEALS": 201,
    },
    {
        "MODEL": "ZombieBlueTier9",
        "AMOUNT": 37,
        "HEALTH": 2000,
        "FIRERATE": 666,
        "SPEED": 2.7,
        "RADIUS": 35,
        "WAVES": "38-40",
        "DEALS": 222,
    },
    {
        "MODEL": "ZombieRedTier1",
        "AMOUNT": 10,
        "HEALTH": 2374,
        "FIRERATE": 600,
        "SPEED": 6.9,
        "RADIUS": 15,
        "WAVES": "39-42",
        "DEALS": 250,
    },
    {
        "MODEL": "ZombieRedTier2",
        "AMOUNT": 15,
        "HEALTH": 2547,
        "FIRERATE": 666,
        "SPEED": 6.1,
        "RADIUS": 16,
        "WAVES": "40-43",
        "DEALS": 270,
    },
    {
        "MODEL": "ZombieRedTier3",
        "AMOUNT": 25,
        "HEALTH": 2777,
        "FIRERATE": 702,
        "SPEED": 5.7,
        "RADIUS": 18,
        "WAVES": "43-47",
        "DEALS": 286,
    },
    {
        "MODEL": "ZombieRedTier4",
        "AMOUNT": 30,
        "HEALTH": 3000,
        "FIRERATE": 723,
        "SPEED": 5,
        "RADIUS": 20,
        "WAVES": "44-51",
        "DEALS": 302,
    },
    {
        "MODEL": "ZombieRedTier5",
        "AMOUNT": 33,
        "HEALTH": 3467,
        "FIRERATE": 748,
        "SPEED": 4.2,
        "RADIUS": 23,
        "WAVES": "48-53",
        "DEALS": 336,
    },
    {
        "MODEL": "ZombieRedTier6",
        "AMOUNT": 35,
        "HEALTH": 3774,
        "FIRERATE": 722,
        "SPEED": 3.7,
        "RADIUS": 27,
        "WAVES": "52-54",
        "DEALS": 359,
    },
    {
        "MODEL": "ZombieRedTier7",
        "AMOUNT": 37,
        "HEALTH": 4076,
        "FIRERATE": 699,
        "SPEED": 3.1,
        "RADIUS": 30,
        "WAVES": "54-56",
        "DEALS": 382,
    },
    {
        "MODEL": "ZombieRedTier8",
        "AMOUNT": 32,
        "HEALTH": 4588,
        "FIRERATE": 702,
        "SPEED": 2.6,
        "RADIUS": 32,
        "WAVES": "55-57",
        "DEALS": 408,
    },
    {
        "MODEL": "ZombieRedTier9",
        "AMOUNT": 40,
        "HEALTH": 5000,
        "FIRERATE": 676,
        "SPEED": 3.2,
        "RADIUS": 35,
        "WAVES": "57-58",
        "DEALS": 426,
    },
    {
        "MODEL": "ZombieYellowTier1",
        "AMOUNT": 16,
        "HEALTH": 5300,
        "FIRERATE": 666,
        "SPEED": 6.01,
        "RADIUS": 15,
        "WAVES": "58-62",
        "DEALS": 466,
    },
    {
        "MODEL": "ZombieYellowTier2",
        "AMOUNT": 26,
        "HEALTH": 5680,
        "FIRERATE": 688,
        "SPEED": 5.7,
        "RADIUS": 16,
        "WAVES": "63-67",
        "DEALS": 500,
    },
    {
        "MODEL": "ZombieYellowTier3",
        "AMOUNT": 30,
        "HEALTH": 5969,
        "FIRERATE": 702,
        "SPEED": 5,
        "RADIUS": 18,
        "WAVES": "68-73",
        "DEALS": 540,
    },
    {
        "MODEL": "ZombieYellowTier4",
        "AMOUNT": 36,
        "HEALTH": 6500,
        "FIRERATE": 723,
        "SPEED": 4.3,
        "RADIUS": 20,
        "WAVES": "71-79",
        "DEALS": 589,
    },
    {
        "MODEL": "ZombieYellowTier5",
        "AMOUNT": 55,
        "HEALTH": 6969,
        "FIRERATE": 666,
        "SPEED": 4.20,
        "RADIUS": 23,
        "WAVES": "77-83",
        "DEALS": 600,
    },
    {
        "MODEL": "ZombieYellowTier6",
        "AMOUNT": 35,
        "HEALTH": 7100,
        "FIRERATE": 711,
        "SPEED": 3.9,
        "RADIUS": 27,
        "WAVES": "80-86",
        "DEALS": 641,
    },
    {
        "MODEL": "ZombieYellowTier7",
        "AMOUNT": 32,
        "HEALTH": 7777,
        "FIRERATE": 699,
        "SPEED": 3.2,
        "RADIUS": 30,
        "WAVES": "84-89",
        "DEALS": 678,
    },
    {
        "MODEL": "ZombieYellowTier8",
        "AMOUNT": 30,
        "HEALTH": 8008,
        "FIRERATE": 702,
        "SPEED": 2.8,
        "RADIUS": 32,
        "WAVES": "87-93",
        "DEALS": 702,
    },
    {
        "MODEL": "ZombieYellowTier9",
        "AMOUNT": 39,
        "HEALTH": 8800,
        "FIRERATE": 676,
        "SPEED": 3.2,
        "RADIUS": 35,
        "WAVES": "90-94",
        "DEALS": 739,
    },
    {
        "MODEL": "ZombiePurpleTier1",
        "AMOUNT": 17,
        "HEALTH": 9000,
        "FIRERATE": 660,
        "SPEED": 6,
        "RADIUS": 15,
        "WAVES": "94-97",
        "DEALS": 800,
    },
    {
        "MODEL": "ZombiePurpleTier2",
        "AMOUNT": 30,
        "HEALTH": 9600,
        "FIRERATE": 690,
        "SPEED": 5.3,
        "RADIUS": 17,
        "WAVES": "98-103",
        "DEALS": 850,
    },
    {
        "MODEL": "ZombiePurpleTier3",
        "AMOUNT": 40,
        "HEALTH": 10000,
        "FIRERATE": 702,
        "SPEED": 5,
        "RADIUS": 19,
        "WAVES": "104-111",
        "DEALS": 901,
    },
    {
        "MODEL": "ZombiePurpleTier4",
        "AMOUNT": 22,
        "HEALTH": 10800,
        "FIRERATE": 723,
        "SPEED": 4.3,
        "RADIUS": 20,
        "WAVES": "108-113",
        "DEALS": 947,
    },
    {
        "MODEL": "ZombiePurpleTier5",
        "AMOUNT": 23,
        "HEALTH": 11000,
        "FIRERATE": 666,
        "SPEED": 4.20,
        "RADIUS": 23,
        "WAVES": "112-115",
        "DEALS": 969,
    },
    {
        "MODEL": "ZombiePurpleTier6",
        "AMOUNT": 30,
        "HEALTH": 11467,
        "FIRERATE": 713,
        "SPEED": 3.9,
        "RADIUS": 25,
        "WAVES": "114-117",
        "DEALS": 999,
    },
    {
        "MODEL": "ZombiePurpleTier7",
        "AMOUNT": 28,
        "HEALTH": 11789,
        "FIRERATE": 699,
        "SPEED": 3.2,
        "RADIUS": 27,
        "WAVES": "116-119",
        "DEALS": 1087,
    },
    {
        "MODEL": "ZombiePurpleTier8",
        "AMOUNT": 23,
        "HEALTH": 12345,
        "FIRERATE": 681,
        "SPEED": 2.8,
        "RADIUS": 30,
        "WAVES": "118-121",
        "DEALS": 1100,
    },
    {
        "MODEL": "ZombiePurpleTier9",
        "AMOUNT": 28,
        "HEALTH": 12578,
        "FIRERATE": 676,
        "SPEED": 3.3,
        "RADIUS": 33,
        "WAVES": "120-122",
        "DEALS": 1134,
    },
    {
        "MODEL": "ZombieOrangeTier1",
        "AMOUNT": 30,
        "HEALTH": 13000,
        "FIRERATE": 660,
        "SPEED": 5.8,
        "RADIUS": 16,
        "WAVES": "121-123",
        "DEALS": 1100,
    },
    {
        "MODEL": "ZombieOrangeTier2",
        "AMOUNT": 24,
        "HEALTH": 14000,
        "FIRERATE": 690,
        "SPEED": 5.3,
        "RADIUS": 20,
        "WAVES": "124-127",
        "DEALS": 1200,
    },
    {
        "MODEL": "ZombieOrangeTier3",
        "AMOUNT": 30,
        "HEALTH": 15000,
        "FIRERATE": 702,
        "SPEED": 5,
        "RADIUS": 24,
        "WAVES": "128-130",
        "DEALS": 1299,
    },
    {
        "MODEL": "ZombieOrangeTier4",
        "AMOUNT": 22,
        "HEALTH": 15800,
        "FIRERATE": 723,
        "SPEED": 4.3,
        "RADIUS": 27,
        "WAVES": "131-134",
        "DEALS": 1398,
    },
    {
        "MODEL": "ZombieOrangeTier5",
        "AMOUNT": 23,
        "HEALTH": 16400,
        "FIRERATE": 666,
        "SPEED": 4.20,
        "RADIUS": 29,
        "WAVES": "135-139",
        "DEALS": 1400,
    },
    {
        "MODEL": "ZombieOrangeTier6",
        "AMOUNT": 25,
        "HEALTH": 17067,
        "FIRERATE": 713,
        "SPEED": 3.9,
        "RADIUS": 31,
        "WAVES": "140-144",
        "DEALS": 1456,
    },
    {
        "MODEL": "ZombieOrangeTier7",
        "AMOUNT": 24,
        "HEALTH": 17789,
        "FIRERATE": 699,
        "SPEED": 3.2,
        "RADIUS": 33,
        "WAVES": "145-149",
        "DEALS": 1502,
    },
    {
        "MODEL": "ZombieOrangeTier8",
        "AMOUNT": 40,
        "HEALTH": 18000,
        "FIRERATE": 681,
        "SPEED": 2.8,
        "RADIUS": 35,
        "WAVES": "150-",
        "DEALS": 1600,
    },
    {
        "MODEL": "ZombieOrangeTier9",
        "AMOUNT": 45,
        "HEALTH": 20000,
        "FIRERATE": 676,
        "SPEED": 3.3,
        "RADIUS": 37,
        "WAVES": "153-",
        "DEALS": 1800,
    },
]