import os,sys,time,platform

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

import myWave
import dspUtil
import numpy
import copy
import generalUtility
fName = 'WilhelmScream.wav'
# http://en.wikipedia.org/wiki/Wilhelm_scream
# http://www.youtube.com/watch?v=Zf8aBFTVNEU
# load the input file
# data is a list of numpy arrays, one for each channel
numChannels, numFrames, fs, data = myWave.readWaveFile(fName)
# normalize the left channel, leave the right channel untouched
data[0] = dspUtil.normalize(data[0])
# just for kicks, reverse (i.e., time-invert) all channels
for chIdx in range(numChannels):
    n = len(data[chIdx])
    dataTmp = copy.deepcopy(data[chIdx])
    for i in range(n):
        data[chIdx][i] = dataTmp[n - (i + 1)]
# save the normalized file (both channels)
# this is the explicit code version, to make clear what we're doing. since we've
# treated the data in place, we could simple write: 
# myWave.writeWaveFile(data, outputFileName, fs) and not declare dataOut
dataOut = [data[0], data[1]] 
fileNameOnly = generalUtility.getFileNameOnly(fName)
outputFileName = fileNameOnly + "_processed.wav"
myWave.writeWaveFile(dataOut, outputFileName, fs)