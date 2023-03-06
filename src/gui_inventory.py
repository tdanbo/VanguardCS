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
import pymongo

from class_sheet import CharacterSheet

from gui_functions import character_xp
from gui_functions import character_stats
from gui_functions import character_morale
from gui_functions import custom_rolls
from gui_functions import roll
from gui_functions import character_reset

from gui_windows.gui_new_char import NewCharacter

class InventoryGUI(QWidget):
    def __init__(self, csheet):
        super().__init__()

        # setting up character sheet
        self.character_sheet = csheet

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
            class_group = self.section_group,
            spacing=3
        )

        self.name_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.portrait_layout.inner_layout(2),
            class_group=self.section_group,
            content_margin=(0,0,0,0),
        )

        self.inventory_scroll = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            scroll=(True,"bottom"),
            title="EQUIPMENT",
            group = True,   
            class_group = self.section_group,
            spacing=5,	
        )

        for count in range(15, 0, -1):
            print(count)
            self.make_item_slot(count, self.inventory_scroll.inner_layout(1), "inventory")

        self.inventory_scroll.get_title()[1].setAlignment(Qt.AlignCenter)

        self.portrait = Widget(
            widget_type=QLabel(),
            parent_layout=self.portrait_layout.inner_layout(1),
            objectname="portrait",
            class_group=self.widget_group,
            height=cons.WSIZE*2,
            width=cons.WSIZE*6,
        )

        self.portrait.get_widget().setAlignment(Qt.AlignCenter)
    

        self.character_name = Widget(
            widget_type=QComboBox(),
            parent_layout=self.name_layout.inner_layout(1),
            stylesheet=style.TEST_COMBO,
            objectname="name",
            text=[""],
            class_group=self.widget_group,
            signal=lambda: self.character_sheet.load_character(self,self.character_name.get_widget().currentText()),

        )

        self.experience= Widget(
            widget_type=QLineEdit(),
            parent_layout=self.name_layout.inner_layout(2),
            stylesheet=tstyle.WIDGETS,
            objectname="experience",
            class_group=self.widget_group,
            align="center"
        )

        self.unspent_experience= Widget(
            widget_type=QLineEdit(),
            parent_layout=self.name_layout.inner_layout(2),
            stylesheet=tstyle.WIDGETS,
            objectname="unspent_experience",
            signal = lambda: character_xp.adjust_xp(self,adjust="add"),
            class_group=self.widget_group,
            align="center"
        )

        portrait_title = self.portrait_layout.get_title()[0]
        portrait_title.clicked.connect(self.open_new_character)

        self.combat_section = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 3),
            parent_layout = self.master_layout,
            title="COMBAT",
            group = True,   
            class_group = self.section_group	
        )

        self.combat_section.get_title()[1].setAlignment(Qt.AlignCenter)

        self.armor = Widget(
            widget_type=QPushButton(),
            parent_layout=self.combat_section.inner_layout(1),
            stylesheet=tstyle.WIDGETS,
            objectname="armor",
            text="0",
            class_group=self.widget_group
        )
        self.armor_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.combat_section.inner_layout(1),
            stylesheet=tstyle.LABELS,
            objectname="armor_label",
            text="ARMOR",
            align="center",
            class_group=self.widget_group
        )

        self.defense = Widget(
            widget_type=QPushButton(),
            parent_layout=self.combat_section.inner_layout(2),
            stylesheet=tstyle.WIDGETS,
            objectname="defense",
            text="0",
            class_group=self.widget_group
        )
        self.defense_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.combat_section.inner_layout(2),
            stylesheet=tstyle.LABELS,
            objectname="defense_label",
            text="DEFENSE",
            align=Qt.AlignCenter,
            class_group=self.widget_group
        )
        self.damage = Widget(
            widget_type=QPushButton(),
            parent_layout=self.combat_section.inner_layout(3),
            stylesheet=tstyle.WIDGETS,
            objectname="damage",
            text="0",
            class_group=self.widget_group
        )

        self.damage_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.combat_section.inner_layout(3),
            stylesheet=tstyle.LABELS,
            objectname="damage_label",
            text="DAMAGE",
            align=Qt.AlignCenter,
            class_group=self.widget_group
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)   

        #Updating the character dropdown
        self.character_sheet.set_inv_vars(self)
        self.update_character_dropdown() 

    def make_item_slot(self,count,layout,descriptor):
        self.slot_layot = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 5),
            parent_layout=layout,
            class_group=self.section_group

        )
        self.backpack= Widget(
            widget_type=QToolButton(),
            stylesheet=style.INVENTORY,
            text="",
            parent_layout=self.slot_layot.inner_layout(1),
            width = cons.WSIZE*1.50,
            height = cons.WSIZE*1.5,
            objectname=f"icon{descriptor}{count}",
            signal=functools.partial(roll.inventory_prepare_double_roll, self,count),
            class_group=self.widget_group
        )

        self.backpack_label = Widget(
            widget_type=QLabel(),
            stylesheet=style.INVENTORY,
            parent_layout=self.slot_layot.inner_layout(1),
            height = cons.WSIZE/1.5,
            objectname=f"icon_label{descriptor}{count}",
            text=f"{count}.",
            align="center",
            class_group=self.widget_group
        )
            
        self.backpack_item = Widget(
            widget_type=QLineEdit(),
            stylesheet=style.INVENTORY,
            parent_layout=self.slot_layot.inner_layout(2),
            height = cons.WSIZE*1.5,
            signal= lambda: self.character_sheet.update_sheet(),
            objectname=f"item{count}",
            class_group=self.widget_group,
            align="center",

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

        self.backpack= Widget(
            widget_type=QPushButton(),
            stylesheet=style.INVENTORY,
            text="",
            parent_layout=self.slot_layot.inner_layout(4),
            height = cons.WSIZE*1.5,
            objectname=f"quality{count}",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed)
        )

        self.backpack_hit_label = Widget(
            widget_type=QLabel(),
            stylesheet=style.INVENTORY,
            text="",
            parent_layout=self.slot_layot.inner_layout(4),
            height = cons.WSIZE/1.5,
            objectname=f"quality_label{count}",
            align="center",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed)
        )

        self.weapon_modifier = Widget(
            widget_type=QPushButton(),
            stylesheet=style.INVENTORY,
            parent_layout=self.slot_layot.inner_layout(5),
            height = cons.WSIZE*1.5,
            objectname=f"roll{count}",
            signal = functools.partial(roll.inventory_prepare_roll, self, "roll", count),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed)

        )

        self.backpack_damage_label = Widget(
            widget_type=QLabel(),
            stylesheet=style.INVENTORY,
            text="",
            parent_layout=self.slot_layot.inner_layout(5),
            height = cons.WSIZE/1.5,
            objectname=f"roll_label{count}",
            align="center",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed)
        )

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
        self.new_character = NewCharacter(self, self.character_sheet)
        self.new_character.show()        

    def select_item(self):
        self.character_sheet.update_sheet()

    def update_character_dropdown(self):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]
        character_list = self.collection.distinct("character")
        self.character_name.get_widget().addItems(character_list)
