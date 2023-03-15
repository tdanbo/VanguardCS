from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons
import functions as func
import functools
import pymongo


from gui_functions import character_xp
from gui_functions import custom_rolls

from gui_functions.class_roll import DiceRoll

from gui_windows.gui_new_char_frame import NewCharacter
from gui_windows.gui_add_sub import AddSub

class InventoryGUI(QWidget):
    def __init__(self, csheet):
        super().__init__()

        # setting up character sheet
        self.character_sheet = csheet

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []
        self.master_layout.setContentsMargins(0,0,0,0)
        #Setting up layouts/sections
        
        self.portrait_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 2),
            parent_layout = self.master_layout,
            group = True,
            title = "Test",
            icon = ("plus.png",cons.WSIZE/2,cons.ICON_COLOR),
            class_group = self.section_group,
            spacing=3
        )

        self.portrait_layout.get_title()[1].setText("")
        
        self.name_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.portrait_layout.inner_layout(2),
            class_group=self.section_group,
            content_margin=(0,0,0,0),
            spacing=3,
        )

        self.inventory_scroll = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            scroll=(True,"bottom"),
            title="BACKPACK",
            group = True,   
            class_group = self.section_group,
            spacing=0,
            content_margin=(0,0,0,0),	
        )

        self.inventory_scroll.get_title()[1].setAlignment(Qt.AlignCenter)

        self.portrait = Widget(
            widget_type=QLabel(),
            parent_layout=self.portrait_layout.inner_layout(1),
            objectname="portrait",
            class_group=self.widget_group,
            height= 58,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
            # width=cons.WSIZE*6,
        )

        self.portrait.get_widget().setAlignment(Qt.AlignCenter)
    

        self.character_name = Widget(
            widget_type=QComboBox(),
            parent_layout=self.portrait_layout.get_title()[2],
            objectname="name",
            text=[""],
            class_group=self.widget_group,
            signal=lambda: self.character_sheet.load_character(self,self.character_name.get_widget().currentText()),
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",

        )

        self.experience_section = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 2),
            parent_layout = self.name_layout.inner_layout(2),
            class_group=self.section_group,
            spacing = 3,
        )

        self.experience= Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(1),
            objectname="experience",
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 16px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.experience_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(1),
            objectname = "",
            class_group=self.widget_group,
            text = "XP",
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        )

        self.unspent_experience= Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(2),
            objectname="total experience",
            signal = self.add_sub,
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 16px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.unspent_experience_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(2),
            objectname = "experience_label",
            class_group=self.widget_group,
            text = "UNSPENT XP",
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        )

        portrait_title = self.portrait_layout.get_title()[0]
        portrait_title.clicked.connect(self.open_new_character)

        self.equipment_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 2),
            parent_layout = self.master_layout,
            group = True,
            title = "EQUIPMENT",
            class_group = self.section_group,
            spacing=0,
            content_margin=(0,0,0,0),
            height=240	
        )

        self.equipment_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.bottom_section = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("HBox", 1),
            parent_layout = self.master_layout,
            class_group = self.section_group,
            spacing=3,
            height=98,
        )
            
        self.active_section = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 4),
            parent_layout = self.bottom_section.inner_layout(1),
            title="ACTIVE",
            group = True,
            class_group = self.section_group,
            spacing=3
        )

        self.active_section.get_title()[1].setAlignment(Qt.AlignCenter)

        #Below is all the widgets used in the character sheet
        for number,stat in enumerate(["ATTACK","DEFENSE","CASTING","SNEAKING"]):
            self.extra_modifier_button = Widget(
                widget_type=QPushButton(),
                parent_layout = self.active_section.inner_layout(number+1),
                objectname=f"{stat} mod",
                class_group=self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
                stylesheet=f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
            )

            self.extra_modifier_label = Widget(
                widget_type=QToolButton(),
                parent_layout=self.active_section.inner_layout(number+1),
                icon=(f"{stat.capitalize()}.png","",cons.FONT_COLOR,cons.WSIZE),
                class_group=self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
                stylesheet=f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_DARK}; font-size: 10px; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
                checkable=True,
                checked=False,
                objectname=f"{stat} button",
                signal=self.check_modifier,
            )

        self.modifier_section = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 5),
            parent_layout = self.bottom_section.inner_layout(1),
            title="MODIFIER",
            group = True,
            class_group = self.section_group,
            spacing=3,
            width = 60
        )

        self.modifier_section.get_title()[1].setAlignment(Qt.AlignCenter)

        self.modifier_button = Widget(
            widget_type=QPushButton(),
            parent_layout = self.modifier_section.inner_layout(1),
            signal=lambda: self.adjust_modifier("add"),
            objectname="modifier",
            class_group=self.widget_group,
            stylesheet=f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        )

        self.modifier_label = Widget(
            widget_type=QToolButton(),
            parent_layout=self.modifier_section.inner_layout(1),
            icon=(f"Modifier.png","",cons.FONT_COLOR,cons.WSIZE),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            stylesheet=f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_DARK}; font-size: 10px; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
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
        if count % 2 == 0:
            color = cons.PRIMARY_DARKER
        else:
            color = cons.PRIMARY

        self.slot_layot = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 5),
            parent_layout=layout,
            class_group=self.section_group,
            stylesheet=f"background-color: {color};"

        )
        self.backpack= Widget(
            widget_type=QToolButton(),
            text="",
            parent_layout=self.slot_layot.inner_layout(1),
            width = cons.WSIZE*1.50,
            height = cons.WSIZE*1.5,
            objectname=f"icon{descriptor}{count}",
            class_group=self.widget_group
        )

        self.backpack_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.slot_layot.inner_layout(1),
            height = cons.WSIZE/1.5,
            objectname=f"icon_label{descriptor}{count}",
            text=f"{count}.",
            align="center",
            class_group=self.widget_group
        )
            
        self.backpack_item = Widget(
            widget_type=QLineEdit(),
            parent_layout=self.slot_layot.inner_layout(2),
            height = cons.WSIZE*1.5,
            signal= lambda: self.character_sheet.update_sheet(),
            objectname=f"item{count}",
            class_group=self.widget_group,
            align="center",

        )

        self.backpack_item_label = Widget(
            widget_type=QLabel(),
            text="",
            parent_layout=self.slot_layot.inner_layout(2),
            height = cons.WSIZE/1.5,
            objectname=f"inventory_label{count}",
            align="center",
            class_group=self.widget_group
        )

        self.backpack= Widget(
            widget_type=QPushButton(),
            text="",
            parent_layout=self.slot_layot.inner_layout(4),
            height = cons.WSIZE*1.5,
            objectname=f"quality{count}",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed)
        )

        self.backpack_hit_label = Widget(
            widget_type=QLabel(),
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
            parent_layout=self.slot_layot.inner_layout(5),
            height = cons.WSIZE,
            objectname=f"roll{count}",
            class_group=self.widget_group,
            stylesheet=f"font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;"

        )

        self.backpack_damage_label = Widget(
            widget_type=QLabel(),
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
            if widget.objectName() == "modifier":
                self.adjust_modifier("subtract")
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

    def roll_dice(self):
        print("rolling dice")
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

    def add_sub(self):
        doc_string = self.sender().objectName()
        add_sub_gui = AddSub(self.character_sheet, self.sender(), doc_item = doc_string)
        add_sub_gui.show()

    def check_modifier(self):
        current_mod = self.sender()
        current_mod_name = current_mod.objectName()
        current_button_name = current_mod_name.replace("button","mod")
        current_button = self.findChild(QWidget, current_button_name)
        print(current_button)

        for button in ["ATTACK button","DEFENSE button","CASTING button","SNEAKING button"]:
            if button != current_mod_name:
                mod_widget = self.findChild(QWidget, button)
                mod_widget.setChecked(False)
                stylesheet=f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
                mod_widget.setStyleSheet(stylesheet)

        for mod in ["ATTACK mod","DEFENSE mod","CASTING mod","SNEAKING mod"]:
            if mod != current_button_name:
                mod_widget = self.findChild(QWidget, mod)
                mod_widget.setChecked(False)
                stylesheet=f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
                mod_widget.setStyleSheet(stylesheet)


        if current_mod.isChecked():
            current_button.setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 20px; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;")
            current_mod.setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 10px; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
        else:
            current_button.setStyleSheet(f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;")
            current_mod.setStyleSheet(f"background-color: {cons.PRIMARY_DARKER}; color: {cons.FONT_COLOR}; font-size: 20px; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")

    def adjust_modifier(self, adjust):
        current_value = int(self.modifier_button.get_widget().text())
        if adjust == "add":
            current_value += 1
        else:
            current_value -= 1
        self.modifier_button.get_widget().setText(str(current_value))   