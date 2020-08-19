from os import *
import os
import taglib
import fnmatch

for x in listdir('./'):
    if fnmatch.fnmatch(x, '*.wav') or fnmatch.fnmatch(x, '*.flac') or fnmatch.fnmatch(x, '*.mp3') or fnmatch.fnmatch(x, '*.FLAC') or fnmatch.fnmatch(x, '*.MP3'):
        tmp = taglib.File(x)
        title = tmp.tags["TITLE"][0].replace(' ', '_').replace(',', '') + "_" + x
        os.rename(x, title)