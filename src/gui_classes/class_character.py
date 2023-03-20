from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import pymongo
import constants as cons
import template.functions as func
import math

from gui_widgets.gui_inventory_frame import InventoryItem
from gui_widgets.gui_ability_frame import AbilityItem
from gui_classes.class_modify_stat import ModifyStat

class Character:
    def __init__(self):
        print("Character class initialized")
    def load_document(self, character_name):
        self.character_name = character_name
        if self.character_name == "":
            return

        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]

        self.query = {"character": self.character_name}
        self.CHARACTER_DOC = self.collection.find_one(self.query)

        # Set the character portrait
        func.set_icon(self.inventory_gui.portrait.get_widget(),f"{self.character_name}.png","")

        # Set character stats
        self.set_stats()

        # Set character inventory
        self.set_inventory()

        # Set character equipment
        self.set_equipment()

        # Set character abilities
        self.set_abilities()

        # Set character equipment
        self.set_stats()

        # Set character modifiers
        self.set_modifiers()

        # Set character calculated stats
        self.set_calculated_stats()

        #Set character xp
        self.set_xp()

        # Set calculated stats
        return self.CHARACTER_DOC

    def save_document(self):
        current_sheet = {"$set": self.CHARACTER_DOC}
        self.collection.update_one(self.query, current_sheet)

    def set_inventory(self):
        self.inventory_layout = self.inventory_gui.inventory_scroll.inner_layout(1)
        func.clear_layout(self.inventory_layout)
        priority = {'melee': 0, 'ranged': 1, 'ammunition': 2, 'armor': 3, 'elixirs': 4, 'treasure': 5, 'misc': 6}
        sorted_list = sorted(self.CHARACTER_DOC["inventory"], key=lambda x: priority.get(x.get('Category', ''), len(priority)))
        self.CHARACTER_DOC["inventory"] = sorted_list

        for count in range(20,-1,-1):
            try:
                item_dict = self.CHARACTER_DOC["inventory"][count]
            except:
                item_dict = {}
            
            item_widget = InventoryItem(self, count, item_dict, self.inventory_layout )

    def set_equipment(self):
        self.equipment_layout = self.inventory_gui.equipment_layout.inner_layout(1)
        func.clear_layout(self.equipment_layout)

        self.mainhand_slot = InventoryItem(self, 1, self.CHARACTER_DOC["equipment"]["armor"], self.equipment_layout, equipment="AR")
        self.offhand_slot = InventoryItem(self, 2, self.CHARACTER_DOC["equipment"]["main hand"], self.equipment_layout, equipment="MH")
        self.armor_slot = InventoryItem(self, 3, self.CHARACTER_DOC["equipment"]["off hand"], self.equipment_layout, equipment="OH")
        
    def set_stats(self):
        for stat in cons.STATS+cons.SECONDARY_STATS:
            stat_base = self.CHARACTER_DOC["stats"][stat]
            stat_mod = ModifyStat(self.CHARACTER_DOC["mods"][f"{stat} mod"]).find_integer()
            stat_total = str(stat_base + stat_mod)

            # Set the base stat
            self.sheet_gui.findChild(QWidget, f"{stat}").setText(stat_total)

            # Set the modifier
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText(self.CHARACTER_DOC["mods"][f"{stat} mod"])

    def set_modifiers(self):
        for stat in cons.STATS:
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText(str(self.CHARACTER_DOC["mods"][f"{stat} mod"]))

        for stat in ["DEFENSE", "CASTING", "SNEAKING", "ATTACK"]:
            modifier = int(self.CHARACTER_DOC[f"{stat} mod"])
            if modifier > 0:
                modifier = f"+{modifier}"
            
            self.inventory_gui.findChild(QWidget, f"{stat} mod").setText(str(modifier))

    def set_calculated_stats(self):
        strong = int(self.sheet_gui.findChild(QWidget, "STRONG").text())
        resolute = int(self.sheet_gui.findChild(QWidget, "RESOLUTE").text())

        maximum_mod = ModifyStat(self.CHARACTER_DOC["mods"]["MAXIMUM mod"]).find_integer()
        pain_mod = ModifyStat(self.CHARACTER_DOC["mods"]["PAIN mod"]).find_integer()
        corruption_mod = ModifyStat(self.CHARACTER_DOC["mods"]["THRESHOLD mod"]).find_integer()

        max_toughness = (10 if strong < 10 else strong)+maximum_mod
        pain_threshold = math.ceil(strong/2)+pain_mod

        self.sheet_gui.toughness_max.get_widget().setText(str(max_toughness))
        self.sheet_gui.toughness_threshold.get_widget().setText(str(pain_threshold))

        corruption_threshold = math.ceil(resolute/2)+corruption_mod
        self.sheet_gui.corruption_threshold.get_widget().setText(f"{corruption_threshold} / {resolute}")

        self.inventory_gui.modifier_button.get_widget().setText("0")

        

    def set_abilities(self):
        self.ability_layout = self.sheet_gui.ability_layout.inner_layout(1)
        func.clear_layout(self.ability_layout)
        priority = {'Ability': 0, 'Mystical Power': 1, 'Ritual': 2, 'Boon': 3, 'Burden': 4}
        self.sorted_list = sorted(self.CHARACTER_DOC["abilities"], key=lambda x: priority.get(x.get('Type', ''), len(priority)))
        for slot,item in enumerate(self.sorted_list):
            ability = AbilityItem(self,item,slot=slot)
            self.ability_layout.addWidget(ability)
        filler_widget = QWidget()
        filler_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ability_layout.addWidget(filler_widget)
        self.set_xp()

    def set_xp(self):
        earned_experience = 0
        for ability in self.CHARACTER_DOC["abilities"]:
            if ability["Rank"] == "Novice":
                earned_experience += 10
            elif ability["Rank"] == "Adept":
                earned_experience += 30
            elif ability["Rank"] == "Master":
                earned_experience += 60

        total_experience = self.CHARACTER_DOC["total experience"]        
        self.CHARACTER_DOC["character experience"] = earned_experience

        self.inventory_gui.experience.get_widget().setText(str(earned_experience))
        self.inventory_gui.unspent_experience.get_widget().setText(str(total_experience-earned_experience))

    def set_inventory_gui(self, inventory_gui=None):
        self.inventory_gui = inventory_gui

    def set_sheet_gui(self, sheet_gui=None):
        self.sheet_gui = sheet_gui

    # def set_combat_gui(self, combat_gui=None):
    #     self.combat_gui = combat_gui

