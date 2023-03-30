from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys

from template.section import Section
from template.widget import Widget
import constants as cons

# from gui_classes.custom_roll import class_custom_rolls
from gui_classes.class_character import Character

from gui_classes.class_roll import DiceRoll
from gui_classes.class_modify_roll import ModifyRoll

from gui_widgets.gui_new_char_frame import NewCharacter
from gui_widgets.gui_add_sub import AddSub
from gui_widgets.gui_del_char_frame import DeleteChar
from gui_widgets.gui_equipment import AddNewEquipment


class InventoryGUI(QWidget):
    def __init__(self, character):
        super().__init__()

        self.top_button = f"QPushButton {{background-color: {cons.PRIMARY_MEDIUM}; color: {cons.FONT_COLOR}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;}}"

        self.bottom_button = (
            f"QPushButton {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;}}"
            f"QPushButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
            f"QPushButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
        )

        self.bottom_tool_button = (
            f"QToolButton {{background-color: {cons.PRIMARY_LIGHTER}; color: {cons.FONT_DARK}; font-size: {cons.FONT_SMALL}; font-weight: bold; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;}}"
            f"QToolButton:hover {{background-color: {cons.PRIMARY_HOVER};}}"
            f"QToolButton:pressed {{background-color: {cons.PRIMARY_LIGHTER};}}"
        )

        # setting up character sheet
        self.character = character

        self.master_layout = QVBoxLayout()
        self.section_group = []
        self.widget_group = []
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.master_layout.setSpacing(0)
        # Setting up layouts/sections

        self.portrait_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 3),
            parent_layout=self.master_layout,
            group=True,
            title="Test",
            icon=("dead.png", cons.PRIMARY_DARKER, cons.ICON_SIZE),
            class_group=self.section_group,
            spacing=3,
            height=100,
        )

        self.portrait_layout.get_title()[1].setText("")
        self.portrait_layout.get_title()[0].setStyleSheet(
            f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};"
        )

        self.name_layout = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("HBox", 2),
            parent_layout=self.portrait_layout.inner_layout(2),
            class_group=self.section_group,
            content_margin=(0, 0, 0, 0),
            spacing=3,
        )

        scroll_style = (
            f"QScrollBar {{background-color: {cons.PRIMARY}; width: 6px;}}"
            f"QWidget {{background-color: {cons.PRIMARY};}}"
            f"QScrollBar::handle:vertical {{background-color: {cons.BORDER}; width: 6px; min-height: 20px; border: none; outline: none;}}"
        )
        self.inventory_scroll = Section(
            outer_layout=QVBoxLayout(),
            inner_layout=("VBox", 1),
            parent_layout=self.master_layout,
            scroll=(True, "bottom"),
            title="BACKPACK",
            group=True,
            class_group=self.section_group,
            spacing=0,
            content_margin=(0, 0, 0, 0),
            stylesheet=scroll_style,
            icon=("codex.png", cons.PRIMARY_DARKER, cons.ICON_SIZE),
        )

        self.inventory_scroll.get_title()[0].clicked.connect(self.show_codex)
        self.inventory_scroll.get_title()[1].setAlignment(Qt.AlignCenter)

        self.portrait = Widget(
            widget_type=QLabel(),
            parent_layout=self.portrait_layout.inner_layout(1),
            objectname="portrait",
            class_group=self.widget_group,
            height=58,
            width=100,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
            # width=cons.WSIZE*6,
        )

        self.portrait.get_widget().setAlignment(Qt.AlignCenter)

        self.character_name = Widget(
            widget_type=QComboBox(),
            parent_layout=self.portrait_layout.get_title()[2],
            objectname="name",
            class_group=self.widget_group,
            signal=lambda: self.load_character(),
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER}; font-size: {cons.FONT_MID}; font-weight: bold; color: {cons.FONT_COLOR};",
        )

        self.create_character = Widget(
            widget_type=QToolButton(),
            parent_layout=self.portrait_layout.get_title()[2],
            objectname="delete",
            class_group=self.widget_group,
            icon=("plus.png", cons.FONT_COLOR, cons.ICON_SIZE),
            signal=self.open_new_character,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
        )

        self.update_character = Widget(
            widget_type=QToolButton(),
            parent_layout=self.portrait_layout.get_title()[2],
            objectname="update",
            class_group=self.widget_group,
            icon=("reload.png", cons.FONT_COLOR, cons.ICON_SIZE),
            signal=self.update_character_dropdown,
            height=cons.WSIZE,
            stylesheet=f"background-color: {cons.PRIMARY_LIGHTER}; border: 1px solid {cons.BORDER};",
        )

        self.experience_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 3),
            parent_layout=self.name_layout.inner_layout(2),
            class_group=self.section_group,
            spacing=3,
        )

        self.movement_button = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(3),
            # signal=self.modify_stat,
            objectname="MOVEMENT",
            class_group=self.widget_group,
            stylesheet=self.top_button,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            hidden=False,
        )

        self.movement_mod_button = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(3),
            text="Ft.",
            objectname=f"MOVEMENT mod",
            class_group=self.widget_group,
            stylesheet=self.bottom_button,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            hidden=False,
        )

        self.experience = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(1),
            objectname="XP",
            class_group=self.widget_group,
            # height=cons.WSIZE * 1.5,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            stylesheet=self.top_button,
        )

        self.experience_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(1),
            objectname="XP mod",
            class_group=self.widget_group,
            text="XP",
            # height=cons.WSIZE,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            stylesheet=self.bottom_button,
        )

        self.unspent_experience = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(2),
            objectname="TOTALXP",
            class_group=self.widget_group,
            # height=cons.WSIZE * 1.5,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            stylesheet=self.top_button,
        )

        self.unspent_experience_label = Widget(
            widget_type=QPushButton(),
            parent_layout=self.experience_section.inner_layout(2),
            objectname="TOTALXP mod",
            class_group=self.widget_group,
            text="UNSPENT",
            # height=cons.WSIZE,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal=self.add_sub,
            stylesheet=self.bottom_button,
        )

        portrait_title = self.portrait_layout.get_title()[0]
        portrait_title.clicked.connect(self.delete_character)

        self.equipment_layout = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 2),
            parent_layout=self.master_layout,
            group=True,
            title="EQUIPMENT",
            class_group=self.section_group,
            content_margin=(0, 0, 0, 0),
            spacing=0,
            height=216,
        )

        self.equipment_layout.get_title()[1].setAlignment(Qt.AlignCenter)

        self.bottom_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("HBox", 1),
            parent_layout=self.master_layout,
            class_group=self.section_group,
            spacing=3,
            height=100,
        )

        self.active_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 5),
            parent_layout=self.bottom_section.inner_layout(1),
            title="ACTIVE",
            group=True,
            class_group=self.section_group,
            spacing=3,
        )

        self.active_section.get_title()[1].setAlignment(Qt.AlignCenter)

        # Below is all the widgets used in the character sheet
        for number, stat in enumerate(
            ["CASTING", "SNEAKING", "SKILL", "DEFENSE", "ATTACK"]
        ):
            self.extra_modifier_button = Widget(
                widget_type=QPushButton(),
                parent_layout=self.active_section.inner_layout(number + 1),
                objectname=f"{stat} mod",
                class_group=self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
                checkable=True,
                checked=False,
                stylesheet=self.top_button,
            )

            self.extra_modifier_label = Widget(
                widget_type=QToolButton(),
                parent_layout=self.active_section.inner_layout(number + 1),
                icon=(f"{stat.capitalize()}.png", cons.DARK, cons.ICON_SIZE),
                class_group=self.widget_group,
                size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
                checkable=True,
                checked=False,
                objectname=f"{stat} button",
                signal=self.change_active_modifier,
                stylesheet=self.bottom_tool_button,
            )

        self.modifier_section = Section(
            outer_layout=QHBoxLayout(),
            inner_layout=("VBox", 5),
            parent_layout=self.bottom_section.inner_layout(1),
            title="MODIFIER",
            group=True,
            class_group=self.section_group,
            spacing=3,
            width=60,
        )

        self.modifier_section.get_title()[1].setAlignment(Qt.AlignCenter)

        self.modifier_mod = Widget(
            widget_type=QPushButton(),
            parent_layout=self.modifier_section.inner_layout(1),
            objectname="MODIFIER mod",
            class_group=self.widget_group,
            stylesheet=f"background-color: {cons.PRIMARY_MEDIUM}; color: {cons.PRIMARY_LIGHTER}; font-size: {cons.FONT_MID}; font-weight: bold; border: 1px solid {cons.BORDER}; border-top-left-radius: 6px; border-top-right-radius: 6px;",
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            signal=lambda: self.adjust_modifier("subtract"),
            enabled=False,
        )

        self.modifier_button = Widget(
            widget_type=QToolButton(),
            parent_layout=self.modifier_section.inner_layout(1),
            icon=(f"Modifier.png", cons.PRIMARY_LIGHTER, cons.ICON_SIZE),
            class_group=self.widget_group,
            size_policy=(QSizePolicy.Expanding, QSizePolicy.Expanding),
            objectname="MODIFIER button",
            stylesheet=f"background-color: {cons.PRIMARY_MEDIUM}; border: 1px solid {cons.BORDER}; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;",
            signal=lambda: self.adjust_modifier("subtract"),
            enabled=False,
        )

        self.update_character_dropdown()

        for widget in self.widget_group:
            widget.connect_to_parent()
            widget.set_signal()

        for section in self.section_group:
            section.connect_to_parent()

        self.setFixedWidth(300)
        self.setStyleSheet(
            f"border-style: outset; color: {cons.FONT_DARK}; background-color: {cons.DARK};border-style: outset;"
        )
        self.setLayout(self.master_layout)
        self.character.set_inventory_gui(self)

    def mousePressEvent(
        self, event
    ):  # this is a very specific event used to subtract values when right clicking on a widget
        if event.button() == Qt.RightButton:
            widget = self.childAt(event.pos())
            if widget.objectName() in ["MODIFIER button", "MODIFIER mod"]:
                self.adjust_modifier("add")

    def load_character(self):
        self.current_character_name = self.character_name.get_widget().currentText()
        print(f"loading character: {self.current_character_name}")
        if self.current_character_name == "":
            self.character.clear_character()
            return
        self.character.load_document(self.current_character_name)

    def open_new_character(self):
        self.new_character = NewCharacter(self, self.character)
        self.new_character.show()

    def update_character_dropdown(self):
        print("updating character dropdown")
        self.db = cons.CLIENT["dnd"]
        self.collection = self.db["characters"]
        character_list = self.collection.distinct("character")
        self.character_name.get_widget().clear()
        self.character_name.get_widget().addItems([""] + character_list)
        # if selected_char in character_list:
        #     self.character_name.get_widget().setCurrentText(selected_char)
        # else:
        #     self.character_name.get_widget().setCurrentText("")

    def delete_character(self):

        current_character = self.character_name.get_widget().currentText()
        print(f"delete {current_character} from database")

        # prompt the deletion
        show_warning = DeleteChar(self, current_character)
        warning = show_warning.show()

    def roll_dice(self):
        self.character = self.character_sheet.character_name
        self.combat_log = self.character_sheet.combat_log
        self.roll_type = self.sender().property("roll")

        if self.roll_type in ["CASTING", "DEFENSE"]:
            self.check = int(self.sender().text())
            self.dice = "1d20"
        else:
            self.check = 0
            self.dice = self.sender().text()

        rolling_dice = DiceRoll(
            self.sender(),
            self.combat_log,
            self.character,
            self.roll_type.capitalize(),
            self.dice,
            check=self.check,
        ).roll()

    def add_sub(self):
        objectname = self.sender().objectName().split(" ")[0]
        number_widget = self.findChild(QPushButton, objectname)
        add_sub_gui = AddSub(
            self.character, number_widget, doc_item=objectname, xp=True
        )
        add_sub_gui.show()

    def change_active_modifier(self):
        ModifyRoll(self.character).change_active(self.sender())

    def adjust_modifier(self, adjust):
        current_value = int(self.modifier_mod.get_widget().text())
        if adjust == "add":
            current_value += 1
        else:
            current_value -= 1

        if current_value > 0:
            current_value = f"+{current_value}"

        self.modifier_mod.get_widget().setText(str(current_value))
        ModifyRoll(self.character).run_set_stats()

    def show_codex(self):
        self.codex = AddNewEquipment(self.character)
        self.codex.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryGUI()
    window.show()
    sys.exit(app.exec_())
