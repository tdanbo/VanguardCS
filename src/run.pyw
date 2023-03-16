import sys
import gui_new
import constants as cons
import functions as func

sys.dont_write_bytecode = True  # Will supress __pycache__ creation

import os
from importlib import *

ROOT = os.path.abspath(os.path.dirname(__file__))
PACKAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".packages")
[sys.path.append(p) for p in [ROOT, PACKAGES] if p not in sys.path]


[reload(module) for module in [gui_new, func, cons]]

def run():
    gui_new.run_gui(cons.SCRIPT_NAME, cons.VERSION)

if __name__ == "__main__":
    run()
