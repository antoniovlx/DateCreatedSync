import ffmpeg
import sys
from pprint import pprint # for printing Python dictionaries in a human-readable way
import magic 
import os

print (os.getcwd())
filename = './video.mp4'
  
# printing the human readable type of the file 
# print(magic.from_file(filename)) 
  
# printing the mime type of the file 
# print(magic.from_file(filename, mime = True))

# read the audio/video file from the command line arguments
# media_file = sys.argv[1]
# uses ffprobe command to extract all possible metadata from the media file
# pprint(ffmpeg.probe(filename)['format']['tags']['creation_time'])

def get_creation_time(f):
    pprint(ffmpeg.probe(f)['format']['tags']['creation_time'])
    return ffmpeg.probe(f)['format']['tags']['creation_time']
