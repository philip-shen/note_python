 import wave, struct
 import numpy, array
 import copy
 import gc
 import dspUtil
 gc.enable()
 
 import scipy.io.wavfile as sciWav
 #from scipy import weave as weave
 
 
 
 
 def readWaveFile(fileName, useRobustButSlowAlgorithm = True):
     
     if useRobustButSlowAlgorithm:
         f = wave.open(fileName, "rb")
         numFrames = f.getnframes()
         numChannels = f.getnchannels()
         fs = f.getframerate()
         dataTmp = f.readframes(numFrames * numChannels)
         sampleWidth = f.getsampwidth()
         #print numChannels, numFrames, fs, sampleWidth, len(dataTmp)
         format = ''
         if sampleWidth == 1:
             format = 'B'
         elif sampleWidth == 2:
             format = 'h'
         elif sampleWidth == 4:
             format = 'i'
         if sampleWidth != 2:
             raise Exception("we only support 16 bit data")
         out = struct.unpack_from (("%d" % (numFrames * numChannels)) + format, dataTmp)
         
         data = []
         for i in range(numChannels):
             data.append(numpy.zeros(numFrames))
             #data.append([0] * numFrames)
         #data = numpy.zeros((numChannels, numFrames))   
             
             
             
         divisor = float(2 ** 15)
         
         for i in range(numChannels):
             arrFrameIdx = range(numFrames) # explicit indexing and garbage collection
             for j in arrFrameIdx:
                 data[i][j] = out[j * numChannels + i] / divisor
             del arrFrameIdx
             
         #for chIdx in range(numChannels):
         #   channelData = data[chIdx]
         #   code = """
         #   for (int frameIdx = 0; frameIdx < numFrames; frameIdx++) {
         #       channelData[frameIdx] = (float)out[frameIdx * numChannels + chIdx] / divisor; 
         #   }   
         #   //return_val = C;
         #   """ 
         #   weave.inline(code,['channelData', 'chIdx', 'out', 'divisor', 
         #       'numChannels', 'numFrames'], verbose=0)
             
             
             
         f.close()
         del dataTmp, out, f
         gc.collect()
         return [numChannels, numFrames, fs, data]
     
     fs, dataRaw = sciWav.read(fileName)
     n = len(dataRaw)
     numChannels = 1
     try: numChannels = dataRaw.shape[1]
     except: pass
     arrChannels = []
     for chIdx in range(numChannels):
         tmp = numpy.zeros(n)
         if numChannels == 1:
             tmp = dataRaw.astype(numpy.float32)
         else:
             tmp = dataRaw[0:, chIdx].astype(numpy.float32)
         tmp /= float(2**15)
         arrChannels.append(tmp)
         del tmp
     del dataRaw
     gc.collect()
     return [numChannels, n, fs, arrChannels]
 
 
 
 
 def readMonoWaveFile(fName):
     numChannels, n, fs, arrChannels = readWaveFile(fName)
     return arrChannels[0], fs
     
 
     
 
 def writeWaveFile(data, fileName, SRate = 44100.0, normalize = False, \
         removeDcWhenNormalizing = True
     ): 
     
     if not type(data).__name__ in ['list', 'ndarray']:
         raise Exception("expected a list data type, but got %s" % type(data).__name__)
     numChannels = 1
     valMin, valMax = None, None
     dataTmp = None
     dataType = type(data[0]).__name__
     absMax = None
     if dataType in ['list', 'ndarray']:
         numChannels = len(data)
         n = len(data[0])
         dataTmp = numpy.zeros((n, numChannels))
         for chIdx in range(numChannels):
             dataTmp2 = None
             dType2 = type(data[chIdx]).__name__
             if dType2 == 'ndarray':
                 dataTmp2 = data[chIdx]
             elif dType2 == 'list':
                 dataTmp2 = numpy.array(data[chIdx], dtype=numpy.float32)
             else:
                 raise Exception("channel data is not a list or a numpy array")
             if normalize:
                 if removeDcWhenNormalizing:
                     dataTmp2 -= dspUtil.nanMean(dataTmp2)
                 absMax = dspUtil.getAbsMax(dataTmp2)
                 dataTmp2 /= absMax * 1.000001
             dataTmp[0:, chIdx] = dataTmp2
             del dataTmp2
     else:
         # this is a mono file
         # force creating a copy, to avoid scaling the original data...
         dataTmp = numpy.array(data) 
         if normalize:
             if removeDcWhenNormalizing:
                 dataTmp -= dspUtil.nanMean(dataTmp)
             absMax = dspUtil.getAbsMax(dataTmp)
             if absMax != 0:
                 dataTmp /= absMax * 1.000001
 
     # save
     #print dataTmp.dtype, dataTmp.shape
     dataTmp *= float(2**15 - 1)
     dataTmp2 = numpy.asarray(dataTmp, dtype=numpy.int16)
     sciWav.write(fileName, SRate, dataTmp2)
     del dataTmp, dataTmp2
     gc.collect(