from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import functions as func
import constants as cons

from class_sheet import CharacterSheet

import functools

from gui_functions import custom_rolls

from gui_abilities import AbilityGUI

import math

from gui_functions.class_roll import DiceRoll

class CharacterSheetGUI(QWidget):
    def __init__(self, csheet):
        super().__init__()

        self.character_sheet = csheet

        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(0,0,0,0)
        self.section_group = []
        self.widget_group = []

        self.top_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.master_layout,
            spacing = 5,
            class_group = self.section_group
        )

        self.stat_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 9),
            parent_layout = self.top_layout.inner_layout(2),
            group = True,
            spacing = 3,
            class_group = self.section_group,
            title = "STATS",
        )

        self.stat_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.ability_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            title = "ABILITIES & POWERS",
            group = True,
            scroll=(True,"top"),
            icon = ("plus.png", cons.WSIZE, cons.ICON_COLOR),
            spacing=5,
            class_group=self.section_group
        )
        
        self.ability_layout.get_title()[0].clicked.connect(self.open_abilities)


        self.character_basic = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 1),
            parent_layout = self.master_layout,
            spacing=10,
            class_group = self.section_group,
        )

        self.hp_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 3),
            parent_layout = self.character_basic.inner_layout(1),
            group = True,
            title = "TOUGHNESS",
            spacing = 3,
            class_group=self.section_group
        )

        self.hp_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.corruption_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 3),
            parent_layout = self.character_basic.inner_layout(1),
            group = True,
            title = "CORRUPTION",
            spacing = 3,
            class_group=self.section_group
        )

        self.corruption_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        for power in range(1, 13):
            #layout_number = math.ceil(power / 2)
            layout_number = 1
            # Below is all the code for the power section
            self.master_power_section = Section(
                outer_layout = QHBoxLayout(),
                inner_layout = ("VBox", 1),
                parent_layout = self.ability_layout.inner_layout(layout_number),
                spacing = 3,
                class_group=self.section_group
            )

            self.add_power_button = Widget(
                widget_type=QWidget(),
                parent_layout = self.master_power_section.inner_layout(1),
                class_group=self.widget_group,
                objectname=f"ability{power}",
                enabled=False,
            )
            
            self.power_section = Section(
                outer_layout = QVBoxLayout(),
                inner_layout = ("HBox", 3),
                parent_layout = self.master_power_section.inner_layout(1),
                title="empty",
                group = True,
                spacing = 10,
                class_group=self.section_group,
                objectname=f"ability{power}_section",
                icon = ("plus.png",cons.WSIZE,cons.ICON_COLOR),
                hidden=True,
            )
            title_layout = self.power_section.get_title()[2]
            self.power_section.get_title()[1].setAlignment(Qt.AlignCenter)
            
            self.rank_label = Widget(
                widget_type=QLabel(),
                parent_layout = self.power_section.inner_layout(1),
                text="Novice",
                class_group=self.widget_group,
                align="top",
                width=35
            )

            self.novice_rank = Widget(
                widget_type=QLabel(),
                parent_layout = self.power_section.inner_layout(1),
                text="",
                objectname=f"ability{power}_label",
                class_group=self.widget_group
            )

            self.novice_rank.get_widget().setWordWrap(True)

            self.rank_label = Widget(
                widget_type=QLabel(),
                parent_layout = self.power_section.inner_layout(2),
                text="Adept",
                class_group=self.widget_group,
                align="top",
                width=35
            )

            self.adept_box = Widget(
                widget_type=QLabel(),
                parent_layout = self.power_section.inner_layout(2),
                class_group=self.widget_group,
                objectname=f"ability{power}",
                enabled=False,
                text = "<b>Passive</b>. The character makes two separate knife-attacks at the same target with every combat action. If the character also has Twin Attack, this ability only affects one of the attacks, for a total of three attacks (two with the main hand and one with the other)."
            )

            self.adept_box.get_widget().setWordWrap(True)

            self.rank_label = Widget(
                widget_type=QLabel(),
                parent_layout = self.power_section.inner_layout(3),
                text="Master",
                class_group=self.widget_group,
                align="top",
                width=35
            )

            self.master_box = Widget(
                widget_type=QLabel(),
                parent_layout = self.power_section.inner_layout(3),
                class_group=self.widget_group,
                objectname=f"ability{power}",
                enabled=False,
                text = "<b>Passive</b>. The character makes two separate knife-attacks at the same target with every combat action. If the character also has Twin Attack, this ability only affects one of the attacks, for a total of three attacks (two with the main hand and one with the other)."

            )

            self.master_box.get_widget().setWordWrap(True)

            self.novice = Widget(
                widget_type=QPushButton(),
                text="N",
                width=cons.WSIZE,
                height=cons.WSIZE,
                objectname=f"ability{power}_Novice"
            )

            self.adept = Widget(
                widget_type=QPushButton(),
                text="A",
                width=cons.WSIZE,
                height=cons.WSIZE,
                objectname=f"ability{power}_Adept"
            )

            self.master = Widget(
                widget_type=QPushButton(),
                text="M",
                width=cons.WSIZE,
                height=cons.WSIZE,
                objectname=f"ability{power}_Master"
            )

            self.delete = Widget(
                widget_type=QToolButton(),
                parent_layout = title_layout,
                class_group=self.widget_group,
                width=cons.WSIZE,
                height=cons.WSIZE,
                icon = ("delete.png",cons.WSIZE,cons.ICON_COLOR),
                objectname=f"ability{power}_delete",
                signal=self.delete_ability
            )


            title_layout.insertWidget(1, self.novice.widget)
            title_layout.insertWidget(2, self.adept.widget)
            title_layout.insertWidget(3, self.master.widget)

            self.master.get_widget().clicked.connect(self.change_rank)
            self.adept.get_widget().clicked.connect(self.change_rank)
            self.novice.get_widget().clicked.connect(self.change_rank)


        self.ability_layout.get_title()[1].setAlignment(Qt.AlignCenter)


        []

        #Below is all the widgets used in the character sheet
        for number,stat in enumerate(cons.STATS):
            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout = self.stat_layout.inner_layout(number),
                signal=self.roll_dice,
                property=("roll",stat),
                objectname=stat,
                class_group=self.widget_group,
                height=cons.WSIZE*2,
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
            )

            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout=self.stat_layout.inner_layout(number),
                text=stat,
                objectname=f"{stat}_label",
                class_group=self.widget_group,
                height=cons.WSIZE,
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

            )

        self.toughness_current= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(1),
            signal=self.open_addsub,
            objectname = "toughness_current",
            class_group=self.widget_group,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.toughness_current_label= Widget(
            widget_type=QLabel(),
            parent_layout=self.hp_layout.inner_layout(1),
            signal=self.open_addsub,
            objectname = "toughness_current",
            text = "CURRENT",
            class_group=self.widget_group,
            align=Qt.AlignCenter,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        )
        self.toughness_max = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname = "toughness_max",
            class_group=self.widget_group,
            stylesheet=f"color: {cons.FONT_DARK}; font-size: 20px;"
        )

        self.toughness_max_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname = "toughness_max",
            class_group=self.widget_group,
            text = "MAXIMUM",
            align=Qt.AlignCenter
        )

        self.toughness_threshold = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(3),
            objectname = "toughness_threshold",
            class_group=self.widget_group,
            stylesheet=f"color: {cons.FONT_DARK}; font-size: 20px;"
        )

        self.toughness_threshold_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.hp_layout.inner_layout(3),
            text = "THRESHOLD",
            class_group=self.widget_group,
            align=Qt.AlignCenter
        )

        self.corruption_threshold = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(1),
            signal=lambda: CharacterSheet(self).update_sheet(),
            text = "",
            class_group=self.widget_group,
            stylesheet=f"color: {cons.FONT_DARK}; font-size: 20px;"
        )

        self.corruption_permanent = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(2),
            objectname = "toughness_permanenet",
            class_group=self.widget_group,
            stylesheet=f"color: {cons.FONT_DARK}; font-size: 20px;"
        )

        self.corruption_temporary= Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(3),
            signal=self.open_addsub,
            objectname = "corruption_current",
            class_group=self.widget_group,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.corruption_threshold_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.corruption_layout.inner_layout(1),
            text = "THRESHOLD",
            class_group=self.widget_group,
            align=Qt.AlignCenter
        )

        self.corruption_permanent_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.corruption_layout.inner_layout(2),
            class_group=self.widget_group,
            text = "PERMANENT",
            align=Qt.AlignCenter
        )

        self.corruption_temporary_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.corruption_layout.inner_layout(3),
            class_group=self.widget_group,
            text = "TEMPORARY",
            align=Qt.AlignCenter,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()
        self.setLayout(self.master_layout)       

        self.character_sheet.set_sheet_vars(self)

    def mousePressEvent(self, event): #this is a very specific event used to subtract values when right clicking on a widget
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if widget.objectName() in [stat+"_label" for stat in cons.STATS]+[stat+"_mod" for stat in cons.STATS]:
                custom_rolls.modify_stat(self, self.character_sheet, widget.objectName().split("_")[0], adjust="subtract")

    def open_abilities(self):
        print("opening abilities")
        slot = f"ability{self.get_free_ability_slot()}"
        self.abilities = AbilityGUI(self, self.character_sheet, slot)
        self.abilities.show()

    def delete_ability(self):
        sender_object = self.sender().objectName()
        sender_object.split("_")[0]
        self.findChild(QWidget, f"{sender_object.split('_')[0]}_section_title").setText("empty")
        self.character_sheet.update_sheet()

    def get_free_ability_slot(self):
        for slot in range(1, 13):
            ability_slot = self.findChild(QWidget, f"ability{slot}_section_title").text()
            if ability_slot == "empty":
                return slot

    def open_addsub(self):
        sender = self.sender()
        self.addsub = AddSubGUI(self, sender)
        self.addsub.show()

    def change_rank(self):
        print("changing rank")
        slot = self.sender().objectName().split("_")[0]
        rank = self.sender().objectName().split("_")[1]
        self.character_sheet.set_rank(slot, rank)

    def roll_dice(self):
        print("rolling dice")
        self.character = self.character_sheet.character_name
        self.combat_log = self.character_sheet.combat_log
        self.roll_type = self.sender().property("roll")

        self.modifier = 0        

        if self.roll_type in cons.STATS:
            self.check = int(self.sender().text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = self.sender().text()

        rolling_dice = DiceRoll(self.combat_log,self.character,self.roll_type.capitalize(),self.dice, check = self.check).roll()