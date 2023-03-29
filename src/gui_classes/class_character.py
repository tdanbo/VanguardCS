from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons
import template.functions as func
import math

from gui_widgets.gui_inventory_frame import InventoryItem
from gui_widgets.gui_ability_frame import AbilityItem
from gui_classes.class_modify_stat import ModifyStat
from gui_classes.class_ability_adjust import AbilityAdjust

import os
import random


class Character:
    def __init__(self):
        self.active_modifier_name = ""
        self.active_modifier = 0
        self.base_modifier = 0

    def load_document(self, character_name):
        self.character_name = character_name
        if self.character_name == "":
            return

        self.db = cons.CLIENT["dnd"]
        self.collection = self.db["characters"]

        self.query = {"character": self.character_name}
        self.CHARACTER_DOC = self.collection.find_one(self.query)

        # Set the character portrait
        if os.path.isfile(os.path.join(cons.ICONS, f"{self.character_name}.png")):
            func.set_icon(
                self.inventory_gui.portrait.get_widget(),
                f"{self.character_name}.png",
                "",
            )
        else:
            random_portrait = random.choice(["unknown"])
            func.set_icon(
                self.inventory_gui.portrait.get_widget(), f"{random_portrait}.png", ""
            )

        self.set_all_stats()

    def set_all_stats(self):
        # Set the active modifiers
        self.reset_active_modifiers()
        # Set character equipment
        self.set_stats()
        # Set secondary stats
        self.set_secondary_stats()
        # Set character abilities
        self.set_abilities()
        # Set character inventory (Needs to be last to have strong counted in)
        self.set_inventory()
        # Set character equipment
        self.set_equipment()
        # Set qualities
        self.set_qualities()
        # final adjust with abilities
        self.set_ability_adjustments()
        # Set character modifiers
        self.set_modifiers()
        # Set character calculated stats
        self.set_calculated_stats()
        # Set character xp
        self.set_xp()

        # Save document
        self.save_document()

    def save_document(self):
        current_sheet = {"$set": self.CHARACTER_DOC}
        self.collection.update_one(self.query, current_sheet)

    def reset_active_modifiers(self):
        self.ATTACK = 0
        self.DEFENSE = 0
        self.CASTING = 0
        self.SPEED = 0

    def set_inventory(self):
        print("Setting inventory")
        self.inventory_layout = self.inventory_gui.inventory_scroll.inner_layout(1)
        func.clear_layout(self.inventory_layout)

        sorted_list = sorted(
            self.CHARACTER_DOC["inventory"],
            key=lambda x: cons.PRIORITY.get(x.get("Category", ""), len(cons.PRIORITY)),
        )

        self.CHARACTER_DOC["inventory"] = sorted_list

        if self.check_abilities("Pack-mule"):
            weight_multiplier = 1.5
        else:
            weight_multiplier = 1

        if int(self.sheet_gui.findChild(QWidget, "STRONG").text()) < 10:
            carry = 10
        else:
            carry = int(self.sheet_gui.findChild(QWidget, "STRONG").text())

        self.carry_weight = math.floor((carry * weight_multiplier)) - 1
        self.carry_limit = self.carry_weight * 2

        for count in range(self.carry_limit, -1, -1):
            try:
                item_dict = self.CHARACTER_DOC["inventory"][count]
            except:
                item_dict = {}
            item_widget = InventoryItem(
                self, count, item_dict, self.inventory_layout, self.carry_weight
            )

        current_weight = len(self.CHARACTER_DOC["inventory"])
        overweight = (self.carry_weight - current_weight) + 1
        if overweight < 0:
            self.DEFENSE += overweight
            self.SPEED += overweight

        scrollbar = self.inventory_gui.inventory_scroll.get_scroll().verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def set_equipment(self):
        print("Setting equipment")
        self.equipment_layout = self.inventory_gui.equipment_layout.inner_layout(1)
        func.clear_layout(self.equipment_layout)

        self.mainhand_slot = InventoryItem(
            self,
            1,
            self.CHARACTER_DOC["equipment"]["armor"],
            self.equipment_layout,
            self.carry_weight,
            equipment="AR",
        )
        self.offhand_slot = InventoryItem(
            self,
            2,
            self.CHARACTER_DOC["equipment"]["main hand"],
            self.equipment_layout,
            self.carry_weight,
            equipment="MH",
        )
        self.armor_slot = InventoryItem(
            self,
            3,
            self.CHARACTER_DOC["equipment"]["off hand"],
            self.equipment_layout,
            self.carry_weight,
            equipment="OH",
        )

    def set_qualities(self):
        armor = self.CHARACTER_DOC["equipment"]["armor"]
        if armor != {}:
            impeding = [
                quality for quality in armor["Quality"] if "Impeding" in quality
            ][0]
            value = ModifyStat(impeding).find_integer()
            self.SPEED += value
            self.DEFENSE += value
            self.CASTING += value

        mh = self.CHARACTER_DOC["equipment"]["main hand"]
        if mh != {}:
            if "Precise" in mh["Quality"]:
                self.ATTACK += 1
            if "Balanced 1" in mh["Quality"]:
                self.DEFENSE += 1
            elif "Balanced 2" in mh["Quality"]:
                self.DEFENSE += 2

        oh = self.CHARACTER_DOC["equipment"]["off hand"]
        if oh != {}:
            if "Precise" in oh["Quality"]:
                self.ATTACK += 1
            if "Balanced 1" in oh["Quality"]:
                self.DEFENSE += 1
            elif "Balanced 2" in oh["Quality"]:
                self.DEFENSE += 2

    def set_stats(self):
        for stat in cons.STATS:
            stat_base = self.CHARACTER_DOC["stats"][stat]
            stat_mod = ModifyStat(
                self.CHARACTER_DOC["mods"][f"{stat} mod"]
            ).find_integer()
            stat_total = str(
                stat_base + stat_mod + self.active_modifier + self.base_modifier
            )

            # Set the base stat
            self.sheet_gui.findChild(QWidget, f"{stat}").setText(stat_total)

            # Set the modifier
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText(
                self.CHARACTER_DOC["mods"][f"{stat} mod"]
            )

    def set_secondary_stats(self):
        for stat in cons.SECONDARY_STATS:
            stat_base = self.CHARACTER_DOC["stats"][stat]
            stat_mod = ModifyStat(
                self.CHARACTER_DOC["mods"][f"{stat} mod"]
            ).find_integer()
            stat_total = str(stat_base + stat_mod)

            # Set the base stat
            self.sheet_gui.findChild(QWidget, f"{stat}").setText(stat_total)

            # Set the modifier
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText(
                self.CHARACTER_DOC["mods"][f"{stat} mod"]
            )

    def set_modifiers(self):
        self.CHARACTER_DOC["DEFENSE mod"] = self.DEFENSE
        self.CHARACTER_DOC["CASTING mod"] = self.CASTING
        self.CHARACTER_DOC["SNEAKING mod"] = self.SPEED
        self.CHARACTER_DOC["ATTACK mod"] = self.ATTACK

        for stat in cons.STATS:
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText(
                str(self.CHARACTER_DOC["mods"][f"{stat} mod"])
            )

        for stat in ["DEFENSE", "CASTING", "SKILL", "SNEAKING", "ATTACK"]:
            modifier = int(self.CHARACTER_DOC[f"{stat} mod"])
            if modifier > 0:
                modifier = f"+{modifier}"

            self.inventory_gui.findChild(QWidget, f"{stat} mod").setText(str(modifier))

        if self.inventory_gui.modifier_mod.get_widget().text() == "":
            self.inventory_gui.modifier_mod.get_widget().setText("0")

    def set_calculated_stats(self):
        strong = int(self.sheet_gui.findChild(QWidget, "STRONG").text())
        resolute = int(self.sheet_gui.findChild(QWidget, "RESOLUTE").text())
        quick = int(self.sheet_gui.findChild(QWidget, "QUICK").text())

        maximum_mod = ModifyStat(
            self.CHARACTER_DOC["mods"]["MAXIMUM mod"]
        ).find_integer()
        pain_mod = ModifyStat(self.CHARACTER_DOC["mods"]["PAIN mod"]).find_integer()
        corruption_mod = ModifyStat(
            self.CHARACTER_DOC["mods"]["THRESHOLD mod"]
        ).find_integer()

        max_toughness = (10 if strong < 10 else strong) + maximum_mod
        pain_threshold = math.ceil(strong / 2) + pain_mod

        self.sheet_gui.toughness_max.get_widget().setText(str(max_toughness))
        self.sheet_gui.toughness_threshold.get_widget().setText(str(pain_threshold))

        corruption_threshold = math.ceil(resolute / 2) + corruption_mod
        self.sheet_gui.corruption_threshold.get_widget().setText(
            f"{corruption_threshold} / {resolute}"
        )

        # set total corruption
        corruption = int(self.sheet_gui.corruption_current.get_widget().text())
        permanent = int(self.sheet_gui.corruption_permanent.get_widget().text())
        self.sheet_gui.corruption_current.get_widget().setText(
            str(corruption + permanent)
        )

        movement = (quick + self.SPEED) * 5
        if movement < 20:
            movement = 20
        self.inventory_gui.movement_button.get_widget().setText(str(movement))

    def set_abilities(self):
        print("Setting abilities")
        self.ability_layout = self.sheet_gui.ability_layout.inner_layout(1)
        func.clear_layout(self.ability_layout)
        priority = {
            "Ability": 0,
            "Mystical Power": 1,
            "Ritual": 2,
            "Boon": 3,
            "Burden": 4,
        }
        self.sorted_list = sorted(
            self.CHARACTER_DOC["abilities"],
            key=lambda x: priority.get(x.get("Type", ""), len(priority)),
        )
        for slot, item in enumerate(self.sorted_list):
            ability = AbilityItem(self, item, slot=slot)
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

        total_experience = self.CHARACTER_DOC["TOTALXP"]
        self.CHARACTER_DOC["XP"] = earned_experience

        self.inventory_gui.experience.get_widget().setText(str(earned_experience))
        self.inventory_gui.unspent_experience.get_widget().setText(
            str(total_experience - earned_experience)
        )

    def set_ability_adjustments(self):
        print("Setting ability adjustments")
        AbilityAdjust(self)

    def clear_character(self):
        self.CHARACTER_DOC = None

        func.set_icon(self.inventory_gui.portrait.get_widget(), "", "")

        func.clear_layout(self.sheet_gui.ability_layout.inner_layout(1))
        func.clear_layout(self.inventory_gui.inventory_scroll.inner_layout(1))
        func.clear_layout(self.inventory_gui.equipment_layout.inner_layout(1))

        for stat in cons.STATS:
            self.sheet_gui.findChild(QWidget, f"{stat}").setText("")
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText("")

        for stat in cons.SECONDARY_STATS:
            self.sheet_gui.findChild(QWidget, f"{stat}").setText("")
            self.sheet_gui.findChild(QWidget, f"{stat} mod").setText("")

        for stat in ["DEFENSE", "CASTING", "SKILL", "SNEAKING", "ATTACK"]:
            self.inventory_gui.findChild(QWidget, f"{stat} mod").setText("")

        self.inventory_gui.modifier_mod.get_widget().setText("")

        self.inventory_gui.experience.get_widget().setText("")
        self.inventory_gui.unspent_experience.get_widget().setText("")

    def set_inventory_gui(self, inventory_gui=None):
        self.inventory_gui = inventory_gui

    def set_sheet_gui(self, sheet_gui=None):
        self.sheet_gui = sheet_gui

    def set_combat_log_gui(self, combat_log=None):
        self.combat_log = combat_log

    def check_abilities(self, name):
        if name in [item["Name"] for item in self.CHARACTER_DOC["abilities"]]:
            self.ability_dict = [
                item for item in self.CHARACTER_DOC["abilities"] if item["Name"] == name
            ][0]
            return True
        else:
            return False

    # def set_combat_gui(self, combat_gui=None):
    #     self.combat_gui = combat_gui
