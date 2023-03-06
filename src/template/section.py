from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import os
import json

import constants as cons

import template.stylesheet as style
import template.functions as func


class Section(QWidget):
    all_sections = []

    def __init__(
        self,
        outer_layout=QVBoxLayout(),
        inner_layout=(QHBoxLayout(), 1),
        parent_layout=None,
        spacing=0,
        group=False,
        scroll=(False, "bottom"),
        title="",
        icon="",
        content_margin="",
        class_group=[],
        width="",
        height="",
        objectname="",
        hidden=False,
    ):
        super().__init__()

        self.outer_layout_type = outer_layout
        self.inner_layout_type = inner_layout[0]
        self.inner_layout_count = inner_layout[1]
        self.parent_layout = parent_layout
        self.group = group
        self.scroll = scroll
        self.spacing = spacing
        self.class_group = class_group
        self.width = width
        self.height = height

        if self.width != "":
            self.setFixedWidth(self.width)
        if self.height != "":
            self.setFixedHeight(self.height)

        self.setObjectName(objectname)
        self.section_layout = QVBoxLayout()
        self.section_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_layouts = self.inner_layout_list()
        self.outer_layout_type.setSpacing(spacing)

        if content_margin != "":
            self.outer_layout_type.setContentsMargins(*content_margin)

        self.section_layout.setSpacing(0)
        if self.group == True:
            if title != "":
                self.title_layout = QHBoxLayout()
                self.title_label = QLabel(title)
                self.title_label.setStyleSheet(style.QTITLE)
                self.title_label.setObjectName("title")
                self.outer_layout_type.addWidget(self.title_label)
                self.title_label.setFixedHeight(cons.WSIZE)
                self.title_icon = ""
                if icon != "":
                    self.title_icon = QToolButton()
                    self.title_icon.setStyleSheet(style.QTITLE)
                    self.title_icon.setFixedSize(cons.WSIZE, cons.WSIZE)
                    func.set_icon(self.title_icon, icon[0], icon[2])
                    self.title_layout.addWidget(self.title_icon)
                self.title_layout.addWidget(self.title_label)

                self.section_layout.addLayout(self.title_layout)

            self.groupbox = QGroupBox()
            self.groupbox.setStyleSheet(style.QGROUPBOX)

            self.groupbox.setLayout(self.outer_layout_type)
            self.section_layout.addWidget(self.groupbox)
        else:
            self.section_layout.addLayout(self.outer_layout_type)

        if self.scroll[0] == True:
            if len(self.inner_layouts) > 1:
                raise ValueError("Scroll layouts can't have more than 1 widget layout")
            else:
                self.scroll_area_widget = QScrollArea()
                self.scroll_area_widget.setObjectName("scroll_widget")
                i_layout = self.inner_layouts[0]
                self.scroll_widget = QWidget()
                self.scroll_widget.setObjectName("scroll_widget")
                self.scroll_widget.setLayout(i_layout)
                self.scroll_area_widget.setWidget(self.scroll_widget)

                if self.scroll[1] == "top":
                    i_layout.setAlignment(Qt.AlignTop)
                else:
                    i_layout.setAlignment(Qt.AlignBottom)

                i_layout.setSpacing(spacing)
                i_layout.setContentsMargins(0, 0, 0, 0)

                self.scroll_area_widget.setWidgetResizable(True)
                self.scroll_area_widget.setHorizontalScrollBarPolicy(
                    Qt.ScrollBarAlwaysOff
                )

                self.scroll_widget.setStyleSheet(style.QGROUPBOX)
                self.scroll_area_widget.setStyleSheet(style.QGROUPBOX)

                self.outer_layout_type.addWidget(self.scroll_area_widget)
        else:
            for layout in self.inner_layouts:
                self.outer_layout_type.addLayout(layout)

        self.all_sections.append(self)
        self.class_group.append(self)

        self.setLayout(self.section_layout)

        if hidden != False:
            self.setHidden(hidden)


    def inner_layout_list(self):
        self.all_inner_layouts = []
        for number in range(self.inner_layout_count):
            if self.inner_layout_type == "VBox":
                i_layout = QVBoxLayout()
            else:
                i_layout = QHBoxLayout()
            self.all_inner_layouts.append(i_layout)

        return self.all_inner_layouts

    def inner_layout(self, count):
        return self.all_inner_layouts[count - 1]

    def outer_layout(self):
        return self.section_layout

    def connect_to_parent(self):
        if self.parent_layout != None:
            self.parent_layout.addWidget(self)

    def get_group(self):
        return self.groupbox

    def get_title(self):
        return (self.title_icon, self.title_label, self.title_layout)
