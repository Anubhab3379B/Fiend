class Stats:
    def __init__(self):
        self.strength = 10
        self.dexterity = 10
        self.intelligence = 10
        self.faith = 10
        self.vitality = 100
        self.endurance = 50

class Player:
    def __init__(self):
        self.name = "Hero"
        self.stats = Stats()
        self.class_type = None
        self.classes = []  # Supports multiclassing
        self.inventory = []
        self.skills = []
        self.faction = None
        self.faction_influence = {}
        self.world_state = {}
        self.gold = 100
        self.active_quests = []

    def choose_action(self):
        print("\nChoose your action:")
        print("1. Attack")
        print("2. Parry")
        print("3. Dodge")
        print("4. Use Skill")
        choice = input("> ")
        if choice == "1":
            return "attack"
        elif choice == "2":
            return "parry"
        elif choice == "3":
            return "dodge"
        elif choice == "4":
            return "use_skill"
        else:
            return "attack"

    def choose_skill(self):
        if not self.skills:
            print("No skills unlocked yet!")
            return None
        print("\nChoose a skill:")
        for i, skill in enumerate(self.skills):
            print(f"{i+1}. {skill.name}")
        choice = input("> ")
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(self.skills):
                return self.skills[choice_idx]
        except ValueError:
            pass
        return None

    def get_weapon_bonus(self):
        bonus = 0
        for item in self.inventory:
            if isinstance(item, dict) and "str_bonus" in item:
                bonus += item["str_bonus"]
        return bonus
