# import functions as func
import os
import sys
import json

ROOT = os.path.abspath(os.path.dirname(__file__))
try:
    ROOT = sys._MEIPASS
except:
    ROOT = os.path.dirname(__file__)

SCRIPT_NAME = "Vanguard 5e"
LICENSE_SCRIPT = "VanguardLauncher"

LOCAL_DIRECTORY = os.path.join(os.getenv("APPDATA"), SCRIPT_NAME)
LICENSE_DIRECTORY = os.path.join(os.getenv("APPDATA"), LICENSE_SCRIPT)

VERSION = "1.0"

cwd = os.getcwd()
KEY_PATH = os.path.join(ROOT,"world.key")

print(f"KEY_PATH: {KEY_PATH}")

LICENSE = json.load(open(os.path.join(KEY_PATH), "r"))
USER = LICENSE["user"]
PASSWORD = LICENSE["password"]
CONNECT = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.2oqhlud.mongodb.net/?retryWrites=true&w=majority"

SETTINGS = os.path.join(LOCAL_DIRECTORY, "settings.json")
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
