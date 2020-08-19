import   vlc

class player:
    # Here will be the instance stored.
    __instance = None
    mediaPlayer = None
    nowPlaying = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if player.__instance == None:
            player()

        return player.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if player.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.mediaPlayer = vlc.MediaPlayer("wonderland.mp3")
            player.__instance = self

    def setFile(self, file):
        if self.mediaPlayer != None:
            if self.mediaPlayer.is_playing():
                self.mediaPlayer.stop()
        self.mediaPlayer = vlc.MediaPlayer(file)
        self.mediaPlayer.play()

    def isPlaying(self):
        if self.mediaPlayer.is_playing():
            return True
        else:
            return False

    def getPosition(self):
        if self.mediaPlayer.is_playing():
            #print(self.mediaPlayer.get_position())
            #print(self.mediaPlayer.get_length())
            return self.mediaPlayer.get_position()*self.mediaPlayer.get_length()
        else:
            return 0
        vlc.mediaPlayer.pause()

    def setPosition(self, value):
        if self.mediaPlayer.is_playing():
            #self.mediaPlayer.pause()
            print(value)
            self.mediaPlayer.set_position(value/self.mediaPlayer.get_length())
            #self.mediaPlayer.play()

    def playPause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def stop(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.stop()

    def stopAt(self, time):
        while True:
            if time < self.mediaPlayer.get_position()*self.mediaPlayer.get_length():
                self.mediaPlayer.pause()
                break