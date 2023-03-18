from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons
import functions as func

from qt_thread_updater import get_updater

entry_dict = {
    "Character": "Beasttoe",
    "Type": "Resolute",
    "Dice": "6d6",
    "Result": "29",
    "Modifier": "-2",
    "Result Breakdown": "6+6+5",
    "Result Message": "Failed",
    "Time": "23:00:00",
}

class CombatEntry(QWidget):
    def __init__(self, count):
        super().__init__()
     
        self.master_layout = QHBoxLayout()
        self.widget_group = []
        self.section_group = []

        if count % 2 == 0:
            bg_color = cons.PRIMARY
        else:
            bg_color = cons.PRIMARY_DARKER      

        self.item_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 4),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            group=True,
            content_margin=(0,0,10,0),
            stylesheet=f"background-color: {bg_color};"
        )

        self.character_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(1),
            class_group=self.widget_group,
            width=5,
            align="left",
        )

        self.portrait = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(2),
            class_group=self.widget_group,
            width=cons.WSIZE*4,
        )

        self.portrait.get_widget().setAlignment(Qt.AlignCenter)

        self.item = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(3),
            class_group=self.widget_group,
            stylesheet="font-size: 14px; font-weight: bold;",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        )

        self.item_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(3),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        )

        self.result_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(4),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
            width=cons.WSIZE*2,
        )

        self.result_message_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(4),
            class_group=self.widget_group,       
            size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
            width=cons.WSIZE*2,     
        )


        self.item_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(2).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(4).setAlignment(Qt.AlignRight)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setFixedWidth(300)
        self.setFixedHeight(cons.WSIZE*2.5)
        self.setLayout(self.master_layout)
        self.master_layout.setContentsMargins(0,0,0,0)

        style_a = f"color: {cons.FONT_DARK}; background-color: {cons.DARK}; border-style: outset;"
        get_updater().call_latest(self.setStyleSheet, style_a)

    def update_widget(self,entry):
        self.character = entry["Character"]
        self.type = entry["Type"]
        self.dice = entry["Dice"]
        self.result = entry["Result"]
        self.modifier= str(entry["Modifier"])
        self.result_message = entry["Result Message"]
        self.result_breakdown = entry["Result Breakdown"]
        self.time = entry["Time"]

        color_type = {"Damage": "#925833", "Armor": "#495C60"}
        if self.type not in color_type:
            type_bg_color = "#926f2b"
        else:
            type_bg_color = color_type[self.type]   

        if self.modifier == "0":
            self.item.get_widget().setText(self.type)
        else:
            self.item.get_widget().setText(self.type+" "+self.modifier)
            
        self.item_label.get_widget().setText(self.character)
        result_widget = self.result_label.get_widget()
        result_widget.setText(str(self.result))
        result_widget.setToolTip(f"{self.result_breakdown}")
        self.result_message_label.get_widget().setText(self.result_message)

        func.set_icon(self.portrait.get_widget(),f"{self.character}.png","")

        style_b = f"background-color: {type_bg_color}"
        get_updater().call_latest(self.character_label.get_widget().setStyleSheet, style_b)

        style_c = f"background-color: {cons.PRIMARY_LIGHTER}; color: {type_bg_color}; font-size: 17px; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"
        get_updater().call_latest(self.result_label.get_widget().setStyleSheet, style_c)