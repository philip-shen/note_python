from pyo import *

s = Server(sr=48000, buffersize=1024).boot()
s.amp = 0.1

# Creates a source (white noise)
n = "SPEECH_001_record.wav";#Noise()

# Sends the bass frequencies (below 1000 Hz) to the left
lp = ButLP(n).out()

# Sends the high frequencies (above 1000 Hz) to the right
hp = ButHP(n).out(1)

s.gui(locals())