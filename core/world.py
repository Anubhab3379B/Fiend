import random
from core.utils import Room, Trap, Treasure, BossRoom
from combat.enemy import Enemy
from combat.boss import Boss

class World:
    def __init__(self):
        self.dungeons = []
        self.game_over = False

    def generate_dungeon(self, floors=3):
        dungeon = []
        for floor in range(floors):
            rooms = self.generate_floor(floor)
            dungeon.append(rooms)
        self.dungeons.append(dungeon)
        return dungeon

    def generate_floor(self, floor_number):
        rooms = []
        num_rooms = random.randint(2, 4)
        for i in range(num_rooms):
            room_type = random.choice(["combat", "trap", "treasure", "boss"])
            if room_type == "combat":
                rooms.append(Room(f"Combat Room {i+1}", enemies=self.spawn_enemies(floor_number)))
            elif room_type == "trap":
                rooms.append(Trap(f"Trap Room {i+1}", difficulty=random.randint(1, 5)))
            elif room_type == "treasure":
                rooms.append(Treasure(f"Treasure Room {i+1}", loot=self.generate_loot()))
            elif room_type == "boss" and i == num_rooms - 1:
                rooms.append(BossRoom(f"Boss Room {i+1}", boss=self.spawn_boss(floor_number)))
        
        # Ensure at least one boss room at the end of the floor if not generated
        if not any(isinstance(r, BossRoom) for r in rooms):
            rooms.append(BossRoom(f"Final Boss Room", boss=self.spawn_boss(floor_number)))

        return rooms

    def spawn_enemies(self, floor_number):
        count = random.randint(1, 3) + floor_number
        enemies = []
        for i in range(count):
            enemies.append(Enemy(f"Goblin Grunt {i+1}", health=30 + (floor_number*10), attack_power=5 + floor_number, attack_speed=5))
        return enemies

    def spawn_boss(self, floor_number):
        boss_names = ["Bandit King", "Corrupted Knight", "Warlord of the Ruin"]
        name = boss_names[min(floor_number, len(boss_names)-1)]
        return Boss(name=name, boss_class="Warrior", level=floor_number+1)

    def generate_loot(self):
        loot_types = ["Rusty Sword", "Leather Armor", "Healing Potion", "Ancient Relic"]
        return random.choice(loot_types)

    def update(self):
        pass
