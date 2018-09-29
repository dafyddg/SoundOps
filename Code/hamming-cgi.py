#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/pkgsrc/20140707/bin/python2.7
#!/usr/bin/python

# bandpass-cgi.py
# D. Gibbon, 2018-09-11

opsys = 'linux'
# opsys = 'solaris'

import warnings
warnings.filterwarnings("ignore")

import numpy as np
from numpy.fft import fft, fftshift
from scipy.signal import butter, lfilter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cgi, cgitb; cgitb.enable()
from cgi import escape

if opsys == 'linux':
        localdirectory = '/var/www/Webtmp/'
        webdirectory = '/Webtmp/'
elif opsys == 'solaris':
        localdirectory = '../../docs/Webtmp/'
        webdirectory = '/gibbon/Webtmp/'
else:
        print 'Unknown operating system.'; exit()

#=========================================================================
# Initialise HTML

def inithtml():
    print "Content-type: text/html\n\n"
    print '<html><head><title>Bandpass filter</title>'
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

#=========================================================================

def terminatehtml():
    print "</body></html>"
    return

#=========================================================================

window = np.hamming(51)

figwidth = 8
figheight = 2
fontsize = 8

plt.figure(1,(figwidth,figheight))
plt.plot(window)
plt.title("Hamming (raised cosine) window",fontsize=fontsize)
plt.ylabel("Amplitude",fontsize=fontsize)
plt.xlabel("Sample",fontsize=fontsize)
plt.tight_layout(pad=0.1,w_pad=0.5,h_pad=0.1)
plt.tick_params(axis='both',labelsize=fontsize)
plt.savefig(localdirectory+'hamming01.png')
plt.close('all')


plt.figure(2,(figwidth,figheight))
A = fft(window, 2048) / 25.5
mag = np.abs(fftshift(A))
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(mag)
response = np.clip(response, -100, 100)
plt.plot(freq, response)
plt.title("Frequency response of Hamming window",fontsize=fontsize)
plt.ylabel("Magnitude [dB]",fontsize=fontsize)
plt.xlabel("Normalized frequency [cycles per sample]",fontsize=fontsize)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.1,w_pad=0.5,h_pad=0.1)
plt.savefig(localdirectory+'hamming02.png')
plt.close('all')

inithtml()

print '<img src=\"'+webdirectory+'hamming01.png\" width=\"100%\">'
print '<img src=\"'+webdirectory+'hamming02.png\" width=\"100%\">'

terminatehtml()

