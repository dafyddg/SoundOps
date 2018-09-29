#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/pkgsrc/20140707/bin/python2.7
#!/usr/bin/python
# fm.py
# D. Gibbon
# D. Gibbon, 2018-09-11

opsys = 'linux'
# opsys = 'solaris'

#=========================================================================
"""
Illustrations of amplitude and frequency modulation and demodulation,
with FFT analysis of both amplitude and frequency modulation.

9 plot options:
- Carrier signal
- Modulating signal
- AM modulated signal
- FFT analysis of AM signal
- AM demodulation with Hilbert transformation
- AM demodulation with rectification and low pass filter
- Frequency modulation: carrier frequency + modulation amplitude
- FFT analysis of FM signal
- FM demodulation: filter slope, amplitude normalisation, Hilbert transcormation

"""
#=========================================================================

import numpy as np
#from numpy.fft import rfft

import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mlab import find

from scipy.signal import butter, hilbert, lfilter, medfilt, hann, hamming, blackmanharris
import scipy.io.wavfile as wave

import cgi, cgitb; cgitb.enable()
from cgi import escape

import modgf0x

if opsys == 'linux':
	localdirectory = '/var/www/Webtmp/'
	webdirectory = '/Webtmp/'
elif opsys == 'solaris':
	localdirectory = '../../docs/Webtmp/'
	webdirectory = '/gibbon/Webtmp/'
else:
	print "Unknown operating system."; exit()

#=========================================================================
# Initialise HTML

def inithtml():
	print '<html><head><title>AM and FM modulation and demodulation. D. Gibbon</title>'
	print """
	<style type="text/css">
		tdp {font-size:14}
		td {font-size:14}
		p {font-size:14}
		li {font-size:14}
		small {font-size:14}
		big {font-size:18;font-weight:bold}
		verybig {font-size:24;font-weight:bold}
	</style>
	"""
	print '</head><body>'
	return

def terminatehtml():
	print "</body></html>"
	return

#==============================================================
# CGI handling
print "Content-type: text/html\n\n"

cgifields = [	'filebase', 'voicetype', 'fft', 'zer0x', 'peak'	]

# Fetch CGI parameters as dictionary

def cgitransferlines(cgifields):
	fs = cgi.FieldStorage()
	fieldvalues = []
	for field in cgifields:
		if fs.has_key(field):
			fieldname = fs[field].value
		else:
			fieldname = '1066'
		fieldvalues = fieldvalues + [(field,fieldname)]
	return dict(fieldvalues)

# recover CGI settings

cgiparamsdict = cgitransferlines(cgifields)
filebase = cgiparamsdict['filebase']
voicetype = cgiparamsdict['voicetype']
fft = cgiparamsdict['fft']
zer0x = cgiparamsdict['zer0x']
peak = cgiparamsdict['peak']

localwavfile = localdirectory+'Data/%s.wav'%filebase
webwavfile = webdirectory+'Data/%s.wav'%filebase

#==============================================================

sampfreq,signal = wave.read(localwavfile)

siglen = len(signal)
sigduration = 1.0*siglen/sampfreq

#==============================================================

minf0 = 120; maxf0 = 400; framerate = 0.01; freqweight = 0.02

# RAPT is not available on the BITS server:
# f0list,voicelist = modgrapt.f0rapt(wavfile, 120, 400, 0.01, 0.02, ('raptf0.f0', 'raptf0.csv', 'raptf0log.f0log', 'raptparams'))

def parabolic(f, x):
	xv = 1.0/2.0 * (f[x-1] - f[x+1]) / float(f[x-1] - 2 * f[x] + f[x+1]) + x
	yv = f[x] - 1.0/4.0 * (f[x-1] - f[x+1]) * (xv - x)
	return (xv, yv)

#=================

def freq_from_fft(sig, fs):
	windowed = sig * blackmanharris(len(sig))
	f = np.fft.rfft(windowed)
	i = np.argmax(abs(f)) # Just use this for less-accurate, naive version
	true_i = parabolic(abs(f), i)[0]
	return fs * true_i / len(windowed)

#=================

def freq_from_crossings(sig, fs):
	indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
	crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]
	diffc = np.diff(crossings)

	# BUG: np.average does not like empty lists
	if len(diffc) > 0:
		return 1.0 * fs / np.average(np.diff(crossings))	# use mean?
	else:
		return 0

def freq_from_crossings_02(sig, fs):

	# Find all indices right before a rising-edge zero crossing
	indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

	# Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
	# crossings = indices

	# More accurate, using linear interpolation to find intersample
	# zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
	crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

	# Some other interpolation based on neighboring points might be better.
	# Spline, cubic, whatever

	return fs / np.mean(np.diff(crossings))

def freq_from_peaks(sig,fs):
	sig = np.diff(sig**2)
	return freq_from_crossings(sig,fs)/2.0	


