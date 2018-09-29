#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/pkgsrc/20140707/bin/python2.7
#!/usr/bin/python

# hilbert-cgi.py
# D. Gibbon, 2018-09-11

opsys = 'linux'
# opsys = 'solaris'

import warnings
warnings.filterwarnings("ignore")

import numpy as np
from scipy.signal import hilbert

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
# Amplitude modulation

mod_shift = np.max(modulator) - np.min(modulator)

am_sig = carrier * (modulation_index * modulator + mod_shift/2)

analyticsignal = hilbert(am_sig)
envelope = abs(analyticsignal)-modulation_index

fontsize = 8
figwidth = 8
figheight = 1

plt.figure(1,(figwidth,figheight))
plt.title("Modulation (information) signal",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)
plt.ylim(-1,1)
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.7)
plt.plot(modulator/2,color='orange',linewidth=4)
plt.savefig(localdirectory+"hilbert01.png")
plt.close('all')

plt.figure(2,(figwidth,figheight))
plt.title("Carrier wave / carrier signal",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)
plt.plot(carrier,color='lightblue')
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.7)
plt.savefig(localdirectory+"hilbert02.png",color='b')
plt.close('all')

plt.figure(3,(figwidth,figheight))
plt.title("Amplitude modulated signal",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)
plt.plot(am_sig,color='blue')
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.7)
plt.savefig(localdirectory+"hilbert03.png")
plt.close('all')

plt.figure(5,(figwidth,figheight))
plt.title("Hilbert transformation: absolute analytic signal, AM envelope",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)
plt.plot(analyticsignal,color='lightblue')
plt.plot(envelope+np.max(analyticsignal)-np.max(envelope),color='r',linewidth='4')
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.7)
plt.savefig(localdirectory+'hilbert04.png')
plt.close('all')

inithtml()

print '<img src=\"'+webdirectory+'hilbert01.png\" width=\"100%\">'
print '<img src=\"'+webdirectory+'hilbert02.png\" width=\"100%\">'
print '<img src=\"'+webdirectory+'hilbert03.png\" width=\"100%\">'
print '<img src=\"'+webdirectory+'hilbert04.png\" width=\"100%\">'

terminatehtml()

