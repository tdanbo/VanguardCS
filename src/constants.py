# import functions as func
import os
import sys
import json
from template.license import License
import pymongo

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

print("Version Below")
print(VERSION)

CONNECT = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.2oqhlud.mongodb.net/?retryWrites=true&w=majority"
ICONS = os.path.join(ROOT, ".icons")


WSIZE = 22
ICON_COLOR = "#CCCCCC"

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
    "CORRUPTION",
    "PERMANENT",
    "THRESHOLD"
]

#ARMOR = ["armor"]

# func.create_folder(LOCAL_DIRECTORY)

RED = "#925833"
BLUE = "#495C60"
PURPLE = "#60495c"
GREEN = "#5c6049"
YELLOW = "#926f2b"
WHITE = "#bfb6ac"

ACTIVE_COLOR = {
    "ATTACK": RED,
    "ABILITY": RED,
    "MELEE": RED,
    "RANGED": RED,
    "DEFENSE": BLUE,
    "ARMOR": BLUE,
    "CASTING": PURPLE,
    "MYSTICAL POWER": PURPLE,
    "RITUAL": PURPLE,
    "ELIXIRS": PURPLE,
    "SNEAKING": GREEN,
    "AMMUNITION": GREEN,
    "TEST":YELLOW,
    "TREASURE": YELLOW,
    "MISC": WHITE
}

#PRIMARY_DARKER = "#e1ddcd"
PRIMARY_DARKER = "#dbd7c8"
PRIMARY = "#f0e8d9"
PRIMARY_LIGHTER = "#f1efe9"

#DARK = "#231f20"
DARK = "#262223"


FONT_LARGE = "17px"
FONT_MID = "15px"
FONT_SMALL = "11px"

FONT_LIGHT = "#f1efe9"
FONT_MEDIUM = "#4d473e"
FONT_DARK = "#282425"
FONT_COLOR = "#864433"

BORDER_LIGHT = "#ccbda5"
BORDER = "#b3a691"
BORDER_DARK = "#998e7c"

client = pymongo.MongoClient(CONNECT)
QUALITIES = client["equipment"]["quality"].find_one()

ABILITIES = {}
db = client["abilities"]
collection_names = db.list_collection_names()
for name in collection_names:
    collection = db[name]
    document = collection.find_one()
    ABILITIES[name] = document