from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import stylesheet as style
import constants as cons

import json
import functions as func
import os
import sys

from template.section import Section
from template.widget import Widget

from class_sheet import CharacterSheet

class AbilityGUI(QWidget):
    def __init__(self, csheet, feature_slot = ""):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.csheet = csheet
        self.feature_slot = feature_slot

        self.master_layout = QVBoxLayout()
        self.master_layout.setSpacing(5)

        self.section_group = []
        self.widget_group = []

        self.feats_scroll = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("VBox", 1),
            parent_layout = self.master_layout,
            scroll=(True,"top"),
            spacing = 0,
            class_group=self.section_group, 
        )

        for feat_dict in os.listdir(cons.FEATURES):
            for feat in json.load(open(os.path.join(cons.FEATURES,feat_dict), "r")):
                self.single_feat_layout = Section(
                    outer_layout = QVBoxLayout(),
                    inner_layout = ("VBox", 1),
                    parent_layout = self.feats_scroll.inner_layout(2),
                    spacing = 0,
                    class_group=self.section_group,
                    group=True,
                    title=feat["name"],
                )


                self.feat_label = Widget(
                    widget_type=QPlainTextEdit(),
                    stylesheet=style.BUTTONS,
                    parent_layout=self.single_feat_layout.inner_layout(1),
                    text = feat["description"],
                    size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
                    class_group=self.widget_group,
                    )
                
                self.select_feat = Widget(
                    widget_type=QPushButton(),
                    stylesheet=style.BUTTONS,
                    parent_layout=self.single_feat_layout.inner_layout(2),
                    text = "Select",
                    size_policy = (QSizePolicy.Expanding , QSizePolicy.Expanding),
                    height = cons.WSIZE,
                    objectname=feat["name"],
                    signal=self.confirm_feat,
                    class_group=self.widget_group
                    )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)     

        self.setWindowTitle("Select Feat")
        self.setStyleSheet(style.BASE_STYLE)

    def confirm_feat(self):
        for feat_dict in os.listdir(cons.FEATURES):
            for feat in json.load(open(os.path.join(cons.FEATURES,feat_dict), "r")):
                if feat["name"] == self.sender().objectName():
                    selected_feat = feat
                    func.set_icon(self.feature_slot, selected_feat["icon"],cons.ICON_COLOR)
                    self.feature_slot.setToolTip(selected_feat["description"])
                    self.feature_slot.setProperty("feat", selected_feat["name"])
                    self.hide()
                    CharacterSheet(self.csheet).update_sheet()
                    return
                
def run_gui(name, version):
    app = QApplication(sys.argv)
    w = AbilityGUI("","")
    w.show()
    app.exec_()

if __name__ == "__main__":
    run_gui("Character Sheet", "0.1")