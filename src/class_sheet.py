from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import pymongo
import constants as cons

import math
import constants as cons
import os
import template.functions as func
import random

import json
import copy

class CharacterSheet():
    def __init__(self):
        self.equipment = self.get_equipment()
        self.abilities = self.get_abilities()

    def update_sheet(self):
        print("Updating Character Sheet - Saving to DB")
        self.set_icon()      

        self.update_inventory()
        self.update_abilities()

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
            "abilities": {
                "ability1": [self.ability1.text(), self.ability1.property("Rank")],
                "ability2": [self.ability2.text(), self.ability2.property("Rank")],
                "ability3": [self.ability3.text(), self.ability3.property("Rank")],
                "ability4": [self.ability4.text(), self.ability4.property("Rank")],
                "ability5": [self.ability5.text(), self.ability5.property("Rank")],
                "ability6": [self.ability6.text(), self.ability6.property("Rank")],
                "ability7": [self.ability7.text(), self.ability7.property("Rank")],
                "ability8": [self.ability8.text(), self.ability8.property("Rank")],
                "ability9": [self.ability9.text(), self.ability9.property("Rank")],
                "ability10": [self.ability10.text(), self.ability10.property("Rank")],
                "ability11": [self.ability11.text(), self.ability11.property("Rank")],
                "ability12": [self.ability12.text(), self.ability12.property("Rank")]
            },
            "toughness current": self.toughness_current.text(),
            "corruption temporary": self.corruption_temporary.text(),
            "corruption permanent": self.corruption_permanent.text(),

        }  
        return character_sheet_dictionary

    def set_rank(self, slot, rank):
        ability_main_widget = self.csheet.findChild(QWidget, f"{slot}_section_title")
        ability_main_widget.setProperty("Rank", rank)
        self.update_sheet()

    def get_abilities(self):
        all_abilities = {}
        client = pymongo.MongoClient(cons.CONNECT)
        # get a list of collection names
        db = client["abilities"]
        collection_names = db.list_collection_names()
        for name in collection_names:
            # get a collection object
            collection = db[name]
            document = collection.find_one()
            all_abilities[name] = document
        return all_abilities

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

    def find_ability(self,item_string,item_rank):
        for category in self.abilities:
            if item_string in self.abilities[category]:
                print(f"found {item_string}")
                item_dict = self.abilities[category][item_string]
                item_dict["Name"] = item_string
                item_dict["Rank"] = item_rank
                item_dict["Category"] = category
                return item_dict
            else:
                pass
        return {"Name":"empty","Category":"","Novice":"","Adept":"","Master":"","Description":"","Rank":"Novice"}

    def update_abilities(self):
        self.all_items = []
        for ability_slot in self.ability_list:
            item_string = ability_slot.text()
            item_rank = ability_slot.property("Rank")
            if item_string == "empty":
                item_string = ability_slot.text()
            self.all_items.append(self.find_ability(item_string,item_rank))

        print("Abilities")
        print(len(self.all_items))

        priority = {'abilities': 0, 'mystical_powers': 1, 'rituals': 2, 'boons': 3, 'burdens': 4}
        self.sorted_list = sorted(self.all_items, key=lambda x: priority.get(x.get('Category', ''), len(priority)))
        for slot,item in enumerate(self.sorted_list):
            self.update_ability(slot+1, item)

    def update_ability(self, slot, item):
        ability_slot = f"ability{slot}"

        ability_rank = item["Rank"]
        ability_text = item[ability_rank]

        if ability_text == "":
            ability_text = item["Description"]

        add_ability_button = self.csheet.findChild(QWidget, f"{ability_slot}")

        slot_section = self.csheet.findChild(QWidget, f"{ability_slot}_section")
        slot_section_icon = slot_section.get_title()[0]
        slot_section_label =  slot_section.get_title()[1]

        func.set_icon(slot_section_icon, f'{item["Category"]}.png',cons.ICON_COLOR)
        slot_section_label.setText(item["Name"])

        slot_main_label = self.csheet.findChild(QWidget, f"{ability_slot}_label")
        slot_main_label.setText(ability_text)

        slot_section.setHidden(False)

        if item["Name"] == "empty":
            add_ability_button.setHidden(False)
            slot_section.setHidden(True)
        else:
            add_ability_button.setHidden(True)
            slot_section.setHidden(False)

        print(f"{ability_slot} {item['Name']} {item['Rank']}")

        # Reset all colors
        novice = self.csheet.findChild(QPushButton, f"{ability_slot}_Novice")
        adept = self.csheet.findChild(QPushButton, f"{ability_slot}_Adept")
        master = self.csheet.findChild(QPushButton, f"{ability_slot}_Master")

        print(f"{novice} {adept} {master}")

        level_list = [novice, adept, master]
        #[level_widget.setStyleSheet(tstyle.LEVEL_BUTTONS_DISABLED) for level_widget in level_list]

        active_rank = self.csheet.findChild(QPushButton, f"{ability_slot}_{ability_rank}")
        #active_rank.setStyleSheet(tstyle.LEVEL_BUTTONS)

    def find_ability_category(self):
        for category in self.abilities:
            if self.ability_name in self.abilities[category]:
                return category
            else:
                return ""


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
            self.update_item(slot+1, item)

    def update_item(self, slot, item):
        self.inventory_icon = self.isheet.findChild(QToolButton, f"icon{slot}")
        self.inventory_quality = self.isheet.findChild(QPushButton, f"quality{slot}")
        self.inventory_roll = self.isheet.findChild(QPushButton, f"roll{slot}")
        self.inventory_slot = self.isheet.findChild(QLineEdit, f"item{slot}")

        self.inventory_icon_label = self.isheet.findChild(QLabel, f"icon_label{slot}")
        self.inventory_quality_label = self.isheet.findChild(QLabel, f"quality_label{slot}")
        self.inventory_roll_label = self.isheet.findChild(QLabel, f"roll_label{slot}")
        self.inventory_slot_label = self.isheet.findChild(QLabel, f"inventory_label{slot}")

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

        #Updating the character sheet gui
        self.isheet = isheet
        #

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

                self.ability1.setText(str(self.character_document["abilities"]["ability1"][0]))
                self.ability2.setText(str(self.character_document["abilities"]["ability2"][0]))
                self.ability3.setText(str(self.character_document["abilities"]["ability3"][0]))
                self.ability4.setText(str(self.character_document["abilities"]["ability4"][0]))
                self.ability5.setText(str(self.character_document["abilities"]["ability5"][0]))
                self.ability6.setText(str(self.character_document["abilities"]["ability6"][0]))
                self.ability7.setText(str(self.character_document["abilities"]["ability7"][0]))
                self.ability8.setText(str(self.character_document["abilities"]["ability8"][0]))
                self.ability9.setText(str(self.character_document["abilities"]["ability9"][0]))
                self.ability10.setText(str(self.character_document["abilities"]["ability10"][0]))
                self.ability11.setText(str(self.character_document["abilities"]["ability11"][0]))
                self.ability12.setText(str(self.character_document["abilities"]["ability12"][0]))

                self.ability1.setProperty("Rank",str(self.character_document["abilities"]["ability1"][1]))
                self.ability2.setProperty("Rank",str(self.character_document["abilities"]["ability2"][1]))
                self.ability3.setProperty("Rank",str(self.character_document["abilities"]["ability3"][1]))
                self.ability4.setProperty("Rank",str(self.character_document["abilities"]["ability4"][1]))
                self.ability5.setProperty("Rank",str(self.character_document["abilities"]["ability5"][1]))
                self.ability6.setProperty("Rank",str(self.character_document["abilities"]["ability6"][1]))
                self.ability7.setProperty("Rank",str(self.character_document["abilities"]["ability7"][1]))
                self.ability8.setProperty("Rank",str(self.character_document["abilities"]["ability8"][1]))
                self.ability9.setProperty("Rank",str(self.character_document["abilities"]["ability9"][1]))
                self.ability10.setProperty("Rank",str(self.character_document["abilities"]["ability10"][1]))
                self.ability11.setProperty("Rank",str(self.character_document["abilities"]["ability11"][1]))
                self.ability12.setProperty("Rank",str(self.character_document["abilities"]["ability12"][1]))

            except:
                print("No modifiers or inventory")
                print("Likely new character")

            self.update_sheet()

    def set_sheet_vars(self, csheet):
        print("Setting sheet vars")
        self.csheet = csheet        

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

        self.ability1 = csheet.findChild(QWidget, "ability1_section_title")
        self.ability2 = csheet.findChild(QWidget, "ability2_section_title")
        self.ability3 = csheet.findChild(QWidget, "ability3_section_title")
        self.ability4 = csheet.findChild(QWidget, "ability4_section_title")
        self.ability5 = csheet.findChild(QWidget, "ability5_section_title")
        self.ability6 = csheet.findChild(QWidget, "ability6_section_title")
        self.ability7 = csheet.findChild(QWidget, "ability7_section_title")
        self.ability8 = csheet.findChild(QWidget, "ability8_section_title")
        self.ability9 = csheet.findChild(QWidget, "ability9_section_title")
        self.ability10 = csheet.findChild(QWidget, "ability10_section_title")
        self.ability11 = csheet.findChild(QWidget, "ability11_section_title")
        self.ability12 = csheet.findChild(QWidget, "ability12_section_title")

        self.ability_list = [self.ability1, self.ability2, self.ability3, self.ability4, self.ability5, self.ability6, self.ability7, self.ability8, self.ability9, self.ability10, self.ability11, self.ability12]

    def set_inv_vars(self, isheet):
        print("Setting inv vars")
        self.isheet = isheet

        self.character_icon = self.isheet.portrait.get_widget()
    
        self.defense = self.isheet.defense.get_widget()
        self.experience = self.isheet.experience.get_widget()

        print(self.experience)
        self.experience_unspent = self.isheet.unspent_experience.get_widget()

        self.inventory1 = self.isheet.findChild(QWidget, "item1")
        self.inventory2 = self.isheet.findChild(QWidget, "item2")
        self.inventory3 = self.isheet.findChild(QWidget, "item3")
        self.inventory4 = self.isheet.findChild(QWidget, "item4")
        self.inventory5 = self.isheet.findChild(QWidget, "item5")
        self.inventory6 = self.isheet.findChild(QWidget, "item6")
        self.inventory7 = self.isheet.findChild(QWidget, "item7")
        self.inventory8 = self.isheet.findChild(QWidget, "item8")
        self.inventory9 = self.isheet.findChild(QWidget, "item9")
        self.inventory10 = self.isheet.findChild(QWidget, "item10")
        self.inventory11 = self.isheet.findChild(QWidget, "item11")
        self.inventory12 = self.isheet.findChild(QWidget, "item12")
        self.inventory13 = self.isheet.findChild(QWidget, "item13")
        self.inventory14 = self.isheet.findChild(QWidget, "item14")
        self.inventory15 = self.isheet.findChild(QWidget, "item15")

        self.inventory_list = [self.inventory1, self.inventory2, self.inventory3, self.inventory4, self.inventory5, self.inventory6, self.inventory7, self.inventory8, self.inventory9, self.inventory10, self.inventory11, self.inventory12, self.inventory13, self.inventory14, self.inventory15]

    def get_character(self):
        return self.character_name.get_widget().currentText()




    