        print("---------------------------") 
        print("Character Sheet Created")

        self.stat_button = None

        self.character_icon = self.invsheet.findChild(QWidget,"portrait")
        self.character = self.invsheet.findChild(QWidget,"name")
        self.experience = self.invsheet.findChild(QWidget,"experience")
        self.experience_unspent = self.invsheet.findChild(QWidget,"unspent_experience")

        #hp
        self.toughness_current = self.csheet.toughness_current.get_widget()
        self.toughness_max = self.csheet.toughness_max.get_widget()
        self.toughness_threshold = self.csheet.toughness_threshold.get_widget()

        #corruption
        self.corruption_temporary = self.csheet.corruption_temporary.get_widget()
        self.corruption_permanent = self.csheet.corruption_permanent.get_widget()
        self.corruption_threshold = self.csheet.corruption_threshold.get_widget()

        #defense
        self.defense = self.invsheet.defense.get_widget()

        print(self.character.currentText())
        print(self.defense.text())

        #stats
        self.ACC = self.csheet.findChild(QWidget, "ACCURATE")
        self.CUN = self.csheet.findChild(QWidget, "CUNNING")
        self.DIS = self.csheet.findChild(QWidget, "DISCREET")
        self.PER = self.csheet.findChild(QWidget, "PERSUASIVE")
        self.QUI = self.csheet.findChild(QWidget, "QUICK")
        self.RES = self.csheet.findChild(QWidget, "RESOLUTE")
        self.STR = self.csheet.findChild(QWidget, "STRONG")
        self.VIG = self.csheet.findChild(QWidget, "VIGILANT")

        #stat modifiers
        self.ACC_mod = self.csheet.findChild(QWidget, "ACCURATE_mod")
        self.CUN_mod = self.csheet.findChild(QWidget, "CUNNING_mod")
        self.DIS_mod = self.csheet.findChild(QWidget, "DISCREET_mod")
        self.PER_mod = self.csheet.findChild(QWidget, "PERSUASIVE_mod")
        self.QUI_mod = self.csheet.findChild(QWidget, "QUICK_mod")
        self.RES_mod = self.csheet.findChild(QWidget, "RESOLUTE_mod")
        self.STR_mod = self.csheet.findChild(QWidget, "STRONG_mod")
        self.VIG_mod = self.csheet.findChild(QWidget, "VIGILANT_mod")

        #all inventory slots
        self.inventory1 = self.invsheet.findChild(QLineEdit, "inventory1")
        self.inventory2 = self.invsheet.findChild(QLineEdit, "inventory2")
        self.inventory3 = self.invsheet.findChild(QLineEdit, "inventory3")
        self.inventory4 = self.invsheet.findChild(QLineEdit, "inventory4")
        self.inventory5 = self.invsheet.findChild(QLineEdit, "inventory5")
        self.inventory6 = self.invsheet.findChild(QLineEdit, "inventory6")
        self.inventory7 = self.invsheet.findChild(QLineEdit, "inventory7")
        self.inventory8 = self.invsheet.findChild(QLineEdit, "inventory8")
        self.inventory9 = self.invsheet.findChild(QLineEdit, "inventory9")
        self.inventory10 = self.invsheet.findChild(QLineEdit, "inventory10")
        self.inventory11 = self.invsheet.findChild(QLineEdit, "inventory11")
        self.inventory12 = self.invsheet.findChild(QLineEdit, "inventory12")
        self.inventory13 = self.invsheet.findChild(QLineEdit, "inventory13")
        self.inventory14 = self.invsheet.findChild(QLineEdit, "inventory14")
        self.inventory15 = self.invsheet.findChild(QLineEdit, "inventory15")