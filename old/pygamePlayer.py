import  time, pygame

class player:
    # Here will be the instance stored.
    __instance = None
    mediaPlayer = None
    nowPlaying = None
    paused = False

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
            player.__instance = self

            pygame.init()
            print("player initialization")

    def setFile(self, file):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print('i was busy')
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        self.paused = False
        #self.nowPlaying = file[1]

    def isPlaying(self):
        if pygame.mixer.music.get_busy():
            return True
        else:
            return False

    def getPosition(self):
        if pygame.mixer.music.get_busy():
            return pygame.mixer.music.get_pos()
        else:
            return 0

    def setPosition(self, value):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_pos(value)

    def playPause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()