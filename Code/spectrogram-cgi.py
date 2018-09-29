#!/usr/bin/python
#-*- coding: UTF8 -*-

#!/usr/pkgsrc/20140707/bin/python2.7
#!/usr/bin/python

opsys = 'linux'
# opsys = 'solaris'

# spectrogram.py
# D. Gibbon 2018-09-03

import warnings
warnings.filterwarnings("ignore")

import scipy.io.wavfile as wave
#from scipy.signal import spectrogram

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

#======================
# Fetch CGI parameters as dictionary

def cgitransferlines(cgifields):
	fieldstorage = cgi.FieldStorage()
	fieldvalues = []
	for field in cgifields:
		if fieldstorage.has_key(field):
			fieldname = fieldstorage[field].value
		else:
			fieldname = '1066'
		fieldvalues = fieldvalues + [(field,fieldname)]
	return dict(fieldvalues)

#=========================================================================

inithtml()

cgifields = [ 'resolution', 'range', 'wavfile' ]
cgifielddict = cgitransferlines(cgifields)
spectrumresolution = int(cgifielddict['resolution'])
spectrumrange = int(cgifielddict['range'])

wavfile = cgifielddict['wavfile']

if wavfile == 'Mandarin':
	wavfile = 'Data/jiayan-5s.wav'
elif wavfile == 'English':
	wavfile = 'Data/Abercrombie-short16k.wav'
else:
	print "Unknown WAV file."; exit()

localwavfile = localdirectory+wavfile
webwavfile = webdirectory+wavfile

sampfreq,signal = wave.read(localwavfile)

plt.figure(1,(8,4))
plt.specgram(signal, NFFT=spectrumresolution, Fs=sampfreq)
plt.ylim(0,spectrumrange)
plt.title('Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.grid(which='both',axis='both',linewidth=2)
plt.tight_layout(pad=1,w_pad=0.5,h_pad=0.5)
plt.savefig(localdirectory+'spectrogram.png')

print '<table><tr>'
#print '<td><b>Example: '+wavfile+'</b></td>'
print '<td width="20%"><b>Example: '+wavfile+'</b></td></td>'
print '<td>'
print '<audio controls style="width: 80%;">'
print '<source src="'+webwavfile+'" type="audio/wav" length="0%">'
print 'Your browser does not support the audio element.</audio>'
print '</td>'
print '</tr><tr><td colspan="2">'
print '<img src=\"'+webdirectory+'spectrogram.png\" width=\"100%\">'
print '</td></tr></table>'

terminatehtml()

