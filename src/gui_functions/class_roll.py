import random
import datetime
import pymongo
import constants as cons

class DiceRoll:
    def __init__(self, combat_log, character, roll_type, dice, check=0):

        self.combat_log = combat_log
        self.modifier_widget = self.combat_log.modifier_button.get_widget()
        self.dice = dice
        self.modifier = int(self.modifier_widget.text())
        self.check = check
        self.entry  = {
            "Character": character,
            "Type": roll_type,
            "Dice": dice,
            "Modifier": self.modifier,
            "Result": "",
            "Result Breakdown": "",
            "Result Message": "",
            "Time": "",
        }

        self.modifier_widget.setText("0")

    def roll(self):
        dice_roll = 0
        breakdowns = []

        initial_split = self.dice.split("_")
        for single_dice in initial_split:
            modifier_split = single_dice.split("+")
            if len(modifier_split) > 1:
                self.modifier += int(modifier_split[1])
                single_dice = modifier_split[0]
            else:
                single_dice

            dice = single_dice.split("d")
            dice_count = int(dice[0])
            dice_type = int(dice[1])

            dice_breakdown = []

            for i in range(dice_count):
                roll = random.randint(1, dice_type)
                dice_roll += roll
                dice_breakdown.append(roll)

            self.breakdown = '+'.join(str(num) for num in dice_breakdown)
            self.full_breakdown = f"{single_dice} = {self.breakdown} modified {self.modifier}"
            breakdowns.append(self.full_breakdown)

        joined_breakdowns = "\n".join(breakdowns)

        self.result = dice_roll + self.modifier      

        self.entry["Result"] = self.result

        if self.modifier > 0:
            self.entry["Result Breakdown"] = joined_breakdowns
        elif self.modifier < 0:
            self.entry["Result Breakdown"] = joined_breakdowns
        else:
            self.entry["Result Breakdown"] = joined_breakdowns

        if self.check > 0:
            self.check_roll()
        self.set_time()

        self.save_to_database()

    def check_roll(self):
        if self.result <= self.check:
            self.entry["Result Message"] = "Success"
        else:
            self.entry["Result Message"] = "Failed"

    def set_time(self):
        self.entry["Time"] = datetime.datetime.now().strftime("%H:%M:%S")

    def save_to_database(self):
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["combatlog"]
        self.collection.insert_one(self.entry)