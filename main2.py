from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        root = BoxLayout(orientation='horizontal', pos=(200, 100))
        left=ScrollView(size_hint=[None, None], size=(194, 334))
        leftGrid = GridLayout(cols=1, size_hint_y=None,padding=20)
        leftGrid.bind(minimum_height=leftGrid.setter('height'))
        for x in range (34):
            image = Image(
                source='other_nick.gif', pos=(0, 0),height=30,size_hint_y=None,)
            label = Label(
                text='hello w. ' + str(x), pos=(-15, 20), height=30,size_hint_y=None,)
            box = BoxLayout(orientation="horizontal", height=40, size_hint_y=None)
            box.add_widget(label)
            box.add_widget(image)

            leftGrid.add_widget(box)

        left.add_widget(leftGrid)
        root.add_widget(left)

        return root

TestApp().run()