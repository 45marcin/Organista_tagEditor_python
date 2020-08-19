from os import *
import os
import taglib
import fnmatch

for x in listdir('./'):
    if fnmatch.fnmatch(x, '*.wav'):
        x = x[0:len(x)-4]
        print(x)
        tmp = taglib.File(x+".wav")
        title = str(tmp.tags["TITLE"][0])
        album = str(tmp.tags["ALBUM"][0])
        try:
            comment = str(tmp.tags["LYRICS"][0])
        except:
            comment = ""
        tmp = taglib.File(x+".flac")
        tmp.tags["TITLE"] = [title]
        tmp.tags["ALBUM"] = [album]
        tmp.tags["TRACKNUMBER"] = ["0"]
        tmp.tags["LYRICS"] = [comment]
        tmp.save()