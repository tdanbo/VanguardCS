import re

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class ModifyStat:
    def __init__(self, string):
        self.string = string

    def find_integer(self):
        split = self.string.split(" ")
        self.string = split[0]
        if len(split) == 1:
            self.number = 0
            return self.number
        else:
            self.number = int(split[1])
            return self.number
    
    def add_one(self, character_sheet, widget):
        stat_mod = widget.objectName()
        integer_value = self.find_integer()
        integer_value += 1
        if integer_value == 0:
            new_value =  self.string
        else:
            new_value = f"{self.string} {integer_value}"
    
        widget.setText(new_value)

        print(stat_mod)

        character_sheet.CHARACTER_DOC["stats"][stat_mod] = new_value
        character_sheet.update_sheet()

    def subtract_one(self, character_sheet, widget):
        stat_mod = widget.objectName()
        integer_value = self.find_integer()
        integer_value -= 1
        if integer_value == 0:
            new_value = self.string
        else:
            new_value = f"{self.string} {integer_value}"

        widget.setText(new_value)

        print(stat_mod)

        character_sheet.CHARACTER_DOC["stats"][stat_mod] = new_value
        character_sheet.update_sheet()