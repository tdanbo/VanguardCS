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
    def __init__(self, character_gui, inventory_gui):
        print("---------------------------") 
        print("Character Sheet Created")

        self.csheet = character_gui
        self.invsheet = inventory_gui

        self.stat_button = None

        self.character_icon = self.invsheet.portrait.get_widget()
        self.character = self.invsheet.character_name.get_widget()
        self.experience = self.invsheet.findChild(QWidget,"experience")
        self.experience_unspent = self.invsheet.findChild(QWidget,"unspent_experience")

        #hp
        self.toughness_current = self.csheet.toughness_current.get_widget()
        self.toughness_max = self.csheet.toughness_max.get_widget()
        self.toughness_threshold = self.csheet.toughness_threshold.get_widget()

        #corruption
        self.corruption_temporary = self.csheet.corruption_temporary.get_widget()
        self.corruption_permanent = self.csheet.corruption_permanent.get_widget()
        self.corruption_threshold = self.csheet.corruption_threshold.get_widget()

        #defense
        self.defense = self.invsheet.defense.get_widget()

        self.hp_adjuster = self.csheet.findChild(QLineEdit, "hp_adjuster")

        #feats
        self.feat1 = self.csheet.findChild(QToolButton, "feat1")
        self.feat2 = self.csheet.findChild(QToolButton, "feat2")
        self.feat3 = self.csheet.findChild(QToolButton, "feat3")

        #stats
        self.ACC = self.csheet.findChild(QWidget, "ACCURATE")
        self.CUN = self.csheet.findChild(QWidget, "CUNNING")
        self.DIS = self.csheet.findChild(QWidget, "DISCREET")
        self.PER = self.csheet.findChild(QWidget, "PERSUASIVE")
        self.QUI = self.csheet.findChild(QWidget, "QUICK")
        self.RES = self.csheet.findChild(QWidget, "RESOLUTE")
        self.STR = self.csheet.findChild(QWidget, "STRONG")
        self.VIG = self.csheet.findChild(QWidget, "VIGILANT")

        #stat modifiers
        self.ACC_mod = self.csheet.findChild(QWidget, "ACCURATE_mod")
        self.CUN_mod = self.csheet.findChild(QWidget, "CUNNING_mod")
        self.DIS_mod = self.csheet.findChild(QWidget, "DISCREET_mod")
        self.PER_mod = self.csheet.findChild(QWidget, "PERSUASIVE_mod")
        self.QUI_mod = self.csheet.findChild(QWidget, "QUICK_mod")
        self.RES_mod = self.csheet.findChild(QWidget, "RESOLUTE_mod")
        self.STR_mod = self.csheet.findChild(QWidget, "STRONG_mod")
        self.VIG_mod = self.csheet.findChild(QWidget, "VIGILANT_mod")

        #all inventory slots
        self.inventory1 = self.invsheet.findChild(QLineEdit, "inventory1")
        self.inventory2 = self.invsheet.findChild(QLineEdit, "inventory2")
        self.inventory3 = self.invsheet.findChild(QLineEdit, "inventory3")
        self.inventory4 = self.invsheet.findChild(QLineEdit, "inventory4")
        self.inventory5 = self.invsheet.findChild(QLineEdit, "inventory5")
        self.inventory6 = self.invsheet.findChild(QLineEdit, "inventory6")
        self.inventory7 = self.invsheet.findChild(QLineEdit, "inventory7")
        self.inventory8 = self.invsheet.findChild(QLineEdit, "inventory8")
        self.inventory9 = self.invsheet.findChild(QLineEdit, "inventory9")
        self.inventory10 = self.invsheet.findChild(QLineEdit, "inventory10")
        self.inventory11 = self.invsheet.findChild(QLineEdit, "inventory11")
        self.inventory12 = self.invsheet.findChild(QLineEdit, "inventory12")
        self.inventory13 = self.invsheet.findChild(QLineEdit, "inventory13")
        self.inventory14 = self.invsheet.findChild(QLineEdit, "inventory14")
        self.inventory15 = self.invsheet.findChild(QLineEdit, "inventory15")

    def update_character_dropdown(self):
        print("Updating Character Dropdown")
        self.character.clear()
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]
        character_list = self.collection.distinct("character")
        self.character.addItems(character_list)

    def update_dictionary(self):
        print("Updating Character Sheet Dictionary")    
        character_sheet_dictionary = {
            "character": self.character.currentText(),
            "rank": "Player",
            "experience": self.experience.text(),
            "experience unspent": self.experience_unspent.text(),
            "toughness current": self.toughness_current.text(),
            "stats": {
                "ACCURATE": int(self.ACC.text()),
                "CUNNING": int(self.CUN.text()),
                "DISCREET": int(self.DIS.text()),
                "PERSUASIVE": int(self.PER.text()),
                "QUICK": int(self.QUI.text()),
                "RESOLUTE": int(self.RES.text()),
                "STRONG": int(self.STR.text()),
                "VIGILANT": int(self.VIG.text())
            },
            "modifiers": {
                "ACCURATE": int(self.ACC_mod.text()),
                "CUNNING": int(self.CUN_mod.text()),
                "DISCREET": int(self.DIS_mod.text()),
                "PERSUASIVE": int(self.PER_mod.text()),
                "QUICK": int(self.QUI_mod.text()),
                "RESOLUTE": int(self.RES_mod.text()),
                "STRONG": int(self.STR_mod.text()),
                "VIGILANT": int(self.VIG_mod.text())
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
        }        
        return character_sheet_dictionary
    
    def update_database(self, directory):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]

        #print(self.character.currentText())

        query = {"character": self.character.currentText()}
        document = self.collection.find_one(query)

        if document is not None:
            new_values = {"$set": directory}
            self.collection.update_one(query, new_values)
        else:
            self.collection.insert_one(directory)

    def update_sheet(self):
        self.set_stats()

        self.set_toughness()
        self.set_corruption()
        self.set_defense()

        self.set_icon()      
        # self.update_inventory()
        updated_character_sheet = self.update_dictionary()
        self.update_database(updated_character_sheet)

    # ITERATE OVER ITEM JSON TO FIND ITEM

    def set_stats(self):
        for widget in [self.ACC, self.CUN, self.DIS, self.PER, self.QUI, self.RES, self.STR, self.VIG]:
            base_objectname = widget.objectName()
            modifier = self.csheet.findChild(QWidget, base_objectname+"_mod")
            widget.setText(str(int(widget.text())+int(modifier.text())))
            if int(modifier.text()) == 0:
                modifier.setHidden(True)

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
        character_name = self.character.currentText().lower()
        func.set_icon(self.character_icon,f"{character_name}.png","")


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

    def load_character(self):
        print(f"Loading {self.character.currentText()}")
        if self.character.currentText() == "":
            return
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]

        query = {"character": self.character.currentText()}
        document = self.collection.find_one(query)
        if document != None:
            print(document)
            self.experience.setText(str(document["experience"]))
            self.experience_unspent.setText(str(document["experience unspent"]))
            
            self.toughness_current.setText(str(document["toughness current"]))

            self.ACC.setText(str(document["stats"]["ACCURATE"]))
            self.CUN.setText(str(document["stats"]["CUNNING"]))
            self.DIS.setText(str(document["stats"]["DISCREET"]))
            self.PER.setText(str(document["stats"]["PERSUASIVE"]))
            self.QUI.setText(str(document["stats"]["QUICK"]))
            self.RES.setText(str(document["stats"]["RESOLUTE"]))
            self.STR.setText(str(document["stats"]["STRONG"]))
            self.VIG.setText(str(document["stats"]["VIGILANT"]))

            self.inventory1.setText(str(document["inventory"]["inventory1"]))
            self.inventory2.setText(str(document["inventory"]["inventory2"]))
            self.inventory3.setText(str(document["inventory"]["inventory3"]))
            self.inventory4.setText(str(document["inventory"]["inventory4"]))
            self.inventory5.setText(str(document["inventory"]["inventory5"]))
            self.inventory6.setText(str(document["inventory"]["inventory6"]))
            self.inventory7.setText(str(document["inventory"]["inventory7"]))
            self.inventory8.setText(str(document["inventory"]["inventory8"]))
            self.inventory9.setText(str(document["inventory"]["inventory9"]))
            self.inventory10.setText(str(document["inventory"]["inventory10"]))
            self.inventory11.setText(str(document["inventory"]["inventory11"]))
            self.inventory12.setText(str(document["inventory"]["inventory12"]))
            self.inventory13.setText(str(document["inventory"]["inventory13"]))
            self.inventory14.setText(str(document["inventory"]["inventory14"]))
            self.inventory15.setText(str(document["inventory"]["inventory15"]))

            self.update_sheet()
                
    def get_character(self):
        return self.character_name.get_widget().currentText()




    