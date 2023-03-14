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

import re

from gui_windows.gui_inventory_frame import InventoryItem
from gui_windows.gui_ability_frame import AbilityItem
from gui_functions.class_modify_stat import ModifyStat

class CharacterSheet(QWidget):
    def __init__(self):
        super().__init__()
        self.equipment = self.get_equipment()

    def update_sheet(self):
        print("Updating Character Sheet - Saving to DB")
        self.set_icon()      

        self.update_inventory()
        self.update_equip()
        self.update_abilities()

        self.set_stats()
        self.modify_stats()
        
        self.set_health() # This will set static toughness, corruption, and defense stats

        self.update_experience()

        self.update_database()

    def update_experience(self):
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

        self.XP.setText(str(earned_experience))
        self.UXP.setText(str(total_experience-earned_experience))

    def find_modifier(self, string):
        match = re.search(r'-?\d+', string)  # search for a sequence of digits with an optional minus sign
        if match:
            integer_value = int(match.group())  # extract the matched string and convert it to an integer
            return integer_value  # outputs: -4
        else:
            print("No integer value found.")

    def set_rank(self, slot, rank):
        ability_main_widget = self.csheet.findChild(QWidget, f"{slot}_section_title")
        ability_main_widget.setProperty("Rank", rank)
        self.update_sheet()

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

    def update_abilities(self):
        func.clear_layout(self.csheet.ability_layout.inner_layout(1))
        priority = {'abilities': 0, 'mystical_powers': 1, 'rituals': 2, 'boons': 3, 'burdens': 4}
        self.sorted_list = sorted(self.CHARACTER_DOC["abilities"], key=lambda x: priority.get(x.get('Category', ''), len(priority)))
        for slot,item in enumerate(self.sorted_list):
            ability = AbilityItem(self,item,slot=slot)
            self.csheet.ability_layout.inner_layout(1).addWidget(ability)
        filler_widget = QWidget()
        filler_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.csheet.ability_layout.inner_layout(1).addWidget(filler_widget)

    def update_database(self):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]

        query = {"character": self.character_name}
        document = self.collection.find_one(query)

        if document is not None:
            new_values = {"$set": self.CHARACTER_DOC}
            self.collection.update_one(query, new_values)
        else:
            print("No document found")

    # ITERATE OVER ITEM JSON TO FIND ITEM

    def set_stats(self):
        print("setting stats")
        self.ACC.setText(str(self.CHARACTER_DOC["stats"]["ACCURATE"]))
        self.CUN.setText(str(self.CHARACTER_DOC["stats"]["CUNNING"]))
        self.DIS.setText(str(self.CHARACTER_DOC["stats"]["DISCREET"]))
        self.PER.setText(str(self.CHARACTER_DOC["stats"]["PERSUASIVE"]))
        self.QUI.setText(str(self.CHARACTER_DOC["stats"]["QUICK"]))
        self.RES.setText(str(self.CHARACTER_DOC["stats"]["RESOLUTE"]))
        self.STR.setText(str(self.CHARACTER_DOC["stats"]["STRONG"]))
        self.VIG.setText(str(self.CHARACTER_DOC["stats"]["VIGILANT"]))

        self.TOU.setText(str(self.CHARACTER_DOC["TOUGHNESS"]))
        self.COR.setText(str(self.CHARACTER_DOC["CORRUPTION"]))
        self.PERC.setText(str(self.CHARACTER_DOC["PERMANENT"]))

        self.ACC_mod.setText(str(self.CHARACTER_DOC["stats"]["ACCURATE mod"]))
        self.CUN_mod.setText(str(self.CHARACTER_DOC["stats"]["CUNNING mod"]))
        self.DIS_mod.setText(str(self.CHARACTER_DOC["stats"]["DISCREET mod"]))
        self.PER_mod.setText(str(self.CHARACTER_DOC["stats"]["PERSUASIVE mod"]))
        self.QUI_mod.setText(str(self.CHARACTER_DOC["stats"]["QUICK mod"]))
        self.RES_mod.setText(str(self.CHARACTER_DOC["stats"]["RESOLUTE mod"]))
        self.STR_mod.setText(str(self.CHARACTER_DOC["stats"]["STRONG mod"]))
        self.VIG_mod.setText(str(self.CHARACTER_DOC["stats"]["VIGILANT mod"]))
        
        if self.CHARACTER_DOC["DEFENSE mod"] != 0:
            self.DEF_mod.setText("DEFENSE "+str(self.CHARACTER_DOC["DEFENSE mod"]))
        else:
            self.DEF_mod.setText("DEFENSE")

        if self.CHARACTER_DOC["CASTING mod"] != 0:
            self.CAS_mod.setText("CASTING "+str(self.CHARACTER_DOC["CASTING mod"]))
        else:
            self.CAS_mod.setText("CASTING")

    def modify_stats(self):
        for widget in [
            (self.ACC, self.ACC_mod), 
            (self.CUN, self.CUN_mod), 
            (self.DIS, self.DIS_mod), 
            (self.PER, self.PER_mod), 
            (self.QUI, self.QUI_mod), 
            (self.RES, self.RES_mod), 
            (self.STR, self.STR_mod), 
            (self.VIG, self.VIG_mod),
            ]:
            modifier_string = widget[1].text()
            modifier_int = ModifyStat(modifier_string).find_integer()

            stat = int(self.CHARACTER_DOC["stats"][widget[0].objectName()])
            modified_stat = stat + modifier_int
            widget[0].setText(str(modified_stat))

    def set_health(self):
        strong = int(self.STR.text())
        max_toughness = 10 if strong < 10 else strong

        pain_threshold = math.ceil(strong/2)

        self.MAX.setText(str(max_toughness))
        self.PAI.setText(str(pain_threshold))

        corruption_threshold = math.ceil(int(self.RES.text())/2)
        self.THR.setText(f"{corruption_threshold} / {self.RES.text()}")

        defense = int(self.QUI.text()) + self.CHARACTER_DOC["DEFENSE mod"]
        casting = int(self.RES.text()) + self.CHARACTER_DOC["CASTING mod"]
        quick = int(self.QUI.text()) + self.CHARACTER_DOC["SPEED mod"]

        self.DEF.setText(str(defense))
        self.CAS.setText(str(casting))
        self.QUI.setText(str(quick))


    def update_equip(self):
        func.clear_layout(self.isheet.equipment_layout.inner_layout(1))

        self.mainhand_slot = InventoryItem(self, 2, self.CHARACTER_DOC["equipment"]["armor"], equipment="AR")
        self.offhand_slot = InventoryItem(self, 3, self.CHARACTER_DOC["equipment"]["main hand"], equipment="MH")
        self.armor_slot = InventoryItem(self, 4, self.CHARACTER_DOC["equipment"]["off hand"], equipment="OH")

        self.isheet.equipment_layout.inner_layout(1).addWidget(self.mainhand_slot)
        self.add_divier(self.isheet.equipment_layout.inner_layout(1))
        self.isheet.equipment_layout.inner_layout(1).addWidget(self.offhand_slot)
        self.add_divier(self.isheet.equipment_layout.inner_layout(1))
        self.isheet.equipment_layout.inner_layout(1).addWidget(self.armor_slot)

    def update_inventory(self):
        func.clear_layout(self.isheet.inventory_scroll.inner_layout(1))

        priority = {'melee': 0, 'ranged': 1, 'armor': 2, 'elixirs': 3}
        sorted_list = sorted(self.CHARACTER_DOC["inventory"], key=lambda x: priority.get(x.get('Category', ''), len(priority)))
        self.CHARACTER_DOC["inventory"] = sorted_list

        for count in range(20,-1,-1):
            try:
                item_dict = self.CHARACTER_DOC["inventory"][count]
            except:
                item_dict = {}
            
            item_widget = InventoryItem(self, count, item_dict)
            item_widget.item.get_widget().editingFinished.connect(self.update_inventory_dict)
            self.isheet.inventory_scroll.inner_layout(1).addWidget(item_widget)
                
            self.add_divier(self.isheet.inventory_scroll.inner_layout(1))

    def add_divier(self, layout):
        self.divider = QFrame()
        self.divider.setFixedHeight(1)
        self.divider.setStyleSheet(f"background-color: {cons.BORDER}")
        layout.addWidget(self.divider)

    def update_inventory_dict(self):
        item = self.sender().text()
        slot = int(self.sender().objectName())
        item_dict = self.find_item(item)

        if item_dict == {}:
            try:
                self.CHARACTER_DOC["inventory"].pop(slot)
            except:
                pass
        else:
            try:
                self.CHARACTER_DOC["inventory"][slot] = item_dict
            except:
                self.CHARACTER_DOC["inventory"].append(item_dict)

        self.update_sheet()

    def find_item(self,item_string):
        print(f"Searching for {item_string}")
        for category in self.equipment:
            for item in self.equipment[category]:
                if item_string.lower() == item.lower():
                    item_dict = self.equipment[category][item]
                    item_dict["Name"] = item
                    item_dict["Category"] = category
                    item_dict["Equipped"] = {}
                    item_dict["Equipped"]["1"] = False
                    item_dict["Equipped"]["2"] = False
                    return item_dict
                else:
                    pass
        return {} # If item not found, return empty dictionary
        

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
        self.CHARACTER_DOC = self.collection.find_one(query)

        # if self.CHARACTER_DOC != None:
        #     self.experience.setText(str(self.CHARACTER_DOC["experience"]))
        #     self.experience_unspent.setText(str(self.CHARACTER_DOC["experience unspent"]))

        #     self.ACC.setText(str(self.CHARACTER_DOC["stats"]["ACCURATE"]))
        #     self.CUN.setText(str(self.CHARACTER_DOC["stats"]["CUNNING"]))
        #     self.DIS.setText(str(self.CHARACTER_DOC["stats"]["DISCREET"]))
        #     self.PER.setText(str(self.CHARACTER_DOC["stats"]["PERSUASIVE"]))
        #     self.QUI.setText(str(self.CHARACTER_DOC["stats"]["QUICK"]))
        #     self.RES.setText(str(self.CHARACTER_DOC["stats"]["RESOLUTE"]))
        #     self.STR.setText(str(self.CHARACTER_DOC["stats"]["STRONG"]))
        #     self.VIG.setText(str(self.CHARACTER_DOC["stats"]["VIGILANT"]))

        #     try:
        #         self.toughness_current.setText(str(self.CHARACTER_DOC["toughness current"]))

        #         self.corruption_permanent.setText(str(self.CHARACTER_DOC["corruption permanent"]))
        #         self.corruption_temporary.setText(str(self.CHARACTER_DOC["corruption temporary"]))

        #         self.DEF_mod.setText(str(self.CHARACTER_DOC["modifiers"]["DEFENSE"]))
        #         self.ACC_mod.setText(str(self.CHARACTER_DOC["modifiers"]["ACCURATE"]))
        #         self.CUN_mod.setText(str(self.CHARACTER_DOC["modifiers"]["CUNNING"]))
        #         self.DIS_mod.setText(str(self.CHARACTER_DOC["modifiers"]["DISCREET"]))
        #         self.PER_mod.setText(str(self.CHARACTER_DOC["modifiers"]["PERSUASIVE"]))
        #         self.QUI_mod.setText(str(self.CHARACTER_DOC["modifiers"]["QUICK"]))
        #         self.RES_mod.setText(str(self.CHARACTER_DOC["modifiers"]["RESOLUTE"]))
        #         self.STR_mod.setText(str(self.CHARACTER_DOC["modifiers"]["STRONG"]))
        #         self.VIG_mod.setText(str(self.CHARACTER_DOC["modifiers"]["VIGILANT"]))

        #         self.ability1.setText(str(self.CHARACTER_DOC["abilities"]["ability1"][0]))
        #         self.ability2.setText(str(self.CHARACTER_DOC["abilities"]["ability2"][0]))
        #         self.ability3.setText(str(self.CHARACTER_DOC["abilities"]["ability3"][0]))
        #         self.ability4.setText(str(self.CHARACTER_DOC["abilities"]["ability4"][0]))
        #         self.ability5.setText(str(self.CHARACTER_DOC["abilities"]["ability5"][0]))
        #         self.ability6.setText(str(self.CHARACTER_DOC["abilities"]["ability6"][0]))
        #         self.ability7.setText(str(self.CHARACTER_DOC["abilities"]["ability7"][0]))
        #         self.ability8.setText(str(self.CHARACTER_DOC["abilities"]["ability8"][0]))
        #         self.ability9.setText(str(self.CHARACTER_DOC["abilities"]["ability9"][0]))
        #         self.ability10.setText(str(self.CHARACTER_DOC["abilities"]["ability10"][0]))
        #         self.ability11.setText(str(self.CHARACTER_DOC["abilities"]["ability11"][0]))
        #         self.ability12.setText(str(self.CHARACTER_DOC["abilities"]["ability12"][0]))

        #         self.ability1.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability1"][1]))
        #         self.ability2.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability2"][1]))
        #         self.ability3.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability3"][1]))
        #         self.ability4.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability4"][1]))
        #         self.ability5.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability5"][1]))
        #         self.ability6.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability6"][1]))
        #         self.ability7.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability7"][1]))
        #         self.ability8.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability8"][1]))
        #         self.ability9.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability9"][1]))
        #         self.ability10.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability10"][1]))
        #         self.ability11.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability11"][1]))
        #         self.ability12.setProperty("Rank",str(self.CHARACTER_DOC["abilities"]["ability12"][1]))

        #     except:
        #         print("No modifiers or inventory")
        #         print("Likely new character")

        self.update_sheet()

    def set_sheet_vars(self, csheet):
        print("Setting sheet vars")
        self.csheet = csheet        
        
        self.TOU = csheet.findChild(QWidget, "TOUGHNESS")
        self.TOU_mod = csheet.findChild(QWidget, "TOUGHNESS_mod")
        self.MAX = csheet.findChild(QWidget, "MAXIMUM")
        self.MAX_mod = csheet.findChild(QWidget, "MAXIMUM_mod")
        self.PAI = csheet.findChild(QWidget, "PAIN")
        self.PAI_mod = csheet.findChild(QWidget, "PAIN_mod")

        self.COR = csheet.findChild(QWidget, "CORRUPTION")
        self.COR_mod = csheet.findChild(QWidget, "CORRUPTION_mod")
        self.PERC = csheet.findChild(QWidget, "PERMANENT")
        self.PERC_mod = csheet.findChild(QWidget, "PERMANENT_mod")
        self.THR = csheet.findChild(QWidget, "THRESHOLD")
        self.THR_mod = csheet.findChild(QWidget, "THRESHOLD_mod")

        self.ACC = csheet.findChild(QWidget, "ACCURATE")
        self.CUN = csheet.findChild(QWidget, "CUNNING")
        self.DIS = csheet.findChild(QWidget, "DISCREET")
        self.PER = csheet.findChild(QWidget, "PERSUASIVE")
        self.QUI = csheet.findChild(QWidget, "QUICK")
        self.RES = csheet.findChild(QWidget, "RESOLUTE")
        self.STR = csheet.findChild(QWidget, "STRONG")
        self.VIG = csheet.findChild(QWidget, "VIGILANT")
        
        self.DEF_mod = csheet.findChild(QWidget, "DEFENSE mod")
        self.ACC_mod = csheet.findChild(QWidget, "ACCURATE mod")
        self.CUN_mod = csheet.findChild(QWidget, "CUNNING mod")
        self.DIS_mod = csheet.findChild(QWidget, "DISCREET mod")
        self.PER_mod = csheet.findChild(QWidget, "PERSUASIVE mod")
        self.QUI_mod = csheet.findChild(QWidget, "QUICK mod")
        self.RES_mod = csheet.findChild(QWidget, "RESOLUTE mod")
        self.STR_mod = csheet.findChild(QWidget, "STRONG mod")
        self.VIG_mod = csheet.findChild(QWidget, "VIGILANT mod")

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

    def set_combat_log(self, clog):
        self.combat_log = clog

    def set_inv_vars(self, isheet):
        print("Setting inv vars")
        self.isheet = isheet

        self.character_icon = self.isheet.portrait.get_widget()

        self.XP = isheet.findChild(QWidget, "experience")
        self.UXP = isheet.findChild(QWidget, "total experience")

        self.DEF = isheet.findChild(QWidget, "DEFENSE")
        self.DEF_mod = isheet.findChild(QWidget, "DEFENSE mod")

        self.CAS = isheet.findChild(QWidget, "CASTING")
        self.CAS_mod = isheet.findChild(QWidget, "CASTING mod")

        self.experience = self.isheet.experience.get_widget()

        self.experience_unspent = self.isheet.unspent_experience.get_widget()

    def get_character(self):
        return self.character_name.get_widget().currentText()
    