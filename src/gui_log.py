from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons
import functools

from gui_classes import class_custom_rolls

from gui_widgets.gui_combat_frame import CombatEntry
from gui_classes.class_roll import DiceRoll

import constants as cons

class CombatLogGUI(QWidget):
    def __init__(self, character):
        super().__init__()
        
        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(0,0,0,0)
        self.section_group = []
        self.widget_group = []

        self.character = character

        #Setting up layouts/sections

        scroll_style = f"QScrollBar {{background-color: {cons.PRIMARY_LIGHTER}; width: 6px;}}"\
                       f"QScrollBar::handle:vertical {{background-color: {cons.BORDER}; width: 6px; min-height: 20px; border: none; outline: none;}}"\

        self.log_scroll = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            scroll=(True,"bottom"),
            title="COMBAT LOG",
            group = True,   
            class_group = self.section_group,
            content_margin=(0,0,0,0),	
            stylesheet=scroll_style,
        )

        self.log_scroll.get_title()[1].setAlignment(Qt.AlignCenter)
        self.log_dice = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("HBox", 2),   
            parent_layout = self.master_layout,
            title="DICE",  
            group = True,
            spacing = 3,	
            class_group = self.section_group,
            height=98
        )

        self.log_dice.get_title()[1].setAlignment(Qt.AlignCenter)

        self.roll_button = Widget(
            widget_type=QPushButton(),
            parent_layout=self.log_dice.get_title()[2],
            text="ROLL",
            height=cons.WSIZE,
            objectname="roll",
            signal= lambda: self.roll_dice(),
            class_group = self.widget_group,
            stylesheet=f"background-color: {cons.FONT_COLOR}; color: {cons.PRIMARY_LIGHTER}; font-weight: bold;"
        )   

        self.roll_button.get_widget().setHidden(True)

        #DICE
        #Small loop that create a widget class for each dice type.
        dice = [("d4",4),("d6",6), ("d8",8), ("d10",10), ("d12",12), ("d20",20)]
        for die_type in dice:
            self.dice_layout = Section(
                outer_layout = QHBoxLayout(),
                inner_layout = ("VBox", 1),
                parent_layout = self.log_dice.inner_layout(0),
                spacing=3,
                class_group = self.section_group                
            )

            self.dice_count = Widget(
                widget_type=QPushButton(),
                parent_layout=self.dice_layout.inner_layout(0),
                text="",
                objectname=f"{die_type[0]}_count",
                signal=functools.partial(
                    class_custom_rolls.add_dice,
                    self,
                    die_type[0],
                ),
                class_group=self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
                stylesheet=f"font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

            )  

            self.dice_w = Widget(
                widget_type=QPushButton(),
                parent_layout=self.dice_layout.inner_layout(0),
                objectname=die_type[0],
                text = die_type[0],
                #icon = (f"{die_type[0]}.png","",cons.FONT_COLOR,100),
                signal=functools.partial(
                    class_custom_rolls.add_dice,
                    self,
                    die_type[0]
                ),
                class_group=self.widget_group,
                stylesheet=f"font-weight: bold; color: {cons.FONT_DARK}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding)
            )     

            self.dice_count.get_widget().setMinimumWidth(cons.WSIZE*1.5)
            self.dice_w.get_widget().setMinimumWidth(cons.WSIZE*1.5)

        self.combet_log_slots = []
        for count in range (21): # Make all static entries in the combatlog
            log_gui_entry = CombatEntry(count)
            self.log_scroll.inner_layout(1).addWidget(log_gui_entry)

            self.divider = QFrame()
            self.divider.setFixedHeight(1)
            self.divider.setStyleSheet(f"background-color: {cons.BORDER}")
            self.log_scroll.inner_layout(1).addWidget(self.divider)

            self.combet_log_slots.append(log_gui_entry)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()    

        self.setLayout(self.master_layout)        

    def mousePressEvent(self, event): #this is a very specific event used to subtract values when right clicking on a widget
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if widget.objectName() in ["d4","d6","d8","d10","d12","d20","d4_count","d6_count","d8_count","d10_count","d12_count","d20_count"]:
                class_custom_rolls.add_dice(self, widget.objectName(), adjust="subtract")
            elif widget.objectName() == "roll":
                class_custom_rolls.clear_rolls(self)

    def roll_dice(self):
        self.character_name = self.character.character_name
        rolls = []
        for dice in ["d4","d6","d8","d10","d12","d20"]:
            counter = self.findChild(QPushButton, f"{dice}_count")
            if counter.text() != "":
                rolls.append(f"{counter.text()}{dice}")
                counter.setText("")

        roll = "_".join(rolls)
        rolling_dice = DiceRoll(self, self.character_name, "Custom", roll, check = 0, character=self.character).roll()

        self.roll_button.get_widget().setHidden(True)
        title_widgets = self.log_dice.get_title()
        title_widgets[1].setHidden(False)