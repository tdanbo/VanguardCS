from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import stylesheet as style
import constants as cons

import json
import functions as func
import os
import sys

import pymongo



from template.section import Section
from template.widget import Widget
import template.stylesheet as tstyle

class AbilityGUI(QWidget):
    def __init__(self, gui_sheet, csheet,slot):
        super().__init__(None, Qt.WindowStaysOnTopHint)
        self.all_abilities = self.get_abilities()

        self.gui_sheet = gui_sheet
        self.character_sheet = csheet
        self.ability_slot = slot

        self.master_layout = QVBoxLayout()
        self.master_layout.setSpacing(5)

        self.section_group = []
        self.widget_group = []

        self.ability_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 2),
            parent_layout = self.master_layout,
            group=True,
            class_group=self.section_group
        )

        for category in self.all_abilities:
            self.ability_widget = Widget(
                widget_type=QToolButton(),
                stylesheet=style.BUTTONS,
                parent_layout=self.ability_section.inner_layout(1),
                icon = (f"{category}.png",cons.WSIZE/2,cons.ICON_COLOR),
                height=cons.WSIZE*2,
                objectname=category,
                class_group=self.widget_group,
                signal=self.add_abilities,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed)
            )

        self.search_section = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox",1),
            parent_layout = self.master_layout,
            group=True,
            class_group=self.section_group,
            title="SEARCH",
            icon=("search.png",cons.WSIZE,cons.ICON_COLOR),
        )

        self.search_bar = Widget(
            widget_type=QLineEdit(),
            stylesheet=style.QADDSUB,
            parent_layout=self.search_section.inner_layout(1),
            text="",
            align="center",
            objectname = "search",
            class_group = self.widget_group,
        )


        self.feats_scroll = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            scroll=(True,"top"),
            spacing = 5,
            class_group=self.section_group, 
        )


        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)     

        self.setWindowTitle("Select Feat")
        self.setStyleSheet(style.BASE_STYLE)

    def add_abilities(self):
        self.category = self.sender().objectName()
        self.clear_layout(self.feats_scroll.inner_layout(1))

        self.ability_section_group = []
        self.ability_widget_group = []

        for item in self.all_abilities[self.category]:
            if item != "_id":
                print(item)
                item_json = self.all_abilities[self.category][item]

                self.ability_section = Section(
                    outer_layout = QVBoxLayout(),
                    inner_layout = ("VBox", 2),
                    parent_layout = self.feats_scroll.inner_layout(1),
                    spacing = 0,
                    class_group=self.ability_section_group
                )
                    
                self.single_feat_layout = Section(
                    outer_layout = QVBoxLayout(),
                    inner_layout = ("VBox", 2),
                    parent_layout = self.ability_section.inner_layout(1),
                    spacing = 0,
                    class_group=self.ability_section_group,
                    group=True,
                    title=item_json["Name"],
                    height=200,
                    icon = (f"{self.category}.png",cons.WSIZE,cons.ICON_COLOR),
                    
                )

                self.feat_label = Widget(
                    widget_type=QPlainTextEdit(),
                    stylesheet=style.BUTTONS,
                    parent_layout=self.single_feat_layout.inner_layout(1),
                    text = item_json["Description"],
                    size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
                    class_group=self.ability_widget_group,
                    objectname=f'{item_json["Name"]}_label'
                    )



                self.select_feat = Widget(
                    widget_type=QPushButton(),
                    stylesheet=style.BUTTONS,
                    parent_layout=self.ability_section.inner_layout(2),
                    text = "Select",
                    height = cons.WSIZE,
                    objectname=item_json["Name"],
                    signal=self.confirm_feat,
                    class_group=self.ability_widget_group
                    )

                # Adding Novice, Adept, Master
                if item_json["Novice"] != "":
                    self.feat_label.get_widget().setPlainText(item_json["Novice"])

                    title_layout = self.single_feat_layout.get_title()[2]

                    self.novice = Widget(
                        widget_type=QPushButton(),
                        text="N",
                        width=cons.WSIZE,
                        height=cons.WSIZE,
                        signal=self.set_level,
                        objectname=f"{item_json['Name']}_Novice",
                        parent_layout=title_layout,
                        class_group=self.ability_widget_group,
                        stylesheet = tstyle.LEVEL_BUTTONS
                    )

                    self.adept = Widget(
                        widget_type=QPushButton(),
                        text="A",
                        width=cons.WSIZE,
                        height=cons.WSIZE,
                        signal=self.set_level,
                        objectname=f"{item_json['Name']}_Adept",
                        parent_layout=title_layout,
                        class_group=self.ability_widget_group,
                        stylesheet = tstyle.LEVEL_BUTTONS_DISABLED
                    )

                    self.master = Widget(
                        widget_type=QPushButton(),
                        text="M",
                        width=cons.WSIZE,
                        height=cons.WSIZE,
                        signal=self.set_level,
                        objectname=f"{item_json['Name']}_Master",
                        parent_layout=title_layout,
                        class_group=self.ability_widget_group,
                        stylesheet = tstyle.LEVEL_BUTTONS_DISABLED
                    )

        for widget in self.ability_widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.ability_section_group:
            section.connect_to_parent()

    def set_level(self):
        print("set level")
        # Getting the label
        item_name = self.sender().objectName().split("_")[0]
        level = self.sender().objectName().split("_")[1]

        label = self.findChild(QPlainTextEdit, f"{item_name}_label")

        # Reset all colors
        novice = self.findChild(QPushButton, f"{item_name}_Novice")
        adept = self.findChild(QPushButton, f"{item_name}_Adept")
        master = self.findChild(QPushButton, f"{item_name}_Master")

        level_list = [novice, adept, master]
        [level_widget.setStyleSheet(tstyle.LEVEL_BUTTONS_DISABLED) for level_widget in level_list]

        [level_widget.setStyleSheet(tstyle.LEVEL_BUTTONS) if level in level_widget.objectName() else None for level_widget in level_list]

        # Set new text
        text = self.all_abilities[self.category][item_name][level]
        label.setPlainText(text)

    def get_abilities(self):
        all_equipment = {}
        client = pymongo.MongoClient(cons.CONNECT)
        # get a list of collection names
        db = client["abilities"]
        collection_names = db.list_collection_names()
        for name in collection_names:
            # get a collection object
            collection = db[name]
            document = collection.find_one()
            all_equipment[name] = document
        return all_equipment

    def confirm_feat(self):
        print("confirming ability")
        selected_ability = self.sender().objectName()
        slot_section = self.gui_sheet.findChild(QWidget, f"{self.ability_slot}_section")
        slot_section_label =  slot_section.get_title()[1]
        slot_section_label.setText(selected_ability)
        slot_section_label.setProperty("Rank", "Novice")
        self.hide()
        self.character_sheet.update_sheet()
                
    def clear_layout(self,layout):
        for item in range(layout.count()):
            layout.itemAt(item).widget().deleteLater()

def run_gui(name, version):
    app = QApplication(sys.argv)
    w = AbilityGUI("","")
    w.show()
    app.exec_()

if __name__ == "__main__":
    run_gui("Character Sheet", "0.1")