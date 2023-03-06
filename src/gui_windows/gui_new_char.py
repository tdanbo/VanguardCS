from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import stylesheet as style
import constants as cons

import json
import functions as func
import os

from class_sheet import CharacterSheet

from template.section import Section
from template.widget import Widget
import template.stylesheet as tstyle
import constants as cons

import pymongo


class NewCharacter(QWidget):
    def __init__(self, isheet, csheet):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.isheet = isheet
        self.csheet = csheet

        # settings up the character sheet
        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        self.name_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.master_layout,
            title="NAME",
            group=True,
            class_group=self.section_group,
        )

        self.name = Widget(
            widget_type=QLineEdit(),
            stylesheet=tstyle.WIDGETS,
            text="",
            align="center",
            objectname = "name",
            class_group = self.widget_group,
            parent_layout=self.name_section.inner_layout(1),
        )

        self.stat_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 8),
            parent_layout = self.master_layout,
            title="STATS",
            group=True,
            class_group=self.section_group,
        )

        self.state = []
        stat_pool = ["5","7","9","10","10","11","13","15"]
        for count, item in enumerate(cons.STATS):
            self.stat_label = Widget(
                widget_type=QPushButton(),
                text=item,
                parent_layout=self.stat_section.inner_layout(count),
                class_group = self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed),
            )

            self.stat_input = Widget(
                widget_type=QPushButton(),
                stylesheet=tstyle.WIDGETS,
                text=stat_pool[count],
                parent_layout=self.stat_section.inner_layout(count),
                class_group = self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed),
                signal=self.set_stat,
                objectname=item,
            )

        self.new_widget_layout = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.master_layout,
            title="New Character",
            icon = ("plus.png",cons.WSIZE*1.5,cons.ICON_COLOR),
            group=(True,None,None),
            class_group = self.section_group,
        )

        self.cancel_widget = Widget(
            widget_type=QPushButton(),
            stylesheet=style.BUTTONS,
            text="Cancel",
            objectname = "cancel",
            size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
            class_group = self.widget_group,
            parent_layout=self.new_widget_layout.inner_layout(2),
            signal=self.create_character
        )

        self.accept_widget = Widget(
            widget_type=QPushButton(),
            stylesheet=style.BUTTONS,
            text="Accept",
            objectname = "accept",
            size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
            class_group = self.widget_group,
            parent_layout=self.new_widget_layout.inner_layout(2),
            signal=self.create_character
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)     

        self.setWindowTitle("New Character")
        self.setStyleSheet(style.BASE_STYLE)

    def set_stat(self):
        if len(self.state) == 0:
            widget1 = self.sender()
            self.state.append((widget1,widget1.text()))
            print("copy")
            print(self.state)
        else:
            print("paste")
            widget2 = self.sender()
            self.state.append((widget2,widget2.text()))

            self.state[0][0].setText(self.state[1][1])
            self.state[1][0].setText(self.state[0][1])

            self.state.clear()



    def create_character(self):
        self.character_name = self.name.get_widget().text()

        for i in range(self.isheet.character_name.get_widget().count()):
            if self.isheet.character_name.get_widget().itemText(i).lower() == self.character_name.lower():
                self.name.get_widget().setText("Character already exists")
                return



        state = self.sender().objectName()
        if state == "accept":
            new_character = {"character":"","rank":"","experience unspent":"","stats":{}}
            new_character["character"] = self.character_name
            new_character["rank"] = "Player"
            new_character["experience"] = "0"
            new_character["experience unspent"] = "40"

            for stat in cons.STATS:
                stat_value = self.findChild(QPushButton,stat).text()
                new_character["stats"][stat] = stat_value

            self.isheet.character_name.get_widget().addItem(self.character_name)
            self.isheet.character_name.get_widget().setCurrentText(self.character_name)

            self.update_database(new_character)
            self.csheet.load_character(self.isheet, self.character_name)

            self.hide()
        else:
            self.hide()

    def update_database(self, directory):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["characters"]
        self.collection.insert_one(directory)