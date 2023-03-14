from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import constants as cons


class AddSub(QWidget):
    def __init__(self, character_sheet, widget, doc_item = ""):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.widget = widget
        self.doc_item = doc_item
        self.character_sheet = character_sheet

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        self.addsub_widget_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.master_layout,
            class_group=self.section_group,
            spacing=5,
        )

        self.integer_line = Widget(
            widget_type=QLineEdit(),
            parent_layout=self.addsub_widget_layout.inner_layout(1),
            align="center",
            objectname = "adjuster",
            size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
            height = cons.WSIZE*1.5,
            class_group = self.widget_group,
            validator="numbers",
            stylesheet= f"font-size: 15px; font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;"

        )

        self.minus_widget = Widget(
            widget_type=QToolButton(),
            parent_layout=self.addsub_widget_layout.inner_layout(2),
            objectname = "minus",
            size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
            class_group = self.widget_group,
            icon=("minus.png",cons.WSIZE,cons.BORDER),
            height = cons.WSIZE*1.5,
            signal=self.send_value,
            stylesheet= f"font-size: 15px; font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;"

        )

        self.plus_widget = Widget(
            widget_type=QToolButton(),
            parent_layout=self.addsub_widget_layout.inner_layout(2),
            objectname = "plus",
            class_group = self.widget_group,
            icon=("plus.png",cons.WSIZE,cons.BORDER),
            size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
            height = cons.WSIZE*1.5,
            signal=self.send_value,
            stylesheet= f"font-size: 15px; font-weight: bold; color: {cons.FONT_COLOR}; background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-radius: 6px;"

        )

        self.setWindowTitle("Set Value")

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setStyleSheet(f"color: {cons.FONT_DARK}; background-color: {cons.DARK}; border-style: outset;")
        self.setLayout(self.master_layout)

    def send_value(self):
        current_value = int(self.character_sheet.CHARACTER_DOC[self.doc_item])
        value = int(self.integer_line.get_widget().text())
    
        state = self.sender().objectName()
        if state == "plus":
            new_value = current_value + value
        else:
            new_value = current_value - value
        
        self.character_sheet.CHARACTER_DOC[self.doc_item] = new_value
        self.character_sheet.update_sheet()
        self.close()