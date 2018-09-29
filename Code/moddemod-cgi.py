#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/bin/python
#!/usr/pkgsrc/20140707/bin/python2.7

# bandpass-cgi.py
# D. Gibbon, 2018-09-11

#!/usr/bin/python
# fm.py
# D. Gibbon

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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import butter, hilbert, lfilter

import cgi, cgitb; cgitb.enable()
from cgi import escape

if opsys == 'solaris':
	localdirectory = '../../docs/Webtmp/'
	webdirectory = '/gibbon/Webtmp/'
elif opsys == 'linux':
	localdirectory = '/var/www/Webtmp/'
	webdirectory = '/Webtmp/'
	

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


cgifields = [
	'carrier',
	'modulator',
	'am',
	'amfft',
	'amdemodhilbert',
	'amdemodcrystalset',
	'fm',
	'fmfft',
	'fmdemod'
	]

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

carrierflag = cgiparamsdict['carrier']
modulatorflag = cgiparamsdict['modulator']
am_sigflag = cgiparamsdict['am']
amfftflag = cgiparamsdict['amfft']
amdemodhilbertflag = cgiparamsdict['amdemodhilbert']
amdemodcrystalsetflag = cgiparamsdict['amdemodcrystalset']
fm_sigflag = cgiparamsdict['fm']
fmfftflag = cgiparamsdict['fmfft']
filterslopeflag = cgiparamsdict['fmdemod']

#=========================================================================
#=========================================================================

print "Content-type: text/html\n\n"

inithtml()

modulator_frequency = 10
carrier_frequency = 200
modulation_index = 0.75

# Generate a sequence 0.0 ... 0.999...
time = np.arange(44100.0) / 44100.0

# Multiply the items in the *time* sequence by 2 pi f (modulation)
modulator = np.sin(2.0 * np.pi * modulator_frequency * time) * modulation_index

# Multiply the items in the *time* sequence by 2 pi f (carrier)
carrier = np.sin(2.0 * np.pi * carrier_frequency * time)

#=========================================================================

# Frequency modulation

# Generate a sequence of zeros of same length (just to get a sequence
# The zeros are of no consequence
fm_sig = np.zeros_like(modulator)

# Multiply the *carrier frequency* (not the carrier) by 2 pi and time point
# Then *add* the current modulator amplitude
# Get the sine function of this
for i, t in enumerate(time):
    fm_sig[i] = np.sin(2. * np.pi * (carrier_frequency * t + modulator[i]))

# fm_sig = [ np.sin(2. * np.pi * (carrier_frequency * t + modulator[t])) for x,t in zip(fm_sig,time) ]

#=========================================================================
# Amplitude modulation

mod_shift = np.max(modulator) - np.min(modulator)
# am_sig = carrier * (1 * modulator + mod_shift/2)
am_sig = carrier * (modulation_index * modulator + mod_shift/2)

#=========================================================================
# Amplitude demodulation

envelope = abs(hilbert(am_sig))-modulation_index

#=========================================================================
# AM FFT

amfft = abs(np.fft.fft(am_sig))[:carrier_frequency*2]


#=========================================================================
# F; FFT

fmfft = abs(np.fft.fft(fm_sig))[:carrier_frequency*2]

#=========================================================================
# Low pass filter

