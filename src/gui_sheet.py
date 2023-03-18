from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import functions as func
import constants as cons
from gui_abilities import AddNewAbility
from gui_functions.class_roll import DiceRoll
from gui_functions.class_modify_stat import ModifyStat

from gui_windows.gui_add_sub import AddSub

class CharacterSheetGUI(QWidget):
    def __init__(self, csheet):
        super().__init__()

        self.character_sheet = csheet

        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(0,0,0,0)
        self.section_group = []
        self.widget_group = []

        self.character_basic = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 1),
            parent_layout = self.master_layout,
            spacing=10,
            class_group = self.section_group,
        )

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
        self.ability_layout.get_title()[1].setAlignment(Qt.AlignCenter)

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


        #Below is all the widgets used in the character sheet
        for number,stat in enumerate(cons.STATS):
            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout = self.stat_layout.inner_layout(number),
                signal=self.roll_dice,
                property=("roll",stat),
                objectname=stat,
                class_group=self.widget_group,
                height=cons.WSIZE*1.5,
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
            )

            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout=self.stat_layout.inner_layout(number),
                text=stat,
                objectname=f"{stat} mod",
                class_group=self.widget_group,
                height=cons.WSIZE,
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
                signal = self.modify_stat
            )

        self.toughness_current= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(1),
            signal=self.add_sub,
            objectname = "TOUGHNESS",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        )

        self.toughness_current_label= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(1),
            objectname = "TOUGHNESS_mod",
            text = "TOUGHNESS",
            class_group=self.widget_group,
            signal=self.modify_stat,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        )

        self.toughness_max= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname = "MAXIMUM",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.toughness_max_mod= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname = "MAXIMUM_mod",
            text = "MAXIMUM",
            class_group=self.widget_group,
            signal=self.modify_stat,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        )

        self.toughness_threshold= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(3),
            objectname = "PAIN",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.toughness_threshold_mod= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(3),
            objectname = "PAIN_mod",
            text = "THRESHOLD",
            class_group=self.widget_group,
            signal=self.modify_stat,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        )

        self.corruption= Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(1),
            signal=self.add_sub,
            objectname = "CORRUPTION",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        )

        self.corruption_mod = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(1),
            class_group=self.widget_group,
            text = "CORRUPTION",
            objectname = "CORRUPTION_mod",
            signal = self.modify_stat,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        )

        self.corruption_permanent= Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(2),
            signal=self.add_sub,
            objectname = "PERMANENT",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        )

        self.corruption_permanent_mod = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(2),
            class_group=self.widget_group,
            text = "PERMANENT",
            objectname = "PERMANENT_mod",
            signal = self.modify_stat,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        )

        self.corruption_threshold= Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(3),
            objectname = "THRESHOLD",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        )

        self.corruption_threshold_mod = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(3),
            class_group=self.widget_group,
            text = "THRESHOLD",
            objectname = "THRESHOLD_mod",
            signal = self.modify_stat,
            height=cons.WSIZE,
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
            if widget.objectName() in [stat+" mod" for stat in cons.STATS]:
                string = widget.text()
                ModifyStat(string).subtract_one(self.character_sheet, widget)

    def open_abilities(self):
        self.abilities = AddNewAbility(self, self.character_sheet)
        self.abilities.show()

    def modify_stat(self):
        widget = self.sender()
        string = widget.text()
        ModifyStat(string).add_one(self.character_sheet, widget)

    def roll_dice(self):
        self.character = self.character_sheet.character_name
        self.combat_log = self.character_sheet.combat_log
        self.roll_type = self.sender().property("roll")   

        if self.roll_type in cons.STATS:
            self.check = int(self.sender().text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = self.sender().text()

        rolling_dice = DiceRoll(self.sender(),self.combat_log,self.character,self.roll_type.capitalize(),self.dice, check = self.check, sheet = self.character_sheet).roll()

    def add_sub(self):
        doc_string = self.sender().objectName()
        add_sub_gui = AddSub(self.character_sheet, self.sender(), doc_item = doc_string)
        add_sub_gui.show()