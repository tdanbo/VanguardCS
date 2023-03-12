from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from qt_thread_updater import get_updater

import pymongo
import os
import constants as cons
from datetime import datetime
from bson import json_util
import json
import threading
import template.functions as func

from gui_windows.gui_combat_entry import CombatEntry

class CombatLog:
    def __init__(
        self,
        combat_log_gui
    ):
        self.combat_log_gui = combat_log_gui
        self.client = pymongo.MongoClient(cons.CONNECT)
        self.db = self.client ["dnd"]
        self.collection = self.db["combatlog"]

    def get_log(self):
        doc = self.collection.find().sort([("_id", -1)]).limit(21)
        json_doc = json.loads(json_util.dumps(doc))
        return list(json_doc)
        
    def get_collection(self):
        return self.collection

    def start_watching(self):
        self.running = True
        thread = threading.Thread(target=self.watch_collection) 
        thread.start()

    def stop_watching(self):
        self.running = False
        
    def watch_collection(self):
        while self.running:
            with self.collection.watch() as change_stream:
                print("Watching collection")
                for update_doc in change_stream:
                    self.update_combat_log()   
        
    def update_combat_log(self):
        print("Updating combat log")
        combat_log = reversed(self.get_log())
        for count,entry in enumerate(combat_log):
            self.combat_log_gui.combet_log_slots[count].update_widget(entry)
            # log_gui_entry = CombatEntry(count, entry)
            # layout.addWidget(log_gui_entry)

            # self.divider = QFrame()
            # self.divider.setFixedHeight(1)
            # self.divider.setStyleSheet(f"background-color: {cons.BORDER}")
            # layout.addWidget(self.divider)