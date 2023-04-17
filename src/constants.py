# import functions as func
import os
import sys
import json
from template.license import License
import pymongo
import certifi

ROOT = os.path.abspath(os.path.dirname(__file__))
try:
    ROOT = sys._MEIPASS
except:
    ROOT = os.path.dirname(__file__)

# SCRIPT_NAME = "Vanguard 5e"
# LOCAL_DIRECTORY = os.path.join(os.getenv("APPDATA"), SCRIPT_NAME)
# SETTINGS = os.path.join(LOCAL_DIRECTORY, "settings.json")


LICENSE = License().get_license()

USER = LICENSE["user"]
PASSWORD = LICENSE["password"]
VERSION = LICENSE["version"]

print(VERSION)

CONNECT = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.2oqhlud.mongodb.net/?retryWrites=true&w=majority"
ICONS = os.path.join(ROOT, ".icons")
SOUNDS = os.path.join(ROOT, ".sounds")

WSIZE = 22
ICON_COLOR = "#CCCCCC"
ICON_SIZE = 18
CHARACTER = "Beasttoe"
START_SLOTS = 6
MAX_SLOTS = 16

STATS = [
    "ACCURATE",
    "CUNNING",
    "DISCREET",
    "PERSUASIVE",
    "QUICK",
    "RESOLUTE",
    "STRONG",
    "VIGILANT",
]

SECONDARY_STATS = [
    "TOUGHNESS",
    "MAXIMUM",
    "PAIN",
]

MOVEMENT = {
    5: -5,
    6: -5,
    7: -5,
    8: -5,
    9: 0,
    10: 0,
    11: 0,
    12: 5,
    13: 5,
    14: 5,
    15: 5,
}


# ARMOR = ["armor"]

# func.create_folder(LOCAL_DIRECTORY)
DARK = "#262223"
RED = "#925833"
BLUE = "#495C60"
PURPLE = "#60495c"
GREEN = "#5c6049"
YELLOW = "#926f2b"
WHITE = "#bfb6ac"
BRIGHT_RED = "#923333"
ACTIVE_COLOR = {
    "ATTACK": RED,
    "DAMAGE": RED,
    "ABILITY": RED,
    "DEFENSE": BLUE,
    "ARMOR": BLUE,
    "CASTING": PURPLE,
    "MYSTICAL POWER": PURPLE,
    "RITUAL": PURPLE,
    "ELIXIRS": PURPLE,
    "SNEAKING": GREEN,
    "AMMUNITION": RED,
    "MONSTEROUS TRAIT": GREEN,
    "TEST": YELLOW,
    "SKILL": YELLOW,
    "PROVISION": GREEN,
    "TREASURE": YELLOW,
    "ORDINARY_WEAPON": RED,
    "ORDINARY_RANGED": RED,
    "ORDINARY_ARMOR": BLUE,
    "QUALITY_WEAPON": RED,
    "QUALITY_RANGED": RED,
    "QUALITY_ARMOR": BLUE,
    "GENERAL_GOOD": YELLOW,
    "LESSER_ARTIFACT": BRIGHT_RED,
    "CORRUPTION": DARK,
}

PRIORITY = {
    "lesser_artifact": 0,
    "quality_weapon": 1,
    "ordinary_weapon": 2,
    "quality_ranged": 3,
    "ordinary_ranged": 4,
    "ammunition": 5,
    "quality_armor": 6,
    "ordinary_armor": 7,
    "elixirs": 8,
    "provision": 9,
    "treasure": 10,
    "tools": 11,
    "General Good": 12,
}

PRIMARY_HOVER = "#fffdf7"
PRIMARY_DARKER = "#dbd7c8"
PRIMARY = "#f0e8d9"
PRIMARY_MEDIUM = "#f2eedf"
PRIMARY_LIGHTER = "#f1efe9"
BORDER_LIGHT = "#ccbda5"
BORDER = "#b3a691"
BORDER_DARK = "#998e7c"

DARK = "#262223"


FONT_LARGE = "17px"
FONT_MID = "15px"
FONT_SMALL = "11px"

FONT_LIGHT = "#f1efe9"
FONT_MEDIUM = "#4d473e"
FONT_DARK = "#282425"
FONT_COLOR = "#864433"

#
# DARK MODE
# PRIMARY_DARKER = "#2d2d2d"
# PRIMARY = "#373737"
# PRIMARY_LIGHTER = "#32393d"
# BORDER_LIGHT = "#2d2d2d"
# BORDER = "#2d2d2d"
# BORDER_DARK = "#2d2d2d"

# READING DATABASE
CLIENT = pymongo.MongoClient(CONNECT, tlsCAFile=certifi.where())
QUALITIES = CLIENT["qualities"]["qualities"].find_one()

ABILITIES = {}
db = CLIENT["abilities"]
collection_names = db.list_collection_names()
for name in collection_names:
    collection = db[name]
    document = collection.find_one()
    ABILITIES[name] = document

EQUIPMENT = {}
db = CLIENT["equipment"]
collection_names = db.list_collection_names()
for name in collection_names:
    collection = db[name]
    document = collection.find_one()
    EQUIPMENT[name] = document

db = CLIENT["dnd"]
COMBAT_LOG = db["combatlog"]

TOOLTIP = {
    "ACCURATE": "Hand-eye coordination, hit antagonist with bow/sword/axe.",
    "CUNNING": "Recollect facts, make conclusions, do research.",
    "DISCREET": "Avoid detection, sneak, smuggle items, trail person, pick pockets.",
    "PERSUASIVE": "Influence/convince others, lead, rally.",
    "QUICK": "Initiative, balance, climb, avoid being hit, sprint.",
    "RESOLUTE": "Succeed with or resist various spells, resist being influenced.",
    "STRONG": "Withstand damage/poison/disease, perform feats of strength.",
    "VIGILANT": "Detect person/item, avoid ambush, sense danger.",
}