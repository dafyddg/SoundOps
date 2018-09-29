#!/usr/bin/python
# chipmunk.py
# D. Gibbon 2018-09-03

#========================================================================
# Import required library modules

import os,sys
import scipy.io.wavfile as wave

wavfile = sys.argv[1]

sampfreq,signal = wave.read(wavfile)
reversesignal = signal[::-1]
wave.write("temp.wav",sampfreq,reversesignal)
os.system("play temp.wav")
