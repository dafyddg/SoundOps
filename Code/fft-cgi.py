#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/pkgsrc/20140707/bin/python2.7
#!/usr/bin/python
# fft-cgi.py
# D. Gibbon, 2018-09-11

opsys = 'linux'
# opsys = 'solaris'

import warnings
warnings.filterwarnings("ignore")

import numpy as np

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

fs = 30.0
freq = 10.0
t = 2.0
txf = t*freq
tvector = np.arange(0,txf,1/fs)	# duration = 1s, 10 cycles, divided by 30 frames
x = np.sin(2*np.pi*freq*tvector)

#=========================================================================

xF = np.fft.fft(x)
N = len(xF)
xF = xF[0:N]
fr = np.linspace(-fs,fs,N)

yvector = abs(xF)**2

#=========================================================================

N2 = N/2
xF2 = xF[N2:]
fr2 = np.linspace(0,fs,N2)

y2vector = abs(xF2)**2

#=========================================================================

figwidth = 8
figheight = 1.4
fontsize = 8

plt.figure(1,(figwidth,figheight))
plt.title('Signal (t=%.2f, f=%dHz, samprate = %dHz)'%(t,freq,fs),fontsize=fontsize)
plt.xlabel('Samples',fontsize=fontsize)
plt.ylabel('Amplitude',fontsize=fontsize)
plt.plot(x,color='lightblue')
xticks = np.linspace(0,len(x),5)
xlabels = [ "%.3f"%s for s in np.linspace(0,t,5)]
plt.xticks(xticks,xlabels)
plt.grid(axis='x', which='both', linewidth=2)
plt.tick_params(axis='both',labelsize=fontsize)
plt.xlim(0,len(x))
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.5)
plt.savefig(localdirectory+'fft01.png')

plt.figure(2,(figwidth,figheight))
plt.title('Symmetrical FFT Spectrum',fontsize=fontsize)
plt.xlabel('Samples',fontsize=fontsize)
plt.ylabel('Magnitude',fontsize=fontsize)
plt.stem(fr,abs(xF)**2,markerfmt='ro')
plt.grid(axis='x', which='both', linewidth=1)
plt.xlim(-fs,fs)
plt.ylim(0,max(yvector)*1.1)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.5)
plt.savefig(localdirectory+'fft02.png')

plt.figure(3,(figwidth,figheight))
plt.title('Asymmetrical (half) FFT Spectrum',fontsize=fontsize)
plt.xlabel('Samples',fontsize=fontsize)
plt.ylabel('Magnitude',fontsize=fontsize)
plt.stem(fr2,abs(xF2)**2,markerfmt='ro')
plt.grid(axis='x', which='both', linewidth=1)
plt.xlim(0,fs)
plt.ylim(0,max(y2vector)*1.1)
plt.tick_params(axis='both',labelsize=fontsize)
plt.tight_layout(pad=0.5,w_pad=0.5,h_pad=0.5)
plt.savefig(localdirectory+'fft03.png')

#=========================================================================

inithtml()

print '<img src=\"'+webdirectory+'fft01.png\" width=\"100%\">'
print '<img src=\"'+webdirectory+'fft02.png\" width=\"100%\">'
print '<img src=\"'+webdirectory+'fft03.png\" width=\"100%\">'

terminatehtml()

