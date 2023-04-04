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

from template.widget import Widget
from template.section import Section


class Character(QWidget):
    def __init__(self):
        super().__init__()
        self.active_modifier_name = ""
        self.active_modifier = 0
        self.base_modifier = 0

        self.section_group = []
        self.widget_group = []

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
        # Set armor qualities
        self.set_armor_qualities()
        # final adjust with abilities
        self.set_ability_adjustments()
        # Set weapon qualities
        self.set_weapon_qualities()
        # Set character modifiers
        self.set_modifiers()
        # Set character calculated stats
        self.set_calculated_stats()
        # Set corruption
        self.set_corruption()
        # Set character xp
        self.set_xp()

        # Save document
        self.save_document()

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

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

    def set_equipment(self):
        print("Setting equipment")
        self.equipment_layout = self.inventory_gui.equipment_layout.inner_layout(1)
        func.clear_layout(self.equipment_layout)

        self.armor_slot = InventoryItem(
            self,
            1,
            self.CHARACTER_DOC["equipment"]["armor"],
            self.equipment_layout,
            self.carry_weight,
            equipment="AR",
        )
        self.mainhand_slot = InventoryItem(
            self,
            2,
            self.CHARACTER_DOC["equipment"]["main hand"],
            self.equipment_layout,
            self.carry_weight,
            equipment="MH",
        )
        self.offhand_slot = InventoryItem(
            self,
            3,
            self.CHARACTER_DOC["equipment"]["off hand"],
            self.equipment_layout,
            self.carry_weight,
            equipment="OH",
        )

    def set_armor_qualities(self):
        armor = self.CHARACTER_DOC["equipment"]["armor"]
        if armor != {}:
            impeding = [
                quality for quality in armor["Quality"] if "Impeding" in quality
            ][0]
            value = ModifyStat(impeding).find_integer()
            self.SPEED += value
            self.DEFENSE += value
            self.CASTING += value

    def set_weapon_qualities(self):
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

        quick = int(self.sheet_gui.findChild(QWidget, "QUICK").text())

        maximum_mod = ModifyStat(
            self.CHARACTER_DOC["mods"]["MAXIMUM mod"]
        ).find_integer()
        pain_mod = ModifyStat(self.CHARACTER_DOC["mods"]["PAIN mod"]).find_integer()

        max_toughness = (10 if strong < 10 else strong) + maximum_mod
        pain_threshold = math.ceil(strong / 2) + pain_mod

        self.sheet_gui.toughness_max.get_widget().setText(str(max_toughness))
        self.sheet_gui.toughness_threshold.get_widget().setText(str(pain_threshold))

        # Calculating speed
        base_speed = 40
        if quick < 5:
            stat_modifier = -10
        elif quick > 15:
            stat_modifier = 10
        else:
            stat_modifier = cons.MOVEMENT[quick]

        total_impeding = self.SPEED * 5
        adjusted_base = base_speed + stat_modifier
        calculated_speed = adjusted_base + total_impeding
        self.inventory_gui.movement_button.get_widget().setText(str(calculated_speed))

    def set_corruption_level(self):
        self.corruption_level = self.CHARACTER_DOC["CORRUPTION LEVEL"]
        func.set_icon(
            self.sheet_gui.corruption_level.get_widget(),
            f"{self.corruption_level}.png",
            cons.DARK,
            width=40,
        )
        self.sheet_gui.corruption_level.get_widget().setObjectName(
            str(self.corruption_level)
        )

    def set_corruption(self):
        print("set corruption")
        self.set_corruption_level()
        self.corruption_group = []
        func.clear_layout(self.sheet_gui.corruption_token_layout.inner_layout(1))
        resolute = int(self.sheet_gui.findChild(QWidget, "RESOLUTE").text())
        self.corruption_threshold = math.ceil(resolute / 2)

        for count in range(self.corruption_threshold):
            count = count + 1
            self.button = QToolButton()
            self.sheet_gui.corruption_token_layout.inner_layout(1).addWidget(
                self.button
            )
            self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.button.clicked.connect(self.change_corruption)
            self.corruption_group.append(self.button)

        if self.corruption_threshold < self.CHARACTER_DOC["stats"]["CORRUPTION"]:
            self.CHARACTER_DOC["stats"]["CORRUPTION"] = self.corruption_threshold

        if self.corruption_threshold < self.CHARACTER_DOC["stats"]["PERMANENT"]:
            self.CHARACTER_DOC["stats"]["PERMANENT"] = self.corruption_threshold

        self.set_corruption_style()
        self.save_document()

    def add_corruption(self, value):
        current_corruption = self.CHARACTER_DOC["stats"]["CORRUPTION"]
        current_permanent = self.CHARACTER_DOC["stats"]["PERMANENT"]

        for point in range(value):
            if current_corruption < self.corruption_threshold:
                current_corruption += 1
            else:
                current_permanent += 1

            if current_permanent == self.corruption_threshold:

                corruption_level = (
                    int(self.sheet_gui.corruption_level.get_widget().objectName()) + 1
                )
                if corruption_level > 3:
                    corruption_level = 3

                print("corruption level")
                print(corruption_level)

                self.sheet_gui.corruption_level.get_widget().setObjectName(
                    str(corruption_level)
                )
                func.set_icon(
                    self.sheet_gui.corruption_level.get_widget(),
                    f"{corruption_level}.png",
                    cons.DARK,
                    width=40,
                )
                self.CHARACTER_DOC["CORRUPTION LEVEL"] = corruption_level
                current_corruption = 0
                current_permanent = 0

        if self.sheet_gui.corruption_level.get_widget().objectName() == "3":
            [button.setObjectName("abom") for button in self.corruption_group]
            self.set_abomination()
            return

        self.CHARACTER_DOC["stats"]["CORRUPTION"] = current_corruption
        self.CHARACTER_DOC["stats"]["PERMANENT"] = current_permanent

        self.set_corruption()
        self.save_document()

    def change_corruption(self):
        sender = self.sender()

        self.CHARACTER_DOC["stats"]["CORRUPTION"] = 0
        self.CHARACTER_DOC["stats"]["PERMANENT"] = 0

        if sender.objectName() == "permanent":
            sender.setObjectName("empty")

        elif sender.objectName() == "temporary":
            sender.setObjectName("permanent")

        elif sender.objectName() == "empty":
            sender.setObjectName("temporary")

        for button in self.corruption_group:
            if button.objectName() == "permanent":
                self.CHARACTER_DOC["stats"]["PERMANENT"] += 1
                self.CHARACTER_DOC["stats"]["CORRUPTION"] += 1
            elif button.objectName() == "temporary":
                self.CHARACTER_DOC["stats"]["CORRUPTION"] += 1

        print(sender.objectName())

        self.save_document()
        self.set_corruption_style()

    def set_corruption_style(self):
        for widget in self.corruption_group:
            widget.setStyleSheet(
                f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;"
            )
            func.set_icon(widget, "", "", width=0)
            widget.setObjectName("empty")

        for slot in range(self.CHARACTER_DOC["stats"]["CORRUPTION"]):
            widget = self.corruption_group[slot]
            widget.setStyleSheet(
                f"background-color: {cons.BORDER_DARK}; border: 1px solid {cons.BORDER}; border-radius: 6px;"
            )
            func.set_icon(widget, "dead.png", cons.BORDER, width=cons.ICON_SIZE)
            widget.setObjectName("temporary")

        for slot in range(self.CHARACTER_DOC["stats"]["PERMANENT"]):
            widget = self.corruption_group[slot]
            widget.setStyleSheet(
                f"background-color: {cons.DARK}; border: 1px solid {cons.BORDER}; border-radius: 6px;"
            )
            func.set_icon(widget, "dead.png", cons.FONT_LIGHT, width=cons.ICON_SIZE)
            widget.setObjectName("permanent")

    def set_abomination(self):
        for widget in self.corruption_group:
            widget.setStyleSheet(
                f"background-color: {cons.PURPLE}; border: 1px solid {cons.BORDER}; border-radius: 6px;"
            )
            func.set_icon(widget, "dead.png", cons.FONT_LIGHT, width=cons.ICON_SIZE)

    def reset_corruption(self):
        for widget in self.corruption_group:
            if widget.objectName() == "temporary":
                widget.setObjectName("empty")

        self.CHARACTER_DOC["stats"]["CORRUPTION"] = self.CHARACTER_DOC["stats"][
            "PERMANENT"
        ]
        self.set_corruption_style()
        self.save_document()

    def set_abilities(self):
        print("Setting abilities")
        self.ability_layout = self.sheet_gui.ability_layout.inner_layout(1)
        func.clear_layout(self.ability_layout)

        for slot, item in enumerate(self.CHARACTER_DOC["abilities"]):
            print(item["Name"])
            print(item["Rank"])
            print("------------------")
            self.new_ability = AbilityItem(self, item, select=False, slot=slot)
            self.ability_layout.addWidget(self.new_ability)
        filler_widget = QWidget()
        filler_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ability_layout.addWidget(filler_widget)
        self.set_xp()

    def set_xp(self):
        earned_experience = 0
        for ability in self.CHARACTER_DOC["abilities"]:
            if ability["Rank"] == "Novice":
                if ability["Type"] == "Trait":
                    earned_experience += 0
                else:
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

        func.set_icon(self.inventory_gui.portrait.get_widget(), "", "", width=0)

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

        for widget in self.corruption_group:
            widget.setStyleSheet(
                f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;"
            )
            func.set_icon(widget, "", "", width=0)
            widget.setObjectName("empty")

        func.set_icon(self.sheet_gui.corruption_level.get_widget(), "", "", width=0)

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
