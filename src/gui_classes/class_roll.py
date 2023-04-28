import random
import datetime
import constants as cons

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from gui_classes.class_modify_roll import ModifyRoll


class DiceRoll:
    def __init__(
        self,
        widget,
        character_name,
        roll_type,
        dice,
        check=0,
        character=None,
        ammo=False,
    ):
        self.character = character
        self.modifier_widget = self.character.inventory_gui.modifier_mod.get_widget()
        self.roll_type = roll_type
        print(f"Roll type: {roll_type}")
        self.active_type = (
            self.character.active_modifier_name
            if not self.character.active_modifier_name == ""
            else "Custom"
        )
        self.dice = dice
        self.modifier = 0
        self.check = check
        self.ammo = ammo
        self.widget = widget

        self.entry = {
            "Character": character_name,
            "Active": self.active_type,
            "Type": self.roll_type,
            "Check": self.check,
            "Dice": dice,
            "Modifier": self.modifier,
            "Result": "",
            "Result Breakdown": "",
            "Result Message": "",
            "Time": "",
            "Skill Modifier": self.modifier_widget.text(),
        }

        self.modifier_widget.setText("0")

    def roll(self):
        if self.ammo == True:
            if self.subtract_ammo() == True:
                pass
                # stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.PRIMARY_DARKER}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"
                # self.widget.setStyleSheet(stylesheet)
            else:
                stylesheet = f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.PRIMARY_DARKER}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"
                self.widget.setStyleSheet(stylesheet)
                return

        dice_roll = 0
        breakdowns = []

        remove_astrix = self.dice.replace("*", "")
        initial_split = remove_astrix.split("_")
        for single_dice in initial_split:
            modifier_split = single_dice.split("+")
            if len(modifier_split) > 1:
                self.modifier += int(modifier_split[1])
                single_dice = modifier_split[0]
            else:
                single_dice

            dice = single_dice.split("d")
            dice_count = int(dice[0])
            dice_type = int(dice[1])

            dice_breakdown = []

            for i in range(dice_count):
                roll = random.randint(1, dice_type)
                dice_roll += roll
                dice_breakdown.append(roll)

            self.breakdown = "+".join(str(num) for num in dice_breakdown)
            self.full_breakdown = (
                f"{single_dice} = {self.breakdown} modified {self.modifier}"
            )
            breakdowns.append(self.full_breakdown)

        joined_breakdowns = "\n".join(breakdowns)

        self.result = dice_roll + self.modifier

        self.entry["Result"] = self.result

        if self.modifier > 0:
            self.entry["Result Breakdown"] = joined_breakdowns
        elif self.modifier < 0:
            self.entry["Result Breakdown"] = joined_breakdowns
        else:
            self.entry["Result Breakdown"] = joined_breakdowns

        if self.check > 0:
            self.check_roll()
        self.set_time()

        # Cleanup
        self.save_to_database()
        self.character.base_modifier = 0
        self.character.active_modifier = 0
        self.character.active_modifier_name = ""
        ModifyRoll(self.character).clear_style()
        self.character.set_stats()
        return self.result

    def subtract_ammo(self):
        has_ammo = False
        for value, item in self.character.CHARACTER_DOC["equipment"].items():
            if item != {}:
                if self.character.CHARACTER_DOC["equipment"][value]["Type"] == "Arrow":
                    if self.character.CHARACTER_DOC["equipment"][value]["Quantity"] > 0:
                        self.character.CHARACTER_DOC["equipment"][value][
                            "Quantity"
                        ] -= 1
                        self.character.set_all_stats()
                        has_ammo = True
                    else:
                        has_ammo = False
        return has_ammo

    def check_roll(self):
        if self.result <= self.check:
            self.entry["Result Message"] = "Success"
        else:
            self.entry["Result Message"] = "Failed"

    def set_time(self):
        self.entry["Time"] = datetime.datetime.now().strftime("%H:%M:%S")

    def save_to_database(self):
        cons.COMBAT_LOG.insert_one(self.entry)
