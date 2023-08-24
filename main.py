from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, WipeTransition

from menu import Menu
from settings import Settings
from pressButton import PressButton

sm = ScreenManager(transition=WipeTransition())
menuComponent = Menu(name="menu", sm=sm)
sm.add_widget(menuComponent)
sm.add_widget(PressButton(name="game", sm=sm, menu=menuComponent))
sm.add_widget(Settings(name="settings", sm=sm))


class PressButtonApp(App):
    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        return sm


if __name__ == "__main__":
    PressButtonApp().run()
