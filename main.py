from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import RabbitMQ as rb
import threading
from kivy.lang.builder import Builder

presentation = Builder.load_string("""
<Label>:
    halign: "left"
    background_color: 0.1,0.5,0.6,1

<Widget>:
    canvas.after:
        Line:
            rectangle: self.x+1,self.y+1,self.width-1,self.height-1
            dash_offset: 5
            dash_length: 3

<FloatLayout>:
    console: console
    idBox: jebaniedisa
    debug:debug
    GridLayout:
        size_hint: 1,0.4
        pos_hint: {"x":0, "top":1}
        cols: 1
        rows:2

        Label:
            id: jebaniedisa
            font_size: 25
            text: root.id1
            size_hint: 1,0.05
            pos_hint: {"x":0, "top":1}
            text_size: self.size
            halign: 'left'


        TextInput:
            id: console
            do_scroll_x: False
            text: ""
            multiline: False
            size_hint: 1,0.35
            pos_hint: {"x":0, "y":0.5}
            text_size: self.size
            halign: 'left'
            foreground_color: (1, 1, 1, 1)
            background_color: 0,0,0,1
            on_text_validate: root.on_enter()
    GridLayout:
        rows:1
        cols:1
        size_hint: 1,0.6
        pos_hint: {"x":0, "y":0}
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            Label:
                id:debug
                size_hint_y: None
                halign: "left"
                text_size: root.width, None
                size: self.texture_size
                height: self.texture_size[1]
                text:
                    root.debug1"""
                                   , filename="my.kv")
server = rb.server()
serverID = rb.server()
serverData = rb.server()
serverSend = rb.server()

serverSend.Connect()
server.Connect()
serverData.Connect()
serverID.Connect()
serverID.ReadConfig("serwer", True)
serverData.ReadConfig("ids", True)
server.ReadConfig("kuba", True)


class MyGui(FloatLayout):
    console = ObjectProperty(None)
    idBox = ObjectProperty()
    debug = ObjectProperty()
    id1 = "ID :"
    debug1 = "Connect to your desired device"

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
        self.command = ""
        self.queue = ""
        self.isInQueue = False
        self.isNeeded = False
        self.words = []
        self.savedDir = ""
        self.lastCommand = "There was no last command"
        self.lastCommandBool = False

    def on_enter(self):
        self.debug.text = self.debug.text + "\n" + self.console.text
        self.command = ""
        self.command = str(self.console.text)
        self.interpretCommand()
        self.lastCommand = str(self.console.text)
        if not self.lastCommandBool:
            self.console.text = ""


    def interpretCommand(self):
        self.words = []
        self.words = self.command.split()
        self.words.append("")
        self.words.append("")
        self.words.append("")
        if len(self.words) > 1 and str(self.words[0].lower()) == "connect":
            self.changeQueue(self.words[1])
            print(self.savedDir)
        elif len(self.words) > 1 and str(self.words[0].lower()) == "giveid":
            self.giveID(self.words[1])
        elif str(self.words[0].lower()) == "cls":
            self.debug.text = ""
        elif str(self.words[0].lower()) == "s" and len(self.words) > 1:
            if self.isInQueue:
                if len(self.words) - 3 > 2:
                    if self.words[2].lower() == "saveddir":
                        self.sendCommand(self.words[1].lower(),
                                         self.savedDir + " " + self.words[3] + " " + self.words[4] + " " + self.words[5])
                    else:
                        self.sendCommand(self.words[1].lower(),
                                         self.words[2] + " " + self.words[3] + " " + self.words[4] + " " + self.words[5])
                else:
                    self.sendCommand(self.words[1].lower(), "")

            else:
                self.debug.text += " - ERROR, you haven't chosen your queue.\n"
        elif str(self.words[0].lower()) == "getids":
            self.getIds()
        elif str(self.words[0].lower()) == "help":
            self.help()
        elif str(self.words[0].lower()) == "savedir":
            self.savedDir = str(self.words[1])
        elif str(self.words[0].lower()) == "last":
            self.console.text = ""
            self.console.text = self.lastCommand
            self.lastCommandBool = True
            self.debugUpdate(False)
        else:
            self.debugUpdate(True)


    def changeQueue(self, args):
        self.queue = str(args)
        self.idBox.text = ""
        if self.queue in self.idList or self.queue == "all":
            self.idBox.text = "ID: " + self.queue
            self.debugUpdate(False)
        else:
            self.debug.text += " -ERROR, there is no such queue"
            self.idBox.text = "ID: "
        self.isInQueue = True

    def debugUpdate(self, didFail):
        if didFail:
            self.debug.text += "- command went up with error."
        else:
            self.debug.text += "- command succeed."

    def idUpdate(self):
        serverID.ReadConfig("serwer", True)
        msg = str(serverID.Read())
        print(msg)
        if msg == "needID":
            self.isNeeded = True
            self.debug.text += " \nNEW DEVICE NEEDS ID, USE COMMAND GIVEID + ID TO ASSIGN NEW ID"
            msg = ""
        self.rerunGetId()
        return True

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
            self.debug.text += " - ERROR, needID command wasn't sent"
            self.isNeeded = False

    def sendCommand(self, command, args):
        if self.queue == "all":
            for i in range (0, len(self.idList)-1):
                serverSend.Write("kuba" + " " + command + " " + args, str(self.idList[i]))
            self.debugUpdate(False)
            return True

        if len(self.words) > 1:
            serverSend.Write("kuba" + " " + command + " " + args, self.queue)
        else:
            serverSend.Write("kuba" + " " + command, self.queue)
        self.debugUpdate(False)

    def getInfoBack(self):
        server.ReadConfig("kuba", True)
        formattedOutput = str(server.Read()).replace("@", " ")
        formattedOutput.split()
        self.debug.text += "\n" + str(formattedOutput).replace(r'" "', '\n').replace(r'\n', '\n')

        self.rerunGetInfoBack()
        return True

    def getIds(self):
        self.debug.text += "\n" + str(self.idList)

    def help(self):
        self.debug.text += "\n" + "Available application commands: \nConnect, use: connect + computers ID\n" \
                                  "Giveid, use: giveid + new machine ID\nCls - purging debugger" \
                                  "\nSend, use: s + command + args\ngetids - returns available queues\n" \
                                  "Savedir - saves your directory provided in given argument. " \
                                  "can be used by calling f/e: send listdir saveddir"

    def rerunGetInfoBack(self):
        self.getInfoBack()

    def rerunGetId(self):
        self.idUpdate()


class MyApp(App):
    def build(self):
        return MyGui()


if __name__ == "__main__":
    MyApp().run()
