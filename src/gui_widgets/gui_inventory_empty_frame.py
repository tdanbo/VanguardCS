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

class InventoryEmptyItem(QWidget):
    def __init__(self, character, count, layout, carry_weight):
        super().__init__()

        self.character = character

        self.master_layout = QVBoxLayout()
        self.widget_group = []
        self.section_group = []
        self.count = count
        self.carry_weight = carry_weight

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
            align="center",
            signal=self.get_item
        )

        # CREATING EMPTY OR POPULATED ITEM WIDGET

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

        layout.addWidget(self)

    def get_item(self):
        self.item_string = self.sender().text()

        self.all_equipment = cons.EQUIPMENT



        if self.item_string != "":
            for category in self.all_equipment:
                for item in self.all_equipment[category]:
                    if self.item_string.lower() == item.lower():
                        self.item_dict = self.all_equipment[category][item]
                        self.select_item()
                        return

            self.item_dict = self.general_item()
            # self.item_dict["Name"] = item_string.title()
            # self.item_dict["Category"] = "General Good"
            # self.item_dict["Equipped"] = {}
            # self.item_dict["Equipped"]["1"] = False
            # self.item_dict["Equipped"]["2"] = False
            self.select_item()
            return


                        # self.item_dict["Name"] = item
                        # self.item_dict["Category"] = category
                        # self.item_dict["Equipped"] = {}
                        # self.item_dict["Equipped"]["1"] = False
                        # self.item_dict["Equipped"]["2"] = False

                        # self.character.CHARACTER_DOC["inventory"].append(self.item_dict)
                        # self.character.set_all_stats()
                        # return

            # Create General Good item!


    def general_item(self):
        item = {"Name":self.item_string, "Quantity": 1, "Category": "General Good", "Type": "General Good", "Quality": []}
        return item

    def select_item(self):
        selected_item = self.item_dict.copy()

        self.character.CHARACTER_DOC["inventory"].append(selected_item)
        self.character.set_all_stats()