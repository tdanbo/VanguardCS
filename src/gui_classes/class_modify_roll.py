from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class ModifyRoll:
    def __init__ (self, character):
        self.character = character

    def change_active(self, widget):
        self.widget = widget

        self.modifier_type = self.widget.objectName().split(" ")[0]
        self.modifier_widget = self.character.inventory_gui.findChild(QWidget, f"{self.modifier_type} mod")
        self.modifier = int(self.modifier_widget.text())


        self.character.active_modifier = self.modifier
        self.run_set_stats()

    def run_set_stats(self):
        self.base_modifier = int(self.character.inventory_gui.modifier_mod.get_widget().text())
        self.character.base_modifier = self.base_modifier
        self.character.set_stats()

        # print(mod)

        # type_color = cons.ACTIVE_COLOR[mod]
        # current_mod = self.findChild(QWidget, mod+" mod")
        # current_button = self.findChild(QWidget, mod+" button")

        # for button in ["ATTACK mod","DEFENSE mod","CASTING mod","SNEAKING mod"]:
        #     if button != current_mod.objectName():
        #         mod_widget = self.findChild(QWidget, button)
        #         mod_widget.setChecked(False)
        #         stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;"
        #         mod_widget.setStyleSheet(stylesheet)

        # for mod in ["ATTACK button","DEFENSE button","CASTING button","SNEAKING button"]:
        #     if mod != current_button.objectName():
        #         mod_widget = self.findChild(QWidget, mod)
        #         mod_widget.setChecked(False)
        #         stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;"
        #         mod_widget.setStyleSheet(stylesheet)


        # if self.sender().isChecked():
        #     current_button.setStyleSheet(f"background-color: {type_color}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
        #     current_mod.setStyleSheet(f"background-color: {type_color}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;")
        #     current_mod.setChecked(True)
        #     current_button.setChecked(True)
        # else:
        #     current_button.setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
        #     current_mod.setStyleSheet(f"background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;")
        #     current_mod.setChecked(False)
        #     current_button.setChecked(False)