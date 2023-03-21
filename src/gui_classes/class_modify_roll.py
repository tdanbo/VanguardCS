from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons


class ModifyRoll:
    def __init__(self, character):
        self.character = character
                
        self.bottom_button=(
                f"QPushButton {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;}}"
                f"QPushButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
                f"QPushButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
            )
        
        self.bottom_tool_button=(
                f"QToolButton {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;}}"
                f"QToolButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
                f"QToolButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
            )

    def change_active(self, widget):
        self.widget = widget

        self.modifier_type = self.widget.objectName().split(" ")[0]
        self.modifier_widget = self.character.inventory_gui.findChild(
            QWidget, f"{self.modifier_type} mod"
        )
        self.modifier = int(self.modifier_widget.text())

        if self.widget.isChecked():
            self.character.active_modifier = self.modifier
            self.character.active_modifier_name = self.modifier_type
        else:
            self.character.active_modifier = 0
            self.character.active_modifier_name = ""
        set_active_style = self.active_style()
        self.run_set_stats()

    def run_set_stats(self):
        self.base_modifier = int(
            self.character.inventory_gui.modifier_mod.get_widget().text()
        )
        self.character.base_modifier = self.base_modifier
        self.character.set_stats()

    def active_style(self):
        type_color = cons.ACTIVE_COLOR[self.modifier_type]
        checked_style = f"background-color: {type_color}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"

        state = self.widget.isChecked()

        self.clear_style()

        if state:
            self.widget.setStyleSheet(checked_style)
            self.widget.setChecked(True)

            for button in cons.STATS:
                button_widget = self.character.sheet_gui.findChild(
                    QWidget, f"{button} mod"
                )
                button_widget.setStyleSheet(checked_style)

            self.character.inventory_gui.modifier_mod.get_widget().setStyleSheet(
                f"background-color: {cons.PRIMARY_MEDIUM}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
            )

            self.character.inventory_gui.modifier_button.get_widget().setStyleSheet(
                checked_style
            )

            self.character.inventory_gui.modifier_mod.get_widget().setEnabled(True)
            self.character.inventory_gui.modifier_button.get_widget().setEnabled(True)

    def clear_style(self):
        unchecked_style = f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        for button in [
            "ATTACK",
            "DEFENSE",
            "CASTING",
            "SKILL",
            "SNEAKING",
        ] + cons.STATS:
            if button in cons.STATS:
                button_widget = self.character.sheet_gui.findChild(
                    QWidget, f"{button} mod"
                )
            else:
                button_widget = self.character.inventory_gui.findChild(
                    QWidget, f"{button} button"
                )
                button_widget.setChecked(False)

            button_widget.setStyleSheet(self.bottom_tool_button)

        for button in cons.STATS:
            button_widget = self.character.sheet_gui.findChild(QWidget, f"{button} mod")
            button_widget.setStyleSheet(self.bottom_button)

        # Resetting the base modifier
        base_modifier_widget = self.character.inventory_gui.modifier_mod.get_widget()
        base_button_widget = self.character.inventory_gui.modifier_button.get_widget()

        base_modifier_widget.setEnabled(False)
        base_button_widget.setEnabled(False)

        base_modifier_widget.setStyleSheet(
            f"background-color: {cons.PRIMARY_MEDIUM}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        )

        base_button_widget.setStyleSheet(
            f"background-color: {cons.PRIMARY_MEDIUM}; color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        )

        # self.character.active_modifier_name = ""
