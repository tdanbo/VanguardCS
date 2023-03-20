from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons
import pymongo

from template.section import Section
from template.widget import Widget

from gui_classes.class_roll import DiceRoll
from gui_classes.class_modify_stat import ModifyStat

from gui_widgets.gui_add_sub import AddSub

class InventoryItem(QWidget):
    def __init__(self, character, count, item_dict, layout, equipment=""):
        super().__init__()

        self.character = character

        self.master_layout = QVBoxLayout()
        self.widget_group = []
        self.section_group = []
        self.count = count

        self.equipment = equipment

        color_type = {"melee": "#925833", "armor": "#495c60", "elixirs": "#926f2b"}

        if count % 2 == 0:
            self.bg_color = cons.PRIMARY
        else:
            self.bg_color = cons.PRIMARY_DARKER             

        self.item_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 5),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            spacing=0,
            group=True,
            stylesheet=f"background-color: {self.bg_color};",
            content_margin=(0,0,0,0)       
        )

        self.item_section.inner_layout(1).setContentsMargins(0, 0, 0, 0)
        self.item_section.inner_layout(2).setContentsMargins(1, 1, 1, 1)
        self.item_section.inner_layout(2).setSpacing(1)
        self.item_section.inner_layout(3).setContentsMargins(5, 5, 5, 5)
        self.item_section.inner_layout(4).setContentsMargins(0, 5, 5, 0)
        self.item_section.inner_layout(5).setContentsMargins(5, 12, 5, 5)

        self.item = Widget(
            widget_type=QLineEdit(),
            parent_layout=self.item_section.inner_layout(4),
            objectname=f"{count}",
            class_group=self.widget_group,
            stylesheet=f"font-size: {cons.FONT_MID}; font-weight: bold;",
            height=cons.WSIZE,
            signal=self.get_item
        )

        # CREATING EMPTY OR POPULATED ITEM WIDGET
        if item_dict == {}:
            self.type_bg_color = self.bg_color
            pass # Setting up empty item
        else:
            self.make_item(item_dict)

        # self.divider = QFrame()
        # self.divider.setFixedHeight(1)
        # self.divider.setStyleSheet(f"background-color: {self.type_bg_color}")

        # self.master_layout.addWidget(self.divider)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        # self.divider = QFrame()
        # self.divider.setFixedHeight(1)
        # self.divider.setStyleSheet(f"background-color: {self.type_bg_color}")

        # self.master_layout.addWidget(self.divider)

        self.divider = QFrame()
        self.divider.setFixedHeight(1)
        self.divider.setStyleSheet(f"background-color: {cons.BORDER}")

        self.master_layout.addWidget(self.divider)

        self.master_layout.setSpacing(0)
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_layout)
        self.setFixedHeight(65)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self)

    def get_item(self):
        item_string = self.sender().text()
        item_slot = int(self.sender().objectName())

        print(item_string, item_slot)

        self.all_equipment = self.get_equipment()
        for category in self.all_equipment:
            for item in self.all_equipment[category]:
                if item_string.lower() == item.lower():
                    item_dict = self.all_equipment[category][item]
                    item_dict["Name"] = item
                    item_dict["Category"] = category
                    item_dict["Equipped"] = {}
                    item_dict["Equipped"]["1"] = False
                    item_dict["Equipped"]["2"] = False

                    self.character.CHARACTER_DOC["inventory"].append(item_dict)
                    self.character.set_inventory()
                    self.character.save_document()
                    return
                else:
                    pass

        self.character.CHARACTER_DOC["inventory"].pop(item_slot)
        self.character.set_inventory()
        self.character.save_document()

    def get_equipment(self):
        all_equipment = {}
        client = pymongo.MongoClient(cons.CONNECT)
        # get a list of collection names
        db = client["equipment"]
        collection_names = db.list_collection_names()
        for name in collection_names:
            # get a collection object
            collection = db[name]
            document = collection.find_one()
            all_equipment[name] = document
        return all_equipment

    def make_item(self, item_dict):
        self.item_dict = item_dict
        self.name = self.item_dict["Name"]
        self.category = self.item_dict["Category"]
        self.item_type = self.item_dict["Type"]

        if "Equipped" in self.item_dict:
            self.equipped = self.item_dict["Equipped"]


        color_type = {"melee": "#925833", "ranged": "#925833", "ammunition": "#925833", "armor": "#495c60", "elixirs": "#4e6e5d",  "treasure": "#a7754d", "misc": "#dcccbb"}
        print(self.category)
        self.type_bg_color = color_type[self.category]

        self.item.widget.setText(self.name)

        if "Equip" in item_dict:
            equip = self.item_dict["Equip"]
            if self.equipment != "":
                self.type_label = Widget(
                    widget_type=QPushButton(),
                    parent_layout=self.item_section.inner_layout(2),
                    class_group=self.widget_group,
                    width=7,
                    stylesheet=f"QPushButton {{ background-color: {cons.BORDER_LIGHT}; }}"\
                               f"QPushButton:hover {{ background-color: {self.type_bg_color}; }}",
                    size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
                    objectname=f"{self.equipment}_EQUIPPED",
                    signal=self.prepare_equip_item,
                )

            else:
                for count, state in enumerate(equip):
                    self.type_label = Widget(
                        widget_type=QPushButton(),
                        parent_layout=self.item_section.inner_layout(2),
                        class_group=self.widget_group,
                        width=7,
                        stylesheet=f"QPushButton {{ background-color: {cons.BORDER_LIGHT}; }}"\
                                   f"QPushButton:hover {{ background-color: {self.type_bg_color}; }}",
                        size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
                        objectname=state,
                        signal=self.prepare_equip_item,
                    )
        else:
            self.type_label = Widget(
                widget_type=QLabel(),
                parent_layout=self.item_section.inner_layout(2),
                class_group=self.widget_group,
                width=7,
                stylesheet=f"background-color: {self.bg_color}",
            )

        self.item_section.inner_layout(1).setSpacing(1)

        # If item has qualities


        self.item_label = Widget(
            widget_type=QLineEdit(),
            parent_layout=self.item_section.inner_layout(4),
            text=self.item_type,
            objectname="item",
            class_group=self.section_group,
            height=cons.WSIZE,
            stylesheet=f"color: {self.type_bg_color}; font-size: {cons.FONT_SMALL}; font-weight: bold;",  
            enabled=False,  
        )

        qualities = self.item_dict["Quality"]
        self.quality_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 2),
            parent_layout=self.item_section.inner_layout(3),
            class_group=self.section_group,
            spacing=2,
        )


        for count in range(4):
            try:
                quality = qualities[count]
                quality_tag = quality[:2]
                style = f"QToolButton {{background-color: {cons.BORDER_LIGHT}; color: {self.type_bg_color}; font-weight: bold; font-size: 10px; border-radius: 6px;}}"\
                        f"QToolTip {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 11px;}}"
            except:
                quality = ""
                style = ""
                quality_tag = ""
            try:
                if quality == "Effect":
                    tooltip = f"<b>{quality}</b>: {self.item_dict['Description']}"
                else:
                    tooltip = f"<b>{quality}</b>: {cons.QUALITIES[quality]['Description']}"
            except:
                tooltip = f"<b>{quality}"

            if count > 1:
                layout = 1
            else:
                layout = 2

            self.item_quality = Widget(
                widget_type=QToolButton(),
                parent_layout=self.quality_section.inner_layout(layout),
                objectname=f"quality{count}",
                class_group=self.widget_group,
                #icon=(f"{quality}.png", cons.WSIZE / 2, cons.BORDER_DARK),
                height=20,
                width=20,
                text=quality_tag,
                tooltip=tooltip,
                stylesheet=style
            )

        #self.quality_section.inner_layout(1).setAlignment(Qt.AlignLeft)



        # If item has a roll

        self.roll_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.item_section.inner_layout(5),
            class_group=self.section_group,
            spacing=2,
        )

        if "Roll" in self.item_dict:
            dice_type = self.item_dict["Roll"][0]
            dice = self.item_dict["Roll"][1]

            self.item_dice = Widget(
                widget_type=QToolButton(),
                parent_layout=self.roll_section.inner_layout(1),
                text=dice,
                objectname="item",
                class_group=self.widget_group,
                stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {self.type_bg_color}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;",
                height=cons.WSIZE,
                signal=self.roll_dice,
                property=("roll",dice_type),
            )

        elif "Quantity" in self.item_dict:
            quantity = self.item_dict["Quantity"]

            self.quantity = Widget(
                widget_type=QToolButton(),
                parent_layout=self.roll_section.inner_layout(1),
                text=f"x {quantity}",
                objectname="quantity",
                class_group=self.widget_group,
                stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;",
                height=cons.WSIZE,
                signal=self.add_sub,
            )

        self.type_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(1),
            objectname="item",
            class_group=self.widget_group,
            width=7,
            stylesheet=f"background-color: {self.type_bg_color}",
            
        )

        self.roll_section.inner_layout(1).setAlignment(Qt.AlignRight)

        # self.item_section.inner_layout(2).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(5).setAlignment(Qt.AlignTop)
        self.item_label.get_widget().setAlignment(Qt.AlignTop)

    def add_sub(self):
        add_sub_gui = AddSub(self.character, self.sender(), doc_item = self.count, item=True)
        add_sub_gui.show()

    def roll_dice(self):
        self.character_name = self.character.character_name
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

        rolling_dice = DiceRoll(self.sender(),self.character_name,self.roll_type.capitalize(), self.dice, check = self.check, character=self.character, ammo=needs_ammo).roll()

    def prepare_equip_item(self):
        print("EQUIP")
        self.equip_button = self.sender()
        self.equip_button_type = self.equip_button.objectName()

        print(self.equip_button)
        print(self.equip_button_type)

        if "EQUIPPED" in self.equip_button_type:
            self.unequip_item()
            print("UNEQUIP")
        else:
            self.equip_item()
            print("EQUIP")

    def equip_item(self):
        if self.equip_button_type == "2H":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)

            if self.character.CHARACTER_DOC["equipment"]["main hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["main hand"])
            if self.character.CHARACTER_DOC["equipment"]["off hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["off hand"])

            self.character.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict
            self.character.CHARACTER_DOC["equipment"]["off hand"] = {}

            self.equip_button.setObjectName("2H_EQUIPPED")

        elif self.equip_button_type == "MH":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)
            
            if self.character.CHARACTER_DOC["equipment"]["main hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["main hand"])

            self.character.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict

            self.equip_button.setObjectName("MH_EQUIPPED")

        elif self.equip_button_type == "OH":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)
            
            if self.character.CHARACTER_DOC["equipment"]["off hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["off hand"])

            self.character.CHARACTER_DOC["equipment"]["off hand"] = self.item_dict

            self.equip_button.setObjectName("OH_EQUIPPED")

        elif self.equip_button_type == "AR":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)
            
            if self.character.CHARACTER_DOC["equipment"]["armor"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["armor"])

            self.character.CHARACTER_DOC["equipment"]["armor"] = self.item_dict

            self.equip_button.setObjectName("AR_EQUIPPED")
        
        self.set_impeding()
        self.character.set_inventory()
        self.character.set_equipment()
        self.character.set_modifiers()
        self.character.save_document()

    def unequip_item(self):
        if self.equip_button_type == "2H_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["main hand"])
            self.character.CHARACTER_DOC["equipment"]["main hand"] = {}
            self.equip_button.setObjectName("2H")

        elif self.equip_button_type == "MH_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["main hand"])
            self.character.CHARACTER_DOC["equipment"]["main hand"] = {}
            self.equip_button.setObjectName("MH")

        elif self.equip_button_type == "OH_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["off hand"])
            self.character.CHARACTER_DOC["equipment"]["off hand"] = {}
            self.equip_button.setObjectName("OH")

        elif self.equip_button_type == "AR_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(self.character.CHARACTER_DOC["equipment"]["armor"])
            self.character.CHARACTER_DOC["equipment"]["armor"] = {}
            self.equip_button.setObjectName("AR")

        self.set_impeding()
        self.character.set_inventory()
        self.character.set_equipment()
        self.character.set_modifiers()
        self.character.save_document()

    def set_impeding(self):
        defense = 0
        casting = 0
        speed = 0
        armor = self.character.CHARACTER_DOC["equipment"]["armor"]
        if armor != {}:
            impeding = [quality for quality in armor["Quality"] if "Impeding" in quality][0]
            value = ModifyStat(impeding).find_integer()
            speed += value
            defense += value
            casting += value

        mh = self.character.CHARACTER_DOC["equipment"]["main hand"]
        if mh != {}:
            if mh["Name"] in ["Shield","Buckler"]:
                defense -= 1
            elif mh["Name"] == "Steel Shield":
                defense -= 2

        oh = self.character.CHARACTER_DOC["equipment"]["off hand"]
        if oh != {}:
            if oh["Name"] in ["Shield","Buckler"]:
                defense -= 1
            elif oh["Name"] == "Steel Shield":
                defense -= 2


        self.character.CHARACTER_DOC["DEFENSE mod"] = defense
        self.character.CHARACTER_DOC["CASTING mod"] = casting
        self.character.CHARACTER_DOC["SNEAKING mod"] = speed

