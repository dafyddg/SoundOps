# SoundOps
Collection of small CGI online apps to illustrate aspects of acoustic phonetics.

Input form: soundops.html
1. Butterworth filters:
  - low-pass: lowpass-cgi.py
  - high-pass: highpass-cgi.py
  - band-pass: bandpass-cgi.py
2. Transforms:
  - Fast Fourier Transform: fft-cgi.py)
  - Hilbert transform (hilbert-cgi.py) to illustrate amplitude demodulation
4. Cosine windows:
  - Hamming window (hamming-cgi.py)
  - Hann (Hanning) window (hanning-cgi.py)
5. Spectrogram (spectrogram-cgi.py)

Input form: fm.html
- Frequency modulation (fm-cgi.py)

Input form: moddemod.html
- FM and AM modulation and demodulation (moddemod.html, moddemod-cgi.py) with modules:
  - modgf0x.py (parametrised F0 estimation)
  - modgrapt.py (wrapper for Debian distribution of David Talkin's RAPT F0 estimation)
