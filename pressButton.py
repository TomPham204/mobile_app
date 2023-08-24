from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from kivy.uix.modalview import ModalView
from kivy.utils import platform
from random import randint

from plyer import vibrator

store = JsonStore("data/data.json")
score = 0
countdown = 0
popup = Popup()

blue = [173 / 128.0, 196 / 128.0, 206 / 128.0, 1]
beige = [249 / 128.0, 225 / 128.0, 209 / 128.0, 1]
orange = [254 / 128.0, 189 / 128.0, 189 / 128.0, 1]
yellow = [251 / 128.0, 241 / 128.0, 213 / 128.0, 1]
purple = [225 / 128.0, 216 / 128.0, 242 / 128.0, 1]
teal = [201 / 128.0, 228 / 128.0, 222 / 128.0, 1]
red = [255 / 128.0, 223 / 128.0, 181 / 128.0, 1]
pink = [245 / 128.0, 209 / 128.0, 229 / 128.0, 1]
lemon = [244 / 128.0, 249 / 128.0, 197 / 128.0, 1]

randomList = [blue, beige, red, yellow, purple, teal, orange, pink, lemon]

currentColorList = [blue, beige, red, yellow, purple]

currentActiveColor = 1
timeMax = 999

timePopup = Popup()
sound = SoundLoader.load("snd/click.wav")
Builder.load_file("UI.kv")


class PressButton(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__()
        self.finalScore = ""
        self.sm = sm
        self.Menu = kwargs["menu"]
        self.name = kwargs["name"]

    def buttons_disabled(self):
        self.ids.button1.disabled = True
        self.ids.button2.disabled = True
        self.ids.button3.disabled = True
        self.ids.button4.disabled = True
        self.ids.button5.disabled = True
        self.ids.button6.disabled = True
        self.ids.button7.disabled = True
        self.ids.button8.disabled = True
        self.ids.button9.disabled = True

    def buttons_enabled(self):
        self.ids.button1.disabled = False
        self.ids.button2.disabled = False
        self.ids.button3.disabled = False
        self.ids.button4.disabled = False
        self.ids.button5.disabled = False
        self.ids.button6.disabled = False
        self.ids.button7.disabled = False
        self.ids.button8.disabled = False
        self.ids.button9.disabled = False

    def check_if_all_clicked(self):
        global currentActiveColor
        return currentActiveColor > len(currentColorList)

    def change_color_list(self):
        global currentActiveColor

        for i in range(0, 5):
            index = randint(0, len(randomList) - 1)
            currentColorList[i] = randomList[index]
            self.ids[f"colorList{i+1}"].background_color = randomList[index]

        currentActiveColor = 1

    def change_text(self):
        existed = []
        for i in range(1, 10):
            temp = 0
            while temp in existed:
                temp = randint(0, 8)
            self.ids[f"button{i}"].background_color = randomList[temp]
            existed.append(temp)

    def start_add_score(self, button):
        self.add_score(button)

    def call_vibrate(self):
        if JsonStore("data/vibrate.json").get("vibrateState")["activeOrNot"] == "True":
            if platform == "android":
                vibrator.vibrate(0.06)
            else:
                print("No vibrator")
        else:
            pass

    def add_score(self, button):
        global score
        global sound

        if (
            self.ids[f"button{button}"].background_color
            == currentColorList[currentActiveColor - 1]
        ):
            self.add_score_number()
            self.animate_after_touch()
            self.play_sound()
        else:
            self.minus_score_number()
            self.call_vibrate()

        self.ids.scoreLabel.text = "Score: " + str(score)

        if self.check_if_all_clicked() == True:
            self.change_text()
            self.change_color_list()
        pass

    def animate_after_touch(self):
        Clock.schedule_once(self.un_animate_after_touch, 0.1)

    def un_animate_after_touch(self, dt):
        self.ids.buttonsGrid.spacing = [3, 3]

    def play_sound(self):
        global sound

        if JsonStore("data/sound.json").get("soundState")["activeOrNot"] == "True":
            sound.play()
        else:
            pass

    def add_score_number(self):
        global score
        global currentActiveColor
        score = score + 1
        currentActiveColor = currentActiveColor + 1

    def minus_score_number(self):
        global score
        score = max(0, score - 1)

    def timer(self, dt):
        global countdown
        global timePopup

        countdown = countdown - 1
        self.ids.timeLabel.text = "Time left: " + str(countdown)

        if countdown <= 0:
            Clock.unschedule(self.timer)
            timePopup = ModalView(auto_dismiss=False, background_color=[1, 0, 0, 0.7])
            timePopup.add_widget(
                Label(text="Time's up", font_size="50sp", color=[1, 1, 1, 1])
            )
            timePopup.open()
            Clock.schedule_once(self.change_to_end, 1.5)

    def start(self):
        global countdown
        self.sm.current = "game"

        self.ids.startButton.disabled = True
        self.buttons_enabled()
        self.change_color_list()
        self.change_text()

        countdown = timeMax
        Clock.schedule_interval(self.timer, 1)

    def reset(self):
        global score
        global timeMax

        timeMax = 8
        score = 0
        self.ids.scoreLabel.text = "Score: " + str(score)
        self.ids.timeLabel.text = f"Time: {timeMax}"
        self.ids.startButton.disabled = False
        self.buttons_disabled()

    def change_to_end(self, dt):
        global score
        global popup
        global timePopup

        timePopup.dismiss()
        self.finalScore = str(score)

        if JsonStore("data/data.json").get("userData")["highScore"] < score:
            JsonStore("data/data.json").put("userData", highScore=score)

        popup_content = BoxLayout(orientation="vertical", spacing=3)
        play_again_button = Button(
            text="Play Again",
            on_release=self.play_again,
            font_size="35sp",
            background_color=[0, 1, 0, 0],
        )
        back_to_menu_button = Button(
            text="Back To Menu",
            on_release=self.change_to_menu,
            font_size="35sp",
            background_color=[0, 1, 0, 0],
        )
        final_score_label = Label(
            text="Score: " + self.finalScore, font_size="50sp", color=[1, 1, 1, 1]
        )
        high_score_label = Label(
            text="High Score: "
            + str(
                JsonStore("data/data.json").get(
                    "userData",
                )["highScore"]
            ),
            font_size="50sp",
            color=[1, 1, 1, 1],
        )

        popup_content.add_widget(final_score_label)
        popup_content.add_widget(high_score_label)
        popup_content.add_widget(play_again_button)
        popup_content.add_widget(back_to_menu_button)

        popup = ModalView(auto_dismiss=False, background_color=[1, 0, 0, 0.7])
        popup.add_widget(popup_content)
        popup.open()

        self.reset()

    def change_to_menu(self, dt):
        global popup
        self.Menu.back_to_menu()
        popup.dismiss()

    def play_again(self, dt):
        global popup
        popup.dismiss()
