from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import RabbitMQ as rb
import threading

server = rb.server()
serverID = rb.server()
serverData = rb.server()

server.Connect()
serverData.Connect()
serverID.Connect()
serverID.ReadConfig("serwer", True)
serverData.ReadConfig("ids", True)
server.ReadConfig("kacper", True)


class MyGui(FloatLayout):
    console = ObjectProperty(None)
    idBox = ObjectProperty()
    debug = ObjectProperty()
    id1 = "ID :"
    debug1 = "Podaj maszyne do ktorej chcesz sie podlaczyc"
    command = ""
    queue = ""
    isInQueue = False
    whileCommand = False
    isNeeded = False
    idString = ""
    idList = []

    def __init__(self, **kwargs):
        super(MyGui, self).__init__(**kwargs)
        t1 = threading.Thread(target=self.idUpdate)
        t1.start()
        t4 = threading.Thread(target=self.getInfoBack)
        t4.start()
        self.idString = str(serverData.Read())
        serverData.Write(self.idString, "ids")
        self.idList = self.idString.split()
        print(self.idList)

    def on_enter(self):
        self.debug.text = self.debug.text + "\n" + self.console.text
        self.command = str(self.console.text)
        self.interpretCommand()
        self.console.text = ""

    def interpretCommand(self):
        self.words = self.command.split()
        self.words.append("")
        self.words.append("")
        self.words.append("")
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
                    self.sendCommand(self.words[1].lower(),
                                     self.words[2] + " " + self.words[3] + " " + self.words[4] + " " + self.words[5])
                else:
                    self.sendCommand(self.words[1].lower(), "")

            else:
                self.debug.text += " - BLAD, nie wybrales kolejki.\n"
        elif str(self.words[0].lower()) == "getids":
            self.getIds()
        elif str(self.words[0].lower()) == "help":
            self.help()
        else:
            self.debugUpdate(True)

    def changeQueue(self, args):
        self.queue = str(args)
        self.idBox.text = ""
        if self.queue in self.idList:
            self.idBox.text = "ID: " + self.queue
            self.debugUpdate(False)
        else:
            self.debug.text += " -Blad, nie ma takiej kolejki"
            self.idBox.text = "ID: "
        self.isInQueue = True

    def debugUpdate(self, didFail):
        if didFail:
            self.debug.text += "- komenda zakonczona niepowodzeniem."
        else:
            self.debug.text += "- komenda zakonczona powodzeniem."

    def idUpdate(self):
        serverID.ReadConfig("serwer", True)
        msg = str(serverID.Read())
        print(msg)
        if msg == "needID":
            self.isNeeded = True
            self.debug.text += " \nURZADZENIE PROSI O ID, WPISZ KOMENDE giveid + ID"
            msg = ""
        self.idUpdate()

    def giveID(self, ID):
        global idString
        if self.isNeeded:
            serverID.Write(ID, "serwer_response")
            serverData.ReadConfig("ids", True)
            self.debugUpdate(False)
            self.isNeeded = False
            self.idString += " " + ID
            self.idList.append(ID)
            serverData.Read()
            serverData.Write(str(self.idString), "ids")
        else:
            self.debug.text += " - Nie otrzymano komendy needID"
            self.isNeeded = False

    def sendCommand(self, command, args):
        if len(self.words) > 1:
            server.Write("kacper" + " " + command + " " + args, self.queue)
        else:
            server.Write("kacper" + " " + command, self.queue)
        self.debugUpdate(False)

    def getInfoBack(self):
        server.ReadConfig("kacper", True)
        if str(server.Read()) != "":
            formattedOutput = []
            formattedOutput = str(server.Read()).replace("@", " ")
            formattedOutput.split()
            formattedOutput.replace("+", " ")
            self.debug.text += "\n" + str(formattedOutput)
            self.getInfoBack()

    def getIds(self):
        self.debug.text += "\n" + str(self.idList)

    def help(self):
        self.debug.text += "\n" + "Dostepne komendy aplikacji to: \nConnect, uzycie: connect + ID komputera\n" \
                                  "Giveid, uzycie: giveid + nowe id maszyny\nCls - czyszczenie debuggera" \
                                  "\nSend, uzycie: send + komenda + ew. arg\nids - zwraca aktywne kolejki"


class MyApp(App):
    def build(self):
        return MyGui()


def start():
    if __name__ == "__main__":
        MyApp().run()


t2 = threading.Thread(target=start)
t2.start()
