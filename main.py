from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


class MyGui(FloatLayout):
    console = ObjectProperty(None)
    id = ObjectProperty(None)
    debug = ObjectProperty
    id1 = "ID :"
    debug1 = "Podaj ID maszyny"

    def on_enter(self):
        self.debug.text = self.debug.text + "\n" + self.console.text

        self.console.text = ""


class MyApp(App):
    def build(self):
        return MyGui()


if __name__ == "__main__":
    MyApp().run()
