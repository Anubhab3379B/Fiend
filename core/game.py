from core.player import Player
from core.world import World
from core.difficulty_manager import DifficultyManager
from core.save_system import SaveSystem
from core.multiclassing import MulticlassingSystem
from core.team_manager import TeamManager
from combat.combat_controller import CombatController
from skills.skill_tree_manager import SkillTreeManager
from equipment.equipment_manager import EquipmentManager
from quests.quest_manager import QuestManager, Quest
from quests.faction_system import FactionSystem
from achievements.achievement_system import AchievementSystem
from narrative.dialogue_manager import DialogueManager
from narrative.ending_manager import EndingManager
from narrative.npc import NPC

class Game:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.save_system = SaveSystem(self.player)
        self.difficulty = DifficultyManager(self.player)
        self.multiclassing = MulticlassingSystem(self.player)
        self.team_manager = TeamManager(self.player)
        self.combat = CombatController(self.player, self.team_manager)
        self.skills = SkillTreeManager(self.player)
        self.equipment = EquipmentManager(self.player)
        self.quests = QuestManager(self.player)
        self.factions = FactionSystem(self.player)
        self.achievements = AchievementSystem(self.player)
        self.dialogue = DialogueManager(self.player)
        self.ending = EndingManager(self.player)
        self.game_over = False

    def start_game(self):
        print("Welcome to the Dungeon RPG: The Tower of Eternal Conflict!")
        slot = input("Choose save slot (save1.json, save2.json, save3.json): ")
        if not slot:
            slot = "save1.json"
        
        choice = input("Load previous save? (y/n): ")
        if choice.lower() == "y":
            self.save_system.load_game(slot)
        else:
            print("Starting a new adventure!")
            self.player.name = input("Enter your hero's name: ")
            self.quests.add_quest(Quest("The First Steps", "Enter the Ruined Kingdom."))

        # Campaign chapters: currently building a demo floor
        dungeon = self.world.generate_dungeon(floors=3)
        self.explore_dungeon(dungeon)
        self.conclude_game()

        save_choice = input("Do you want to save your progress? (y/n): ")
        if save_choice.lower() == "y":
            self.save_system.save_game(slot)

    def explore_dungeon(self, dungeon):
        for floor_idx, floor in enumerate(dungeon):
            print(f"\n--- Exploring Floor {floor_idx + 1} ---")
            for room in floor:
                print(f"\nEntering {room.name}")
                if hasattr(room, "enemies"):
                    for enemy in room.enemies:
                        self.combat.handle_combat(enemy)
                elif hasattr(room, "loot"):
                    print(f"Found treasure: {room.loot}")
                    self.equipment.equip({"name": room.loot, "str_bonus": 5, "rarity": "Common", "class_restriction": None})
                elif hasattr(room, "boss"):
                    print(f"\n! Boss Encounter: {room.boss.name} !")
                    self.combat.handle_combat(room.boss)

            # NPC Interactions post floor
            self.npc_interactions()

            # Faction dialogue branching
            dialogue_options = self.dialogue.faction_dialogue()
            if dialogue_options:
                outcome = self.dialogue.present_choice(dialogue_options)
                if "Quest" in outcome:
                    quest_name = outcome.split(": ")[1]
                    self.quests.add_quest(Quest(quest_name, "Faction-driven quest."))
                elif "StatBoost" in outcome:
                    stat, boost = outcome.split(": ")[1].split(" +")
                    current_stat = getattr(self.player.stats, stat.lower())
                    setattr(self.player.stats, stat.lower(), current_stat + int(boost))
                    print(f"{stat} increased by {boost}!")

            # Difficulty adjusts per floor
            self.difficulty.update()
            
            # Level-based unlocks (multiclassing demo)
            if floor_idx == 1 and "Warrior" not in self.player.classes:
                self.multiclassing.unlock_class("Warrior")

    def npc_interactions(self):
        villager = NPC("Elda", role="villager")
        merchant = NPC("Borin", role="merchant")
        villager.greet(self.player)
        merchant.merchant_behavior(self.player)

    def conclude_game(self):
        ending = self.ending.determine_ending()
        print(f"\nGame Over! Your ending: {ending}")
        self.game_over = True