def freq_from_autocorr(sig, fs):
	"""
	Estimate frequency using autocorrelation
	"""
	# Calculate autocorrelation (same thing as convolution, but with
	# one input reversed in time), and throw away the negative lags
	corr = fftconvolve(sig, sig[::-1], mode='full')
	corr = corr[len(corr)//2:]

	# Find the first low point
	d = np.diff(corr)
	start = find(d > 0)[0]

	# Find the next peak after the low point (other than 0 lag).  This bit is
	# not reliable for long signals, due to the desired peak occurring between
	# samples, and other peaks appearing higher.
	# Should use a weighting function to de-emphasize the peaks at longer lags.
	peak = argmax(corr[start:]) + start
	px, py = parabolic(corr, peak)

	return fs / px

#==============================================================
# Filter definitions
# b, a = butter(order, cutoff, type)	# define filter
# y = lfilter(b, a, data)							# apply filter


# Butterworth impulse response
# b, a = signal.butter(4, 100, 'low', analog=True)
# w, h = signal.freqs(b, a)
# plt.plot(w, 20 * np.log10(abs(h)))
# plt.xscale('log')

def butterworth(data, fs, type, cutoff, order):
	nyq = 0.5*fs
	cutoff = cutoff/nyq # check this
	b, a = butter(order,cutoff,btype=type)
	y = lfilter(b, a, data)
	return y

def cclip(signal,proportion):
	ccsig = np.array([ 0 if (abs(x)<signalmedian*proportion) else x for x in signal ])
	return ccsig

def pclip(signal,proportion):
	pcsig = np.array([ np.log10(x) if (abs(x)>signalmedian*proportion) else x for x in signal ])
	return pcsig


#==============================================================
#==============================================================


signalfilt = signal

winlen = int(float(1.0/framerate))

signalreference = np.array([ x for x in signalfilt if x > np.max(signalfilt)*0.01 ])
signalmedian = np.median(signalreference)

#==============================================================
#==============================================================


if voicetype == 'low':
	f0min = 50
	f0max = 250
	cutoffhi =  95
	orderhi = 3
	cutofflo = 135
	orderlo = 5
	f0clipmin = 60
	f0clipmax = 250
	centreclip = 0.07

elif voicetype == 'mid':
	f0min = 100
	f0max = 320
	cutoffhi =  110
	orderhi = 3
	cutofflo = 200
	orderlo = 5
	f0clipmin = 100
	f0clipmax = 300
	centreclip = 0.1

elif voicetype == 'high':
	f0min = 150
	f0max = 400
	cutoffhi = 180
	orderhi = 3
	cutofflo = 300
	orderlo = 5
	f0clipmin = 150
	f0clipmax = 400
	centreclip = 0.15

else:
	print "Undefined Voice Type."; exit()

polydegree = 16
f0framerate = 0.01
f0stepfactor = 1
f0median = 5

f0fft,f0xpoly = modgf0x.f0x(signalfilt, sampfreq, "on", "off", "off", polydegree, f0framerate, f0stepfactor, f0median, f0min, f0max, centreclip, f0clipmin, f0clipmax, cutoffhi, orderhi, cutofflo, orderlo)

f0zer0x,f0xpoly = modgf0x.f0x(signalfilt, sampfreq, "off", "on", "off", polydegree, f0framerate, f0stepfactor, f0median, f0min, f0max, centreclip, f0clipmin, f0clipmax, cutoffhi, orderhi, cutofflo, orderlo)

f0peak,f0xpoly = modgf0x.f0x(signalfilt, sampfreq, fft, zer0x, peak, polydegree, f0framerate, f0stepfactor, f0median, f0min, f0max, centreclip, f0clipmin, f0clipmax, cutoffhi, orderhi, cutofflo, orderlo)

#==============================================================
#==============================================================

figwidth = 8
figheight = 1.4
fontsize = 8

plt.figure(1,(figwidth,figheight))
plt.plot(range(len(signal)),signal,color='lightblue')
plt.xticks(np.linspace(0,siglen,6),np.linspace(0,sigduration,6))
plt.xlim(-0.01,len(signal)+0.01)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
plt.savefig(localdirectory+'fm01.png')
plt.close('all')

plt.figure(2,(figwidth,figheight))
plt.ylabel('FFT peak', fontsize=fontsize)
plt.scatter(range(len(f0fft)),f0fft,s=1, color='g')
plt.xticks(np.linspace(0,len(f0fft),6),np.linspace(0,sigduration,6))
plt.xlim(-0.01,len(f0fft)+0.01)
plt.ylim(minf0,maxf0)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
plt.savefig(localdirectory+'fm02.png')
plt.close('all')

plt.figure(3,(figwidth,figheight))
plt.ylabel('Zero Xing periodicity', fontsize=fontsize)
plt.scatter(range(len(f0zer0x)),f0zer0x,s=1,color='b')
plt.xticks(np.linspace(0,len(f0zer0x),6),np.linspace(0,sigduration,6))
plt.xlim(-0.01,len(f0zer0x)+0.01)
plt.ylim(minf0,maxf0)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
plt.savefig(localdirectory+'fm03.png')
plt.close('all')

plt.figure(4,(figwidth,figheight))
plt.ylabel('Combinations',fontsize=fontsize)
plt.scatter(range(len(f0peak)),f0peak,s=1, color='c')
plt.xticks(np.linspace(0,len(f0peak),6),np.linspace(0,sigduration,6))
plt.xlim(-0.01,len(f0peak)+0.01)
plt.ylim(minf0,maxf0)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
plt.savefig(localdirectory+'fm04.png')
plt.close('all')

audioaddress = webwavfile
print '<table align=center>'
print '<tr><td width="100%"><audio controls style="width: 100%;">'
print '<source src="'+audioaddress+'" type="audio/wav">'
print 'Your browser does not support the audio element.</audio>'
print '</td></tr>'
print '<tr><td><b>Source: '+filebase+'</b></td><tr>'
print '<tr><td width="100%"><img src=\"'+webdirectory+'fm01.png\" alt=\"Waveform.\">'
print '</td></tr>'

print '<tr><td width="100%"><img src=\"'+webdirectory+'fm02.png\" alt=\"F0 detection by Fourier transform and detection of the most prominent spectral peak.\">'
print '</td></tr>'

print '<tr><td width="100%"><img src=\"'+webdirectory+'fm03.png\" alt=\"F0 detection as the inverse of intervals between rising edge zero-crossings.\">'
print '</td></tr>'

print '<tr><td width="100%"><img src=\"'+webdirectory+'fm04.png\" alt=\"F0 detection as the inverse of intervals between signal peaks.\">'
print '</td></tr>'

print '</table>'
