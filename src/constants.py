# import functions as func
import os
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
try:
    ROOT = sys._MEIPASS
except:
    ROOT = os.path.dirname(__file__)

SCRIPT_NAME = "Vanguard 5e"
LOCAL_DIRECTORY = os.path.join(os.getenv("APPDATA"), SCRIPT_NAME)
VERSION = "1.0"
USER = "test-user"
PASSWORD = "7kHYdt9kna9d9w3t"
TOKEN = "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"
CONNECT = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.2oqhlud.mongodb.net/?retryWrites=true&w=majority"
SETTINGS = os.path.join(LOCAL_DIRECTORY, "settings.json")
ICONS = os.path.join(ROOT, ".icons")
FEATURES = os.path.join(ROOT, ".feats")

ITEMS = os.path.join(ROOT, ".items")

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
ARMOR = ["armor"]

# func.create_folder(LOCAL_DIRECTORY)

PRIMARY_DARKER = "#e1ddcd"
PRIMARY = "#f0e8d9"
PRIMARY_LIGHTER = "#f1efe9"

DARK = "#231f20"


FONT_LIGHT = "#ffffff"
FONT_DARK = "#282425"
FONT_COLOR = "#864433"

BORDER = "#BAAD96"
