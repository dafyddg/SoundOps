#!/usr/bin/python -u

import math
import pyaudio
import sys

PyAudio = pyaudio.PyAudio

# See http://en.wikipedia.org/wiki/Bit_rate#Audio

if len(sys.argv) == 2:
	freq = int(sys.argv[1])
	duration = 1
elif len(sys.argv) == 3:
	freq = int(sys.argv[1])
	duration = int(sys.argv[2])
else:
	print "Usage: freqgen frequency duration"
	exit()

BITRATE = 16000 # number of frames per second/frameset.      
FREQUENCY = freq # Hz, waves per second, 261.63=C4-note.
LENGTH = duration # seconds to play sound

if FREQUENCY > BITRATE:
	BITRATE = FREQUENCY+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''    

print "Frequency doubled. DG. 2018-9-06"
for x in xrange(NUMBEROFFRAMES):
	WAVEDATA = WAVEDATA+chr(int(math.sin(x/((0.49*BITRATE/FREQUENCY)/math.pi))*127+128))    

for x in xrange(RESTFRAMES): 
	WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
		channels = 1, 
		rate = BITRATE, 
		output = True)

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()
