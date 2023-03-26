from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from qt_thread_updater import get_updater

import constants as cons
from bson import json_util
import json
import threading

import certifi
import pymongo

class CombatLog:
    def __init__(self, combat_log_gui):
        self.combat_log_gui = combat_log_gui
        print("Combat Log Initialized")

    def get_log(self):
        db = cons.CLIENT["dnd"]
        self.COMBAT_LOG = db["combatlog"]
        doc = self.COMBAT_LOG.find()
        doc_list = list(doc)
        # json_doc = json.loads(json_util.dumps(doc))
        # print(json_doc)
        # return list(json_doc)
        # print(list(doc))
        return doc_list

    def get_collection(self):
        return self.COMBAT_LOG

    def start_watching(self):
        self.running = True
        thread = threading.Thread(target=self.watch_collection)
        thread.start()

    def stop_watching(self):
        self.running = False

    def watch_collection(self):
        while self.running:
            with self.COMBAT_LOG.watch() as change_stream:
                for update_doc in change_stream:
                    self.update_combat_log()

    def update_combat_log(self):
        combat_log = self.get_log()
        for count, entry in enumerate(combat_log):
            self.combat_log_gui.combet_log_slots[count].update_widget(entry)
        scrollbar = self.combat_log_gui.log_scroll.get_scroll().verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
