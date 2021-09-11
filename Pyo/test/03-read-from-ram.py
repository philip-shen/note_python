from pyo import *

s = Server(sr=48000, buffersize=1024).boot()

path = "SPEECH_001_record.wav"#SNDS_PATH + "/transparent.aif"

# Loads the sound file in RAM. Beginning and ending points
# can be controlled with "start" and "stop" arguments.
t = SndTable(path)

# Gets the frequency relative to the table length.
freq = t.getRate()

# Simple stereo looping playback (right channel is 180 degrees out-of-phase).
osc = Osc(table=t, freq=freq, phase=[0], mul=0.4).out()
#osc = Osc(table=t, freq=freq, phase=[0.5], mul=0.4).out()

s.gui(locals())