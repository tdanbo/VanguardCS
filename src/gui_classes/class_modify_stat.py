import re

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class ModifyStat:
    def __init__(self, string):
        self.string = string

    def find_integer(self):
        print(self.string)
        split = self.string.split(" ")
        self.string = split[0]
        if len(split) == 1:
            self.number = 0
            return self.number
        else:
            self.number = int(split[1])
            return self.number

    def add_one(self, character, widget):
        stat_mod = widget.objectName()
        integer_value = self.find_integer()
        integer_value += 1
        if integer_value == 0:
            new_value = self.string
        else:
            if integer_value > 0:
                new_value = f"{self.string} +{integer_value}"
            else:
                new_value = f"{self.string} {integer_value}"

        widget.setText(new_value)

        character.CHARACTER_DOC["mods"][stat_mod] = new_value
        character.set_stats()
        character.set_secondary_stats()
        character.set_calculated_stats()
        character.save_document()

    def subtract_one(self, character, widget):
        stat_mod = widget.objectName()
        integer_value = self.find_integer()
        integer_value -= 1
        if integer_value == 0:
            new_value = self.string
        else:
            if integer_value > 0:
                new_value = f"{self.string} +{integer_value}"
            else:
                new_value = f"{self.string} {integer_value}"

        widget.setText(new_value)

        character.CHARACTER_DOC["mods"][stat_mod] = new_value
        character.set_stats()
        character.set_secondary_stats()
        character.set_calculated_stats()
        character.save_document()
