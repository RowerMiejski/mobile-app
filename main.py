from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import RabbitMQ as rb
/import threading


message = "jebanko"
server = rb.Server()
server.Connect()
serverID = rb.Server()
server.ReadConfig("serwer", True)


class MyGui(FloatLayout):
    console = ObjectProperty(None)
    id = ObjectProperty(None)
    debug = ObjectProperty
    id1 = "ID :"
    debug1 = "Podaj ID maszyny"
    command = ""
    queue = ""
    whileCommand = False

    def __init__(self, **kwargs):
        super(MyGui,self).__init__(**kwargs)
        t1 = threading.Thread(target=self.idUpdate)
        t1.start()

    def on_enter(self):
        self.debug.text = self.debug.text + "\n" + self.console.text
        self.command = str(self.console.text)
        self.interpretCommand()
        self.console.text = ""

    def interpretCommand(self):
        words = self.command.split()
        self.whileCommand = True
        if len(words)>1 and str(words[0].lower()) == "connect":
            self.changeQueue(words[1])
        elif len(words)>1 and str(words[0].lower()) == "giveid":
            self.giveID(words[1])
        elif str(words[0].lower()) == "!reset":
            self.giveID(words[1])
        else:
            self.debugUpdate(True)



    def changeQueue(self, args):
        queue = str(args)
        print(queue)
        server.Write("kacper knuciarz jebany", queue)
        self.debugUpdate(False)


    def debugUpdate(self, didFail):
        if didFail:
            self.debug.text += ", command failed."
        else:
            self.debug.text += ", command done succesfully."


    def idUpdate(self):
        serverID.ReadConfig("serwer", True)
        if str(serverID.Read()) == "needID":
            print("jebanko disa powieksa penisa")
            if not self.whileCommand:
                self.debug.text += "\n\n URZADZENIE PROSI O ID, WPISZ KOMENDE giveid + ID"
            else:
                self.debug.text += "\n\n URZADZENIE PROSI O ID, WPISZ KOMENDE !reset, aby zresetowac polaczenie a nastepnie giveid + ID"

    def giveID(self, ID):
        serverID.Write(ID, "serwer")


class MyApp(App):
    def build(self):
        return MyGui()


def start():
    if __name__ == "__main__":
        MyApp().run()

t2 = threading.Thread(target=start)
t2.start()
