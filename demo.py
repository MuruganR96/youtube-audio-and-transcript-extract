import webvtt
import audiosegment as AudioSegment
import wave
import pyaudio
import numpy 
import scipy
import os
import csv
import re
from collections import Counter
count = Counter()
outputdir = "/home/dell/Music/myc_project/21-09-2018/youtubedownloadscripts/train_data/train"
        vtt_files = []
        global count
        rootDir = '/home/dell/Music/myc_project/21-09-2018/youtubedownloadscripts/speech_data/'
        for dirName, subdirList, fileList in os.walk(rootDir):
            print('Found directory: %s' % dirName)
            for fname in fileList:
                if ".en.vtt" in fname:
                    vtt_files.append(rootDir+'/'+fname)
                    for file in vtt_files:
                        count[file] = + 1
                        print(count)
