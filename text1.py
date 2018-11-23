import webvtt
import audiosegment as AudioSegment
import wave
import pyaudio
import numpy 
import scipy
import os
import csv
import os
import collections
import re
from os import listdir
from os.path import isfile, join
from num2words import num2words
import re
import csv
import unicodedata


outputdir = "../youtubedownloadscripts/speech_data/train_demo"
vtt_files = []
count=0
current_occurance =""
wav_filename =""
wav_fileDir = '../youtubedownloadscripts/speech_data/wav_demo'
rootDir = '../youtubedownloadscripts/speech_data/vtt_demo'

fileList = [f for f in listdir(rootDir) if isfile(join(rootDir, f))]
for fname in fileList:
    if ".en.vtt" in fname:
        wav_file_name = fname.replace('.en.vtt','.wav')
        wav_file = wav_fileDir+'/'+wav_file_name
        vtt_file = rootDir+'/'+fname
        count =count + 1
        
        for i, caption in enumerate(webvtt.read(vtt_file)):
            transcript = ""
            wav_transcript =""
            time1 = caption.start
            time2 = caption.end
            k=time1.split(':')
            time1_secs = (float(k[0])*3600)+(float(k[1])*60)+float(k[2])
            l=time2.split(':')
            time2_secs = (float(l[0])*3600)+(float(l[1])*60)+float(l[2])
            split_duration = (time2_secs-time1_secs)
                                
            if split_duration > 0.1000:
                save_file_name = "splited1demo_audio"+str(count)
                myaudio = AudioSegment.from_file(wav_file)
                print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                print("# audio_cutter_starting_time: {}".format(time1_secs * 1000))
                print("# audio_cutter_ending_time  : {}".format((time1_secs+split_duration)* 1000))
                chunk_data = myaudio[time1_secs * 1000:(time1_secs+split_duration)* 1000]
                print(chunk_data) 
                chunk_name = save_file_name+"_{}.wav".format(i/2)
                parts = chunk_name.split('_')  
                a = parts[-1].split('.')
                b = a[0]
                if(len(b) == 1):
                    b = "0"+b
                chunk_name = parts[0]+"_"+parts[1]+"_"+b+".wav"
                print("# exporting_wavfile_location:", chunk_name)
                print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                chunk_data.export(outputdir+"/"+chunk_name, format="wav")   
                wav_filename =outputdir+"/"+chunk_name
                wav_filesize =os.path.getsize(wav_filename)
                    
            else:
                print("less than 1 seconds")
                transcript =caption.text
                
                pos_val_rupees = []
                pos_val_dollars = []
                pos_val_percentage = []
                pos_val_and = []
                pos_val_plus = []
                data1 =[]
                data2 =[]
                data3 =[]
                data4 =[]
                data5 =[]

                str_dollar='dollars'
                str_rupees='rupees'
                str_percentage='percentage'
                str_and ='and'
                str_plus='plus'

                trans = transcript.replace('$', r' $ ').replace('%', r' % ').replace('₹',r' ₹ ').replace('+', r' + ').replace('&', r' & ')
                words = trans.split()
                for i,word in enumerate(words):
                    if word == "₹":
                        pos_val_rupees.append(i)
                        data1.append(str_rupees)
                    if word == "$":
                        pos_val_dollars.append(i)
                        data2.append(str_dollar)
                    if word == "%":
                        pos_val_percentage.append(i)
                        data3.append(str_percentage)
                    if word == "&":
                        pos_val_and.append(i)
                        data4.append(str_and)
                    if word == "+":
                        pos_val_plus.append(i)
                        data5.append(str_plus)

                for d,inc in zip(data1,pos_val_rupees):
                    words[inc]= words[inc+1]
                    words[inc+1] = d

                for d,inc in zip(data2,pos_val_dollars):
                    words[inc]= words[inc+1]
                    words[inc+1] = d

                for d,inc in zip(data3,pos_val_percentage):
                    words[inc]= d

                for d,inc in zip(data4,pos_val_and):
                    words[inc]= d

                for d,inc in zip(data5,pos_val_plus):
                    words[inc]= d

                transcript_pure=''
                for abc in words:
                    transcript_pure += abc + " "

                print(transcript_pure)
                
                if re.findall(r'-?\d+\.?\d*', transcript_pure):
                    answer1={}
                    count =0
                    new_word = transcript_pure.split(" ")
                    index = 0 
                    values = []
                    for inf in new_word:                       
                        if re.findall(r'-?\d+\.?\d*', inf):
                            values.append(index)
                        index += 1
                    for i,s in enumerate(re.findall(r'-?\d+\.?\d*', transcript_pure)):
                        a = float(s)
                        word = str(a).split(".")
                        number_dec = int(word[1])
                        if number_dec > 0.0:
                            answer1[i] = a
                        else:
                            answer1[i] = int(a)
                    new_transcript = ""
                    for value,inc in zip(answer1,values):
                        new_word[inc]= num2words(answer1[value])

                    for abc in new_word:
                        new_transcript += abc + " "

                    remove_specialchar = new_transcript.translate ({ord(c): " " for c in "!@#^*()[]{;}:,./<>?\|`~-_"})
                    remove_nonascii = unicodedata.normalize('NFKD', u'{}'.format(remove_specialchar)).encode('ASCII', 'ignore')
                    wav_transcript = remove_nonascii.lower()
                    fieldnames = [wav_filename, wav_filesize, wav_transcript]
                    with open('speech_data/train_demo1.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(fieldnames)
                
                else:
                    remove_specialchar = transcript_pure.translate ({ord(c): " " for c in "!@#^*()[]{;}:,./<>?\|`~-_"})
                    remove_nonascii = unicodedata.normalize('NFKD',  u'{}'.format(remove_specialchar)).encode('ASCII', 'ignore')
                    wav_transcript = remove_nonascii.lower()
                    fieldnames = [wav_filename, wav_filesize, wav_transcript]
                    with open('speech_data/train_demo1.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(fieldnames)

            print("##############################################################################")
            print("#  time1         : {}                       ".format(time1))
            print("#  time2         : {}                       ".format(time2))
            print("#  time1_secs    : {}                       ".format(time1_secs))
            print("#  time2_secs    : {}                       ".format(time2_secs))
            print("#  split_duration: {}                       ".format(split_duration))
            print("#  wav_filename  : {}                       ".format(wav_filename))
            print("#  wav_filesize  : {}                       ".format(wav_filesize))
            print("#  transcript    : {}                       ".format(wav_transcript))
            print("##############################################################################")
            

            

