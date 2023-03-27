from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons


class DeleteChar(QWidget):
    def __init__(self, inventory_gui, character_name):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        self.character_name = character_name
        self.inventory_gui = inventory_gui

        self.warning_layout = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 2),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            spacing=5,
        )

        self.integer_line = Widget(
            widget_type=QLabel(),
            parent_layout=self.warning_layout.inner_layout(1),
            objectname="adjuster",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            class_group=self.widget_group,
            text=f"Are you sure you want to delete\n{self.character_name}?",
            align="center",
            stylesheet=f"font-size: {cons.FONT_MID}; color: {cons.FONT_LIGHT}; font-weight: bold; background-color: {cons.DARK};",
        )

        self.minus_widget = Widget(
            widget_type=QToolButton(),
            parent_layout=self.warning_layout.inner_layout(2),
            objectname="no",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            class_group=self.widget_group,
            text = "NO",
            height=cons.WSIZE,
            signal=self.send_value,
            stylesheet=f"font-size: {cons.FONT_SMALL}; font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;",
        )

        self.plus_widget = Widget(
            widget_type=QToolButton(),
            parent_layout=self.warning_layout.inner_layout(2),
            objectname="yes",
            class_group=self.widget_group,
            text = "YES",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            height=cons.WSIZE,
            signal=self.send_value,
            stylesheet=f"font-size: {cons.FONT_SMALL}; font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;",
        )

        self.setWindowTitle("Character deletion?")

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setStyleSheet(
            f"color: {cons.FONT_DARK}; background-color: {cons.DARK}; border-style: outset;"
        )
        self.setLayout(self.master_layout)

    def send_value(self):
        self.value = self.sender().objectName()
        if self.value == "yes":
            self.db = cons.CLIENT["dnd"]
            self.collection = self.db["characters"]
            result = self.collection.delete_one({"character": f"{self.character_name}"})
            self.inventory_gui.update_character_dropdown()
        else:
            pass
        self.close()
