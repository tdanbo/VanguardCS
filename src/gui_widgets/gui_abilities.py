from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import constants as cons
import sys
from gui_widgets.gui_ability_frame import AbilityItem
from template.section import Section
from template.widget import Widget


class AddNewAbility(QWidget):
    def __init__(self, character):
        super().__init__(None, Qt.WindowStaysOnTopHint)
        self.all_abilities = cons.ABILITIES

        self.character = character

        self.master_layout = QVBoxLayout()
        self.master_layout.setSpacing(5)

        self.section_group = []
        self.widget_group = []

        self.ability_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.master_layout,
            group=True,
            class_group=self.section_group,
            content_margin=(0, 0, 0, 0),
        )

        for category in self.all_abilities:
            self.ability_widget = Widget(
                widget_type=QToolButton(),
                parent_layout=self.ability_section.inner_layout(1),
                icon=(f"{category}.png", cons.FONT_COLOR, cons.ICON_SIZE),
                height=cons.WSIZE * 2,
                objectname=category,
                class_group=self.widget_group,
                signal=self.add_abilities,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Fixed),
                stylesheet=f"background-color: {cons.PRIMARY}; border: 1px solid {cons.BORDER};",
                tooltip=category.replace("_", " ").title(),
            )

        self.search_section = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.master_layout,
            group=True,
            class_group=self.section_group,
            title="SEARCH",
            icon=("search.png", cons.PRIMARY_LIGHTER, cons.ICON_SIZE),
        )

        self.search_bar = Widget(
            widget_type=QLineEdit(),
            parent_layout=self.search_section.inner_layout(1),
            text="",
            align="center",
            objectname="search",
            class_group=self.widget_group,
            signal=self.add_abilities,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
        )

        self.search_section.get_title()[1].setAlignment(Qt.AlignCenter)
        self.search_section.get_title()[1].setStyleSheet(
            f"color: {cons.FONT_LIGHT}; padding-right: 12px;"
        )

        scroll_style = (
            f"QScrollBar {{background-color: {cons.PRIMARY}; width: 6px;}}"
            f"QWidget {{background-color: {cons.PRIMARY};}}"
            f"QScrollBar::handle:vertical {{background-color: {cons.BORDER}; width: 6px; min-height: 20px; border: none; outline: none;}}"
        )
        self.feats_scroll = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("VBox", 1),
            parent_layout=self.master_layout,
            scroll=(True, "top"),
            group=True,
            spacing=10,
            class_group=self.section_group,
            stylesheet=scroll_style,
        )

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setLayout(self.master_layout)
        self.setStyleSheet(
            f"border-style: outset; color: {cons.FONT_DARK}; background-color: {cons.DARK};"
        )
        self.setMinimumHeight(cons.WSIZE * 30)
        self.setMinimumWidth(cons.WSIZE * 20)
        self.setWindowTitle("Select Ability")

    def add_abilities(self):
        for button in self.all_abilities:
            self.findChild(QToolButton, button).setStyleSheet(
                f"background-color: {cons.PRIMARY}; border: 1px solid {cons.BORDER};"
            )

        self.sender().setStyleSheet(
            f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};"
        )

        self.category = self.sender().objectName()
        self.clear_layout(self.feats_scroll.inner_layout(1))

        if self.category == "search":
            if self.search_bar.get_widget().text() != "":
                for category in self.all_abilities:
                    for item in self.all_abilities[category]:
                        if item != "_id":
                            search_string = self.search_bar.get_widget().text().lower()
                            strings = [
                                self.all_abilities[category][item]["Name"],
                                self.all_abilities[category][item]["Tradition"],
                                self.all_abilities[category][item]["Description"],
                                self.all_abilities[category][item]["Novice"],
                                self.all_abilities[category][item]["Adept"],
                                self.all_abilities[category][item]["Master"],
                            ]

                            if any(
                                search_string in string.lower() for string in strings
                            ):
                                self.ability_dict = self.all_abilities[category][item]
                                self.add_ability()

            self.search_bar.get_widget().clearFocus()

        else:
            self.search_bar.get_widget().setText("")
            for item in self.all_abilities[self.category]:
                if item != "_id":
                    if self.search_bar.get_widget().text() == "":
                        self.ability_dict = self.all_abilities[self.category][item]
                        self.add_ability()
                    else:
                        print("Searching")

    def add_ability(self):
        self.ability_dict["Rank"] = "Master"
        ability = AbilityItem(self.character, self.ability_dict, select=True)
        self.feats_scroll.inner_layout(1).addWidget(ability)

    def clear_layout(self, layout):
        for item in range(layout.count()):
            layout.itemAt(item).widget().deleteLater()


def run_gui(name, version):
    app = QApplication(sys.argv)
    w = AddNewAbility("", "")
    w.show()
    app.exec_()


if __name__ == "__main__":
    run_gui("Character Sheet", "0.1")
