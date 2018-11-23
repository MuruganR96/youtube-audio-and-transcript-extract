import os
from multiprocessing import Pool
import math,time

command = r'youtube-dl -x --audio-format "wav" --write-auto-sub --prefer-ffmpeg --audio-quality 9 --sub-format "srt" "{}" --postprocessor-args "-ac 1 -ar 16000" -o {} '


data=[]
with open('youtube_news.txt','r') as fin:
	for line in fin:
		if len(line.split())>0:
 			data.append(line.strip('\n'))
			
        
def download_youtube(input):
	output = "/speech_data/youtube_news_old/'%(title)s-%(id)s.%(ext)s'"
	os.system(command.format(input,output))
	#print(command.format(input,output))


import pandas as pd
p = Pool(30)
dev = p.map(download_youtube, data)
p.close()
p.join()
