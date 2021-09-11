from pyo import *

s = Server(sr=48000, buffersize=1024).boot()

path = "SPEECH_001_record.wav"#SNDS_PATH + "/transparent.aif"

# stereo playback with a slight shift between the two channels.
sf = SfPlayer(path, speed=[1, 0.995], loop=False, mul=0.4).out()

s.gui(locals())