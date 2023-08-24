from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore


class Menu(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__()
        self.sm = sm
        self.name = kwargs["name"]

    high_score_menu_label_text = "High Score: " + str(
        JsonStore("data/data.json").get("userData")["highScore"]
    )

    def call_start(self):
        Clock.schedule_once(self.start_game, 0)

    def start_game(self, dt):
        self.sm.current = "game"
        Clock.schedule_interval(self.set_high_score, 1)

    def back_to_menu(self):
        self.sm.current = "menu"
        high_score_menu_label_text = "High Score: " + str(
            JsonStore("data/data.json").get("userData")["highScore"]
        )
        self.ids.highScoreMenuLabel.text = high_score_menu_label_text

    def set_high_score(self, dt):
        high_score_menu_label_text = "High Score: " + str(
            JsonStore("data/data.json").get("userData")["highScore"]
        )
        self.ids.highScoreMenuLabel.text = high_score_menu_label_text

    def change_to_settings(self):
        self.sm.current = "settings"
