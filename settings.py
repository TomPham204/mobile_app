from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore


class Settings(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__()
        self.sm = sm
        self.name = kwargs["name"]

    def back_to_menu(self):
        self.sm.current = "menu"

    def check_sound(self):
        if JsonStore("data/sound.json").get("soundState")["activeOrNot"] == "True":
            return True
        else:
            return False

    def change_sound(self, active):
        if active == True:
            JsonStore("data/sound.json").put("soundState", activeOrNot="True")
        else:
            JsonStore("data/sound.json").put("soundState", activeOrNot="False")

    def check_vibrate(self):
        if JsonStore("data/vibrate.json").get("vibrateState")["activeOrNot"] == "True":
            return True
        else:
            return False

    def change_vibrate(self, active):
        if active == True:
            JsonStore("data/vibrate.json").put("vibrateState", activeOrNot="True")
        else:
            JsonStore("data/vibrate.json").put("vibrateState", activeOrNot="False")
