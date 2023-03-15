from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons

from template.section import Section
from template.widget import Widget

from gui_functions.class_roll import DiceRoll
from gui_functions.class_modify_stat import ModifyStat

from gui_windows.gui_add_sub import AddSub

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
        self.item_type = self.item_dict["Type"]

        if "Equipped" in self.item_dict:
            self.equipped = self.item_dict["Equipped"]


        color_type = {"melee": "#925833", "ranged": "#925833", "armor": "#495c60", "elixirs": "#926f2b", "ammunition": "#925833", "treasure": "#926f2b", "misc": "#926f2b"}
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

        # If item has qualities

        if "Quality" in self.item_dict:
            qualities = self.item_dict["Quality"]
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

            self.quality_section.inner_layout(1).setAlignment(Qt.AlignLeft)

        self.item_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(3),
            text=self.item_type,
            objectname="item",
            class_group=self.widget_group,
            align="right",
            height=cons.WSIZE,
            
        )

        # If item has a roll

        if "Roll" in self.item_dict:
            dice_type = self.item_dict["Roll"][0]
            dice = self.item_dict["Roll"][1]

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

        elif "Quantity" in self.item_dict:
            quantity = self.item_dict["Quantity"]

            self.quantity = Widget(
                widget_type=QToolButton(),
                parent_layout=self.item_section.inner_layout(3),
                text=str(quantity),
                objectname="quantity",
                class_group=self.widget_group,
                stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {self.type_bg_color}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;",
                height=cons.WSIZE,
                signal=self.add_sub,
            )

        self.item_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(2).setAlignment(Qt.AlignRight)
        self.item_label.get_widget().setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def add_sub(self):
        add_sub_gui = AddSub(self.character_sheet, self.sender(), doc_item = self.count, item=True)
        add_sub_gui.show()

    def roll_dice(self):
        self.character = self.character_sheet.character_name
        self.roll_type = self.sender().property("roll") 

        if self.roll_type in cons.STATS:
            self.check = int(self.sender().text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = self.sender().text()

        if self.item_type == "Ranged Weapon":
            needs_ammo = True
        else:
            needs_ammo = False

        rolling_dice = DiceRoll(self.combat_log,self.character,self.roll_type.capitalize(), self.dice, check = self.check, sheet=self.character_sheet, ammo=needs_ammo).roll()

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
        
        self.set_impeding()
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

        self.set_impeding()
        self.character_sheet.update_sheet()

    def set_impeding(self):
        defense = 0
        casting = 0
        speed = 0
        armor = self.character_sheet.CHARACTER_DOC["equipment"]["armor"]
        if armor != {}:
            impeding = [quality for quality in armor["Quality"] if "Impeding" in quality][0]
            print(impeding)
            value = ModifyStat(impeding).find_integer()
            speed += value
            defense += value
            casting += value

        mh = self.character_sheet.CHARACTER_DOC["equipment"]["main hand"]
        if mh != {}:
            if mh["Name"] in ["Shield","Buckler"]:
                defense -= 1
            elif mh["Name"] == "Steel Shield":
                defense -= 2

        oh = self.character_sheet.CHARACTER_DOC["equipment"]["off hand"]
        if oh != {}:
            if oh["Name"] in ["Shield","Buckler"]:
                defense -= 1
            elif oh["Name"] == "Steel Shield":
                defense -= 2


        self.character_sheet.CHARACTER_DOC["DEFENSE mod"] = defense
        self.character_sheet.CHARACTER_DOC["CASTING mod"] = casting
        self.character_sheet.CHARACTER_DOC["SNEAKING mod"] = speed