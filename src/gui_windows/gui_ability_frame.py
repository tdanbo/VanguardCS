from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons
import pymongo

from gui_functions.class_roll import DiceRoll

import re

class AbilityItem(QWidget):
    def __init__(self, character_sheet, ability_dict, select = False, slot = None):
        super().__init__()
        self.select = select

        self.character_sheet = character_sheet
        self.ability_dict = ability_dict
        
        self.experience = self.character_sheet.XP
        self.unspent_xp = self.character_sheet.UXP

        self.slot = slot
        # an empty widget was used to push the content together. might need to introduce.

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        self.power_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 6),
            parent_layout = self.master_layout,
            group = True,
            spacing = 5,
            class_group=self.section_group,
            objectname=f"ability_section",
            stylesheet=f"background-color: {cons.PRIMARY_DARKER}; border-radius: 5px; padding: 5px;"
        )
        
        # self.header_icon = Widget(
        #     widget_type=QToolButton(),
        #     parent_layout = self.power_section.inner_layout(1),
        #     icon = (f"{self.ability_dict['Category']}.png",cons.WSIZE,cons.FONT_COLOR),
        #     height=cons.WSIZE,
        #     width=cons.WSIZE,
        #     objectname=f"ability_icon",
        #     class_group=self.widget_group,
        # )

        if self.select:
            self.header_select = Widget(
                widget_type=QToolButton(),
                parent_layout = self.power_section.inner_layout(1),
                icon = ("plus.png",cons.WSIZE,cons.BORDER),
                height=cons.WSIZE,
                width = cons.WSIZE,
                objectname=f"ability_select",
                class_group=self.widget_group,
                signal=self.select_ability,
            )
        else:
            self.header_delete = Widget(
                widget_type=QToolButton(),
                parent_layout = self.power_section.inner_layout(1),
                icon = ("delete.png",cons.WSIZE,cons.BORDER),
                height=cons.WSIZE,
                width = cons.WSIZE,
                objectname=f"ability_delete",
                class_group=self.widget_group,
                signal=self.delete_ability,
            )

        self.header_label = Widget(
            widget_type=QLabel(),
            parent_layout = self.power_section.inner_layout(1),
            text=self.ability_dict["Name"].upper(),
            objectname=f"ability_name",
            class_group=self.widget_group,
            stylesheet=f"font-size: 14px; font-weight: bold; color: {cons.FONT_COLOR}"
        )

        self.set_rank_novice = Widget(
            widget_type=QToolButton(),
            parent_layout = self.power_section.inner_layout(1),
            text="N",
            height=cons.WSIZE,
            width=cons.WSIZE,
            objectname=f"ability_novice",
            class_group=self.widget_group,
            signal=self.change_rank,
            stylesheet = f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"
        )

        self.set_rank_adept = Widget(
            widget_type=QToolButton(),
            parent_layout = self.power_section.inner_layout(1),
            text = "A",
            height=cons.WSIZE,
            width=cons.WSIZE,
            objectname=f"ability_adept",
            class_group=self.widget_group,
            signal=self.change_rank,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.BORDER}; font-size: 11px; border: 1px solid {cons.BORDER}; border-radius: 6px;",
        )

        self.set_rank_master = Widget(
            widget_type=QToolButton(),
            parent_layout = self.power_section.inner_layout(1),
            text = "M",
            height=cons.WSIZE,
            width=cons.WSIZE,
            objectname=f"ability_master",
            class_group=self.widget_group,
            signal=self.change_rank,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.BORDER}; font-size: 11px; border: 1px solid {cons.BORDER}; border-radius: 6px;",
        )

        self.power_section.inner_layout(1).setSpacing(2)

        self.description = Widget(
            widget_type=QLabel(),
            parent_layout = self.power_section.inner_layout(2),
            text=self.ability_dict["Description"],
            objectname=f"ability_description",
            class_group=self.widget_group,
            stylesheet=f"font-size: 10px; color: {cons.DARK}; font-style: italic;",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            hidden=True
        )

        self.description.get_widget().setWordWrap(True)

        self.divider = Widget(
            widget_type=QFrame(),
            parent_layout = self.power_section.inner_layout(3),
            height=1,
            stylesheet=f"background-color: {cons.BORDER}",
            class_group=self.section_group
        )

        self.novice_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 3),
            parent_layout = self.power_section.inner_layout(4),
            spacing = 5,
            class_group=self.section_group,
            hidden=False
        )

        self.novice_rank = Widget(
            widget_type=QPushButton(),
            parent_layout = self.novice_section.inner_layout(1),
            text="NOVICE",
            class_group=self.widget_group,
            width=50,
            stylesheet=f"font-size: 10px; font-weight: bold; color: {cons.FONT_COLOR}"
        )

        self.novice_box = Widget(
            widget_type=QLabel(),
            parent_layout = self.novice_section.inner_layout(1),
            text=self.ability_dict["Novice"],
            objectname=f"ability_label",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        )

        self.build_dice_section(self.ability_dict["Novice"], self.novice_section.inner_layout(2))

        self.novice_box.get_widget().setWordWrap(True)

        self.divider = Widget(
            widget_type=QFrame(),
            parent_layout = self.novice_section.inner_layout(3),
            height=1,
            stylesheet=f"background-color: {cons.BORDER}",
            class_group=self.section_group
        )

        self.adept_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 3),
            parent_layout = self.power_section.inner_layout(5),
            spacing = 5,
            class_group=self.section_group,
            hidden=True
        )

        self.adept_rank = Widget(
            widget_type=QPushButton(),
            parent_layout = self.adept_section.inner_layout(1),
            text="ADEPT",
            class_group=self.widget_group,
            width=50,
            stylesheet=f"font-size: 10px; font-weight: bold; color: {cons.FONT_COLOR}"
        )

        self.adept_box = Widget(
            widget_type=QLabel(),
            parent_layout = self.adept_section.inner_layout(1),
            class_group=self.widget_group,
            objectname=f"ability",
            enabled=False,
            text = self.ability_dict["Adept"],
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        )

        self.build_dice_section(self.ability_dict["Adept"], self.adept_section.inner_layout(2))

        self.adept_box.get_widget().setWordWrap(True)

        self.divider = Widget(
            widget_type=QFrame(),
            parent_layout = self.adept_section.inner_layout(3),
            height=1,
            stylesheet=f"background-color: {cons.BORDER}",
            class_group=self.section_group
        )

        self.master_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 3),
            parent_layout = self.power_section.inner_layout(6),
            spacing = 5,
            class_group=self.section_group,
            hidden=True
        )

        self.master_rank = Widget(
            widget_type=QPushButton(),
            parent_layout = self.master_section.inner_layout(1),
            text="MASTER",
            class_group=self.widget_group,
            width=50,
            stylesheet=f"font-size: 10px; font-weight: bold; color: {cons.FONT_COLOR}"
        )

        self.master_box = Widget(
            widget_type=QLabel(),
            parent_layout = self.master_section.inner_layout(1),
            class_group=self.widget_group,
            objectname=f"ability",
            enabled=False,
            text = self.ability_dict["Master"],
        )

        self.build_dice_section(self.ability_dict["Master"], self.master_section.inner_layout(2))

        self.master_box.get_widget().setWordWrap(True)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.gui_rank_state()

        self.setStyleSheet(f"border-style: outset; color: {cons.FONT_DARK}; background-color: {cons.PRIMARY};border-style: outset;")
        self.master_layout.setSpacing(0)
        self.master_layout.setContentsMargins(0,0,0,0)    

        self.setLayout(self.master_layout)  

    def delete_ability(self):
        self.character_sheet.CHARACTER_DOC["abilities"].pop(self.slot)
        self.character_sheet.update_sheet()

    def gui_rank_state(self):
        if self.ability_dict["Rank"] == "Novice":
            self.novice_section.setHidden(False)
            self.adept_section.setHidden(True)
            self.master_section.setHidden(True)

            self.set_rank_novice.get_widget().setStyleSheet(f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;")
            self.set_rank_adept.get_widget().setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.BORDER}; font-size: 11px; border: 1px solid {cons.BORDER}; border-radius: 6px;")
            self.set_rank_master.get_widget().setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.BORDER}; font-size: 11px; border: 1px solid {cons.BORDER}; border-radius: 6px;")

        elif self.ability_dict["Rank"] == "Adept":
            self.novice_section.setHidden(False)
            self.adept_section.setHidden(False)
            self.master_section.setHidden(True)

            self.set_rank_novice.get_widget().setStyleSheet(f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;")
            self.set_rank_adept.get_widget().setStyleSheet(f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;")
            self.set_rank_master.get_widget().setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.BORDER}; font-size: 11px; border: 1px solid {cons.BORDER}; border-radius: 6px;")

        elif self.ability_dict["Rank"] == "Master":
            self.novice_section.setHidden(False)
            self.adept_section.setHidden(False)
            self.master_section.setHidden(False)

            self.set_rank_novice.get_widget().setStyleSheet(f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;")
            self.set_rank_adept.get_widget().setStyleSheet(f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;")
            self.set_rank_master.get_widget().setStyleSheet(f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;")

    def change_rank(self):
        rank = self.sender().objectName()
        if rank == "ability_novice":
            self.ability_dict["Rank"] = "Novice"

        elif rank == "ability_adept":
            self.ability_dict["Rank"] = "Adept"

        elif rank == "ability_master":
            self.ability_dict["Rank"] = "Master"

        self.character_sheet.update_sheet()

    def build_dice_section(self, string, layout):

        matches = re.findall(r'\b\d*[dD]\d+\+?\d*\b', string)
        if not matches:
            pass  # Output: ['1D8', '4d20', '2d10+2']
        else:
            self.dice_section = Section(
                outer_layout = QHBoxLayout(),
                inner_layout = ("HBox", 1),
                parent_layout = layout,
                spacing = 10,
                class_group=self.section_group,

            )
            for dice in matches:
                self.ability_dice = Widget(
                    widget_type=QToolButton(),
                    parent_layout=self.dice_section.inner_layout(1),
                    text=dice.lower(),
                    objectname="item",
                    class_group=self.widget_group,
                    stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;",
                    height=cons.WSIZE,
                    signal=self.roll_dice,
                    property=("roll",self.ability_dict["Name"])
                )

            self.dice_section.inner_layout(1).setAlignment(Qt.AlignRight)

    def select_ability(self):
        self.ability_dict["Rank"] = "Novice"
        self.character_sheet.CHARACTER_DOC["abilities"].append(self.ability_dict)
        self.character_sheet.update_sheet()

    def roll_dice(self):
        self.character = self.character_sheet.character_name
        self.combat_log = self.character_sheet.combat_log
        self.roll_type = self.sender().property("roll")   

        if self.roll_type in ["CASTING","DEFENSE"]:
            self.check = int(self.sender().text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = self.sender().text()

        rolling_dice = DiceRoll(self.combat_log,self.character,self.roll_type.capitalize(),self.dice, check = self.check).roll()

def get_abilities(category, name):
    all_equipment = {}
    client = pymongo.MongoClient(cons.CONNECT)
    # get a list of collection names
    db = client["abilities"]
    collection_names = db.list_collection_names()
    for coll in collection_names:
        # get a collection object
        collection = db[coll]
        document = collection.find_one()
        all_equipment[coll] = document
    
    ability_dict = all_equipment[category][name]
    ability_dict["Category"] = category
    return ability_dict

if __name__ == "__main__":
    app = QApplication()
    ability = get_abilities("abilities","Backstab")
    window = AbilityItem(ability)
    window.show()
    app.exec_()



#         self.all_abilities = self.get_abilities()
#         self.ability_dict = self.all_abilities[self.category][item]