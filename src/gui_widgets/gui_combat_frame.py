from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import os
import random
import constants as cons
import template.functions as func

from qt_thread_updater import get_updater


class CombatEntry(QWidget):
    def __init__(self, count):
        super().__init__()

        self.master_layout = QHBoxLayout()
        self.widget_group = []
        self.section_group = []

        if count % 2 == 0:
            self.bg_color = cons.PRIMARY
        else:
            self.bg_color = cons.PRIMARY_DARKER

        self.item_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 3),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            group=True,
            content_margin=(0, 0, 10, 0),
            stylesheet=f"background-color: {self.bg_color };",
        )

        # self.character_label = Widget(
        #     widget_type=QLabel(),
        #     parent_layout=self.item_section.inner_layout(3),
        #     class_group=self.widget_group,
        #     width=7,
        #     align="left",
        # )

        self.portrait = Widget(
            widget_type=QLabel(),
            parent_layout=self.item_section.inner_layout(3),
            class_group=self.widget_group,
            width=cons.WSIZE * 4,
        )

        self.portrait.get_widget().setAlignment(Qt.AlignCenter)

        self.item = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(2),
            class_group=self.widget_group,
            stylesheet=f"font-size: {cons.FONT_MID}; font-weight: bold;",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        )

        # self.item_label = Widget(
        #     widget_type=QPushButton(),
        #     parent_layout=self.item_section.inner_layout(3),
        #     class_group=self.widget_group,
        #     size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
        # )

        self.result_message_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(2),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            stylesheet=f"font-size: {cons.FONT_SMALL};",
        )

        self.result_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.item_section.inner_layout(1),
            class_group=self.widget_group,
            width=cons.WSIZE * 2,
            height=cons.WSIZE * 2,
        )

        self.item_section.inner_layout(1).setContentsMargins(5, 5, 5, 5)
        self.item_section.inner_layout(2).setContentsMargins(5, 5, 5, 5)
        self.item_section.inner_layout(3).setContentsMargins(1, 1, 1, 1)
        self.item_section.inner_layout(1).setAlignment(Qt.AlignLeft)
        self.item_section.inner_layout(2).setAlignment(Qt.AlignLeft)

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setFixedWidth(300)
        self.setFixedHeight(cons.WSIZE * 2.5)
        self.setLayout(self.master_layout)

        self.master_layout.setAlignment(Qt.AlignBottom)
        self.master_layout.setContentsMargins(0, 0, 0, 0)

        style_a = f"color: {cons.FONT_DARK}; background-color: {cons.DARK}; border-style: outset;"
        get_updater().call_latest(self.setStyleSheet, style_a)

    def update_widget(self, entry):
        self.character = entry["Character"]
        self.active = entry["Active"]
        self.type = entry["Type"]
        self.check = entry["Check"]
        self.dice = entry["Dice"]
        self.result = entry["Result"]
        self.modifier = str(entry["Modifier"])
        self.result_message = entry["Result Message"]
        self.result_breakdown = entry["Result Breakdown"]
        self.time = entry["Time"]

        if "Skill Modifier" in entry:
            if entry["Skill Modifier"] != "0":
                self.skill_modifier = f"{entry['Skill Modifier']} "
            else:
                self.skill_modifier = ""
        else:
            self.skill_modifier = ""

        color_type = cons.ACTIVE_COLOR
        if self.active.upper() not in color_type:
            type_bg_color = color_type["GENERAL_GOOD"]
        else:
            type_bg_color = color_type[self.active.upper()]

        get_updater().call_latest(
            self.item.get_widget().setText, self.skill_modifier + self.type.title()
        )
        if self.check == 0:
            result = f"{self.dice} {self.active.title()}"
            get_updater().call_latest(
                self.result_message_label.get_widget().setText, result
            )
            func.set_icon(
                self.result_message_label.get_widget(),
                "",
                "",
                0,
            )
        else:
            if self.result_message == "Success":
                result = f" {self.active.title()}"
                get_updater().call_latest(
                    self.result_message_label.get_widget().setText, result
                )
                func.set_icon(
                    self.result_message_label.get_widget(),
                    "success.png",
                    "#4e874d",
                    15,
                )
            elif self.result_message:
                result = f" {self.active.title()}"
                get_updater().call_latest(
                    self.result_message_label.get_widget().setText, result
                )
                func.set_icon(
                    self.result_message_label.get_widget(),
                    "fail.png",
                    "#874d4d",
                    15,
                )

        #  ({self.result_message}) Removed success/fail message

        # self.item_label.get_widget().setText(self.character)
        result_widget = self.result_label.get_widget()
        get_updater().call_latest(result_widget.setText, str(self.result))
        result_widget.setToolTip(f"{self.result_breakdown}")

        if os.path.isfile(os.path.join(cons.ICONS, f"{self.character}.png")):
            func.set_icon(self.portrait.get_widget(), f"{self.character}.png", "")
        else:
            random_portrait = random.choice(["unknown"])
            func.set_icon(self.portrait.get_widget(), f"{random_portrait}.png", "")

        self.portrait.get_widget().setToolTip(f"{self.character}")

        style_c = f"background-color: {type_bg_color}; color: {cons.PRIMARY}; font-size: {cons.FONT_LARGE}; font-weight: bold; border: 1px solid {cons.BORDER}; border-radius: 6px;"

        get_updater().call_latest(self.result_label.get_widget().setStyleSheet, style_c)
