#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/pkgsrc/20140707/bin/python2.7
#!/usr/bin/python

# lowpass-cgi.py
# D. Gibbon, 2018-09-11

opsys = 'linux'
# opsys = 'solaris'

import warnings
warnings.filterwarnings("ignore")

import numpy as np
from scipy import signal

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

figwidth = 8
figheight = 4
fontsize = 8

plt.figure(1,(figwidth,figheight))
b, a = signal.butter(4, 100, 'low', analog=True)
w, h = signal.freqs(b, a)
plt.plot(w, 20 * np.log10(abs(h)))
plt.xscale('log')
plt.title('Butterworth low pass filter frequency response',fontsize=fontsize)
plt.xlabel('Frequency [radians / second]',fontsize=fontsize)
plt.ylabel('Amplitude [dB]',fontsize=fontsize)
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green') # cutoff frequency

plt.tight_layout(pad=0.1,w_pad=0.5,h_pad=0.1)
plt.tick_params(axis='both',labelsize=fontsize)
plt.savefig(localdirectory+'lowpass.png')

inithtml()

print '<img src=\"'+webdirectory+'lowpass.png\" width=\"100%\">'

terminatehtml()

