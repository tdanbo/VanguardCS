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
        self.equipment = self.get_equipment()

    def update_sheet(self):
        self.set_icon()      

        self.set_stats()
        self.set_toughness()
        self.set_corruption()
        self.set_defense()

        updated_character_sheet = self.update_dictionary()
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
    
    def get_equipment(self):
        all_equipment = {}
        client = pymongo.MongoClient(cons.CONNECT)
        # get a list of collection names
        db = client["equipment"]
        collection_names = db.list_collection_names()
        for name in collection_names:
            # get a collection object
            collection = db[name]
            document = collection.find_one()
            all_equipment[name] = document
        return all_equipment

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

    def update_inventory(self, isheet):
        self.all_items = []
        for inventory_slot in self.inventory_list:
            item_string = inventory_slot.text().lower()
            if item_string == "":
                item_string = inventory_slot.objectName()
            self.all_items.append(self.find_item(item_string))

        print(self.all_items)

        priority = {'melee': 0, 'ranged': 1, 'armor': 2, 'elixirs': 3}
        self.sorted_list = sorted(self.all_items, key=lambda x: priority.get(x.get('Category', ''), len(priority)))
        for slot,item in enumerate(self.sorted_list):
            self.update_item(isheet, slot+1, item)
        self.update_sheet()

    def update_item(self, isheet, slot, item):
        self.inventory_icon = isheet.findChild(QToolButton, f"icon{slot}")
        self.inventory_quality = isheet.findChild(QPushButton, f"quality{slot}")
        self.inventory_roll = isheet.findChild(QPushButton, f"roll{slot}")
        self.inventory_slot = isheet.findChild(QLineEdit, f"item{slot}")

        self.inventory_icon_label = isheet.findChild(QLabel, f"icon_label{slot}")
        self.inventory_quality_label = isheet.findChild(QLabel, f"quality_label{slot}")
        self.inventory_roll_label = isheet.findChild(QLabel, f"roll_label{slot}")
        self.inventory_slot_label = isheet.findChild(QLabel, f"inventory_label{slot}")

        self.inventory_slot.setText(item["Name"])
        self.inventory_slot_label.setText(item["Category"])

        self.inventory_roll.setText(item["Roll"][1])
        self.inventory_roll_label.setText(item["Roll"][0])
        
        if "Quality" in item:
            self.inventory_quality.setText(",".join(item["Quality"]))
            self.inventory_quality_label.setText("Quality")
        else:
            self.inventory_quality.setText("")
            self.inventory_quality_label.setText("")

    def find_item(self,item_string):
        for category in self.equipment:
            for item in self.equipment[category]:
                if item_string == item.lower():
                    print(f"found {item}")
                    item_dict = self.equipment[category][item]
                    item_dict["Name"] = item
                    item_dict["Category"] = category
                    return item_dict
                else:
                    pass
        return {"Name":"","Category":"","Roll":["",""]}
        

    def set_icon(self):
        func.set_icon(self.character_icon,f"{self.character_name}.png","")

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

    def load_character(self, isheet, character_name):
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

            self.update_inventory(isheet)
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

        self.inventory1 = isheet.findChild(QWidget, "item1")
        self.inventory2 = isheet.findChild(QWidget, "item2")
        self.inventory3 = isheet.findChild(QWidget, "item3")
        self.inventory4 = isheet.findChild(QWidget, "item4")
        self.inventory5 = isheet.findChild(QWidget, "item5")
        self.inventory6 = isheet.findChild(QWidget, "item6")
        self.inventory7 = isheet.findChild(QWidget, "item7")
        self.inventory8 = isheet.findChild(QWidget, "item8")
        self.inventory9 = isheet.findChild(QWidget, "item9")
        self.inventory10 = isheet.findChild(QWidget, "item10")
        self.inventory11 = isheet.findChild(QWidget, "item11")
        self.inventory12 = isheet.findChild(QWidget, "item12")
        self.inventory13 = isheet.findChild(QWidget, "item13")
        self.inventory14 = isheet.findChild(QWidget, "item14")
        self.inventory15 = isheet.findChild(QWidget, "item15")

        self.inventory_list = [self.inventory1, self.inventory2, self.inventory3, self.inventory4, self.inventory5, self.inventory6, self.inventory7, self.inventory8, self.inventory9, self.inventory10, self.inventory11, self.inventory12, self.inventory13, self.inventory14, self.inventory15]

    def get_character(self):
        return self.character_name.get_widget().currentText()




    