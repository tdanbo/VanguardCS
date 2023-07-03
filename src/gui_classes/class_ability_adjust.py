class AbilityAdjust:
    def __init__(self, character):
        self.character = character

        self.main_hand = self.character.CHARACTER_DOC["equipment"]["main hand"]
        self.off_hand = self.character.CHARACTER_DOC["equipment"]["off hand"]
        self.armor = self.character.CHARACTER_DOC["equipment"]["armor"]

        # check and adjust for all special abilities
        self.shield_fighter()
        self.man_at_arms()
        self.armored_mystic()
        self.twin_attack()
        self.sword_saint()
        self.marksman()

    def shield_fighter(self):
        if self.check_abilities("Shield Fighter"):
            weapon_list = [
                "Sword",
                "Axe",
                "Mace",
                "Spear",
                "Greatsword",
                "Greataxe",
                "Maul",
                "Dagger",
                "Dirk",
                "Knife",
                "Bastard Sword 1",
                "Fencing Sword",
                "Crow's Beak",
                "Lance 1",
                "Flail",
                "Long-Hammer 1",
                "Long-Whip",
                "Estoc",
                "Stiletto",
                "Halberd",
                "Pike",
                "Sturdy Staff",
                "Wooden Staff",
                "Quarterstaff",
                "Chain Staff",
                "Lance 2",
                "Knuckles",
                "Battle Claw",
                "Bastard Sword 2",
                "Double-Axe",
                "Battle Flail"
                "Executioner's Axe",
                "Warhammer",
                "Long-Hammer 2",
                "Executioner's Sword",
                "Heavy Flail",
                "Grappling Axe 2"

            ]
            if self.main_hand != {}:
                if self.main_hand["Name"] in ["Shield", "Buckler", "Steel Shield"]:
                    self.character.DEFENSE += 1

            if self.off_hand != {}:
                if self.off_hand["Name"] in ["Shield", "Buckler", "Steel Shield"]:
                    self.character.DEFENSE += 1

            if self.main_hand != {}:
                if self.main_hand["Name"] in weapon_list:
                    if self.off_hand["Name"] in ["Shield", "Buckler", "Steel Shield"]:
                        widget = self.character.mainhand_slot.get_roll_widget()
                        roll = self.upgrade_roll(self.main_hand["Roll"][1])
                        widget.setText(roll)

            if self.off_hand != {}:
                if self.off_hand["Name"] in weapon_list:
                    if self.main_hand["Name"] in ["Shield", "Buckler", "Steel Shield"]:
                        widget = self.character.offhand_slot.get_roll_widget()
                        roll = self.upgrade_roll(self.off_hand["Roll"][1])
                        widget.setText(roll)

    def man_at_arms(self):
        if self.check_abilities("Man-at-Arms"):
            if self.ability_dict["Rank"] in ["Adept", "Master"]:
                self.character.DEFENSE = 0
                self.character.SPEED = 0

            if self.armor != {}:
                widget = self.character.armor_slot.get_roll_widget()
                roll = self.upgrade_roll(self.armor["Roll"][1])
                widget.setText(roll)

    def armored_mystic(self):
        if self.check_abilities("Armored Mystic"):
            if self.armor != {}:
                if self.ability_dict["Rank"] in ["Adept"]:
                    if self.armor["Type"] in ["Light Armor", "Medium Armor"]:
                        self.character.CASTING = 0
                elif self.ability_dict["Rank"] in ["Master"]:
                    if self.armor["Type"] in [
                        "Light Armor",
                        "Medium Armor",
                        "Heavy Armor",
                    ]:
                        self.character.CASTING = 0
                else:
                    pass

    def twin_attack(self):
        if self.check_abilities("Twin Attack"):
            if self.main_hand != {}:
                if self.main_hand["Category"] in ["quality_weapon", "ordinary_weapon"]:
                    if self.off_hand != {}:
                        if self.off_hand["Category"] in [
                            "quality_weapon",
                            "ordinary_weapon",
                        ]:
                            self.character.DEFENSE += 1

    def sword_saint(self):
        self.state = False
        if self.check_abilities("Sword Saint"):
            if self.main_hand != {}:
                if self.main_hand["Name"] in [
                    "Bastard Sword 1",
                    "Fencing Sword",
                    "Estoc",
                    "Sword",
                ]:
                    if self.off_hand != {}:
                        if self.off_hand["Name"] == "Parrying Dagger":
                            self.state = True

        if self.state == True:
            widget = self.character.mainhand_slot.get_roll_widget()

            if self.ability_dict["Rank"] in ["Novice", "Adept"]:
                roll = self.upgrade_roll(self.main_hand["Roll"][1])
                widget.setText(roll)
            elif self.ability_dict["Rank"] in ["Master"]:
                roll = self.upgrade_roll(self.main_hand["Roll"][1], step=4)
                widget.setText(roll)

    def marksman(self):
        if self.check_abilities("Marksman"):
            weapon_list = [
                "Bow",
                "Crossbow",
                "Arbalest",
                "Small Crossbow",
                "Repeating Crossbow",
                "Longbow",
                "Horsema's Longbow",
                "Composite Bow",
            ]

            if self.main_hand != {}:
                if self.main_hand["Name"] in weapon_list:
                    widget = self.character.mainhand_slot.get_roll_widget()
                    roll = self.upgrade_roll(self.main_hand["Roll"][1])
                    widget.setText(roll)

            if self.off_hand != {}:
                if self.off_hand["Name"] in weapon_list:
                    widget = self.character.offhand_slot.get_roll_widget()
                    roll = self.upgrade_roll(self.off_hand["Roll"][1])
                    widget.setText(roll)

    def check_abilities(self, name):
        if name in [item["Name"] for item in self.character.CHARACTER_DOC["abilities"]]:
            self.ability_dict = [
                item
                for item in self.character.CHARACTER_DOC["abilities"]
                if item["Name"] == name
            ][0]
            return True
        else:
            return False

    def upgrade_roll(self, roll, step=2):
        modifier_split = roll.split("+")
        modifier = 0
        if len(modifier_split) > 1:
            modifier += int(modifier_split[1])
            single_dice = modifier_split[0]
        else:
            single_dice = roll

        dice = single_dice.lower().split("d")
        dice_count = int(dice[0])
        dice_type = int(dice[1]) + step

        if modifier > 0:
            return f"*{dice_count}d{dice_type}+{modifier}"
        else:
            return f"*{dice_count}d{dice_type}"
