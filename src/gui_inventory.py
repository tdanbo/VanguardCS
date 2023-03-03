from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons
import functions as func
import functools
import stylesheet as style
import template.stylesheet as tstyle

from character_sheet import CharacterSheet

from gui_new_char import NewCharacter
from gui_sheet import CharacterSheetGUI

from gui_functions import character_xp
from gui_functions import character_stats
from gui_functions import character_morale
from gui_functions import custom_rolls
from gui_functions import roll
from gui_functions import character_reset

class InventoryGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        #Setting up layouts/sections
        
        self.portrait_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 2),
            parent_layout = self.master_layout,
            group = True,
            title = "CHARACTER",
            icon = ("plus.png",cons.WSIZE/2,cons.ICON_COLOR),
            spacing = 3,
            class_group = self.section_group,
        )

        self.inventory_scroll = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            scroll=(True,"bottom"),
            title="INVENTORY",
            group = True,   
            icon = ("combatlog.png",cons.WSIZE/2,cons.ICON_COLOR),	
            class_group = self.section_group,	
        )

        self.equipment_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            title = "WEAPONS & ARMOR",
            group = True,
            spacing=5,
            class_group=self.section_group
        )

        self.currency_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 1),
            parent_layout = self.master_layout,
            title="CURRENCY",
            group = True,   
            class_group = self.section_group	
        )

        self.portrait = Widget(
            widget_type=QLabel(),
            parent_layout=self.portrait_layout.inner_layout(1),
            stylesheet=style.PORTRAIT,
            objectname="portrait",
            class_group=self.widget_group
        )

        self.character_name = Widget(
            widget_type=QComboBox(),
            parent_layout=self.portrait_layout.inner_layout(2),
            stylesheet=style.TEST_COMBO,
            objectname="name",
            text=[""],
            signal=lambda: CharacterSheet(CharacterSheetGUI(), self).load_character(),
            class_group=self.widget_group

        )

        self.character_level= Widget(
            widget_type=QPushButton(),
            parent_layout=self.portrait_layout.inner_layout(2),
            stylesheet=style.BIG_BUTTONS,
            objectname="level",
            signal = lambda: character_xp.adjust_xp(self,adjust="add"),
            class_group=self.widget_group
        )

        portrait_title = self.portrait_layout.get_title()[0]
        portrait_title.clicked.connect(self.open_new_character)

        self.equipment_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        # below you will find the widges that make up the inventory
        for count in range(1,5):
            self.slot_layot = Section(
                outer_layout = QHBoxLayout(),
                inner_layout = ("VBox", 5),
                parent_layout=self.equipment_layout.inner_layout(1),
                content_margin=(0,0,8,0),
                class_group=self.section_group

            )
            self.backpack= Widget(
                widget_type=QToolButton(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(1),
                width = cons.WSIZE*1.50,
                height = cons.WSIZE,
                objectname=f"icon{count}",
                signal=functools.partial(roll.inventory_prepare_double_roll, self,count),
                class_group=self.widget_group
            )

            self.backpack_label = Widget(
                widget_type=QLabel(),
                stylesheet=style.INVENTORY,
                parent_layout=self.slot_layot.inner_layout(1),
                height = cons.WSIZE/1.5,
                objectname=f"icon_label{count}",
                text=f"{count}.",
                align="center",
                class_group=self.widget_group
            )
                
            self.backpack_item = Widget(
                widget_type=QLineEdit(),
                stylesheet=style.INVENTORY,
                parent_layout=self.slot_layot.inner_layout(2),
                height = cons.WSIZE,
                signal= self.select_item,
                objectname=f"inventory{count}",
                align="center",
                class_group=self.widget_group

            )

            self.backpack_item_label = Widget(
                widget_type=QLabel(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(2),
                height = cons.WSIZE/1.5,
                objectname=f"inventory_label{count}",
                align="center",
                class_group=self.widget_group
            )

            self.backpack_action= Widget(
                widget_type=QPushButton(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(3),
                width = cons.WSIZE*3,
                height = cons.WSIZE,
                objectname=f"evoke{count}",
                signal = functools.partial(roll.inventory_prepare_roll, self, "evoke", count),
                class_group=self.widget_group
            )

            self.backpack_action_label = Widget(
                widget_type=QLabel(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(3),
                height = cons.WSIZE/1.5,  
                objectname=f"evoke_label{count}",
                align="center",
                class_group=self.widget_group
            )

            self.backpack= Widget(
                widget_type=QPushButton(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(4),
                width = cons.WSIZE*3,
                height = cons.WSIZE,
                objectname=f"hit_dc{count}",
                signal = functools.partial(roll.inventory_prepare_roll, self, "hit_dc", count),
                class_group=self.widget_group
            )

            self.backpack_hit_label = Widget(
                widget_type=QLabel(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(4),
                height = cons.WSIZE/1.5,
                objectname=f"hit_dc_label{count}",
                align="center",
                class_group=self.widget_group
            )

            self.weapon_modifier = Widget(
                widget_type=QPushButton(),
                stylesheet=style.INVENTORY,
                parent_layout=self.slot_layot.inner_layout(5),
                width = cons.WSIZE*3,
                height = cons.WSIZE,
                objectname=f"roll{count}",
                signal = functools.partial(roll.inventory_prepare_roll, self, "roll", count),
                class_group=self.widget_group

            )

            self.backpack_damage_label = Widget(
                widget_type=QLabel(),
                stylesheet=style.INVENTORY,
                text="",
                parent_layout=self.slot_layot.inner_layout(5),
                height = cons.WSIZE/1.5,
                objectname=f"roll_label{count}",
                align="center",
                class_group=self.widget_group
            )

        self.thaler = Widget(
            widget_type=QLabel(),
            parent_layout=self.currency_section.inner_layout(1),
            stylesheet=style.LABELS,
            objectname="thaler",
            text="0",
            class_group=self.widget_group
        )

        self.Schellings = Widget(
            widget_type=QLabel(),
            parent_layout=self.currency_section.inner_layout(1),
            stylesheet=style.LABELS,
            objectname="schellings",
            text="0",
            class_group=self.widget_group
        )

        self.ortheg = Widget(
            widget_type=QLabel(),
            parent_layout=self.currency_section.inner_layout(1),
            stylesheet=style.LABELS,
            objectname="ortheg",
            text="0",
            class_group=self.widget_group
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)    

    def mousePressEvent(self, event): #this is a very specific event used to subtract values when right clicking on a widget
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if widget.objectName() in ["d4","d6","d8","d10","d12","d20","MOD","d4_count","d6_count","d8_count","d10_count","d12_count","d20_count","MOD_count"]:
                print("Right button was clicked on a stat widget")
                custom_rolls.add_dice(self, widget.objectName(), adjust="subtract")
            elif widget.objectName() == "roll":
                custom_rolls.clear_rolls(self)

    def get_charater(self):
        self.character = self.csheet.findChild(QComboBox, "name").currentText()
        return  self.character

    def open_new_character(self):
        self.new_character = NewCharacter(self)
        self.new_character.show()        

    def select_item(self):
        sender = self.sender()
        if sender.text().lower() in cons.SPELL_LISTS:
            self.spells = SpellsGUI(self, sender)
        else:
            CharacterSheet(self).update_sheet()
