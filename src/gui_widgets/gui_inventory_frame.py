from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons

from template.section import Section
from template.widget import Widget
import template.functions as func

from gui_classes.class_roll import DiceRoll
from gui_classes.class_modify_stat import ModifyStat

from gui_widgets.gui_add_sub import AddSub


class InventoryItem(QWidget):
    def __init__(self, character, count, item_dict, layout, carry_weight, equipment=""):
        super().__init__()

        self.character = character

        self.master_layout = QVBoxLayout()
        self.widget_group = []
        self.section_group = []
        self.count = count
        self.carry_weight = carry_weight
        self.item_dict = item_dict

        self.equipment = equipment

        color_type = {"melee": "#925833", "armor": "#495c60", "elixirs": "#926f2b"}

        if count % 2 == 0:
            self.bg_color = cons.PRIMARY
            color = QColor(cons.PRIMARY)
            self.bg_darker_color = color.darker(130).name()
            if count > self.carry_weight:
                self.bg_color = self.bg_darker_color
        else:
            self.bg_color = cons.PRIMARY_DARKER
            color = QColor(cons.PRIMARY_DARKER)
            self.bg_darker_color = color.darker(130).name()
            if count > self.carry_weight:
                self.bg_color = self.bg_darker_color

        self.item_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 5),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            spacing=0,
            group=True,
            stylesheet=f"background-color: {self.bg_color};",
            content_margin=(0, 0, 0, 0),
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
            signal=self.get_item,
            align="center",
        )

        # CREATING EMPTY OR POPULATED ITEM WIDGET
        if self.item_dict == {}:
            self.type_bg_color = self.bg_color
            pass  # Setting up empty item
        else:
            self.make_item()

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.divider = QFrame()
        self.divider.setFixedHeight(1)
        self.divider.setStyleSheet(f"background-color: {cons.BORDER}")

        self.master_layout.addWidget(self.divider)

        self.master_layout.setSpacing(0)
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.master_layout)
        self.setFixedHeight(65)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        if self.equipment:
            self.item.widget.setDisabled(True)

        layout.addWidget(self)

    def get_item(self):
        item_string = self.sender().text()
        item_slot = int(self.sender().objectName())

        self.all_equipment = cons.EQUIPMENT
        if item_string != "":
            for category in self.all_equipment:
                for item in self.all_equipment[category]:
                    if item_string.lower() == item.lower():
                        self.item_dict = self.all_equipment[category][item]
                        self.item_dict["Name"] = item
                        self.item_dict["Category"] = category
                        self.item_dict["Equipped"] = {}
                        self.item_dict["Equipped"]["1"] = False
                        self.item_dict["Equipped"]["2"] = False

                        self.character.CHARACTER_DOC["inventory"].append(self.item_dict)
                        self.character.set_all_stats()
                        return
                    else:
                        pass

            # Create General Good item!
            self.item_dict = self.general_item()
            self.item_dict["Name"] = item_string.title()
            self.item_dict["Category"] = "General Good"
            self.item_dict["Equipped"] = {}
            self.item_dict["Equipped"]["1"] = False
            self.item_dict["Equipped"]["2"] = False

            self.character.CHARACTER_DOC["inventory"].append(self.item_dict)
            self.character.set_all_stats()
            return

    def delete_item(self):
        self.character.CHARACTER_DOC["inventory"].pop(self.count)
        self.character.set_all_stats()

    def general_item(self):
        item = {"Quantity": 1, "Type": "General Good", "Quality": []}
        return item

    def make_item(self):
        self.name = self.item_dict["Name"]
        self.category = self.item_dict["Category"]
        self.item_type = self.item_dict["Type"]

        if "Equipped" in self.item_dict:
            self.equipped = self.item_dict["Equipped"]

        if self.category.upper() in cons.ACTIVE_COLOR:
            self.type_bg_color = cons.ACTIVE_COLOR[self.category.upper()]
            color = QColor(self.type_bg_color)
            self.dark_type_bg_color = color.darker(150)
        else:
            self.type_bg_color = cons.ACTIVE_COLOR["GENERAL_GOOD"]
            color = QColor(self.type_bg_color)
            self.dark_type_bg_color = color.darker(150)

        self.item.widget.setText(self.name)
        self.item.widget.setAlignment(Qt.AlignLeft)
        self.item.widget.setDisabled(True)

        if "Equip" in self.item_dict:
            equip = self.item_dict["Equip"]
            if self.equipment != "":
                self.type_label = Widget(
                    widget_type=QPushButton(),
                    parent_layout=self.item_section.inner_layout(2),
                    class_group=self.widget_group,
                    width=10,
                    stylesheet=f"QPushButton {{ background-color: {cons.BORDER_LIGHT}; }}"
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
                        width=10,
                        stylesheet=f"QPushButton {{ background-color: {cons.BORDER_LIGHT}; }}"
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
                style = (
                    f"QToolButton {{background-color: {cons.BORDER_LIGHT}; color: {self.type_bg_color}; font-weight: bold; font-size: 10px; border-radius: 6px;}}"
                    f"QToolTip {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 11px;}}"
                )
            except:
                quality = ""
                style = ""
                quality_tag = ""
            try:
                if quality == "Effect":
                    tooltip = rf"<b>{quality}</b>: {self.item_dict['Description']}"
                else:
                    tooltip = f"<b>{quality}</b>: {str(cons.QUALITIES[quality]['Description'])}"
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
                # icon=(f"{quality}.png", cons.WSIZE / 2, cons.BORDER_DARK),
                height=20,
                width=20,
                text=quality_tag,
                tooltip=tooltip,
                stylesheet=style,
            )

        # self.quality_section.inner_layout(1).setAlignment(Qt.AlignLeft)

        # If item has a roll

        self.roll_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 2),
            parent_layout=self.item_section.inner_layout(5),
            class_group=self.section_group,
            spacing=2,
        )

        self.dice_button_style = (
            f"QToolButton {{padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {self.type_bg_color}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;}}"
            f"QToolButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
            f"QToolButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
        )

        self.quantity_dice_button_style = (
            f"QToolButton {{padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: 12px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;}}"
            f"QToolButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
            f"QToolButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
        )

        if "Roll" in self.item_dict:
            dice_type = self.item_dict["Roll"][0]
            dice = self.item_dict["Roll"][1].replace("D", "d")

            self.item_dice = Widget(
                widget_type=QToolButton(),
                parent_layout=self.roll_section.inner_layout(1),
                text=dice,
                objectname="item",
                class_group=self.widget_group,
                height=cons.WSIZE,
                signal=self.roll_dice,
                property=("roll", dice_type),
                stylesheet=self.dice_button_style,
            )

        elif "Quantity" in self.item_dict:
            quantity = self.item_dict["Quantity"]

            self.quantity = Widget(
                widget_type=QToolButton(),
                parent_layout=self.roll_section.inner_layout(1),
                text=f"x {quantity}",
                objectname="quantity",
                class_group=self.widget_group,
                height=cons.WSIZE,
                signal=self.add_sub,
                stylesheet=self.quantity_dice_button_style,
            )

            if self.equipment == "codex":
                self.quantity.get_widget().setDisabled(True)

        self.roll_section.inner_layout(2).setAlignment(Qt.AlignRight)

        if self.equipment == "codex":
            print("CODEX")
            self.cost_label = Widget(
                widget_type=QLabel(),
                parent_layout=self.roll_section.inner_layout(2),
                text=f"{self.item_dict['Cost']}",
                objectname="cost",
                class_group=self.widget_group,
                height=cons.WSIZE,
                stylesheet=f"color: {self.type_bg_color}; font-size: {cons.FONT_SMALL};",
            )

            self.type_label = Widget(
                widget_type=QToolButton(),
                parent_layout=self.item_section.inner_layout(1),
                objectname="item",
                class_group=self.widget_group,
                width=10,
                stylesheet=f"background-color: {self.type_bg_color};padding-right: 1px",
                signal=self.select_item,
                icon=("plus.png", self.dark_type_bg_color, cons.WSIZE / 2),
                size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
            )

        else:
            self.type_label = Widget(
                widget_type=QToolButton(),
                parent_layout=self.item_section.inner_layout(1),
                objectname="item",
                class_group=self.widget_group,
                width=10,
                stylesheet=f"background-color: {self.type_bg_color};padding-right: 1px",
                signal=self.delete_item,
                icon=("delete.png", self.dark_type_bg_color, cons.WSIZE / 2),
                size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
            )

        self.roll_section.inner_layout(1).setAlignment(Qt.AlignRight)

        # self.item_section.inner_layout(2).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(5).setAlignment(Qt.AlignTop)
        self.item_label.get_widget().setAlignment(Qt.AlignTop)

        if self.equipment not in ["", "codex"]:
            self.type_label.get_widget().setDisabled(True)
            func.set_icon(self.type_label.get_widget(), "", "", 0)

    def select_item(self):
        print(self.select_item)
        self.character.CHARACTER_DOC["inventory"].append(self.item_dict)
        self.character.set_all_stats()

    def add_sub(self):
        add_sub_gui = AddSub(
            self.character, self.sender(), doc_item=self.count, item=True, equipment=self.equipment
        )
        add_sub_gui.show()

    def roll_dice(self):
        self.character_name = self.character.character_name

        self.check = 0
        self.dice = self.sender().text()

        self.character.active_modifier_name = self.sender().property("roll")
        self.roll_type = f"{self.dice} {self.name}"

        if self.item_type == "Ranged Weapon":
            needs_ammo = True
        else:
            needs_ammo = False

        rolling_dice = DiceRoll(
            self.sender(),
            self.character_name,
            self.roll_type,
            self.dice,
            check=self.check,
            character=self.character,
            ammo=needs_ammo,
        ).roll()

    def prepare_equip_item(self):
        self.equip_button = self.sender()
        self.equip_button_type = self.equip_button.objectName()

        if "EQUIPPED" in self.equip_button_type:
            self.unequip_item()
        else:
            self.equip_item()

    def equip_item(self):
        if self.equip_button_type == "2H":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)

            if self.character.CHARACTER_DOC["equipment"]["main hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(
                    self.character.CHARACTER_DOC["equipment"]["main hand"]
                )
            if self.character.CHARACTER_DOC["equipment"]["off hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(
                    self.character.CHARACTER_DOC["equipment"]["off hand"]
                )

            self.character.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict
            self.character.CHARACTER_DOC["equipment"]["off hand"] = {}

            self.equip_button.setObjectName("2H_EQUIPPED")

        elif self.equip_button_type == "MH":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)

            if self.character.CHARACTER_DOC["equipment"]["main hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(
                    self.character.CHARACTER_DOC["equipment"]["main hand"]
                )

            self.character.CHARACTER_DOC["equipment"]["main hand"] = self.item_dict

            self.equip_button.setObjectName("MH_EQUIPPED")

        elif self.equip_button_type == "OH":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)

            if self.character.CHARACTER_DOC["equipment"]["off hand"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(
                    self.character.CHARACTER_DOC["equipment"]["off hand"]
                )

            self.character.CHARACTER_DOC["equipment"]["off hand"] = self.item_dict

            self.equip_button.setObjectName("OH_EQUIPPED")

        elif self.equip_button_type == "AR":
            self.character.CHARACTER_DOC["inventory"].pop(self.count)

            if self.character.CHARACTER_DOC["equipment"]["armor"] != {}:
                self.character.CHARACTER_DOC["inventory"].append(
                    self.character.CHARACTER_DOC["equipment"]["armor"]
                )

            self.character.CHARACTER_DOC["equipment"]["armor"] = self.item_dict

            self.equip_button.setObjectName("AR_EQUIPPED")

        self.character.set_all_stats()

    def get_roll_widget(self):
        return self.item_dice.get_widget()

    def unequip_item(self):
        if self.equip_button_type == "2H_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(
                self.character.CHARACTER_DOC["equipment"]["main hand"]
            )
            self.character.CHARACTER_DOC["equipment"]["main hand"] = {}
            self.equip_button.setObjectName("2H")

        elif self.equip_button_type == "MH_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(
                self.character.CHARACTER_DOC["equipment"]["main hand"]
            )
            self.character.CHARACTER_DOC["equipment"]["main hand"] = {}
            self.equip_button.setObjectName("MH")

        elif self.equip_button_type == "OH_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(
                self.character.CHARACTER_DOC["equipment"]["off hand"]
            )
            self.character.CHARACTER_DOC["equipment"]["off hand"] = {}
            self.equip_button.setObjectName("OH")

        elif self.equip_button_type == "AR_EQUIPPED":
            self.character.CHARACTER_DOC["inventory"].append(
                self.character.CHARACTER_DOC["equipment"]["armor"]
            )
            self.character.CHARACTER_DOC["equipment"]["armor"] = {}
            self.equip_button.setObjectName("AR")

        self.character.set_all_stats()
