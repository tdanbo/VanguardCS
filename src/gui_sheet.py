from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget
import constants as cons
from gui_widgets.gui_abilities import AddNewAbility
from gui_classes.class_roll import DiceRoll
from gui_classes.class_modify_stat import ModifyStat

from gui_widgets.gui_add_sub import AddSub

import sys
import time
import template.functions as func


class CharacterSheetGUI(QWidget):
    def __init__(self, character):
        super().__init__()

        self.top_button = f"QPushButton {{background-color: {cons.PRIMARY_MEDIUM}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_LARGE}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;}}"

        self.bottom_button = (
            f"QPushButton {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;}}"
            f"QPushButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
            f"QPushButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
        )

        self.character = character

        self.master_layout = QVBoxLayout()
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.master_layout.setSpacing(0)
        self.section_group = []
        self.widget_group = []

        self.character_basic = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.master_layout,
            spacing=10,
            class_group=self.section_group,
            height=100,
        )

        scroll_style = (
            f"QScrollBar {{background-color: {cons.PRIMARY}; width: 6px;}}"
            f"QWidget {{background-color: {cons.PRIMARY};}}"
            f"QScrollBar::handle:vertical {{background-color: {cons.BORDER}; width: 6px; min-height: 20px; border: none; outline: none;}}"
        )

        self.ability_layout = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("VBox", 1),
            parent_layout=self.master_layout,
            title="ABILITIES & POWERS",
            group=True,
            scroll=(True, "top"),
            icon=("plus.png", cons.PRIMARY_LIGHTER, cons.ICON_SIZE),
            spacing=10,
            class_group=self.section_group,
            stylesheet=scroll_style,
        )

        self.ability_layout.get_title()[0].clicked.connect(self.open_abilities)
        self.ability_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.top_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("HBox", 2),
            parent_layout=self.master_layout,
            spacing=5,
            class_group=self.section_group,
        )

        self.stat_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 9),
            parent_layout=self.top_layout.inner_layout(2),
            group=True,
            spacing=3,
            class_group=self.section_group,
            title="STATS",
            height=100,
        )

        self.stat_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.hp_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 3),
            parent_layout=self.character_basic.inner_layout(1),
            group=True,
            title="TOUGHNESS",
            spacing=3,
            class_group=self.section_group,
        )

        self.hp_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.corruption_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.character_basic.inner_layout(1),
            group=True,
            title="CORRUPTION",
            spacing=3,
            class_group=self.section_group,
        )

        self.corruption_token_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.corruption_layout.inner_layout(1),
            spacing=3,
            class_group=self.section_group,
        )

        self.corruption_roll_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 2),
            parent_layout=self.corruption_layout.inner_layout(1),
            spacing=3,
            class_group=self.section_group,
            content_margin=(0, 0, 0, 0),
        )

        self.corruption_level = Widget(
            widget_type=QToolButton(),
            parent_layout=self.corruption_roll_layout.inner_layout(1),
            width=cons.WSIZE * 2.6,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER};border-radius: 6px; border: 1px solid {cons.BORDER}; font-size: 20px;",
            class_group=self.widget_group,
            signal=self.change_corruption_level,
            size_policy=(QSizePolicy.Fixed, QSizePolicy.Expanding),
        )

        self.reset_corruption = Widget(
            widget_type=QToolButton(),
            parent_layout=self.corruption_roll_layout.inner_layout(2),
            signal=self.character.reset_corruption,
            icon=("reload.png", cons.DARK, cons.ICON_SIZE),
            width=cons.WSIZE * 1.3,
            height=cons.WSIZE * 1.3,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER};border-radius: 6px; border: 1px solid {cons.BORDER};",
            class_group=self.widget_group,
        )

        self.make_corruption = Widget(
            widget_type=QToolButton(),
            parent_layout=self.corruption_roll_layout.inner_layout(2),
            signal=self.roll_corruption,
            icon=("dead.png", cons.DARK, cons.ICON_SIZE),
            width=cons.WSIZE * 1.3,
            height=cons.WSIZE * 1.3,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER};border-radius: 6px; border: 1px solid {cons.BORDER};",
            class_group=self.widget_group,
        )

        self.corruption_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.show_combat_log = Widget(
            widget_type=QToolButton(),
            parent_layout=self.corruption_layout.get_title()[2],
            icon=("show_hide_log.png", cons.PRIMARY_DARKER, cons.ICON_SIZE),
            signal=self.open_combat_log,
            checkable=True,
            checked=False,
            class_group=self.widget_group,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.DARK}",
        )

        # Below is all the widgets used in the character sheet
        for number, stat in enumerate(cons.STATS):
            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout=self.stat_layout.inner_layout(number),
                signal=self.modify_stat,
                objectname=stat,
                class_group=self.widget_group,
                height=cons.WSIZE * 1.3,
                stylesheet=self.top_button,
            )

            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout=self.stat_layout.inner_layout(number),
                text=stat,
                objectname=f"{stat} mod",
                class_group=self.widget_group,
                height=cons.WSIZE * 1.3,
                signal=self.roll_dice,
                property=("roll", stat),
                stylesheet=self.bottom_button,
                tooltip=cons.TOOLTIP[stat],
            )

        self.toughness_current = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(1),
            objectname="TOUGHNESS",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal=self.modify_stat,
            stylesheet=self.top_button,
        )

        self.toughness_current_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(1),
            objectname="TOUGHNESS mod",
            text="TOUGHNESS",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal=self.add_sub,
            stylesheet=self.bottom_button,
        )

        self.toughness_max = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname="MAXIMUM",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal=self.modify_stat,
            stylesheet=self.top_button,
        )

        self.toughness_max_mod = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname="MAXIMUM mod",
            text="MAXIMUM",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),  #
            stylesheet=self.bottom_button,
        )

        self.toughness_threshold = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(3),
            objectname="PAIN",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal=self.modify_stat,
            stylesheet=self.top_button,
        )

        self.toughness_threshold_mod = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(3),
            objectname="PAIN mod",
            text="THRESHOLD",
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            stylesheet=self.bottom_button,
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)
        self.character.set_sheet_gui(self)

    def change_corruption_level(self):
        level = self.sender().objectName()

        if level == "1":
            self.character.CHARACTER_DOC["CORRUPTION LEVEL"] = "2"

        if level == "2":
            self.character.CHARACTER_DOC["CORRUPTION LEVEL"] = "3"

        if level == "3":
            self.character.CHARACTER_DOC["CORRUPTION LEVEL"] = "1"

        self.character.set_corruption()

    def mousePressEvent(
        self, event
    ):  # this is a very specific event used to subtract values when right clicking on a widget
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if widget.objectName() in cons.STATS + cons.SECONDARY_STATS:
                button_widget = self.findChild(
                    QPushButton, widget.objectName() + " mod"
                )
                string = button_widget.text()
                ModifyStat(string).add_one(self.character, button_widget)

    def open_abilities(self):
        self.abilities = AddNewAbility(self.character)
        self.abilities.show()

    def modify_stat(self):
        number_widget = self.sender().objectName()
        button_widget = self.findChild(QPushButton, number_widget + " mod")
        string = button_widget.text()
        ModifyStat(string).subtract_one(self.character, button_widget)

    def roll_corruption(self):
        self.character_name = self.character.character_name
        self.character.active_modifier_name = "Corruption"
        dice_roll = DiceRoll(
            self.sender(),
            self.character.character_name,
            "1d4",
            "1d4",
            check=0,
            character=self.character,
        ).roll()

        time.sleep(1)
        self.character.add_corruption(dice_roll)

    def roll_dice(self):
        self.character_name = self.character.character_name

        objectname = self.sender().objectName().split(" ")[0]
        number_widget = self.findChild(QPushButton, objectname)

        self.roll_type = self.sender().property("roll")

        if self.roll_type in cons.STATS:
            self.check = int(number_widget.text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = number_widget.text()

        rolling_dice = DiceRoll(
            number_widget,
            self.character_name,
            self.roll_type.capitalize(),
            self.dice,
            check=self.check,
            character=self.character,
        ).roll()

    def add_sub(self):
        objectname = self.sender().objectName().split(" ")[0]
        number_widget = self.findChild(QPushButton, objectname)
        add_sub_gui = AddSub(self.character, number_widget, doc_item=objectname)
        add_sub_gui.show()

    def open_combat_log(self):
        if self.sender().isChecked():
            self.character.combat_log.show()
        else:
            self.character.combat_log.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CharacterSheetGUI()
    window.show()
    sys.exit(app.exec_())
