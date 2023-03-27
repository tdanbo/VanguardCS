class AbilityAdjust():
    def __init__ (self,character):
        self.character = character

        self.main_hand = self.character.CHARACTER_DOC["equipment"]["main hand"]
        self.off_hand = self.character.CHARACTER_DOC["equipment"]["off hand"]
        self.armor = self.character.CHARACTER_DOC["equipment"]["armor"]

        #check and adjust for all special abilities
        self.shield_fighter()
        self.man_at_arms()
        self.armored_mystic()

    def shield_fighter(self):
        print("Running")
        if self.check_abilities("Shield Fighter"):
            if self.main_hand != {}:
                if self.main_hand["Name"] in ["Shield", "Buckler", "Steel Shield"]:
                    self.character.DEFENSE += 1

            if self.off_hand != {}:
                if self.off_hand["Name"] in ["Shield", "Buckler", "Steel Shield"]:
                    self.character.DEFENSE += 1

    def man_at_arms(self):
        if self.check_abilities("Man-at-Arms"):
            if self.ability_dict["Rank"] in ["Adept","Master"]:
                self.character.DEFENSE = 0
                self.character.SPEED = 0

    def armored_mystic(self):
        if self.check_abilities("Armored Mystic"):
            if self.armor != {}:
                if self.ability_dict["Rank"] in ["Adept"]:
                    if self.armor["Type"] in ["Light Armor", "Medium Armor"]:  
                        self.character.CASTING = 0
                elif self.ability_dict["Rank"] in ["Master"]:
                    if self.armor["Type"] in ["Light Armor", "Medium Armor", "Heavy Armor"]:  
                        self.character.CASTING = 0
                else:
                    pass

    def check_abilities(self,name):
        if name in [item["Name"] for item in self.character.CHARACTER_DOC["abilities"]]:
            self.ability_dict = [item for item in self.character.CHARACTER_DOC["abilities"] if item["Name"] == name][0]
            return True
        else:
            return False