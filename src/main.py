
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from gui_sheet import CharacterSheetGUI
from gui_inventory import InventoryGUI
from gui_log import CombatLogGUI
import sys
from gui_classes.class_combat import CombatLog
from gui_classes.class_character import Character
import constants as cons
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layouts
        self.main_layout = QHBoxLayout()

        self.character = Character()

        self.character_sheet_gui = CharacterSheetGUI(self.character)
        self.character_inventory_gui = InventoryGUI(self.character)

        # 3 Main GUIS
        combat_log_gui = CombatLogGUI(self.character)

        # Simple styling
        combat_log_gui.setFixedWidth(300)

        # 2 Main classes
        self.combat_log = CombatLog(combat_log_gui)

        self.main_layout.addWidget(self.character_inventory_gui)
        self.main_layout.addWidget(self.character_sheet_gui)
        self.main_layout.addWidget(combat_log_gui)

        combat_log_gui.setHidden(True)

        self.setLayout(self.main_layout)
        self.spacing = 0
        self.setStyleSheet(
            f"border-style: outset; color: {cons.FONT_DARK}; background-color: {cons.DARK};border-style: outset;"
        )

        self.combat_log.update_combat_log()
        self.combat_log.start_watching()

    def closeEvent(self, event: QCloseEvent):
        self.combat_log.stop_watching()

    def show_hide_settings(self):
        if self.sender().isChecked():
            self.settings_section.get_group().setHidden(False)
        else:
            self.settings_section.get_group().setHidden(True)


def run_gui(version):
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle(version)
    w.show()
    app.exec_()

if __name__ == "__main__":
    run_gui(cons.VERSION)
