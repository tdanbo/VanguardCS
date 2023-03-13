from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons

import json
import functions as func
import os

from template.section import Section
from template.widget import Widget

from gui_functions.class_roll import DiceRoll

class InventoryItem(QWidget):
    def __init__(self, character_sheet, count, item_dict, equipment=""):
        super().__init__()

        self.character_sheet = character_sheet
        self.combat_log = character_sheet.combat_log

        self.master_layout = QHBoxLayout()
        self.widget_group = []
        self.section_group = []
        self.count = count

        self.equipment = equipment

        color_type = {"melee": "#925833", "armor": "#495c60", "elixirs": "#926f2b"}

        if count % 2 == 0:
            bg_color = cons.PRIMARY
        else:
            bg_color = cons.PRIMARY_DARKER             

        self.item_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 3),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            spacing=5,
            group=True,
            stylesheet=f"background-color: {bg_color};",           
        )

        self.item = Widget(
            widget_type=QLineEdit(),
            parent_layout=self.item_section.inner_layout(2),
            objectname=f"{count}",
            class_group=self.widget_group,
            stylesheet=f"font-size: 13px; font-weight: bold;",
            height=cons.WSIZE,
            signal=self
        )

        # CREATING EMPTY OR POPULATED ITEM WIDGET
        if item_dict == {}:
            pass # Setting up empty item
        else:
            self.make_item(item_dict)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_layout)
        self.setFixedHeight(75)

    def make_item(self, item_dict):
        self.item_dict = item_dict
        self.name = self.item_dict["Name"]
        self.category = self.item_dict["Category"]
        item_type = "Weapon" #item_dict["Type"] SET UP TYPES
        qualities = self.item_dict["Quality"]
        dice_type = self.item_dict["Roll"][0]
        dice = self.item_dict["Roll"][1]
        self.equipped = self.item_dict["Equipped"]

        if "Impeding" in self.item_dict:
            impeding = f" {self.item_dict['Impeding']}"
        else:
            impeding = ""

        color_type = {"melee": "#925833", "ranged": "#925833", "armor": "#495c60", "elixirs": "#926f2b"}
        self.type_bg_color = color_type[self.category]

        self.item.widget.setText(self.name)
        
        if "Equip" in item_dict:
            equip = self.item_dict["Equip"]
            if self.equipment != "":
                self.type_label = Widget(
                    widget_type=QPushButton(),
                    parent_layout=self.item_section.inner_layout(1),
                    class_group=self.widget_group,
                    width=5,
                    stylesheet=f"background-color: {self.type_bg_color};",
                    size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
                    objectname=f"{self.equipment}_EQUIPPED",
                    signal=self.prepare_equip_item,
                )
            else:
                for count, state in enumerate(equip):
                    self.type_label = Widget(
                        widget_type=QPushButton(),
                        parent_layout=self.item_section.inner_layout(1),
                        class_group=self.widget_group,
                        width=5,
                        stylesheet=f"background-color: {cons.BORDER};",
                        size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
                        objectname=state,
                        signal=self.prepare_equip_item,
                    )
        else:
            self.type_label = Widget(
                widget_type=QLabel(),
                parent_layout=self.item_section.inner_layout(1),
                class_group=self.widget_group,
                width=5,
                stylesheet=f"background-color: {cons.BORDER}",
            )

        self.item_section.inner_layout(1).setSpacing(1)

        self.quality_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.item_section.inner_layout(2),
            class_group=self.section_group,
            spacing=2,
        )

        for count, quality in enumerate(qualities):
            self.item_quality = Widget(
                widget_type=QToolButton(),
                parent_layout=self.quality_section.inner_layout(1),
                objectname=quality,
                class_group=self.widget_group,
                icon=(f"{quality}.png", cons.WSIZE / 2, cons.FONT_COLOR),
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-radius: 6px;",
                height=cons.WSIZE,
                width=cons.WSIZE,
            )

        self.item_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(3),
            text=item_type + impeding,
            objectname="item",
            class_group=self.widget_group,
            align="right",
            height=cons.WSIZE,
            
        )

        self.item_dice = Widget(
            widget_type=QToolButton(),
            parent_layout=self.item_section.inner_layout(3),
            text=dice,
            objectname="item",
            class_group=self.widget_group,
            stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {self.type_bg_color}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;",
            height=cons.WSIZE,
            signal=self.roll_dice,
            property=("roll",dice_type)
        )

        self.quality_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(2).setAlignment(Qt.AlignRight)
        self.item_label.get_widget().setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def roll_dice(self):
        self.character = self.character_sheet.character_name
        self.roll_type = self.sender().property("roll") 

        if self.roll_type in cons.STATS:
            self.check = int(self.sender().text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = self.sender().text()

        rolling_dice = DiceRoll(self.combat_log,self.character,self.roll_type.capitalize(), self.dice, check = self.check).roll()

    def prepare_equip_item(self):
        self.equip_button = self.sender()
        self.equip_button_type = self.equip_button.objectName()

        if "EQUIPPED" in self.equip_button_type:
            self.unequip_item()
        else:
            self.equip_item()

    def equip_item(self):
        if self.equip_button_type == "2H":
            self.character_sheet.CHARACTER_DOC["inventory"].pop(self.count)

            if self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] != {}:
                self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["main hand"])
            if self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] != {}:
                self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["off hand"])

            self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict
            self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] = {}

            self.equip_button.setObjectName("2H_EQUIPPED")

        elif self.equip_button_type == "MH":
            self.character_sheet.CHARACTER_DOC["inventory"].pop(self.count)
            
            if self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] != {}:
                self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["main hand"])

            self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict

            self.equip_button.setObjectName("MH_EQUIPPED")

        elif self.equip_button_type == "OH":
            self.character_sheet.CHARACTER_DOC["inventory"].pop(self.count)
            
            if self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] != {}:
                self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["off hand"])

            self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] = self.item_dict

            self.equip_button.setObjectName("OH_EQUIPPED")

        elif self.equip_button_type == "AR":
            self.character_sheet.CHARACTER_DOC["inventory"].pop(self.count)
            
            if self.character_sheet.CHARACTER_DOC["equipment"]["armor"] != {}:
                self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["armor"])

            self.character_sheet.CHARACTER_DOC["equipment"]["armor"] = self.item_dict

            self.equip_button.setObjectName("AR_EQUIPPED")
        
        self.character_sheet.update_sheet()

    def unequip_item(self):
        if self.equip_button_type == "2H_EQUIPPED":
            self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["main hand"])
            self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = {}
            self.equip_button.setObjectName("2H")

        elif self.equip_button_type == "MH_EQUIPPED":
            self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["main hand"])
            self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = {}
            self.equip_button.setObjectName("MH")

        elif self.equip_button_type == "OH_EQUIPPED":
            self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["off hand"])
            self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] = {}
            self.equip_button.setObjectName("OH")

        elif self.equip_button_type == "AR_EQUIPPED":
            self.character_sheet.CHARACTER_DOC["inventory"].append(self.character_sheet.CHARACTER_DOC["equipment"]["armor"])
            self.character_sheet.CHARACTER_DOC["equipment"]["armor"] = {}
            self.equip_button.setObjectName("AR")

        self.character_sheet.update_sheet()

    # def equip_item(self):
    #     self.equip_button = self.sender()
    #     self.equip_button_type = self.equip_button.objectName()

    #     self.equip_1 = self.item_dict["Equipped"]["1"]
    #     self.equip_2 = self.item_dict["Equipped"]["2"]

    #     if self.equip_button_type == "2H":
    #         self.unequip_2hander()
    #         if self.equip_1 == False:
    #             self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict
    #             self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] = {}
    #             self.item_dict["Equipped"]["1"] = True
    #             self.item_dict["Equipped"]["2"] = True
    #         else:
    #             self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = {}
    #             self.item_dict["Equipped"]["1"] = False
    #             self.item_dict["Equipped"]["2"] = False

    #     elif self.equip_button_type == "MH":
    #         self.unequip_main_hand()
    #         if self.equip_1 == False:
    #             print(f"equipping {self.item_dict['Name']}")
    #             self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict
    #             self.item_dict["Equipped"]["1"] = True
    #             self.item_dict["Equipped"]["2"] = False
    #         else:
    #             print(f"Un-equipping {self.item_dict['Name']}")
    #             self.character_sheet.CHARACTER_DOC["equipment"]["main hand"] = {}
    #             self.item_dict["Equipped"]["1"] = False

    #     elif self.equip_button_type == "OH":
    #         self.unequip_off_hand()
    #         if self.equip_2 == False:
    #             self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] = self.item_dict
    #             self.item_dict["Equipped"]["1"] = False
    #             self.item_dict["Equipped"]["2"] = True
    #         else:
    #             self.character_sheet.CHARACTER_DOC["equipment"]["off hand"] = {}
    #             self.item_dict["Equipped"]["2"] = False

    #     elif self.equip_button_type == "AR":
    #         self.unequip_armor()
    #         if self.equip_2 == False:
    #             self.character_sheet.CHARACTER_DOC["equipment"]["armor"] = self.item_dict
    #             self.item_dict["Equipped"]["1"] = True
    #             self.item_dict["Equipped"]["2"] = True
    #         else:
    #             self.character_sheet.CHARACTER_DOC["equipment"]["armor"] = {}
    #             self.item_dict["Equipped"]["2"] = False
    #             self.item_dict["Equipped"]["2"] = False

    #     print(self.item_dict["Equipped"]["1"])
    #     print(self.item_dict["Equipped"]["2"])
    #     self.character_sheet.update_sheet()

    # def unequip_main_hand(self):
    #     print(f"unequipping main hand")
    #     for item in self.character_sheet.CHARACTER_DOC["inventory"]:
    #         if item["Category"] in ["melee","ranged"]:
    #             item["Equipped"]["1"] = False
    #         else:
    #             pass

    # def unequip_armor(self):
    #     print(f"unequipping armor")
    #     for item in self.character_sheet.CHARACTER_DOC["inventory"]:
    #         if item["Category"] == "armor":
    #             item["Equipped"]["1"] = False
    #             item["Equipped"]["2"] = False
    #         else:
    #             pass

    # def unequip_off_hand(self):
    #     print(f"unequipping off hand")
    #     for item in self.character_sheet.CHARACTER_DOC["inventory"]:
    #         if item["Category"] in ["melee","ranged"]:
    #             item["Equipped"]["2"] = False
    #         else:
    #             pass

    # def unequip_2hander(self):
    #     print(f"unequipping 2hander")
    #     for item in self.character_sheet.CHARACTER_DOC["inventory"]:
    #         if item["Category"] in ["melee","ranged"]:
    #             item["Equipped"]["1"] = False
    #             item["Equipped"]["2"] = False
    #         else:
    #             pass