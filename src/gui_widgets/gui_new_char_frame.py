from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import constants as cons

from template.section import Section
from template.widget import Widget
import constants as cons
import math


class NewCharacter(QWidget):
    def __init__(self, isheet, character):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.isheet = isheet
        self.character = character

        self.left_button=(
                f"QPushButton {{background-color: {cons.PRIMARY_MEDIUM}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-bottom-left-radius: 6px;}}"
            )
        
        self.right_button=(
                f"QPushButton {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-right-radius: 6px; border-bottom-right-radius: 6px;}}"
                f"QPushButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
                f"QPushButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
            )


        # settings up the character sheet
        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        self.name_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 2),
            parent_layout=self.master_layout,
            title="NAME",
            group=True,
            class_group=self.section_group,
        )

        self.name_section.get_title()[1].setAlignment(Qt.AlignCenter)

        self.name = Widget(
            widget_type=QLineEdit(),
            text="",
            align="center",
            objectname="name",
            class_group=self.widget_group,
            parent_layout=self.name_section.inner_layout(1),
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};font-size: {cons.FONT_LARGE};color: {cons.FONT_COLOR};",
            height=cons.WSIZE * 2,
        )

        self.stat_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 8),
            parent_layout=self.master_layout,
            title="STATS",
            group=True,
            class_group=self.section_group,
        )

        self.stat_section.get_title()[1].setAlignment(Qt.AlignCenter)

        self.state = []
        stat_pool = ["5", "7", "9", "10", "10", "11", "13", "15"]
        for count, item in enumerate(cons.STATS):
            self.stat_label = Widget(
                widget_type=QPushButton(),
                text=item,
                parent_layout=self.stat_section.inner_layout(count),
                class_group=self.widget_group,
                height=cons.WSIZE * 1.5,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed),
                stylesheet=self.left_button,
            )

            self.stat_input = Widget(
                widget_type=QPushButton(),
                text=stat_pool[count],
                parent_layout=self.stat_section.inner_layout(count),
                class_group=self.widget_group,
                height=cons.WSIZE * 1.5,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed),
                signal=self.set_stat,
                objectname=item,
                stylesheet=self.right_button,
            )

        self.new_widget_layout = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 2),
            parent_layout=self.master_layout,
            title="New Character",
            icon=("plus.png", cons.WSIZE * 1.5, cons.PRIMARY_LIGHTER),
            group=(True, None, None),
            class_group=self.section_group,
        )

        self.cancel_widget = Widget(
            widget_type=QPushButton(),
            text="Cancel",
            objectname="cancel",
            class_group=self.widget_group,
            parent_layout=self.new_widget_layout.inner_layout(2),
            signal=self.create_character,
            height=cons.WSIZE * 2,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
        )

        self.accept_widget = Widget(
            widget_type=QPushButton(),
            text="Accept",
            objectname="accept",
            height=cons.WSIZE * 2,
            class_group=self.widget_group,
            parent_layout=self.new_widget_layout.inner_layout(2),
            signal=self.create_character,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setWindowTitle("New Character")
        self.setLayout(self.master_layout)
        self.setFixedSize(cons.WSIZE * 15, cons.WSIZE * 20)
        self.setStyleSheet(
            f"border-style: outset; color: {cons.FONT_DARK}; background-color: {cons.DARK};"
        )

    def set_stat(self):
        if len(self.state) == 0:
            widget1 = self.sender()
            self.state.append((widget1, widget1.text()))
        else:
            widget2 = self.sender()
            self.state.append((widget2, widget2.text()))

            self.state[0][0].setText(self.state[1][1])
            self.state[1][0].setText(self.state[0][1])

            self.state.clear()

    def create_character(self):
        self.character_name = self.name.get_widget().text()

        for i in range(self.isheet.character_name.get_widget().count()):
            if (
                self.isheet.character_name.get_widget().itemText(i).lower()
                == self.character_name.lower()
            ):
                self.name.get_widget().setText("Character already exists")
                return

        state = self.sender().objectName()
        if state == "accept":
            new_character = {
                "character": "",
                "rank": "",
                "stats": {},
                "mods": {},
            }
            new_character["character"] = self.character_name
            new_character["rank"] = "Player"
            new_character["Type"] = "Character"
            new_character["XP"] = 0
            new_character["TOTALXP"] = 50

            for stat in cons.STATS + cons.SECONDARY_STATS:
                try:
                    stat_value = self.findChild(QPushButton, stat).text()
                except:
                    stat_value = 0

                new_character["stats"][stat] = int(stat_value)
                new_character["mods"][stat + " mod"] = stat

            strong = int(new_character["stats"]["STRONG"])
            toughness = 10 if strong < 10 else strong



            new_character["stats"]["TOUGHNESS"] = toughness
            new_character["stats"]["CORRUPTION"] = 0
            new_character["stats"]["PERMANENT"] = 0

            new_character["DEFENSE mod"] = 0
            new_character["CASTING mod"] = 0
            new_character["SNEAKING mod"] = 0
            new_character["ATTACK mod"] = 0
            new_character["SKILL mod"] = 0

            new_character["inventory"] = []
            new_character["abilities"] = []
            new_character["equipment"] = {"armor": {}, "main hand": {}, "off hand": {}}

            self.isheet.character_name.get_widget().addItem(self.character_name)
            self.isheet.character_name.get_widget().setCurrentText(self.character_name)

            self.update_database(new_character)
            self.character.load_document(self.character_name)

            self.hide()
        else:
            self.hide()

    def update_database(self, directory):
        self.db = cons.CLIENT["dnd"]
        self.collection = self.db["characters"]
        self.collection.insert_one(directory)
