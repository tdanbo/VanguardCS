from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import pymongo
import constants as cons

import math
import constants as cons
import os
import functions as func

import random
import stylesheet as style

import json
import copy

class CharacterSheet():
    def __init__(self):
        print("Initializing Character Sheet")

    def update_sheet(self):
        self.set_icon()      
        # self.update_inventory()
        updated_character_sheet = self.update_dictionary()
        self.set_stats()
        self.set_toughness()
        self.set_corruption()
        self.set_defense()
        self.update_database(updated_character_sheet)
    def update_dictionary(self):
        print("Updating Character Sheet Dictionary")    
        character_sheet_dictionary = {
            "experience": self.experience.text(),
            "experience unspent": self.experience_unspent.text(),
            "modifiers": {
                "ACCURATE": self.ACC_mod.text(),
                "CUNNING": self.CUN_mod.text(),
                "DISCREET": self.DIS_mod.text(),
                "PERSUASIVE": self.PER_mod.text(),
                "QUICK": self.QUI_mod.text(),
                "RESOLUTE": self.RES_mod.text(),
                "STRONG": self.STR_mod.text(),
                "VIGILANT": self.VIG_mod.text()
            },
            "inventory": {
                "inventory1": self.inventory1.text(),
                "inventory2": self.inventory2.text(),
                "inventory3": self.inventory3.text(),
                "inventory4": self.inventory4.text(),
                "inventory5": self.inventory5.text(),
                "inventory6": self.inventory6.text(),
                "inventory7": self.inventory7.text(),
                "inventory8": self.inventory8.text(),
                "inventory9": self.inventory9.text(),
                "inventory10": self.inventory10.text(),
                "inventory11": self.inventory11.text(),
                "inventory12": self.inventory12.text(),
                "inventory13": self.inventory13.text(),
                "inventory14": self.inventory14.text(),
                "inventory15": self.inventory15.text(),
            },
            "toughness current": self.toughness_current.text(),
            "corruption temporary": self.corruption_temporary.text(),
            "corruption permanent": self.corruption_permanent.text(),

        }  
        return character_sheet_dictionary
    
    def update_database(self, directory):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]

        query = {"character": self.character_name}
        document = self.collection.find_one(query)

        if document is not None:
            new_values = {"$set": directory}
            self.collection.update_one(query, new_values)
        else:
            self.collection.insert_one(directory)

    # ITERATE OVER ITEM JSON TO FIND ITEM

    def set_stats(self):
        for widget in [(self.ACC, self.ACC_mod), (self.CUN, self.CUN_mod), (self.DIS, self.DIS_mod), (self.PER, self.PER_mod), (self.QUI, self.QUI_mod), (self.RES, self.RES_mod), (self.STR, self.STR_mod), (self.VIG, self.VIG_mod)]:
            stat = int(self.character_document["stats"][widget[0].objectName()])
            modifier = int(widget[1].text())
            modified_stat = stat + modifier

            widget[0].setText(str(modified_stat))
            if modifier == 0:
                widget[1].setHidden(True)
            else:
                widget[1].setHidden(False)

        pass

    def set_defense(self):
        self.defense.setText(self.QUI.text())


    def set_toughness(self):
        strong = int(self.STR.text())
        toughness_threshold_math = math.ceil(strong/2)
        toughness_math = 10 if strong < 10 else strong

        self.toughness_max.setText(str(toughness_math))
        self.toughness_current.setText(str(toughness_math))
        self.toughness_threshold.setText(str(toughness_threshold_math))


    def set_corruption(self):
        corruption_threshold_math = math.ceil(int(self.RES.text())/2)

        self.corruption_permanent.setText("0")
        self.corruption_temporary.setText("0")
        self.corruption_threshold.setText(str(corruption_threshold_math))

    def update_inventory(self):
        all_items = []

        self.empty_slot_dict = {"Hit":"","Evoke":"","Evoke Mod":["","",""],"Hit Mod":["","",""],"Roll":"","Roll Mod":["","",""]}
        for slot in range(1,5):
            self.inventory_slot = self.csheet.findChild(QLineEdit, f"inventory{slot}")
            if self.inventory_slot.text() != "":
                all_items.append(self.inventory_slot.text())
            else:
                pass

        for slot in range(1,5):
            self.update_item(slot, "", "", self.empty_slot_dict)

        misc_items = copy.deepcopy(all_items)
        self.armor_items = []
        slot = 1
        for item_type in os.listdir(cons.ITEMS):
            item_type_json = func.read_json(os.path.join(cons.ITEMS,item_type))
            for item in all_items:
                for item_key in item_type_json:
                    if item_key.lower() == item.lower():
                        this_item_type = item_type.split(".")[0].split("_")[1]
                        if this_item_type == "armor":
                            self.armor_items.append(item)
                        self.update_item(slot, item_key, this_item_type, item_type_json[item_key])
                        misc_items.remove(item)
                        slot += 1

        for item in misc_items:
            self.update_item(slot, item, "misc", self.empty_slot_dict)
            all_items.remove(item)
            slot += 1

        self.set_ac()
        self.set_hp()
        self.set_feats()

    def update_item(self, slot, item, inventory_type, inventory_item):
        self.inventory_icon = self.csheet.findChild(QToolButton, f"icon{slot}")
        self.inventory_evoke = self.csheet.findChild(QPushButton, f"evoke{slot}")
        self.inventory_hit = self.csheet.findChild(QPushButton, f"hit_dc{slot}")
        self.inventory_roll = self.csheet.findChild(QPushButton, f"roll{slot}")
        self.inventory_slot = self.csheet.findChild(QLineEdit, f"inventory{slot}")

        self.inventory_icon_label = self.csheet.findChild(QLabel, f"icon_label{slot}")
        self.inventory_evoke_label = self.csheet.findChild(QLabel, f"evoke_label{slot}")
        self.inventory_hit_label = self.csheet.findChild(QLabel, f"hit_dc_label{slot}")
        self.inventory_roll_label = self.csheet.findChild(QLabel, f"roll_label{slot}")
        self.inventory_slot_label = self.csheet.findChild(QLabel, f"inventory_label{slot}")

        inventory_widgets = [self.inventory_icon,self.inventory_evoke,self.inventory_hit,self.inventory_roll,self.inventory_slot]
        inventory_labels = [self.inventory_icon_label,self.inventory_evoke_label,self.inventory_hit_label,self.inventory_roll_label,self.inventory_slot_label]
        func.set_icon(self.inventory_icon,f"{inventory_type}.png",cons.ICON_COLOR)

        self.inventory_evoke.setText("")
        self.inventory_evoke_label.setText("")
        self.inventory_hit.setText("")
        self.inventory_hit_label.setText("")
        self.inventory_roll.setText("")
        self.inventory_roll_label.setText("")   

        # if "Evoke" in inventory_item:
        #     if inventory_item["Evoke"] != "":
        #         self.inventory_evoke.setText(self.get_action_modifier(inventory_item["Evoke"],inventory_item["Evoke Mod"]))
        #         self.inventory_evoke_label.setText(inventory_item["Evoke"])


        # if "Hit" in inventory_item:
        #     if inventory_item["Hit"] != "":
        #         self.inventory_hit.setText(self.get_action_modifier(inventory_item["Hit"],inventory_item["Hit Mod"]))
        #         self.inventory_hit_label.setText(inventory_item["Hit"])

        # if "Roll" in inventory_item:
        #     if inventory_item["Roll"] != "":
        #         self.inventory_roll.setText(self.get_roll(inventory_item["Roll Mod"],inventory_type))
        #         self.inventory_roll_label.setText(inventory_item["Roll"])
                
        self.inventory_slot.setText(item)

        if "level" in inventory_item:
            self.inventory_slot_label.setText(inventory_type.capitalize()+" "+inventory_item["level"])
        else:
            self.inventory_slot_label.setText(inventory_type.capitalize())

        if inventory_type == "damage":     
            [widget.setStyleSheet(style.INVENTORY_INJURY) for widget in inventory_widgets]
            [widget.setStyleSheet(style.INVENTORY_INJURY_LABELS) for widget in inventory_labels]
            func.set_icon(self.inventory_icon,f"{inventory_type}.png",style.INJURY_RED_BRIGHT)
        elif inventory_type != "":

            label_style = f"QLabel {{font: 10px; color:{style.TEXT_DARK_COLOR}; background-color: {cons.COLOR_LABEL[inventory_type]}; border: 0px; border-bottom: 1px solid {cons.COLOR_LABEL[inventory_type]};}}"
            label_style2 = f"QLabel {{font: 10px; color:{style.TEXT_DARK_COLOR}; background-color: {style.DARK_COLOR}; border: 0px; border-bottom: 1px solid {cons.COLOR_LABEL[inventory_type]};}}"\
                           f"QPushButton {{font: 10px; color:{style.TEXT_DARK_COLOR}; background-color: {style.DARK_COLOR}; border: 0px; border-bottom: 1px solid {cons.COLOR_LABEL[inventory_type]};}}"\

            self.inventory_icon_label.setStyleSheet(label_style)
            self.inventory_slot_label.setStyleSheet(label_style2)
            self.inventory_evoke_label.setStyleSheet(label_style2)
            self.inventory_hit_label.setStyleSheet(label_style2)
            self.inventory_roll_label.setStyleSheet(label_style2)

        else:
            [widget.setStyleSheet(style.INVENTORY) for widget in inventory_widgets]
            [widget.setStyleSheet(style.INVENTORY) for widget in inventory_labels]

        self.inventory_slot.clearFocus()        

    def set_icon(self):
        func.set_icon(self.character_icon,f"{self.character_name}.png","")


    def set_ac(self):
        ac = int(self.ac.text())
        ac += len(self.armor_items)
        self.ac.setText(str(ac))

    def set_hp(self):
        level = math.floor(float(self.level.text()))
        if level == 0:
            hp_formula = cons.HIT_DICE
            self.toughness_current.setText(str(hp_formula))
        else:
            hp_formula = (cons.HIT_DICE*level) + int(self.CON.text())
        self.toughness_max.setText(str(hp_formula))
        

    def adjust_hp(self, state, value):
        toughness_current = int(self.toughness_current.text())
        self.max_slots = int(self.CON.text())+cons.START_SLOTS

        self.toughness_current.setStyleSheet(style.BUTTONS)
        for point in range(1,int(value)+1):
            if state == "minus":
                toughness_current -= 1
                if toughness_current < 0:
                    self.add_injury()
            else:  
                if toughness_current < 0:
                    self.remove_injury()
                toughness_current += 1


        if toughness_current > int(self.toughness_max.text()):
            self.toughness_current.setText(self.toughness_max.text())
        elif toughness_current < -abs(self.max_slots):
            self.toughness_current.setText(str(-abs(self.max_slots)))
        else:
            self.toughness_current.setText(str(toughness_current))   

        if toughness_current >= 0:
            self.toughness_current.setStyleSheet(style.BIG_BUTTONS)
        else:
            self.toughness_current.setStyleSheet(style.BUTTONS_INJURY)

        self.update_sheet()

    def remove_injury(self):
        print("remove injury")
        self.empty_slot_dict = {"Hit":"","Evoke":"","Evoke Mod":["","",""],"Hit Mod":["","",""],"Roll":"","Roll Mod":["","",""]}
        self.max_slots = int(self.CON.text())+cons.START_SLOTS
        for slot in range(1,self.max_slots+1):
            widget_slot = self.csheet.findChild(QLineEdit, f"inventory{slot}")
            if widget_slot.text() == "Injury":
                self.update_item(slot, "", "", self.empty_slot_dict)
                return
            else:
                pass

    def add_injury(self):
        self.empty_slot_dict = {"Hit":"","Evoke":"","Evoke Mod":["","",""],"Hit Mod":["","",""],"Roll":"","Roll Mod":["","",""]}
        current_slots = int(self.CON.text())+cons.START_SLOTS
        free_slots = []
        for slot in range(1,current_slots+1):
            widget_slot = self.csheet.findChild(QLineEdit, f"inventory{slot}")
            if widget_slot.text() == "Injury":
                pass
            else:
                free_slots.append(slot)
        if free_slots == []:
            return
        else:
            injury_slot = random.choice(free_slots)
            self.update_item(injury_slot, "Injury", "damage", self.empty_slot_dict)

    def set_feats(self):
        current_level = math.floor(float(self.level.text()))
        if current_level < 3:
            self.feat1.setEnabled(False)
            self.feat2.setEnabled(False)
            self.feat3.setEnabled(False)
        if current_level == 3:
            self.feat1.setEnabled(True)
            self.feat2.setEnabled(False)
            self.feat3.setEnabled(False)
        elif current_level == 6:
            self.feat1.setEnabled(True)
            self.feat2.setEnabled(True)
            self.feat3.setEnabled(False)
        elif current_level == 9:
            self.feat1.setEnabled(True)
            self.feat2.setEnabled(True)
            self.feat3.setEnabled(True)

    def load_character(self, character_name):
        print(f"Loading {character_name}")
        self.character_name = character_name

        if self.character_name == "":
            return

        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]

        query = {"character": self.character_name}
        self.character_document = self.collection.find_one(query)
        if self.character_document != None:
            self.experience.setText(str(self.character_document["experience"]))
            self.experience_unspent.setText(str(self.character_document["experience unspent"]))

            self.ACC.setText(str(self.character_document["stats"]["ACCURATE"]))
            self.CUN.setText(str(self.character_document["stats"]["CUNNING"]))
            self.DIS.setText(str(self.character_document["stats"]["DISCREET"]))
            self.PER.setText(str(self.character_document["stats"]["PERSUASIVE"]))
            self.QUI.setText(str(self.character_document["stats"]["QUICK"]))
            self.RES.setText(str(self.character_document["stats"]["RESOLUTE"]))
            self.STR.setText(str(self.character_document["stats"]["STRONG"]))
            self.VIG.setText(str(self.character_document["stats"]["VIGILANT"]))

            try:
                self.toughness_current.setText(str(self.character_document["toughness current"]))

                self.corruption_permanent.setText(str(self.character_document["corruption permanent"]))
                self.corruption_temporary.setText(str(self.character_document["corruption temporary"]))

                self.ACC_mod.setText(str(self.character_document["modifiers"]["ACCURATE"]))
                self.CUN_mod.setText(str(self.character_document["modifiers"]["CUNNING"]))
                self.DIS_mod.setText(str(self.character_document["modifiers"]["DISCREET"]))
                self.PER_mod.setText(str(self.character_document["modifiers"]["PERSUASIVE"]))
                self.QUI_mod.setText(str(self.character_document["modifiers"]["QUICK"]))
                self.RES_mod.setText(str(self.character_document["modifiers"]["RESOLUTE"]))
                self.STR_mod.setText(str(self.character_document["modifiers"]["STRONG"]))
                self.VIG_mod.setText(str(self.character_document["modifiers"]["VIGILANT"]))

                self.inventory1.setText(str(self.character_document["inventory"]["inventory1"]))
                self.inventory2.setText(str(self.character_document["inventory"]["inventory2"]))
                self.inventory3.setText(str(self.character_document["inventory"]["inventory3"]))
                self.inventory4.setText(str(self.character_document["inventory"]["inventory4"]))
                self.inventory5.setText(str(self.character_document["inventory"]["inventory5"]))
                self.inventory6.setText(str(self.character_document["inventory"]["inventory6"]))
                self.inventory7.setText(str(self.character_document["inventory"]["inventory7"]))
                self.inventory8.setText(str(self.character_document["inventory"]["inventory8"]))
                self.inventory9.setText(str(self.character_document["inventory"]["inventory9"]))
                self.inventory10.setText(str(self.character_document["inventory"]["inventory10"]))
                self.inventory11.setText(str(self.character_document["inventory"]["inventory11"]))
                self.inventory12.setText(str(self.character_document["inventory"]["inventory12"]))
                self.inventory13.setText(str(self.character_document["inventory"]["inventory13"]))
                self.inventory14.setText(str(self.character_document["inventory"]["inventory14"]))
                self.inventory15.setText(str(self.character_document["inventory"]["inventory15"]))
            except:
                print("No modifiers or inventory")
                print("Likely new character")

            self.update_sheet()

    def set_sheet_vars(self, csheet):
        print("Setting sheet vars")
        self.toughness_current = csheet.toughness_current.get_widget()
        self.toughness_max = csheet.toughness_max.get_widget()
        self.toughness_threshold = csheet.toughness_threshold.get_widget()

        self.corruption_permanent = csheet.corruption_permanent.get_widget()
        self.corruption_temporary = csheet.corruption_temporary.get_widget()
        self.corruption_threshold = csheet.corruption_threshold.get_widget()

        self.ACC = csheet.findChild(QWidget, "ACCURATE")
        print(self.ACC)
        self.CUN = csheet.findChild(QWidget, "CUNNING")
        self.DIS = csheet.findChild(QWidget, "DISCREET")
        self.PER = csheet.findChild(QWidget, "PERSUASIVE")
        self.QUI = csheet.findChild(QWidget, "QUICK")
        self.RES = csheet.findChild(QWidget, "RESOLUTE")
        self.STR = csheet.findChild(QWidget, "STRONG")
        self.VIG = csheet.findChild(QWidget, "VIGILANT")
        
        self.ACC_mod = csheet.findChild(QWidget, "ACCURATE_mod")
        self.CUN_mod = csheet.findChild(QWidget, "CUNNING_mod")
        self.DIS_mod = csheet.findChild(QWidget, "DISCREET_mod")
        self.PER_mod = csheet.findChild(QWidget, "PERSUASIVE_mod")
        self.QUI_mod = csheet.findChild(QWidget, "QUICK_mod")
        self.RES_mod = csheet.findChild(QWidget, "RESOLUTE_mod")
        self.STR_mod = csheet.findChild(QWidget, "STRONG_mod")
        self.VIG_mod = csheet.findChild(QWidget, "VIGILANT_mod")

    def set_inv_vars(self, isheet):
        print("Setting inv vars")

        self.character_icon = isheet.portrait.get_widget()

        self.defense = isheet.defense.get_widget()
        self.experience = isheet.experience.get_widget()

        print(self.experience)
        self.experience_unspent = isheet.unspent_experience.get_widget()

        self.inventory1 = isheet.findChild(QWidget, "inventory1")
        self.inventory2 = isheet.findChild(QWidget, "inventory2")
        self.inventory3 = isheet.findChild(QWidget, "inventory3")
        self.inventory4 = isheet.findChild(QWidget, "inventory4")
        self.inventory5 = isheet.findChild(QWidget, "inventory5")
        self.inventory6 = isheet.findChild(QWidget, "inventory6")
        self.inventory7 = isheet.findChild(QWidget, "inventory7")
        self.inventory8 = isheet.findChild(QWidget, "inventory8")
        self.inventory9 = isheet.findChild(QWidget, "inventory9")
        self.inventory10 = isheet.findChild(QWidget, "inventory10")
        self.inventory11 = isheet.findChild(QWidget, "inventory11")
        self.inventory12 = isheet.findChild(QWidget, "inventory12")
        self.inventory13 = isheet.findChild(QWidget, "inventory13")
        self.inventory14 = isheet.findChild(QWidget, "inventory14")
        self.inventory15 = isheet.findChild(QWidget, "inventory15")

    def get_character(self):
        return self.character_name.get_widget().currentText()




    