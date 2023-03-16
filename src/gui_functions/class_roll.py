import random
import datetime
import pymongo
import constants as cons

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class DiceRoll:
    def __init__(self, widget, combat_log, character, roll_type, dice, check=0, sheet=None, ammo=False):

        self.character_sheet = sheet
        self.combat_log = combat_log
        self.modifier_widget = self.character_sheet.modifier
        self.dice = dice
        self.modifier = int(self.modifier_widget.text())
        self.check = check
        self.roll_type = roll_type
        self.ammo = ammo
        self.widget = widget

        self.check_active_modifiers()

        print(roll_type)
        print(roll_type)

        self.entry  = {
            "Character": character,
            "Type": self.roll_type,
            "Dice": dice,
            "Modifier": self.modifier,
            "Result": "",
            "Result Breakdown": "",
            "Result Message": "",
            "Time": "",
        }

        self.modifier_widget.setText("0")

    def roll(self):
        if self.ammo == True:
            if self.subtract_ammo() == True:
                pass
                # stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.PRIMARY_DARKER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"
                # self.widget.setStyleSheet(stylesheet)
            else:
                print("No ammo")
                stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.PRIMARY_DARKER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"
                self.widget.setStyleSheet(stylesheet)
                return

        dice_roll = 0
        breakdowns = []

        initial_split = self.dice.split("_")
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

            self.breakdown = '+'.join(str(num) for num in dice_breakdown)
            self.full_breakdown = f"{single_dice} = {self.breakdown} modified {self.modifier}"
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

        self.save_to_database()

    def subtract_ammo(self):
        has_ammo = False
        for value, item in self.character_sheet.CHARACTER_DOC["equipment"].items():
            if item != {}:
                if self.character_sheet.CHARACTER_DOC["equipment"][value]["Type"] == "Arrow":
                    if self.character_sheet.CHARACTER_DOC["equipment"][value]["Quantity"] > 0:
                        self.character_sheet.CHARACTER_DOC["equipment"][value]["Quantity"] -= 1
                        self.character_sheet.update_sheet()
                        has_ammo = True
                    else:
                        has_ammo = False
        return has_ammo

    def check_roll(self):
        if self.result <= self.check:
            self.entry["Result Message"] = "Success"
        else:
            self.entry["Result Message"] = "Failed"

    def check_active_modifiers(self):
        atk_value = self.character_sheet.ATK_mod
        def_value = self.character_sheet.DEF_mod
        cas_value = self.character_sheet.CAS_mod
        sne_value = self.character_sheet.SNE_mod

        atk_mod = self.character_sheet.ATK
        def_mod = self.character_sheet.DEF
        cas_mod = self.character_sheet.CAS
        sne_mod = self.character_sheet.SNE
        
        stylesheet_mod = f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        stylesheet_button  = f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        if atk_mod.isChecked():
            self.modifier += int(atk_value.text())
            atk_mod.setChecked(False)
            self.roll_type = "Attack"
            atk_mod.setStyleSheet(stylesheet_button)
            atk_value.setStyleSheet(stylesheet_mod)
            return
        
        if def_mod.isChecked():
            self.modifier += int(def_value.text())
            def_mod.setChecked(False)
            self.roll_type = "Defense"
            def_mod.setStyleSheet(stylesheet_button)
            def_value.setStyleSheet(stylesheet_mod)
            return
        
        if cas_mod.isChecked():
            self.modifier += int(cas_value.text())
            cas_mod.setChecked(False)
            self.roll_type = "Casting"
            cas_mod.setStyleSheet(stylesheet_button)
            cas_value.setStyleSheet(stylesheet_mod)
            return
        
        if sne_mod.isChecked():
            self.modifier += int(sne_value.text())
            sne_mod.setChecked(False)
            self.roll_type = "Sneaking"
            sne_mod.setStyleSheet(stylesheet_button)
            sne_value.setStyleSheet(stylesheet_mod)
            return


    def set_time(self):
        self.entry["Time"] = datetime.datetime.now().strftime("%H:%M:%S")

    def save_to_database(self):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["combatlog"]
        self.collection.insert_one(self.entry)