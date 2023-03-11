from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons

import json
import functions as func
import os

from template.section import Section
from template.widget import Widget


class InventoryItem(QWidget):
    def __init__(self, count, item_dict):
        super().__init__()
        print(f"Making Widget")
        print(f"item_dict: {item_dict}")
        self.master_layout = QHBoxLayout()
        self.widget_group = []
        self.section_group = []

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
            objectname="item",
            class_group=self.widget_group,
            stylesheet=f"font-size: 13px; font-weight: bold;",
            height=cons.WSIZE,
        )

        # CREATING EMPTY OR POPULATED ITEM WIDGET
        if item_dict == {}:
            pass # Setting up empty item
        else:
            print("item_dict", item_dict)
            self.make_item(item_dict)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.master_layout.setContentsMargins(0, 0, 0, 0)
        #self.setFixedHeight(50)
        self.setLayout(self.master_layout)

    def make_item(self, item_dict):
        print(item_dict)
        self.name = item_dict["Name"]
        self.category = item_dict["Category"]
        item_type = "Weapon" #item_dict["Type"] SET UP TYPES
        qualities = item_dict["Quality"]
        dice_type = item_dict["Roll"][0]
        dice = item_dict["Roll"][1]

        if "Impeding" in item_dict:
            impeding = f" {item_dict['Impeding']}"
        else:
            impeding = ""

        color_type = {"melee": "#925833", "armor": "#495c60", "elixirs": "#926f2b"}
        type_bg_color = color_type[self.category]

        self.item.widget.setText(self.name)

        self.type_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(1),
            class_group=self.widget_group,
            width=5,
            stylesheet=f"background-color: {type_bg_color}",
        )

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

        self.item_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(3),
            text=item_type + impeding,
            objectname="item",
            class_group=self.widget_group,
            align="right",
            height=cons.WSIZE,
        )

        self.item_dice = Widget(
            widget_type=QToolButton(),
            parent_layout=self.item_section.inner_layout(3),
            text=dice,
            objectname="item",
            class_group=self.widget_group,
            stylesheet=f"padding-left: 5px; padding-right: 5px; background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: 11px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;",
            height=cons.WSIZE,
        )

        self.quality_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(2).setAlignment(Qt.AlignRight)
        self.item_label.get_widget().setAlignment(Qt.AlignRight | Qt.AlignVCenter)