from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from qt_thread_updater import get_updater
import pymongo
import constants as cons
from bson import json_util
import json
import threading


class CombatLog:
    def __init__(
        self,
        combat_log_gui
    ):
        self.combat_log_gui = combat_log_gui
        print("Combat Log Initialized")
        
    def get_log(self):
        doc = cons.COMBAT_LOG.find().sort([("_id", -1)]).limit(21)
        json_doc = json.loads(json_util.dumps(doc))
        return list(json_doc)
        
    def get_collection(self):
        return cons.COMBAT_LOG

    def start_watching(self):
        self.running = True
        thread = threading.Thread(target=self.watch_collection) 
        thread.start()

    def stop_watching(self):
        self.running = False
        
    def watch_collection(self):
        while self.running:
            with cons.COMBAT_LOG.watch() as change_stream:
                for update_doc in change_stream:
                    self.update_combat_log()   
        
    def update_combat_log(self):
        combat_log = reversed(self.get_log())
        for count,entry in enumerate(combat_log):
            self.combat_log_gui.combet_log_slots[count].update_widget(entry)
        scrollbar = self.combat_log_gui.log_scroll.get_scroll().verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())