from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import RabbitMQ as rb
import threading

message = "jebanko"
server = rb.Server()
server.Connect()
serverID = rb.Server()
server.ReadConfig("serwer", True)


class MyGui(FloatLayout):
    console = ObjectProperty(None)
    idBox = ObjectProperty()
    debug = ObjectProperty()
    id1 = "ID :"
    debug1 = "Podaj swoje imie"
    command = ""
    queue = ""
    isInQueue = False
    whileCommand = False
    isNeeded = False

    def __init__(self, **kwargs):
        super(MyGui, self).__init__(**kwargs)
        t1 = threading.Thread(target=self.idUpdate)
        t1.start()

    def on_enter(self):
        self.debug.text = self.debug.text + "\n" + self.console.text
        self.command = str(self.console.text)
        self.interpretCommand()
        self.console.text = ""

    def interpretCommand(self):
        self.words = self.command.split()
        self.whileCommand = True
        if len(self.words) > 1 and str(self.words[0].lower()) == "connect":
            self.changeQueue(self.words[1])
        elif len(self.words) > 1 and str(self.words[0].lower()) == "giveid":
            self.giveID(self.words[1])
        elif str(self.words[0].lower()) == "cls":
            self.debug.text = ""
        elif str(self.words[0].lower()) == "send" and len(self.words) > 1:
            if self.isInQueue:
                if len(self.words) > 2:
                    print(len(self.words))
                    self.sendCommand(self.words[1].lower(), self.words[2])
                else:
                    self.sendCommand(self.words[1].lower(), "")

            else:
                self.debug.text += " - BLAD, nie wybrales kolejki.\n"
        else:
            self.debugUpdate(True)

    def changeQueue(self, args):
        self.queue = str(args)
        self.idBox.text = ""
        self.idBox.text = "ID: " + self.queue
        self.debugUpdate(False)
        self.isInQueue = True

    def debugUpdate(self, didFail):
        if didFail:
            self.debug.text += "- komenda zakonczona niepowodzeniem.\n"
        else:
            self.debug.text += "- komenda zakonczona powodzeniem.\n"

    def idUpdate(self):
        serverID.ReadConfig("serwer", True)
        server.ReadConfig("kuba", True)

        if str(serverID.Read()) == "needID":
            self.isNeeded = True
            self.debug.text += " \nURZADZENIE PROSI O ID, WPISZ KOMENDE giveid + ID"
            self.idUpdate()
        elif str(server.Read()) != "":
            formattedOutput = []
            formattedOutput = str(server.Read()).split()
            print(formattedOutput)
            self.debug.text += str(formattedOutput)
            self.idUpdate()

    def giveID(self, ID):
        if self.isNeeded:
            serverID.Write(ID, "serwer_response")
            self.debugUpdate(False)
            self.isNeeded = False
        else:
            self.debug.text += " - Nie otrzymano komendy needID"
            self.isNeeded = False

    def sendCommand(self, command, args):
        if len(self.words) > 1:
            server.Write("kuba" + " " + command + " " + args, self.queue)
        else:
            server.Write("kuba" + " " + command, self.queue)
        self.debugUpdate(False)


class MyApp(App):
    def build(self):
        return MyGui()


def start():
    if __name__ == "__main__":
        MyApp().run()


t2 = threading.Thread(target=start)
t2.start()