def butter_lowpass(cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

def butter_lowpass_filter(data, cutoff, fs, order):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

#=========================================================================

cutoff_frequency = 2
sampling_frequency = carrier_frequency *10
order = 3
crystalset = butter_lowpass_filter(abs(am_sig),cutoff_frequency,sampling_frequency,order)-0.5

#=========================================================================

cutoff_frequency = modulator_frequency * 1.6
sampling_frequency = carrier_frequency * 10
order = 6

# Filter on slope of a low-pass filter
filterslope = butter_lowpass_filter(abs(fm_sig),cutoff_frequency,sampling_frequency,order)

# Normalise amplitude around zero
filterslope = filterslope - np.median(filterslope)
# Apply Hilbert transformation
filterslope = np.abs(hilbert(filterslope))

#=========================================================================

def plotsignalrow(title,time,data,colour,fontsize,row):
	row +=1
	plt.subplot(rows,1,row)
	plt.title(title,fontsize=fontsize)
	plt.plot(time,data,color=colour)
	plt.yticks([-1,0,1],[-1,0,1])
	plt.tick_params(axis='both', labelsize=fontsize)
	return row

#=========================================================================

def plotfftrow(title,data,modulationindex,colour,fontsize,row):
	"Where does the modulationindex go?"
	row +=1
	plt.subplot(rows,1,row)
	plt.title(title,fontsize=fontsize)
	plt.plot(data,color=colour)
	yticks = np.linspace(np.min(data),np.max(data),3)
	plt.yticks(yticks,[0,0.5,1])
	plt.tick_params(axis='both', labelsize=fontsize)
	return row

#=========================================================================

def plotfmdemodrow(title,time,data,colour,fontsize,row):
	row +=1
	plt.subplot(rows,1,row)
	plt.tick_params(axis='both', labelsize=fontsize)
	plt.title(title,fontsize=fontsize)
	plt.plot(data,color=colour,linewidth=2)
	slopelen = len(filterslope)
	xticks = np.linspace(0,slopelen,6)
	xlabels = np.linspace(0,1,6)
	plt.xlim(0,slopelen)
	plt.xticks(xticks,xlabels)
	datamin = np.min(data)
	datamax = np.max(data)
	datamedian = np.median(data)
	plt.ylim(datamin,datamedian*2.5)
	yticks = np.linspace(np.min(filterslope),2.5*np.median(filterslope),3)
	plt.yticks(yticks,[-1,0,1])

	return row

#=========================================================================
#=========================================================================
# Figure

#=========================================================================
# Figure

row = 0

figwidth = 8 
figheight = 7
fontsize = 8

plotlist = [modulatorflag, carrierflag, am_sigflag, amfftflag, amdemodhilbertflag, amdemodcrystalsetflag, fm_sigflag, fmfftflag, filterslopeflag ]

onlist = [ x for x in plotlist if x == 'on' ]
rows = len(onlist)

plt.figure(1,(figwidth,figheight))
plt.suptitle("Amplitude and Frequency Modulation",fontsize=fontsize+4)

#=========================================================================
# ======== Modulator
if modulatorflag == 'on':
	row = plotsignalrow("Modulating signal (information signal): sinusoid, frequency "+str(modulator_frequency)+")",time,modulator,'orange',fontsize,row)

# ======== Carrier
if carrierflag == 'on':
	row = plotsignalrow("Carrier signal: sinusoid, frequency "+str(carrier_frequency)+")",time,carrier,'b',fontsize,row)

# ======== AM modulated, am_sig
if am_sigflag == 'on':
	row = plotsignalrow("Amplitude Modulation (AM): carrier amplitude x information amplitude",time,am_sig,'g',fontsize,row)

# ======== AM FFT of am modulatedflag:
if amfftflag == 'on':
	row = plotfftrow("AM analysis with FFT, showing carrier and modulation sidebands",amfft,modulation_index,'r',fontsize,row)

# ======== AM demodulation: Hilbert
if amdemodhilbertflag == 'on':
	row = plotsignalrow("Amplitude envelope demodulation: Hilbert transformation",time,envelope,'r',fontsize,row)

# ======== AM demodulation: rectification and low pass filter 
if amdemodcrystalsetflag == 'on':
	row = plotsignalrow("Alternative amplitude envelope demodulation: rectification & low-pass filter",time,crystalset,'g',fontsize,row)

# ======== FM modulated, fm_sig
if fm_sigflag == 'on':
	row = plotsignalrow("Frequency modulation: carrier frequency + modulation amplitude)",time,fm_sig,'c',fontsize,row)

# ======== FM FFT of fm modulated
if fmfftflag == 'on':
	row = plotfftrow("FM analysis with FFT, showing carrier and modulation sidebands",fmfft,modulation_index,'r',fontsize,row)

# ======== FM demodulation:
# - convert to AM on filter slope,
# - normalise amplitude to zero,
# - apply Hilbert transformation
if filterslopeflag == 'on':
	row = plotfmdemodrow("Frequency demodulation: convert to AM, normalise, Hilbert transformation",time,filterslope,'r',fontsize,row)
#=========================================================================

#plt.tight_layout()
plt.tight_layout(pad=2.5, w_pad=0.5, h_pad=0.5)

plt.savefig(localdirectory+"moddemod.png")


print '<img src=\"'+webdirectory+'moddemod.png\" width=\"100%\">'

#=========================================================================

terminatehtml()
#=========================================================================
