# youtube-audio-and-transcript-extract
split audio_segmentation with corresponding transcript for youtube datasets 


# how can i handle youtube dataset with the indian accent. then segmented with a correct transcript?

first downloading .mp3 playlist for youbute indian speakers with .vtt subtitle file.

.vtt file format like starting-ending timing with the audio transcript.
i was segmenting that youtube audiofile with Start-End time.

and i applied some preprocessing like data cleaning, wav file format 16bit 16khz mono, and then use it deepspeech training.

# step 1: create youtube speakers playlist text file.

youtube_news.txt

# step 2: downloading .mp3 playlist for youbute indian speakers with .vtt subtitle file

python3 youtube_download.py

# step 3: segmenting that youtube audiofile with Start-End time

python3 text1.py



