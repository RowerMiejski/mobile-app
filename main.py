from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import RabbitMQ as rb
from time import sleep


message = "jebanko"
server = rb.Server()
server.Connect()
server.MakeQueue("hahaKACPERKNUT")
#server.Write(message, "telefon1")
#server.ReadConfig("telefon1", True)
#misiak = server.Read()
#print(message)
#print(misiak)
#server.Delete()
#print(server.Read())


class MyGui(FloatLayout):
    console = ObjectProperty(None)
    id = ObjectProperty(None)
    debug = ObjectProperty
    id1 = "ID :"
    debug1 = "Podaj ID maszyny"
    command = ""
    queue = ""

    def on_enter(self):
        self.debug.text = self.debug.text + "\n" + self.console.text
        self.command = str(self.console.text)
        self.interpretCommand()
        self.console.text = ""


    def interpretCommand(self):
        words = self.command.split()
        if str(words[0].lower()) == "connect":
            self.changeQueue(words[1])

    def changeQueue(self, args):
        queue = str(args)
        print(queue)
        server.Write("kacper knuciarz jebany", queue)


class MyApp(App):
    def build(self):
        return MyGui()



if __name__ == "__main__":
    MyApp().run()
