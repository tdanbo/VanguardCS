from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

'''
This area of code handles the functions of the dice roller.
'''

def add_dice(self, dice, adjust="add"):
    print(dice)
    if "_count" in dice:
        count_widget = self.findChild(QPushButton, f"{dice}")
    else:
        count_widget = self.findChild(QPushButton, f"{dice}_count")

    if count_widget.text() == "":
        current_value = 0
    else:
        current_value = int(count_widget.text())

    if adjust == "add":
        count_widget.setText(str(current_value + 1))
    else:
        if current_value > 0:
            count_widget.setText(str(current_value - 1))
            if count_widget.text() == "0":
                count_widget.setText("")                
        else:
            count_widget.setText("")
    if count_widget.text() == "":
        roll_button(self, shown=False)
    else:
        roll_button(self, shown=True)
            
def roll_button(self, shown=False):
    title_widgets = self.log_dice.get_title()
    title_widgets[1].setHidden(shown)

    self.roll_button.get_widget().setHidden(not shown)

def clear_rolls(self):
    for objectname in ["d4","d6","d8","d10","d12","d20"]:
        counter = self.findChild(QPushButton, f"{objectname}_count")
        counter.setText("")
    roll_button(self, shown=False)