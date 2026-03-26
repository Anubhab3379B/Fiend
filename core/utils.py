class Room:
    def __init__(self, name, enemies=None):
        self.name = name
        self.enemies = enemies or []

class Trap:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

class Treasure:
    def __init__(self, name, loot):
        self.name = name
        self.loot = loot

class BossRoom:
    def __init__(self, name, boss):
        self.name = name
        self.boss = boss
