import fnmatch
import locale
import sys
from os import listdir, path

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog

from MainWindow import Ui_MainWindow

import vlc
import taglib
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btn_stop.clicked.connect(self.on_click)
        self.btn_open.clicked.connect(self.on_open_click)
        self.btn_play.clicked.connect(self.on_play_click)
        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_test_point.clicked.connect(self.on_btn_test_click)
        self.btn_add_stop_point.clicked.connect(self.on_add_stop_clicked)
        self.btn_remove_stop_point.clicked.connect(self.on_btn_remove_time_clicked)
        self.btn_add_text.clicked.connect(self.on_btn_add_text_clicked)
        self.btn_remove_text.clicked.connect(self.on_btn_remove_text_clicked)

        self.files = []
        self.files_path = {}
        self.model = QStandardItemModel(self.lv_files)
        self.lv_files.setModel(self.model)
        self.lv_files.selectionModel().selectionChanged.connect(self.on_item_changed)
        self.mediaplayer = vlc.MediaPlayer("silent.mp3")
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()

        self.file = ""
        self.timeStop = 99999

        self.model_time_stop = QStandardItemModel(self.lv_stops)
        self.lv_stops.setModel(self.model_time_stop)
        self.lv_stops.selectionModel().selectionChanged.connect(self.on_item_stops_changed)

        self.model_time_text = QStandardItemModel(self.lv_text)
        self.lv_text.setModel(self.model_time_text)
        self.lv_text.selectionModel().selectionChanged.connect(self.on_item_text_changed)

        self.time_stops = []
        self.time_text = []
        self.texts = {}
        print(locale.getlocale())

        # self.lv_files.clicked[QtCore.QModelIndex].connect(self.on_item_changed)

    @pyqtSlot()
    def on_item_changed(self):
        for ix in self.lv_files.selectedIndexes():
            self.mediaplayer.stop()
            self.mediaplayer = vlc.MediaPlayer(self.files_path[self.files[ix.row()]])
            self.slider_time.setMaximum(10000)
            self.mediaplayer.play()
            self.model_time_text.clear()
            self.model_time_stop.clear()
            self.time_stops = []
            self.time_text = []
            self.texts = {}
            self.readFile(self.files_path[self.files[ix.row()]])
            self.timer.start()


    @pyqtSlot()
    def on_item_text_changed(self):
        for ix in self.lv_text.selectedIndexes():
            print(ix.row())
            print(ix.data())
            self.text_text_text.setText(self.texts[ix.data()])
            self.text_time_text.setText(ix.data())

    @pyqtSlot()
    def on_btn_add_text_clicked(self):
        time = float(self.text_time_text.toPlainText())
        text = self.text_text_text.toPlainText()
        self.texts[str(time)] = text
        self.time_text.append(time)
        self.time_text.sort()
        self.reloadTexts()

    @pyqtSlot()
    def on_btn_remove_text_clicked(self):
        time = float(self.text_time_text.toPlainText())
        del self.texts[str(time)]
        self.time_text.remove(time)
        self.reloadTexts()

    def reloadTexts(self):
        self.model_time_text.clear()
        self.time_text.sort()
        for x in self.time_text:
            self.model_time_text.appendRow(QStandardItem(str(x)))

    @pyqtSlot()
    def on_item_stops_changed(self):
        try:
            for ix in self.lv_stops.selectedIndexes():
                self.text_stop_time.setText(str(self.time_stops[ix.row()]))
        except:
            None

    @pyqtSlot()
    def on_btn_remove_time_clicked(self):
        for ix in self.lv_stops.selectedIndexes():
            self.time_stops.remove(float(ix.data()))
        self.reloadTimeStop()

    def reloadTimeStop(self):
        self.model_time_stop.clear()
        self.time_stops.sort()
        for x in self.time_stops:
            self.model_time_stop.appendRow(QStandardItem(str(x)))

    @pyqtSlot()
    def on_add_stop_clicked(self):
        x = float(self.text_stop_time.toPlainText())
        self.time_stops.append(x)
        self.reloadTimeStop()


    @pyqtSlot()
    def on_btn_test_click(self):
        #try:
            self.timeStop = float(self.text_stop_time.toPlainText())
            self.mediaplayer.pause()
            self.mediaplayer.set_position(((float(self.text_stop_time.toPlainText()) - 5)*1000)/float(self.mediaplayer.get_length()))
            self.mediaplayer.play()
            self.timer.stop()
            self.timer.start()
        #except:
           # print("here btn test click")

    def update_ui(self):
        # print("update ui")
        # print(not not self.mediaplayer.is_playing())
        # print(self.mediaplayer.get_position())
        if (self.mediaplayer.is_playing()):
            try:
                self.slider_time.setSliderPosition(int(self.mediaplayer.get_position() * 10000))
                m, s = divmod(int(self.mediaplayer.get_position() * self.mediaplayer.get_length() / 1000), 60)
                self.label_time.setText("%02d:%02d" % (m, s))
            except:
                print("here 1")

            #print(self.mediaplayer.get_position()*self.mediaplayer.get_lengrth())

            try:
                if (self.mediaplayer.get_position()*self.mediaplayer.get_length()/1000 > self.timeStop) & (self.timeStop > 0):
                    self.mediaplayer.pause()
                    self.timer.stop()
                    self.timeStop = 0
            except:
                None
                #print("Error")


    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    @pyqtSlot()
    def on_play_click(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.btn_play.setText("play")
            self.text_stop_time.setText(
                str(int(self.mediaplayer.get_position() * self.mediaplayer.get_length() / 100) / 10))
            self.text_time_text.setText(
                str(int(self.mediaplayer.get_position() * self.mediaplayer.get_length() / 100) / 10))
            self.timer.stop()
        elif not self.mediaplayer.is_playing():
            self.mediaplayer.play()
            self.btn_play.setText("pause")
            self.timer.start()

    @pyqtSlot()
    def on_open_click(self):
        print('create new file list')
        self.model.clear()
        self.files_path.clear()

        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.importAudioFiles(file)
        self.files.sort()
        for x in self.files:
            self.model.appendRow(QStandardItem(x))

    @pyqtSlot()
    def on_save_click(self):
        print("saving")
        self.mediaplayer.stop()
        self.mediaplayer.stop()
        self.timer.stop()
        self.saveFile()
        print("saved")

    def importAudioFiles(self, Patch):
        try:
            for x in listdir(Patch):
                if not (path.isfile(Patch + "/" + x)):
                    self.importAudioFiles(Patch + "/" + x)
                if Patch.__contains__("lost+found"):
                    print("do nothing")
                elif fnmatch.fnmatch(x, '*.wav') or fnmatch.fnmatch(x, '*.WAV') or fnmatch.fnmatch(x,
                                                                                                   '*.flac') or fnmatch.fnmatch(
                        x, '*.mp3') or fnmatch.fnmatch(x, '*.FLAC') or fnmatch.fnmatch(x, '*.MP3') or fnmatch.fnmatch(x,
                                                                                                                      '*.MP4') or fnmatch.fnmatch(
                        x, '*.mp4') or fnmatch.fnmatch(x, '*.AVI') or fnmatch.fnmatch(x, '*.avi') or fnmatch.fnmatch(x,
                                                                                                                     '*.mpeg') or fnmatch.fnmatch(
                        x, '*.MPEG') or fnmatch.fnmatch(x, '*.flv') or fnmatch.fnmatch(x, '*.FLV'):
                    self.files_path[x] = Patch + "/" + x
                    self.files.append(x)
                    self.file = x

        except:
            print("permission error on " + Patch)

    def readFile(self, path):
        x = taglib.File(path)
        print(x.tags)
        try:
            self.text_album.setText(x.tags["ALBUM"][0])
        except:
            None
        try:
            self.text_title.setText(x.tags["TITLE"][0])
        except:
            None
        try:
            self.unpackJson(self.Decrypt(x.tags["COMMENT"][0]))
        except:
            None
        self.file = path

    def saveFile(self):
        try:
            x = taglib.File(self.file)
            try:
                x.tags["ALBUM"] = self.text_album.toPlainText()
            except:
                x.tags["ALBUM"] = []
                x.tags["ALBUM"].append(self.text_album.toPlainText())

            try:
                x.tags["TITLE"] = self.text_title.toPlainText()
            except:
                x.tags["TITLE"] = []
                x.tags["TITLE"].append(self.text_title.toPlainText())

            try:
                x.tags["COMMENT"] = self.packJson()
            except:
                x.tags["COMMENT"] = []
                x.tags["COMMENT"].append(self.packJson())
            print(self.packJson())
            x.save()
        except:
            print("cannot read file")

    def unpackJson(self, text):
        data = json.loads(text)
        try:
            self.time_stops = data["STOPS"]
        except:
            self.time_stops = []

        try:
            self.texts = {}
            self.time_text = []
            tmp = data["TEXT"]
            for x in tmp:
                self.time_text.append(float(x["time"]))
                self.texts[x["time"]] = str(x["text"])
        except:
            self.texts = {}
            self.time_text = []

        self.reloadTimeStop()
        self.reloadTexts()
        try:
            self.text_number.setText(str(data["number"]))
        except:
            self.text_number.setText("0")
        print(data["STOPS"])
        print(self.texts)
        print(self.time_text)

    def packJson(self):
        dickt = {}
        #dickt["TEXT"] = self.texts
        dickt["TEXT"] = []
        for x in self.texts:
            tmp = {}
            tmp["text"] = self.texts[x]
            tmp["time"] = x
            dickt["TEXT"].append(tmp)


        dickt["STOPS"] = self.time_stops
        try:
            dickt["number"] = int(self.text_number.toPlainText())
        except:
            dickt["number"] = 0
        return json.dumps(dickt).encode('utf-8')

    def Decrypt(self, tagValue):
        return tagValue

    def Encrypt(self, stringValue):
        return stringValue


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
