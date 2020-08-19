import kivy
from kivy.uix.listview import ListItemButton

kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.slider import Slider
from kivy.uix.filechooser import abspath
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
import threading
import vlcPlayer
import taglib
import time
import pickle
import json
import threading
from kivy.uix.modalview import ModalView
#Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'fullscreen', '0')

#Builder.load_file('myapp.kv')

p = vlcPlayer.player.getInstance()
44.5


class tagEditor (GridLayout):
    title = StringProperty()
    artist = StringProperty()
    album = StringProperty()
    number = StringProperty()
    stopPoints = ListProperty([])
    stopValue = StringProperty()
    text = StringProperty()
    oneTimeTextValue = StringProperty()
    textTimesValues = ListProperty()
    slowa = {}

    def change(self, change):
        self.stopValue = str(change.text)
        if str(change.text) in self.slowa:
            self.text = self.slowa[str(change.text)]


    length = NumericProperty()
    position = NumericProperty()
    path = ""





    def doSomething(self):
        title = "something happend"

    def sliderLive(self):
        p = vlcPlayer.player.getInstance()
        while p.isPlaying:
            self.position = p.getPosition()
            time.sleep(0.1)


    def addText(self, text, time):
        self.textTimesValues.append(time)
        self.slowa[time] = text
        self.oneTimeTextValue = " "
        self.oneTimeTextValue = ""
        self.text = " "
        self.text = ""



    def select(self, file):
        try:
            if file:
                if ".wav" in file[0][len(file[0])-4:len(file[0])] or ".flac" in file[0][len(file[0])-5:len(file[0])] or ".mp3" in file[0][len(file[0])-4:len(file[0])] or ".ogg" in file[0][len(file[0])-4:len(file[0])] or ".FLAC" in file[0][len(file[0])-5:len(file[0])] or ".MP3" in file[0][len(file[0])-4:len(file[0])]:
                    self.title = ""
                    self.album = ""
                    self.artist = ""
                    self.number = ""
                    del self.stopPoints[:]
                    del self.textTimesValues[:]
                    p = vlcPlayer.player.getInstance()
                    p.setFile(file[0])
                    tmp = taglib.File(file[0])
                    print(tmp.tags)
                    try:
                        self.title = str(tmp.tags["TITLE"][0])
                    except:
                        None
                    try:
                        self.title = str(tmp.tags["TITLE"][0])
                    except:
                        None
                    try:
                        self.artist = str(tmp.tags["ARTIST"][0])
                    except:
                        None
                    try:
                        self.album = str(tmp.tags["ALBUM"][0])
                    except:
                        None
                    try:
                        self.length = int(tmp.length)*1000
                    except:
                        None

                    try:
                        self.slowa = json.loads(str(tmp.tags["COMMENT"][0]))
                        for i in self.slowa:
                            self.textTimesValues.append(i)
                    except:
                        self.slowa = {}

                    self.length = int(tmp.length)*1000
                    try:
                        self.number = str(tmp.tags["TRACKNUMBER"])[2:str(tmp.tags["TRACKNUMBER"])-2]
                    except: self.number = "no number"
                    try:
                        for x in str(tmp.tags["LYRICS"][0]).split():
                            self.stopPoints.append(x)
                    except:
                        None
                    try:
                        self.stopPoints.sort().sort()
                    except:
                        None
                    self.path = file[0]
                    t = threading.Thread(target=self.sliderLive)
                    t.start()
        except:
            None


    def sliderMoved(self, value, position):
        if 10 < int(position[0]) < 640:
            if 10 < int(position[1]) < 36:
                p = vlcPlayer.player.getInstance()
                p.setPosition(int(value))

    def remove(self, value):
        try:
            self.stopPoints.remove(value)
        except:
            None
        try:
            del self.slowa[value]
            self.textTimesValues.remove(value)
        except:
            None

    def playPause(self):
        p = vlcPlayer.player.getInstance()
        p.playPause()

    def stop(self):
        p = vlcPlayer.player.getInstance()
        p.stop()

    def save(self, title, artist, album, no):
        tmp = taglib.File(self.path)
        print(tmp.tags)
        tmp.tags["TITLE"] = [title]
        tmp.tags["ARTIST"] = [artist]
        tmp.tags["ALBUM"] = [album]
        tmp.tags["TRACKNUMBER"] = [no]
        tmp.tags["COMMENT"] = json.dumps(self.slowa)
        if len(self.stopPoints) > 0:
            tmp.tags["LYRICS"] = ''.join(str(x)+' ' for x in self.stopPoints)
        else:
            tmp.tags["LYRICS"] = ''
        tmp.save()

    def prrint(self, value):
        print(value)

    def testPoint(self, value):
        p = vlcPlayer.player.getInstance()
        if p.isPlaying():
            None
        else:
            p.playPause()
        time.sleep(0.1)
        try:
            p.setPosition(float(value)*1000-3000)
        except:
            None
        p.setPosition(float(value)*1000-3000)
        t = threading.Thread(target=p.stopAt, args={float(value)*1000})
        t.start()







class MyApp(App):
    def build(self):
        self.title = "SimpleTagEditor"
        return tagEditor()

MyApp().run()