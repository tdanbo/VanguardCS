from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from template.section import Section
from template.widget import Widget

import functions as func
import constants as cons

from class_sheet import CharacterSheet

import functools
import stylesheet as style
import template.stylesheet as tstyle

from gui_functions import character_stats
from gui_functions import custom_rolls

class CharacterSheetGUI(QWidget):
    def __init__(self, gui_inventory = None):
        super().__init__()


        self.gui_inventory = gui_inventory

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []

        self.stat_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 9),
            parent_layout = self.master_layout,
            group = True,
            spacing = 3,
            class_group = self.section_group
        )

        self.inventory_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 2),
            parent_layout = self.master_layout,
            title = "ABILITIES & POWERS",
            group = True,
            spacing=5,
            class_group=self.section_group
        )

        self.character_basic = Section(
            outer_layout = QVBoxLayout(),
            inner_layout = ("HBox", 1),
            parent_layout = self.master_layout,
            spacing=10,
            class_group = self.section_group,
        )

        self.corruption_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 3),
            parent_layout = self.character_basic.inner_layout(1),
            group = True,
            title = "CORRUPTION",
            spacing = 3,
            class_group=self.section_group
        )

        self.corruption_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.hp_layout = Section(
            outer_layout = QHBoxLayout(),
            inner_layout = ("VBox", 3),
            parent_layout = self.character_basic.inner_layout(1),
            group = True,
            title = "TOUGHNESS",
            spacing = 3,
            class_group=self.section_group
        )

        self.hp_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        for power in range(1, 13):
            if power % 2 == 0:
                layout_number = 1
            else:
                layout_number = 2
                
            title = "Acrobatics"
            test_text = "The character may roll against Quick to avoid Free Attacks from enemies in melee combat, either when trying to slip past an enemy or when attempting to withdraw from melee. Should the test fail, the player must choose to either remain in its original place or to move anyway and suffer a Free Attack from the opponent."


            self.power_section = Section(
                outer_layout = QHBoxLayout(),
                inner_layout = ("HBox", 1),
                parent_layout = self.inventory_layout.inner_layout(layout_number),
                title=title,
                group = True,
                spacing = 3,
                class_group=self.section_group
            )

            title_layout = self.power_section.get_title()[2]
            self.power_section.get_title()[1].setAlignment(Qt.AlignCenter)
            
            self.power_description = Widget(
                widget_type=QTextEdit(),
                stylesheet=style.QSTATS,
                parent_layout = self.power_section.inner_layout(1),
                text=test_text,
                objectname="power_description",
                class_group=self.widget_group
            )

            self.novice = Widget(
                widget_type=QPushButton(),
                stylesheet=tstyle.QTITLE,
                text="N",
                width=cons.WSIZE,
                height=cons.WSIZE
            )

            self.adept = Widget(
                widget_type=QPushButton(),
                stylesheet=tstyle.QTITLE,
                text="A",
                width=cons.WSIZE,
                height=cons.WSIZE,
                enabled=False
            )

            self.master = Widget(
                widget_type=QPushButton(),
                stylesheet=tstyle.QTITLE,
                text="M",
                width=cons.WSIZE,
                height=cons.WSIZE,
                enabled=False
            )

            self.delete = Widget(
                widget_type=QToolButton(),
                stylesheet=tstyle.QTITLE,
                parent_layout = title_layout,
                class_group=self.widget_group,
                width=cons.WSIZE,
                height=cons.WSIZE,
                icon = ("delete.png",cons.WSIZE,cons.ICON_COLOR),
            )

            title_layout.insertWidget(0, self.novice.widget)
            title_layout.insertWidget(1, self.adept.widget)
            title_layout.insertWidget(2, self.master.widget)


        self.inventory_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        #Below is all the widgets used in the character sheet
        for number,stat in enumerate(cons.STATS):
            number = number + 1
            print(stat)
            self.stat_button = Widget(
                widget_type=QPushButton(),
                stylesheet=style.BIG_BUTTONS,
                parent_layout = self.stat_layout.inner_layout(number),
                text="10",
                signal=functools.partial(
                    character_stats.adjust_stat,
                    self,
                    stat,
                    adjust="add"
                ),
                objectname=stat,
                class_group=self.widget_group,
                height=cons.WSIZE*2,
            )
            self.stat_sub_layout = Section(
                outer_layout = QHBoxLayout(),
                inner_layout = ("HBox", 1),
                parent_layout = self.stat_layout.inner_layout(number),
                spacing=0,
                class_group = self.section_group
                
            )

            self.stat_button = Widget(
                widget_type=QPushButton(),
                parent_layout=self.stat_sub_layout.inner_layout(0),
                text=stat,
                stylesheet=style.QSTATS,
                objectname=f"{stat}_label",
                signal=functools.partial(
                    custom_rolls.modify_stat,
                    self,
                    stat
                ),
                class_group=self.widget_group,
                height=cons.WSIZE
            )

            self.stat_modifier = Widget(
                widget_type=QPushButton(),
                parent_layout=self.stat_sub_layout.inner_layout(0),
                text="0",
                stylesheet=style.QSTATS,
                objectname=f"{stat}_mod",
                signal=functools.partial(
                    custom_rolls.modify_stat,
                    self,
                    stat
                ),
                class_group=self.widget_group,
                height=cons.WSIZE
            )   

        self.toughness_threshold = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(1),
            objectname = "toughness_threshold",
            class_group=self.widget_group,
            stylesheet = tstyle.WIDGETS
        )

        self.toughness_max = Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname = "toughness_max",
            class_group=self.widget_group,
            stylesheet = tstyle.WIDGETS
        )

        self.toughness_current= Widget(
            widget_type=QPushButton(),
            parent_layout=self.hp_layout.inner_layout(3),
            signal=self.open_addsub,
            objectname = "toughness_current",
            class_group=self.widget_group,
            stylesheet = tstyle.WIDGETS
        )

        self.toughness_threshold_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.hp_layout.inner_layout(1),
            text = "THRESHOLD",
            class_group=self.widget_group,
            stylesheet = tstyle.LABELS,
            align=Qt.AlignCenter
        )

        self.toughness_max_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.hp_layout.inner_layout(2),
            objectname = "toughness_max",
            class_group=self.widget_group,
            text = "MAXIMUM",
            stylesheet = tstyle.LABELS,
            align=Qt.AlignCenter
        )

        self.toughness_current_label= Widget(
            widget_type=QLabel(),
            parent_layout=self.hp_layout.inner_layout(3),
            signal=self.open_addsub,
            objectname = "toughness_current",
            text = "CURRENT",
            class_group=self.widget_group,
            stylesheet = tstyle.LABELS,
            align=Qt.AlignCenter
        )

        self.corruption_threshold = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(1),
            signal=lambda: CharacterSheet(self).update_sheet(),
            text = "99",
            class_group=self.widget_group,
            stylesheet = tstyle.WIDGETS
        )

        self.corruption_permanent = Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(2),
            objectname = "toughness_permanenet",
            class_group=self.widget_group,
            stylesheet = tstyle.WIDGETS
        )

        self.corruption_temporary= Widget(
            widget_type=QPushButton(),
            parent_layout=self.corruption_layout.inner_layout(3),
            signal=self.open_addsub,
            objectname = "corruption_current",
            class_group=self.widget_group,
            stylesheet = tstyle.WIDGETS
        )

        self.corruption_threshold_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.corruption_layout.inner_layout(1),
            text = "THRESHOLD",
            class_group=self.widget_group,
            stylesheet = tstyle.LABELS,
            align=Qt.AlignCenter
        )

        self.corruption_permanent_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.corruption_layout.inner_layout(2),
            class_group=self.widget_group,
            stylesheet = tstyle.LABELS,
            text = "PERMANENT",
            align=Qt.AlignCenter
        )

        self.corruption_temporary_label = Widget(
            widget_type=QLabel(),
            parent_layout=self.corruption_layout.inner_layout(3),
            class_group=self.widget_group,
            stylesheet = tstyle.LABELS,
            text = "TEMPORARY",
            align=Qt.AlignCenter
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)       

    def mousePressEvent(self, event): #this is a very specific event used to subtract values when right clicking on a widget
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if widget.objectName() in [stat+"_label" for stat in self.attribute_list]+[stat+"_mod" for stat in self.attribute_list]:
                custom_rolls.modify_stat(self, widget.objectName().split("_")[0], adjust="subtract")

    def open_features(self):
        sender = self.sender()
        self.features = FeatsGUI(self, sender)
        self.features.show()

    def open_addsub(self):
        sender = self.sender()
        self.addsub = AddSubGUI(self, sender)
        self.addsub.show()