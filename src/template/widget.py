from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import os
import json

import constants as cons

import template.functions as func


class Widget:
    all_widgets = []

    def __init__(
        self,
        widget_type,
        parent_layout=None,
        text="",
        tooltip="",
        objectname="",
        signal="",
        icon=("", 30, 0, 0),
        width="",
        height="",
        align="",
        enabled=True,
        checkable=False,
        validator="",
        placeholder="",
        setting="",
        stylesheet="",
        size_policy=None,
        checked=False,
        property=("", ""),
        class_group=[],
        hidden = False
    ):
        self.class_group = class_group
        self.text = text
        self.widget = widget_type
        if isinstance(self.widget, QComboBox):
            self.setup_combobox(self.widget, text)
        if isinstance(self.widget, QPushButton):
            self.widget.setFocusPolicy(Qt.NoFocus)
        self.parent_layout = parent_layout
        self.object = objectname
        self.setting = setting
        self.widget.setToolTip(tooltip)
        self.widget.setObjectName(self.object)
        self.widget.setStyleSheet(stylesheet)
        self.widget.setProperty(property[0], property[1])
        self.widget_key = f"{self.object}_{self.setting}"
        self.signal = signal
        self.set_enabled(enabled)
        self.set_checkable(checkable, checked)
        self.set_text(self.widget, self.text)
        self.set_alignment(self.widget, align)
        self.set_size(self.widget, width, height)
        self.set_validator(self.widget, validator)
        self.set_placeholder(self.widget, placeholder)
        self.load_setting(self.setting)
        if icon[0] != "":
            if len(icon) == 4:
                pix_width = icon[3]
            else:
                pix_width = 0
            func.set_icon(self.widget, icon[0], icon[2], width=pix_width)
        if size_policy != None:
            self.widget.setSizePolicy(size_policy[0], size_policy[1])

        self.all_widgets.append(self)
        self.class_group.append(self)

        if hidden == True:
            self.widget.setHidden(True)

    def setup_combobox(self, widget, text):
        #widget.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        model = QStandardItemModel(widget)

        widget.setEditable(True)
        widget.lineEdit().setReadOnly(True)
        widget.lineEdit().setAlignment(Qt.AlignCenter)

        # Add items to the model and center their text
        for i, item in enumerate(text):
            si = QStandardItem(item)
            si.setData(Qt.AlignCenter, Qt.TextAlignmentRole)
            model.appendRow(si)
        # Set the model for the combo box
        widget.setModel(model)

    def load_setting(self, setting):
        if os.path.exists(cons.SETTINGS):
            open_file = open(cons.SETTINGS, "r")
            open_json = json.load(open_file)
            if self.widget_key in open_json:
                if setting == "checked":
                    self.widget.setChecked(open_json[self.widget_key])
                elif setting == "text":
                    self.widget.setText(open_json[self.widget_key])
                elif setting == "value":
                    self.widget.setValue(open_json[self.widget_key])
                if self.setting == "button":
                    self.widget.setText(open_json[self.widget_key])
        else:
            pass
        # self.save_setting()

    def save_setting(self):
        if os.path.exists(cons.SETTINGS):
            open_json = json.load(open(cons.SETTINGS, "r"))
        else:
            json.dump({}, open(cons.SETTINGS, "w"), indent=4)
            open_json = json.load(open(cons.SETTINGS, "r"))

        if self.setting == "button":
            open_json[self.widget_key] = self.widget.text()
        if self.setting == "text":
            open_json[self.widget_key] = self.widget.text()
        elif self.setting == "value":
            open_json[self.widget_key] = self.widget.value()
        elif self.setting == "checked":
            open_json[self.widget_key] = self.widget.isChecked()
        elif self.setting == "items":
            open_json[self.widget_key] = self.widget.currentText()
        json.dump(open_json, open(cons.SETTINGS, "w"), indent=4)

    def set_enabled(self, enabled):
        try:
            self.widget.setEnabled(enabled)
        except:
            pass

    def set_placeholder(self, widget, placeholder):
        if placeholder != "":
            widget.setPlaceholderText(placeholder)

    def set_validator(self, widget, validator):
        if validator == "":
            pass
        elif validator == "numbers":
            widget.setValidator(QIntValidator())
        elif validator == "percent":
            regex = QRegExp("^(0|[1-9]\d{0,2})(\.\d{1,2})?$")
            validator = QRegExpValidator(regex)
            widget.setValidator(validator)
        else:
            pass

    def set_checkable(self, checkable, checked):
        try:
            self.widget.setCheckable(checkable)
            self.widget.setChecked(checked)
        except:
            pass

    def get_inner_layout(self, layout):
        return layout

    def get_widget(self):
        return self.widget

    def set_alignment(self, widget, align):
        if align == "":
            pass
        elif align == "left":
            widget.setAlignment(Qt.AlignLeft)
        elif align == "right":
            widget.setAlignment(Qt.AlignRight)
        elif align == "vcenter":
            widget.setAlignment(Qt.AlignVCenter)
        else:
            widget.setAlignment(Qt.AlignHCenter)

    def set_text(self, widget, text):
        try:
            widget.setText(text)
        except:
            pass
        try:
            widget.setPlainText(text)
        except:
            pass
        try:
            widget.setValue(int(text))
        except:
            pass

    def set_size(self, widget, width, height):
        try:
            widget.setFixedWidth(width)
        except:
            pass
        try:
            widget.setFixedHeight(height)
        except:
            pass

    def set_signal(self):
        if self.setting == "checked":
            self.widget.clicked.connect(self.save_setting)
        elif self.setting == "text":
            self.widget.textEdited.connect(self.save_setting)

        if self.signal != "":
            try:
                self.widget.currentIndexChanged.connect(self.signal)
            except:
                pass
            try:
                self.widget.editingFinished.connect(self.signal)
            except:
                pass
            try:
                self.widget.clicked.connect(self.signal)
                return
            except:
                pass

    def connect_to_parent(self):
        self.parent_layout.addWidget(self.widget)
