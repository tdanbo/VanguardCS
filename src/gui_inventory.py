
import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from template.section import Section
from template.widget import Widget
import constants as cons
import pymongo

#from gui_classes.custom_roll import class_custom_rolls
from gui_classes.class_character import Character

from gui_classes.class_roll import DiceRoll
from gui_widgets.gui_new_char_frame import NewCharacter
from gui_widgets.gui_add_sub import AddSub

class InventoryGUI(QWidget):
    def __init__(self, character):
        super().__init__()

        # setting up character sheet
        self.character = character

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []
        self.master_layout.setContentsMargins(0,0,0,0)
        self.master_layout.setSpacing(0)
        #Setting up layouts/sections
        
        self.portrait_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 2),
            parent_layout = self.master_layout,
            group = True,
            title = "Test",
            icon = ("plus.png",cons.WSIZE/2,cons.FONT_COLOR),
            class_group = self.section_group,
            spacing=3,
            height=100
        )

        self.portrait_layout.get_title()[1].setText("")
        self.portrait_layout.get_title()[0].setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};")


        self.name_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.portrait_layout.inner_layout(2),
            class_group=self.section_group,
            content_margin=(0,0,0,0),
            spacing=3,
        )

        scroll_style = f"QScrollBar {{background-color: {cons.PRIMARY}; width: 6px;}}"\
                       f"QWidget {{background-color: {cons.PRIMARY};}}"\
                       f"QScrollBar::handle:vertical {{background-color: {cons.BORDER}; width: 6px; min-height: 20px; border: none; outline: none;}}"\

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
            stylesheet=scroll_style	
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
            text=[""],
            objectname="name",
            class_group=self.widget_group,
            signal=self.load_character,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; font-size: {cons.FONT_MID}; font-weight: bold; color: {cons.FONT_COLOR};",

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
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.experience_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(1),
            objectname = "",
            class_group=self.widget_group,
            text = "XP",
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        )

        self.unspent_experience= Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(2),
            objectname="total experience",
            signal = self.add_sub,
            class_group=self.widget_group,
            height=cons.WSIZE*1.5,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"

        )

        self.unspent_experience_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(2),
            objectname = "experience_label",
            class_group=self.widget_group,
            text = "UNSPENT XP",
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
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
            content_margin=(0,0,0,0),
            spacing=0,
            height=216
        )

        self.equipment_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.bottom_section = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("HBox", 1),
            parent_layout = self.master_layout,
            class_group = self.section_group,
            spacing=3,
            height=100,
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
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;",
                signal=self.check_modifier,
                checkable=True,
                checked=False,
            )

            self.extra_modifier_label = Widget(
                widget_type=QToolButton(),
                parent_layout=self.active_section.inner_layout(number+1),
                icon=(f"{stat.capitalize()}.png","",cons.DARK,cons.WSIZE),
                class_group=self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
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
            objectname="modifier",
            class_group=self.widget_group,
            stylesheet=f"background-color: {cons.FONT_COLOR}; color: {cons.FONT_LIGHT}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal = lambda: self.adjust_modifier("add")
        )

        self.modifier_label = Widget(
            widget_type=QToolButton(),
            parent_layout=self.modifier_section.inner_layout(1),
            icon=(f"Modifier.png","",cons.PRIMARY_LIGHTER,cons.WSIZE),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            objectname="modifier button",
            stylesheet=f"background-color: {cons.FONT_COLOR}; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
            signal = lambda: self.adjust_modifier("add")
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setFixedWidth(300)
        self.setStyleSheet(
            f"border-style: outset; color: {cons.FONT_DARK}; background-color: {cons.DARK};border-style: outset;"
        )
        self.setLayout(self.master_layout)   
        self.update_character_dropdown() 
        self.character.set_inventory_gui(self)

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
            signal= lambda: self.find_item,
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
            if widget.objectName() in ["modifier","modifier button"]:
                self.adjust_modifier("subtract")

    def load_character(self):
        self.current_character_name = self.sender().currentText()
        self.character.load_document(self.current_character_name)

    def find_item(self):
        print("WHAT")

    def open_new_character(self):
        self.new_character = NewCharacter(self, self.character)
        self.new_character.show()        

    def update_character_dropdown(self):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]
        character_list = self.collection.distinct("character")
        self.character_name.get_widget().addItems(character_list)

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

        rolling_dice = DiceRoll(self.sender(),self.combat_log,self.character,self.roll_type.capitalize(),self.dice, check = self.check).roll()

    def add_sub(self):
        doc_string = self.sender().objectName()
        add_sub_gui = AddSub(self.character, self.sender(), doc_item = doc_string)
        add_sub_gui.show()

    def check_modifier(self):
        mod = self.sender().objectName().split(" ")[0]
        print(mod)

        type_color = cons.ACTIVE_COLOR[mod]
        current_mod = self.findChild(QWidget, mod+" mod")
        current_button = self.findChild(QWidget, mod+" button")

        for button in ["ATTACK mod","DEFENSE mod","CASTING mod","SNEAKING mod"]:
            if button != current_mod.objectName():
                mod_widget = self.findChild(QWidget, button)
                mod_widget.setChecked(False)
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
                mod_widget.setStyleSheet(stylesheet)

        for mod in ["ATTACK button","DEFENSE button","CASTING button","SNEAKING button"]:
            if mod != current_button.objectName():
                mod_widget = self.findChild(QWidget, mod)
                mod_widget.setChecked(False)
                stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
                mod_widget.setStyleSheet(stylesheet)


        if self.sender().isChecked():
            current_button.setStyleSheet(f"background-color: {type_color}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
            current_mod.setStyleSheet(f"background-color: {type_color}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;")
            current_mod.setChecked(True)
            current_button.setChecked(True)
        else:
            current_button.setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
            current_mod.setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;")
            current_mod.setChecked(False)
            current_button.setChecked(False)
    def adjust_modifier(self, adjust):
        current_value = int(self.modifier_button.get_widget().text())
        if adjust == "add":
            current_value += 1
        else:
            current_value -= 1
        
        if current_value > 0:
            current_value = f"+{current_value}"
        self.modifier_button.get_widget().setText(str(current_value))   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryGUI()
    window.show()
    sys.exit(app.exec_())