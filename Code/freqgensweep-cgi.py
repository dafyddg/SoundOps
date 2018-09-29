#!/usr/bin/python -u
# freqgensweep.py
# D. Gibbon
# Modified from
# http://stackoverflow.com/questions/9770073/sound-generation-synthesis-with-python

import math
import pyaudio
import sys

PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 64000 #number of frames per second/frameset.      

start = 1000
end = 25000
step = 1000
duration = 1

if len(sys.argv) !=5:
	print "Usage: freqgensweep.py startfreq endfreq stepfreq dur"
	exit()
if end <= start:
	print "Input error: End before start."
	exit()
if step < 1 or duration <= 0:
	print "Input error: Negative duration"
	exit()
start = int(sys.argv[1])
end = int(sys.argv[2])
step = int(sys.argv[3])
duration = int(sys.argv[4])

for freq in range(start,end,step):
	print freq
	FREQUENCY = freq # Hz, waves per second, 261.63=C4-note.
	LENGTH = duration # seconds to play sound

	if FREQUENCY > BITRATE:
		BITRATE = FREQUENCY+100

	NUMBEROFFRAMES = int(BITRATE * LENGTH)
	RESTFRAMES = NUMBEROFFRAMES % BITRATE
	WAVEDATA = ''    

	for x in xrange(NUMBEROFFRAMES):
	 	WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    
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

