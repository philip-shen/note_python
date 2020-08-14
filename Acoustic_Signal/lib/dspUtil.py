 import math
 import numpy
 import generalUtility
 import copy
 from matplotlib import pyplot as plt
 from scipy import stats
 from scipy import signal
 import myWave
 import os
 import praatUtil
 
 import scipy.misc 
 import scipy
 from scipy import signal as scisig
 
 scipy.factorial = scipy.misc.factorial
 import scipy.signal
 
 try:
     from scipy import weave as weave
 except:
     import weave
     
 
 
 DSP_MIDDLE_C = 440.0 * math.pow(2.0, (-9.0 / 12.0))
 LOG10_TWO = 0.301029995664
 
 LOOKUP_TABLE_NONE = 0
 LOOKUP_TABLE_SINE = 1
 LOOKUP_TABLE_COSINE = 2
 LOOKUP_TABLE_HAMMING = 3
 LOOKUP_TABLE_HANN = 4
 #LOOKUP_TABLE_GAUSSIAN = 5
  
 
 def normalize(data, maxOut = 1.0, minOut = 0.0):
     dataType = type(data).__name__
     data = copy.deepcopy(data)
     if dataType == 'ndarray':
         maxIn = numpy.nanmax(data)
         minIn = numpy.nanmin(data)
         data -= float(minIn)
         factor = (maxOut - minOut) / (maxIn - minIn)
         data *= factor
         data += minOut
         return data
     if dataType == 'list':
         maxIn = max(data)
         minIn = min(data)
         factor = (maxOut - minOut) / (maxIn - maxIn)
         for i in range(len(data)):
             val = data[i]
             val -= minIn
             val *= factor
             val += minOut
         return data
     raise Exception("only works on a numpy array or a list")
         
 
 
 
 def getFrameIndex(t, fs):
     return int(round(float(t) * float(fs)))
 
 
 
 
 def extractSegment(signal, fs, tStart, tEnd, wavFileName = None,
         overwriteExistingFile = False, doNormalize = False):
     
     n = len(signal)
     offsetL = getFrameIndex(tStart, fs)
     offsetR = getFrameIndex(tEnd, fs)
     
     if offsetL >= offsetR:
         raise Exception("start time must be below end time")
     if offsetL < 0:
         raise Exception("negative start time not allowed")
     if offsetR >= n:
         raise Exception("end time out of range")
         
     arrOut = signal[offsetL:offsetR]
     
     if not wavFileName is None:
         if os.path.isfile(wavFileName) and overwriteExistingFile != True:
             raise Exception("output file '%s' already exists" % wavFileName)
         myWave.writeWaveFile(arrOut, wavFileName, SRate = fs, 
             normalize = doNormalize, removeDcWhenNormalizing = False)
             
     return arrOut
     
 
 
 
 def getTimeIndices(signal, fs):
     n = len(signal)
     arrT = numpy.zeros(n)
     for i in range(n):
         arrT[i] = float(i) / float(fs)
     return arrT
 
 
 
 
 def containsNanInf(data):
     for val in data:
         if numpy.isnan(val): return True
         if numpy.isinf(val): return True
     return False
     
 
 
 
 def getValMax(
     data,
     ignoreNan = True,
     ignoreInf = True,
 ):
     raise Exception("this function is deprecated (performance too slow!). use numpy.nanmax instead")
     valMax = numpy.nan
     n = len(data)
     for i in range(n):
         val = data[i]
         consider = True
         if ignoreNan == True and numpy.isnan(val):
             consider = False
         if ignoreInf == True and numpy.isinf(val):
             consider = False
         if consider:
             if numpy.isnan(valMax):
                 valMax = val
             else:
                 if val > valMax:
                     valMax = val
     return valMax
         
 
 
 
 def getValMin(
     data,
     ignoreNan = True,
     ignoreInf = True,
 ):
     raise Exception("this function is deprecated (performance too slow!). use numpy.nanmin instead")
     valMin = numpy.nan
     n = len(data)
     for i in range(n):
         val = data[i]
         consider = True
         if ignoreNan == True and numpy.isnan(val):
             consider = False
         if ignoreInf == True and numpy.isinf(val):
             consider = False
         if consider:
             if numpy.isnan(valMin):
                 valMin = val
             else:
                 if val < valMin:
                     valMin = val
     return valMin
         
 
 
 
 def getAbsMax(data):
     n = len(data)
     valMin = None
     valMax = None
     for i in range(n):
         x = data[i]
         if (not math.isnan(x)) and (not math.isinf(x)) and (not x is None):
             if valMin is None:
                 valMin = x
                 valMax = x
             else:
                 if x < valMin: valMin = x
                 if x > valMax: valMax = x
     absMax = valMax
     if valMin is None:
         raise Exception("no min/max values found, all nan or None")
     if valMin < 0:
         if abs(valMin) > valMax:
             absMax = abs(valMin)
     return absMax
         
 
 
 
 def nanMean(data):
     cnt = 0
     sum = 0
     for val in data:
         if not val is None:
             if not numpy.isnan(val):
                 sum += val
                 cnt += 1
     if cnt == 0:
         return numpy.NaN
     return float(sum) / float(cnt)
         
 
 
 
 def createLookupTable(size, type = LOOKUP_TABLE_HAMMING):
     data = numpy.zeros(size)
     for i in range(size):
         xrel = float(i) / float(size)
         if type == LOOKUP_TABLE_NONE:
             tmp = 1
         elif type == LOOKUP_TABLE_SINE:
             tmp = math.sin (xrel * math.pi * 2)
         elif type == LOOKUP_TABLE_COSINE:
             tmp = math.cos (xrel * math.pi * 2)
         elif type == LOOKUP_TABLE_HAMMING:
             tmp = 0.54 - 0.46 * math.cos(2 * math.pi * xrel)
         elif type == LOOKUP_TABLE_HANN:
             tmp = 0.5 - 0.5 * math.cos(2 * math.pi * xrel)
         #elif type == LOOKUP_TABLE_GAUSSIAN:
         #   // y = exp(1) .^ ( - ((x-size./2).*pi ./ (size ./ 2)) .^ 2 ./ 2);
         #   tmp = pow((double)exp(1.0), (double)(( - pow ((double)(((FLOAT)x-table_size / 2.0) * math.pi / (table_size / 2.0)) , (double)2.0)) / 2.0));
         else:
             raise Exception('type ' + str(type) + ' not recognized')
         data[i] = tmp
     return data
 
 
 
 
 class CPulseGenerator:
     
     def __init__(self, freq = 100.0, samplingRate = 44100.0):
         self.samplingRate = float(samplingRate)
         self.setFreq(freq)
         self.reset()
         
     def reset(self):
         self.frameCount = self.framesPerCycle
         
     
     def setFreq(self, freq):
         self.freq = freq
         self.framesPerCycle = float(self.samplingRate) / float(freq) 
 
     
     def tick(self, f0 = None):
         #tmp = self.freq / self.samplingRate
         if f0:
             self.setFreq(f0)
         val = 0
         if self.frameCount >= self.framesPerCycle:
             val = 1
             self.frameCount = 0
         self.frameCount += 1
         return val
     
 
 
 
 class osc:
     
     def __init__(self, freq = 100.0, samplingRate = 44100.0):
         self.freq = float(freq)
         self.samplingRate = float(samplingRate)
         self.reset()
     
     def reset(self):
         self.phaseIncrement = 0
         self.phase = 0
         self.setPhaseIncrement()
         self.numCycles = 0
         
     
     def setPhaseIncrement(self):
         period = self.samplingRate / float(self.freq)
         self.phaseIncrement = (math.pi * 2.0) / period
 
     
     def tick(self, f0 = None):
         #tmp = self.freq / self.samplingRate
         if f0:
             self.setFreq(f0)
         val = math.sin(self.phase)
         self.incrementPhase()
         return val
         
     
     def setPhase(self, phase):
         self.phase = phase
 
     
     def getPhase(self):
         return self.phase
         
     
     def setFreq(self, freq):
         self.freq = freq
         self.setPhaseIncrement()
             
     
     def incrementPhase(self):
         self.phase += self.phaseIncrement
         while (self.phase >= math.pi * 2.0):
             self.numCycles += 1
             self.phase -= math.pi * 2.0
     
 
         
 
 class additiveSynthesizer:
 
     
     
     def __init__(self, 
             numOscillators, 
             freq = 100.0, 
             spectralSlope = -12.0, 
             samplingRate = 44100.0,
             randomizePhases = False
     ):
     
         self.oscillatorBank = []
         self.spectralSlope = spectralSlope
         self.samplingRate = samplingRate        
         self.VTTFfmax = None
         self.arrVTTFamp = None
         tmp = 0
         for i in range(numOscillators):
             self.oscillatorBank.append(osc(freq * float(i + 1), samplingRate))
             oct = math.log(i + 1) / math.log(2)
             dB = oct * self.spectralSlope
             tmp = tmp + math.pow(10.0, ((dB) / 20.0))
         self.scalingFactor = 1.0 / tmp
         if randomizePhases:
             self.randomizePhases()
         
     def reset(self):
         for i in range(numOscillators):
             self.oscillatorBank[i].reset()
         
     
     def tick(self, f0 = None, ignoreAliasing = False):
         if f0:
             self.setFreq(f0)
         val = 0
         vttfBinWidth, vttfN = None, None
         if not self.VTTFfmax is None:
             vttfN = len(self.arrVTTFamp)
             vttfBinWidth = self.VTTFfmax / float(vttfN)
         for i in range(len(self.oscillatorBank)):
             f = self.oscillatorBank[i].freq
             if f < self.samplingRate / 2.0 or ignoreAliasing:
                 oct = math.log(i + 1) / math.log(2)
                 dB = oct * self.spectralSlope
                 amplitudeScaling = math.pow(10.0, ((dB) / 20.0))
                 # fade out partials if we approach Nyquist frequency, in order
                 # to avoid abrupt timbral changes (which would result in mini-
                 # clicks)
                 if f > self.samplingRate * 0.475 and not ignoreAliasing:
                     amplitudeScaling *= 1.0 - (f - self.samplingRate * 0.475) \
                         / (self.samplingRate * 0.025)
                 if not self.VTTFfmax is None:
                     # consider a vocal tract transfer function
                     A = None
                     if f <= self.VTTFfmax:
                         idx = int(f / vttfBinWidth)
                         if idx > 0 and idx < len(self.arrVTTFamp):
                             xRel = (f / vttfBinWidth - idx) / vttfBinWidth
                             A = generalUtility.interpolateLinear(self.arrVTTFamp[idx-1], self.arrVTTFamp[idx], xRel)
                         else:
                             A = self.arrVTTFamp[0]
                     else:
                         A = self.arrVTTFamp[-1] 
                     #print f, A, dbToRms(A)
                     amplitudeScaling *= dbToRms(A)
                 tmp = self.oscillatorBank[i].tick() * amplitudeScaling
                 val = val + tmp
         val = val * self.scalingFactor
         return val
         
     def setFreq(self, newFreq):
         for i in range(len(self.oscillatorBank)):
             self.oscillatorBank[i].setFreq(newFreq * (i + 1))
             
     
     def setVTTF(self, fMax, arrAmp):
         self.VTTFfmax = fMax
         self.arrVTTFamp = arrAmp
 
     def randomizePhases(self):
         for i in range(len(self.oscillatorBank)):
             ph = numpy.random.random() * numpy.pi * 2.0
             self.oscillatorBank[i].setPhase(ph)
 
         
 
 
 LINEAR = 0
 PARABOLIC = 1
 
 def getInterpolatedData(arrData, arrTimeOffsetsData, arrTimeOffsetsInterpolated,
         doIgnoreOutliers = True, interpolationMethod = LINEAR
     ):
     
     if not isinstance(arrTimeOffsetsInterpolated, numpy.ndarray):
         if not type(arrTimeOffsetsInterpolated).__name__ == 'list':
             raise Exception("arrTimeOffsetsInterpolated must either be a list or a numpy array")
         arrTimeOffsetsInterpolated = numpy.arange(arrTimeOffsetsInterpolated)
     arrTimeOffsetsInterpolated.sort()
     
     nTarget = len(arrTimeOffsetsInterpolated)
     nSource = len(arrData)
     if nSource != len(arrTimeOffsetsData):
         raise Exception("length of input arrays does not match!")
     tSource = arrTimeOffsetsData[0]
     
     # "fast-forward" to the first data point that can actually be 
     # retrieved from the data
     for startOffsetTarget in range(nTarget):
         t = arrTimeOffsetsInterpolated[startOffsetTarget]
         if t >= arrTimeOffsetsData[0]:
             break
         else:
             if not doIgnoreOutliers:
                 raise Exception("requested time offset (%f) not covered by input data" % t)
     
     # proper processing
     idxSource = 0
     arrDataOut = numpy.zeros(nTarget)
     arrT = numpy.zeros(nTarget)
     for i in range(nTarget):
         arrDataOut[i] = numpy.NaN
         arrT[i] = numpy.NaN
     tSource = arrTimeOffsetsData[idxSource]
     for idxTarget in range(startOffsetTarget, nTarget):
         tTarget = arrTimeOffsetsInterpolated[idxTarget]
         #print idxTarget, nTarget, tTarget, tSource
         if tTarget == tSource:
             arrDataOut[idxTarget] = arrData[idxSource]
             arrT[idxTarget] = tTarget
         elif tTarget < tSource:
             raise Exception("ERROR: inconsistent data")
         else:
             doIt = True
             while doIt:
                 #print "\t", idxSource
                 if idxSource + 1 >= nSource:
                     if not doIgnoreOutliers:
                         raise Exception("requested time offset (%f) not covered by input data" % t)
                     else:
                         doIt = False
                         break
                 tSource2 = arrTimeOffsetsData[idxSource + 1]
                 if tSource2 == tTarget:
                     arrDataOut[idxTarget] = arrData[idxSource]
                     arrT[idxTarget] = tTarget
                     doIt = False
                 elif tSource2 < tTarget:
                     idxSource += 1
                     if idxSource >= nSource:
                         if not doIgnoreOutliers:
                             raise Exception("requested time offset (%f) not covered by input data" % t)
                         else:
                             doIt = False
                             #break
                 else:
                     if tSource2 <= tSource:
                         raise Exception("error: input data time array not sorted")
                     dt = tSource2 - tSource
                     tRel = (t - tSource) / dt
                     val1 = arrData[idxSource]
                     val2 = arrData[idxSource + 1]
                     valOut = 0
                     if interpolationMethod == LINEAR:
                         valOut = generalUtility.interpolateLinear(val1, val2, tRel)
                     elif interpolationMethod == PARABOLIC:
                         raise Exception("not implemented yet. sorry.")
                         if tRel > 0.5:
                             valOut = generalUtility.interpolateParabolic(val1, 
                                 val2, arrData[idxSource+2], tRel-1)
                         else:
                             valOut = generalUtility.interpolateParabolic(arrData[idxSource-1], 
                                 val1, val2, tRel)
                     else:
                         raise Exception("interpolation method not recognized")
                     arrDataOut[idxTarget] = valOut
                     arrT[idxTarget] = tTarget
                     doIt = False
                     #break
                             
     return arrT, arrDataOut
 
 
 
 
 def getCommonTimeOffsets(arr1, arr2, timeStep):
     arrIdx = []
     recentIdx2 = 0
     n2 = len(arr2)
     dt = float(timeStep) * 0.50000001
     for idx1, t1 in enumerate(arr1):
         for idx2 in range(recentIdx2, n2):
             t2 = arr2[idx2]
             tmp = abs(t1 - t2)
             if tmp <= dt:
                 recentIdx2 = idx2 + 1
                 arrIdx.append([idx1, idx2])
                 break
     return arrIdx
 
 
 
 
 def alignTimeSeries(arrT1, arrData1, arrT2, arrData2, timeStep):
     #arrIdx = getCommonTimeOffsets(arrT1, arrT2, timeStep)
     tMin = arrT1[0]
     tMax = arrT1[-1]
     if arrT2[0] < tMin:
         tMin = arrT2[0]
     if arrT2[-1] > tMax:
         tMax = arrT2[-1]
     duration = tMax - tMin
     n = int(round(duration / float(timeStep))) + 1
     tStart = int(round(tMin / float(timeStep))) * float(timeStep)
     arrT = numpy.zeros(n)
     arrDataOut = [
         numpy.zeros(n) * numpy.nan,
         numpy.zeros(n) * numpy.nan
     ]
     for i in range(n):
         arrT[i] = tStart + float(i) * timeStep
     arrTin = [arrT1, arrT2]
     arrDataIn = [arrData1, arrData2]
     for channelIdx in range(2):
         for i, t in enumerate(arrTin[channelIdx]):
             idx = int(round(t / float(timeStep)))
             arrDataOut[channelIdx][idx] = arrDataIn[channelIdx][i]
             #print channelIdx, i, t, idx
     return arrT, arrDataOut[0], arrDataOut[1]
 
 
 
 
 def mapOntoTimeLine(arrTmaster, arrTdata, arrData, ignoreOutOfBoundsErrors = False):
     arrDrv = toDerivative(arrTmaster, derivativeType=DERIVATIVE_TYPE_FORWARD,
         shortenArrayByOne=True)
     if arrDrv.std() > 0.00000000001:
         raise Exception("the master time series must have a constant time step")
     timeStep = arrDrv[0]
     n = len(arrTmaster)
     arrDataOut = numpy.ones(n) * numpy.nan
     for i, t in enumerate(arrTdata):
         idx = int(round(t / float(timeStep)))
         if idx < 0 or idx >= n:
             if not ignoreOutOfBoundsErrors:
                 print i, len(arrTdata)
                 raise Exception("time offset %f is out of bounds (%f - %f)" % \
                     (t, arrTmaster[0], arrTmaster[-1]))
         arrDataOut[idx] = arrData[i]
     return arrDataOut
 
 
 
 
 def roundToPowerOfTwo(val, alwaysRoundUp = True):
     tmp = numpy.log2(val)
     if alwaysRoundUp:
         if tmp != int(tmp):
             tmp = int(tmp) + 1
     else:
         tmp = int(round(tmp))
     return int(pow(2, tmp))
 
 
     
 
 def calculateRMS(data, convertToDb = False):
     
     """
     # obsolete code, keep for now, just to be sure...
     tmp = 0
     size = len(data)
     for i in range(size):
         tmp += data[i]
     mean = tmp / float(size)
     #print "mean: ", mean
     tmp = 0
     for i in range(size):
         tmp2 = data[i] - mean
         tmp += tmp2 * tmp2
     tmp /= float(size)
     if convertToDb:
         return rmsToDb(math.sqrt(tmp))
     return math.sqrt(tmp)
     """
     
     # this is the new "speedy" implementation using weave
     code = """
     float tmp = 0;
     int i;
     for (i = 0; i < size; i++) {
         tmp += data[i];
     }
     float mean = tmp / (float) size;
     //printf ("mean: %f", mean);
     tmp = 0;
     for (i = 0; i < size; i++) {
         float tmp2 = data[i] - mean;
         tmp += tmp2 * tmp2;
     }
     tmp /= (float)size;
     return_val = sqrt(tmp);
     """
     
     support = "#include <math.h>"
     size = len(data)
     RMS = weave.inline(code,['data', 'size'], verbose=0, support_code = support)
     
     if convertToDb:
         return rmsToDb(RMS)
     return RMS
     
     
 
     
 
 def calculateRmsOfSignal(
         data, # an array containing the signal
         windowSize, # in milli-seconds
         samplingFrequency, # Hz
         overlap = 0, # overlap between individual windows, specified in milli-seconds
         convertToDb = False
     ):
     if windowSize < 1:  
         raise Exception("window size must not below 1 ms")
     t = 0
     numFrames = len(data)
     duration = numFrames / float(samplingFrequency)
     if overlap >= windowSize:
         raise Exception("overlap must not exceed window size")
     readProgress = (windowSize - overlap) / 1000.0
     outputSize = int(duration / readProgress)
     dataX = numpy.zeros(outputSize)
     dataY = numpy.zeros(outputSize)
     t = 0
     halfWindowSize = windowSize / 2000.0
     for idx in range(outputSize):
         left = int((t - halfWindowSize) * float(samplingFrequency))
         right = left + int(windowSize * float(samplingFrequency) / 1000.0)
         if right >= numFrames: right = numFrames - 1
         numFramesLocal = right - left
         #print idx, t, left, right, readProgress
         if numFramesLocal <= 0:
             raise Exception("zero window size (t = " + str(t) + " sec.)")
         dataTmp = numpy.zeros(numFramesLocal)
         for i in range(numFramesLocal):
             dataTmp[i] = data[i + left]
         dataX[idx] = t 
         t += readProgress
         rms = calculateRMS(dataTmp)
         if convertToDb:
             if rms > 0:
                 dataY[idx] = rmsToDb(rms)
             else:
                 dataY[idx] = numpy.nan
         else:
             dataY[idx] = rms
     return dataX, dataY
     
 
 
 POWER_QUANTITY = 1 # energy, power
 FIELD_QUANTITY = 2 # pressure
 
 def rmsToDb(
         rmsValue, 
         valueType = FIELD_QUANTITY, 
         dbBase = 0, 
         rmsBase = 1.0 
     ):
 
     factor = None
     if valueType == FIELD_QUANTITY: factor = 20.0
     elif valueType == POWER_QUANTITY: factor = 10.0
     else:
         raise Exception("undefined value type (must be either FIELD_QUANTITY " \
             + "or POWER_QUANTITY")
 
     if not isinstance(rmsValue, numpy.ndarray):
         if rmsValue <= 0:
             raise Exception("RMS value must not be zero or below")
     return dbBase + (factor * numpy.log10(rmsValue / float(rmsBase)))
     
 
     
 
 def dbToRms(
         dbValue,  
         valueType = FIELD_QUANTITY, 
         dbBase = 0, 
         rmsBase = 1.0 
     ):
     divisor = None
     if valueType == FIELD_QUANTITY: divisor = 20.0
     elif valueType == POWER_QUANTITY: divisor = 10.0
     else:
         raise Exception("undefined value type (must be either FIELD_QUANTITY " \
             + "or POWER_QUANTITY")
     return rmsBase * numpy.power(10.0, ((dbValue - dbBase) / divisor))
     
 
 
 
 def getSoundPressure(SPL, valueType = FIELD_QUANTITY, p0 = 0.00002):
     divisor = None
     if valueType == FIELD_QUANTITY: divisor = 20.0
     elif valueType == POWER_QUANTITY: divisor = 10.0
     else:
         raise Exception("undefined value type (must be either FIELD_QUANTITY " \
             + "or POWER_QUANTITY")
     return p0 * numpy.power(10, SPL / float(divisor))
 
 
 
 
 def calculateDbWeighting(f):
 
     C1000 = -0.062
     A1000 = -2.0
 
     D = math.sqrt(0.5)
 
     fa = 10.0 ** 2.45
     fh = 10.0 ** 3.9
     fl = 10 ** 1.5
     fr = 1000.0
 
     frSq = fr * fr
     flSq = fl * fl
     fhSq = fh * fh
 
     b = (1.0 / (1.0 - D)) * (frSq + (flSq * fhSq /frSq) - D * (flSq + fhSq))
     c = flSq * fhSq
 
     f1 = math.sqrt((-b-math.sqrt(b * b - 4.0 * c)) / 2.0)
     f2 = ((3.0 - math.sqrt(5.0)) / 2.0) * fa
     f3 = ((3.0 + math.sqrt(5.0)) / 2.0) * fa
     f4 = math.sqrt((-b+math.sqrt(b * b - 4.0 * c)) / 2.0)
 
     #print f, f1, f2, f3, f4
 
     fSqu = f * f
     f1Squ = f1 * f1
     f2Squ = f2 * f2
     f3Squ = f3 * f3
     f4Squ = f4 * f4
 
     tmp = (fSqu + f1Squ) * (fSqu + f4Squ)
     Cf = 20.0 * math.log10((f4Squ * fSqu) / tmp) - C1000
     tmp *= math.sqrt(fSqu + f2Squ) * math.sqrt(fSqu + f3Squ)
     Af = 20.0 * math.log10((f4Squ * fSqu * fSqu) / tmp) - A1000
 
     return [Af, Cf]
 
 
 
 WEIGHTING_A = 'A'
 WEIGHTING_C = 'C'
 WEIGHTING_Z = 'Z'
 
 
 def simulateDbWeighting(signal, fs, measuredSPL, originalWeighting,
         lowerCutoff = 20, upperCutoff = None):
 
     if not originalWeighting in [WEIGHTING_A, WEIGHTING_C, WEIGHTING_Z]:
         raise Exception("parameter 'originalWeighting' must either be A, C, or Z")
 
     # convert from dB(C) to dB(A)
     RMS = calculateRMS(signal, convertToDb = False)
     calVal = measuredSPL - rmsToDb(RMS, valueType = POWER_QUANTITY)
     spectrumX, spectrumY = calculateFFT(signal, fs, len(signal),
         applyWindow = False, convertToDb = False,
         spectrumType = POWER_SPECTRUM, zeroPaddingFactor = 1
     )
     # plt.plot(spectrumX, spectrumY)
     # plt.show()
     spectrumY /= spectrumY.sum()
     spectrumY *= RMS
     arrTmp = {
         WEIGHTING_A: numpy.ones(len(spectrumY)) * numpy.nan,
         WEIGHTING_C: numpy.ones(len(spectrumY)) * numpy.nan,
         WEIGHTING_Z: numpy.ones(len(spectrumY)) * numpy.nan,
     }
     for i, f in enumerate(spectrumX):
         if f >= lowerCutoff:
             if f == 0:
                 # ignore DC offset
                 for w in [WEIGHTING_A, WEIGHTING_C, WEIGHTING_Z]:
                     arrTmp[w][i] = 0
             else:
                 rms_Z = numpy.nan
                 A, C = calculateDbWeighting(f)
                 factor_A = dbToRms(A, valueType = POWER_QUANTITY)
                 factor_C = dbToRms(C, valueType = POWER_QUANTITY)
                 # first compute Z weighted value, then all the others
                 if originalWeighting == WEIGHTING_A:
                     rms_Z = spectrumY[i] / factor_A
                 elif originalWeighting == WEIGHTING_C:
                     rms_Z = spectrumY[i] / factor_C
                 elif originalWeighting == WEIGHTING_Z:
                     rms_Z = spectrumY[i]
                 else:
                     raise Exception("unrecognized dB weighting indicator (%s)" \
                         % str(originalWeighting))
                 arrTmp[WEIGHTING_A][i] = rms_Z * factor_A
                 arrTmp[WEIGHTING_C][i] = rms_Z * factor_C
                 arrTmp[WEIGHTING_Z][i] = rms_Z
     RMS_A = numpy.nansum(arrTmp[WEIGHTING_A])
     RMS_C = numpy.nansum(arrTmp[WEIGHTING_C])
     RMS_Z = numpy.nansum(arrTmp[WEIGHTING_Z])
     if 1 == 2:
         # debug
         plt.clf()
         ax = plt.subplot(111)
         ax.plot(spectrumX, rmsToDb(arrTmp[WEIGHTING_A]), label="dB(A)")
         ax.plot(spectrumX, rmsToDb(arrTmp[WEIGHTING_C]), label="dB(C)")
         ax.plot(spectrumX, rmsToDb(arrTmp[WEIGHTING_Z]), label="dB(Z)")
         ax.grid()
         ax.set_xlabel("Frequency [Hz]")
         ax.set_ylabel("Level (dB)")
         ax.legend(loc='best')
         plt.show()
         exit(1)
     A = rmsToDb(RMS_A, valueType = POWER_QUANTITY) + calVal
     C = rmsToDb(RMS_C, valueType = POWER_QUANTITY) + calVal
     Z = rmsToDb(RMS_Z, valueType = POWER_QUANTITY) + calVal
     return A, C, Z
 
 
 
 
 def hertzToCents(
         freq, 
         baseFreq = DSP_MIDDLE_C 
     ):
     return 1200.0 * (numpy.log10(freq / baseFreq) / LOG10_TWO)
     
 
  
 
 def centsToHertz(
     cents, # the Cent value that should be converted to Hertz
     baseFreq = DSP_MIDDLE_C # the base frequency (must not be zero or below)
     ):
     return baseFreq * numpy.power(2.0, (cents / 1200.0))
     
 
 
 POWER_SPECTRUM = 0
 AMPLITUDE_SPECTRUM = 1
 
 def calculateFFT(
         data, 
         fs, 
         windowSize, 
         applyWindow = True, 
         convertToDb = False, 
         spectrumType = POWER_SPECTRUM,
         zeroPaddingFactor = 1
     ):
     # calculate the spectrum
     if not isinstance(data, numpy.ndarray):
         raise Exception("data must be a numpy array")
     dataTmp = data.copy()
     if applyWindow:
         fftWindow = createLookupTable(len(data), LOOKUP_TABLE_HANN)
         dataTmp *= fftWindow
     if len(dataTmp) != windowSize:
         # zero-pad to windowSize
         tmp = numpy.zeros(windowSize - len(dataTmp))
         dataTmp = numpy.hstack((dataTmp, tmp))
     if zeroPaddingFactor > 1:
         m = int(round(windowSize * float(zeroPaddingFactor)))
         dataTmp = numpy.hstack((dataTmp, numpy.zeros(m - windowSize)))
     n = len(dataTmp)
     fftBinWidth = fs / (float(n))
     X = numpy.fft.rfft(dataTmp)
     # get the power spectrum
     spectrumY = numpy.real(X*numpy.conjugate(X))
     spectrumX = numpy.zeros(len(spectrumY))
     spectrumY /= ((n * n) / 8.0)
     #spectrumY /= (n)
     for i in range(len(spectrumX)):
         spectrumX[i] = i * fftBinWidth
         val = spectrumY[i]
         if spectrumType == AMPLITUDE_SPECTRUM:
             val = numpy.sqrt(val)
         if convertToDb:
             try:
                 spectrumY[i] = rmsToDb(val)
             except Exception as e:
                 #print "WARNING:", e
                 spectrumY[i] = -999
         else:
             spectrumY[i] = val
         # amplitude spectrum, expressed in dB
         #spectrumY[i] = dspUtil.rmsToDb(math.sqrt(spectrumY[i]))
     #plt.plot(spectrumX, spectrumY)
     #plt.show()
     return spectrumX, spectrumY
     
 
 
 
 def stretchArray(data, newSize):
     n = len(data)
     X = numpy.fft.fft(data)
     #print len(X), len(data), newSize
     
     Xnew = numpy.zeros(newSize, dtype=X.dtype)
     m = n / 2
     if newSize/2 < m: m = newSize/2
     for i in range(m):
         Xnew[i] = X[i]
         Xnew[-i] = X[-i]
     dataOut = numpy.fft.ifft(Xnew)
     dataOut /= float(n)
     dataOut *= float(newSize)
     return numpy.real(dataOut)
 
 
 
 
 def calculateSpectrogram(
         data, 
         fs, 
         windowSize = 4096, 
         readProgress = 0.05, 
         fMax = 5000, 
         dynamicRange = 50,
         spectrumType = POWER_SPECTRUM,
         zeroPaddingFactor = 1
     ):
     
     duration = len(data) / float(fs)
     t = 0
     fftBinWidth = fs / (float(windowSize * zeroPaddingFactor))
     numBins = int(fMax / fftBinWidth)
     arrSpectrum = []
     valMax = 0
     numFrames = len(data)
     while t < duration:
         
         left = int(t * float(fs)) - windowSize / 2
         right = left + windowSize
         if left < 0: left = 0
         if right >= numFrames: right = numFrames - 1
         #print t, left, right, numFrames
         dataY = data[left:right].copy()
         
         spectrumX, spectrumY = calculateFFT(dataY, fs, windowSize, \
             applyWindow = True, convertToDb = False, 
             spectrumType = POWER_SPECTRUM, zeroPaddingFactor = zeroPaddingFactor)
         #spectrumY[0] = 0 # ignore DC
         limit = numBins
         if len(spectrumY) < limit: limit = len(spectrumY)
         #print numBins, len(spectrumY)
         for i in range(limit):
             spectrumY[i] = math.sqrt(spectrumY[i])
         arrSpectrum.append(spectrumY[:limit])
         tmp = max(spectrumY[:limit])
         if tmp > valMax: valMax = tmp
         
         t += readProgress
         
     #print valMax
     
     spectrogramData = numpy.zeros((numBins, len(arrSpectrum)))
     for x in range(len(arrSpectrum)):
         X = arrSpectrum[x]
         for y in range(len(X)):
             val = - dynamicRange
             try:
                 val = rmsToDb(X[y] / valMax)
                 #print val
             except Exception as e:
                 pass
             if val * -1.0 > dynamicRange:
                 val = dynamicRange * -1.0
             val += dynamicRange
             val /= dynamicRange
             val = math.sqrt(val)
             col = 1.0 - val
             spectrogramData[y][x] = col
     return spectrogramData
     
 
 
 
 def calculateReassignedSpectrogram(
         arrSignal,
         fs,
         windowSize,
         fftWindowSize = None,
         readProgress = None,
         windowType = LOOKUP_TABLE_HANN,
         verbose = False
     ):
     if not type(arrSignal).__name__ == 'ndarray':
         raise Exception("arrSignal must be a numpy array")
     if fftWindowSize is None: fftWindowSize = windowSize
     if fftWindowSize < windowSize:
         raise Exception("error: fftWindowSize (%s) must not be smaller than " \
             + "windowSize (%s)" % (str(fftWindowSize), str(windowSize)))
     
     if readProgress is None:
         readProgress = windowSize / 2
     
     TWOPI = numpy.pi * 2.0
     numFrames = len(arrSignal)
     numWindows = int((numFrames - windowSize) / float(readProgress)) + 1
     offset = windowSize / 2
     
     arrT = numpy.zeros(numWindows)
     arrCIF = []
     arrLGD = []
     arrA = []
     for windowIdx in range(numWindows):
         if verbose: print ("\t\t%d of %d" % (windowIdx + 1, numWindows))
         offset1 = offset - windowSize / 2
         offset2 = offset1 + windowSize
         if offset1 < 0: offset1 = 0
         if offset2 >= numFrames-1: offset2 = numFrames - 2
         arrData = [
             copy.deepcopy(arrSignal[offset1:offset2]),
             copy.deepcopy(arrSignal[offset1+1:offset2+1])
         ]
         t = float(offset) / float(fs)
         offset += readProgress
         
         # calculate F0
         if 1 == 2:
             arrF0 = calculateF0(arrData[0], fs, Fmin = 50, Fmax = 2000,
                 voicingThreshold = 0.1, applyWindow = False)
             f0 = numpy.array(arrF0['freq']).mean()
             #print "\t\tF0: %f" % f0
             if f0:
                 windowSize = int(round(float(fs) / f0))
                 windowSize *= 3 # three cycles
                 fftWindowSize = windowSize * 2
                 offset1 = offset - windowSize / 2
                 offset2 = offset1 + windowSize
                 if offset1 < 0: offset1 = 0
                 if offset2 >= numFrames-1: offset2 = numFrames - 2
                 arrData = [
                     copy.deepcopy(arrSignal[offset1:offset2]),
                     copy.deepcopy(arrSignal[offset1+1:offset2+1])
                 ]
         
         
         # apply window and zero-pad
         for data in arrData:
             fftWindow = createLookupTable(windowSize, LOOKUP_TABLE_HANN)
             data *= fftWindow
             if windowSize != fftWindowSize:
                 # zero-pad to windowSize
                 tmp = numpy.zeros(fftWindowSize - windowSize)
                 data = numpy.hstack((data, tmp))
         
         # calculate the FFT
         STFT = numpy.fft.rfft(arrData[0])
         STFTdel = numpy.fft.rfft(arrData[1])
         STFTfreqdel = copy.deepcopy(STFT)
         numBins = len(STFTfreqdel)
         tmp = STFTfreqdel[-1]
         for i in range(numBins - 2, -1, -1):
             STFTfreqdel[i+1] = STFTfreqdel[i]
         STFTfreqdel[0] = tmp
         
         # get the power spectrum
         fftBinWidth = fs / (float(windowSize))
         spectrumY = numpy.real(STFT*numpy.conjugate(STFT))
         spectrumX = numpy.zeros(len(spectrumY))
         spectrumY /= ((windowSize * windowSize) / 8.0)
         for i in range(len(spectrumX)):
             spectrumX[i] = i * fftBinWidth
             val = numpy.sqrt(spectrumY[i])
             try:
                 spectrumY[i] = rmsToDb(val)
             except Exception as e:
                 print ("WARNING: %s" % e)
                 spectrumY[i] = -999
         
         # compute the channelized instantaneous frequency (CIF)
         CIF = numpy.zeros(len(STFT))
         for i in range(numBins):
             Xdel = STFTdel[i]
             X = STFT[i]
             tmp = numpy.angle(Xdel) - numpy.angle(X)
             CIF[i] = (fs / TWOPI) * numpy.mod(tmp.real, TWOPI)
         
         # compute the localized group delay (LGD)
         LGD = numpy.zeros(len(STFT))
         for i in range(numBins):
             Xfreqdel = STFTfreqdel[i]
             X = STFT[i]
             tmp = numpy.angle(Xfreqdel) - numpy.angle(X)
             LGD[i] = (fftWindowSize / (fs * TWOPI)) * numpy.mod(tmp.real, TWOPI)    
             
         arrT[windowIdx] = t
         arrCIF.append(CIF)
         arrLGD.append(LGD)
         arrA.append(spectrumY)
     
     return (arrT, arrCIF, arrLGD, arrA)
 
 
 
 
 def calculateSpectralFlatness(powerSpectrum):
     geometricMean = numpy.float64(0)
     arithmeticMean = 0
     #print spectrumY, len(powerSpectrum)
     for i in range(len(powerSpectrum)):
         y = numpy.float64(powerSpectrum[i])
         #geometricMean *= y
         geometricMean += numpy.float64(math.log(y))
         arithmeticMean += y
         #print i, y, geometricMean
     #geometricMean = geometricMean ** (1.0 / len(spectrumY))
     geometricMean /= numpy.float64(len(powerSpectrum))
     geometricMean = math.exp(geometricMean)
     arithmeticMean /= float(len(powerSpectrum))
     spectralFlatness = geometricMean / arithmeticMean
     #print spectralFlatness, geometricMean, arithmeticMean
     return spectralFlatness
     
 
 
 
 def calculateF0once( 
     data, 
     fs, 
     Fmin = 50,
     Fmax = 3000,
     voicingThreshold = 0.3,
     applyWindow = False
 ):
     dataTmp = copy.deepcopy(data)
     
     # apply window
     if applyWindow:
         fftWindow = createLookupTable(len(dataTmp), LOOKUP_TABLE_HANN)
         dataTmp *= fftWindow
     
     # autocorrelation
     result = numpy.correlate(dataTmp, dataTmp, mode = 'full')
     r = result[result.size/2:] / float(len(data))
     
     # find peak in AC
     freq = numpy.nan
     try:
         xOfMax, valMax = generalUtility.findArrayMaximum(r,
             int(round(float(fs) / Fmax)),
             int(round(float(fs) / Fmin)))
         valMax /= max(r)
         freq = float(fs) / xOfMax
     except Exception as e:
         pass
     return freq
     
 
 
 
 def calculateF0( 
     data, 
     fs, 
     Fmin = 50,
     Fmax = 3000,
     numPeriods = 5.0,
     progressPeriods = 1,
     voicingThreshold = 0.3,
     applyWindow = False
 ):
     numFrames = len(data)
     readSize = int(numPeriods * float(fs) / Fmin)
     offset = 0
     numCycles = 0
     arrF0 = { 't':[], 'freq':[] }
     F0progressPeriods = progressPeriods
     while (offset < numFrames):
         dataTmp = numpy.zeros(readSize)
         for i in range(readSize):
             idx = i + offset - (readSize / 2)
             if idx >= 0 and idx < numFrames:
                 dataTmp[i] = data[idx]
         
         freq = calculateF0once(dataTmp, fs, Fmin = Fmin, Fmax = Fmax, 
             voicingThreshold = voicingThreshold, applyWindow = applyWindow)
         
         periodSize = 0
         if freq > 0:
             periodSize = fs / freq
         t = (offset + (periodSize / 2.0))/fs
         if freq >= Fmin and freq <= Fmax:
             arrF0['t'].append(t)
             arrF0['freq'].append(freq)
         else:
             # set F0 to zero if out of bounds
             arrF0['t'].append(t)
             arrF0['freq'].append(0)
             
         if periodSize > 10:
             offset += periodSize * progressPeriods
         else:
             offset += 10
     arrF0['t'] = numpy.array(arrF0['t'])
     arrF0['freq'] = numpy.array(arrF0['freq'])
     return arrF0
 
 
 
 
 def corr(
         signal1, # input array
         signal2, # the other input array
         alignSize = True, # if true, the shorter array is scaled to \
                           # the longer one
         octaveCost = 0.1, # favour higher harmonics - \
                            # see Praat and Boerma (1993)
         fMin = 10, # Hz
         fMax = 4000, # Hz
         fs = 44100, # sampling frequency
         zeroPaddingFactor = 2.0, # zero padding 
 ):
     MAX_FFT_LENGTH = 2**20
     
     signalSize1 = len(signal1)
     signalSize2 = len(signal2)
     if alignSize == False:
         if signalSize1 != signalSize2:
             raise Exception("the size of the two input signals does not match")
     
     signalSize = signalSize1
     if signalSize2 > signalSize: signalSize = signalSize2
     if signalSize <= 0 or signalSize >= MAX_FFT_LENGTH:
         raise Exception("the size of the input signals (" + str(signalSize) \
             + ") is out of range.")
     
     # make the actual window size a power of two
     targetWindowSize = int(signalSize * float(zeroPaddingFactor))
     realWindowSize = 1;
     while realWindowSize < targetWindowSize:
          realWindowSize *= 2
     
     if realWindowSize > MAX_FFT_LENGTH or realWindowSize < 1: 
         raise Exception("array size (" + str(realWindowSize) \
             + ") is not allowed (range = 1 - " + str(MAX_FFT_LENGTH) + ").")
     
     arrIn1 = numpy.zeros(realWindowSize)
     arrIn2 = numpy.zeros(realWindowSize)
     arrIn3 = numpy.zeros(realWindowSize / 2)
     
     # copy the input data to the object's input data array
     # since the target array is longer, it is automatically zero-padded
     for k in range(signalSize1):
         arrIn1[k] = signal1[k]
     for k in range(signalSize2):
         arrIn2[k] = signal2[k]
     
     # calculate the FFTs
     arrFft1 = numpy.fft.rfft(arrIn1)
     arrFft2 = numpy.fft.rfft(arrIn2)
     
     # multiply result 1 with complex conjugate of result 2 and store it.
     for k in range(realWindowSize / 2):
         arrIn3[k] = arrFft1[k].conjugate() * arrFft2[k]
     
     # do the reverse fftp
     r = numpy.fft.irfft(arrIn3) * 2.0
     r /= r[0]
     
     # favour smaller lags (avoid period doubling/tripling ...)
     for i in range(len(r)):
         r[i] *= 1.0 - i * octaveCost / len(r)
     
     # find the maximum in the lag function
     pMax = float(fs) / fMax
     pMin = float(fs) / fMin
     if pMin > signalSize - 1:
         pMin = signalSize - 1
     xOfMax, valMax = findArrayMaximum(r, int(pMax), int(pMin))
     
     return xOfMax * -1.0, r
 
 
     
 
 def calculateTimeVaryingDominantFrequency(signal, fs, timeStep = 0.01,
         windowSize = 2048, fMin = 0, fMax = None, applyWindow = True,
         fftZeroPaddingFactor = 1
     ):
 
     n = len(signal)
     duration = float(n) / float(fs)
     arrT = []
     arrDF = []
     t = 0
     while t < duration:
         offset = int(round(t * float(fs)))
         o1 = offset - windowSize / 2
         o2 = offset + windowSize / 2
         if o1 < 0: o1 = 0
         if o2 >= n: o2 = n-1
         df = calculateDominantFrequency(signal[o1:o2], fs, fMin = fMin,
             fMax = fMax, applyWindow = applyWindow,
             fftZeroPaddingFactor = fftZeroPaddingFactor)
         arrT.append(t)
         arrDF.append(df)
         t += timeStep
     arrT = numpy.array(arrT, dtype = numpy.float32)
     arrDF = numpy.array(arrDF, dtype = numpy.float32)
     return arrT, arrDF
 
 
 
 
 def calculateDominantFrequency(signal, fs, fMin = 0, fMax = None, applyWindow = True,
         fftZeroPaddingFactor = 1
     ):
     n = len(signal)
     signalTmp = copy.deepcopy(signal)
     if applyWindow:
         fftWindow = createLookupTable(len(signalTmp), LOOKUP_TABLE_HANN)
         signalTmp *= fftWindow
     if fftZeroPaddingFactor > 1:
         m = int(round(n * fftZeroPaddingFactor))
         signalTmp = numpy.append(signalTmp, numpy.zeros(m - n))
     spectrumX, spectrumY = calculateFFT(signalTmp, fs, len(signalTmp), 
             applyWindow = False, convertToDb = True, 
             spectrumType = AMPLITUDE_SPECTRUM)
 
     binWidth = spectrumX[1] - spectrumX[0]
     idx1 = 0
     if fMin > 0:
         idx1 = int(round(fMin / float(binWidth)))
     idx2 = -1
     if fMax > 0:
         idx2 = int(round(fMax / float(binWidth)))
     domFreq = numpy.nan
     try:
         domFreq, dummy = generalUtility.findArrayMaximum(spectrumY, idx1, idx2, doInterpolate = True)
         domFreq *= binWidth
     except Exception as e:
         pass
 
     # domFreq = None
     # eMax = None
     # if fMax is None:
     #   fMax = fs / 2.0
     # for i in range(len(spectrumY)):
     #   f = spectrumX[i]
     #   if f >= fMin and f <= fMax:
     #       if domFreq is None:
     #           domFreq = spectrumX[i]
     #           eMax = spectrumY[i]
     #       else:
     #           if spectrumY[i] > eMax:
     #               domFreq = spectrumX[i]
     #               eMax = spectrumY[i]
     # print domFreq, domFreq2
     return domFreq
 
 
     
 
 def calculateAlphaRatio(
         data, 
         fs, 
         cutoff = 1000, 
         fMin = 50, 
         fMax = 5000, 
         debugGraphOutputFileName = '', 
         returnSpectrum = False
     ):
     windowSize = len(data)
     # calculate the FFT
     fftWindow = createLookupTable(windowSize, LOOKUP_TABLE_HANN)
     dataTmp = data * fftWindow
     fftBinWidth = fs / (float(windowSize))
     X = numpy.fft.rfft(dataTmp)
     # get the power spectrum
     spectrumY = numpy.real(X*numpy.conjugate(X))
     spectrumX = numpy.zeros(len(spectrumY))
     spectrumY /= (windowSize)
     for i in range(len(spectrumX)):
         spectrumX[i] = i * fftBinWidth
         # amplitude spectrum, expressed in dB
         #spectrumY[i] = dspUtil.rmsToDb(math.sqrt(spectrumY[i]))
         spectrumY[i] = math.sqrt(spectrumY[i])
     #plt.plot(spectrumX, spectrumY)
     #plt.show()
     # normalize
     #spectrumY -= spectrumY.max()
     lBound = int(round(float(fMin) / fftBinWidth))
     rBound = int(round(float(fMax) / fftBinWidth))
     center = int(float(cutoff) / fftBinWidth)
     e1 = 0
     e2 = 0
     #print lBound, center, rBound, fftBinWidth
     for i in range(lBound, center + 1):
         e1 += spectrumY[i]
     for i in range(center + 1, rBound + 1):
         e2 += spectrumY[i]
     #print e1, e2
     
     alphaRatio = rmsToDb(e2) - rmsToDb(e1)
     
     if debugGraphOutputFileName != '':
         plt.clf()
         plt.subplot(211)
         plt.plot(data)
         plt.grid()
         plt.title('.'.join(debugGraphOutputFileName.split('/')[-1].split('.')[:-1]))
         plt.subplot(212)
         plt.plot(spectrumX, spectrumY)
         plt.grid()
         plt.xlabel("Frequency [Hz]")
         plt.ylabel("Amplitude")
         txt = ('%3.3f' % e1) + ' / ' + ('%3.3f' % e2) + ' -> ' \
             + ('%3.3f' % alphaRatio) + ' dB'
         plt.text(500, spectrumY.max() * 0.9, txt)
         plt.savefig(debugGraphOutputFileName)
     
     if returnSpectrum:
         return alphaRatio, spectrumX, spectrumY
     return alphaRatio
 
 
 
 def calculateSpectralSlopeOfSignal(
         data, 
         fs,
         arrT,
         arrFo,
         windowDuration = 0.1, # seconds
         numPartials = 30, 
         zeroPaddingFactor = 2.0, 
         peakDetectionThresholdAboveNoiseLevel = 10, 
         peakFMax = 5000, 
         peakFMin = 50
     ):
     n = len(data)
     arrSlope = []
     arrIntercept = []
     for i, t in enumerate(arrT):
         fo = arrFo[i]
         gradient, intercept = numpy.nan, numpy.nan
         if fo > 0:
             t1 = t - windowDuration * 0.5
             t2 = t + windowDuration * 0.5
             o1 = int(round(t1 * float(fs)))
             o2 = int(round(t2 * float(fs)))
             if o1 < 0: o1 = 0
             if o2 >= n: o2 = n-1
             if o1 < o2:
                 try:
                     tmp = calculateSpectralSlope(data[o1:o2], fs, fo,
                         numPartials = numPartials, zeroPaddingFactor = zeroPaddingFactor,
                         peakDetectionThresholdAboveNoiseLevel = peakDetectionThresholdAboveNoiseLevel,
                         peakFMax = peakFMax, peakFMin = peakFMin, returnPeaks = False )
                     gradient, intercept, r_value, p_value, std_err = tmp
                 except Exception as e:
                     pass
                     pass
         arrSlope.append(gradient)
         arrIntercept.append(intercept)
     return [arrSlope, arrIntercept]
 
 
 
 
 
 def calculateSpectralSlope(
         data,
         fs,
         f0,
         numPartials = 30,
         zeroPaddingFactor = 2.0,
         peakDetectionThresholdAboveNoiseLevel = 10,
         peakFMax = 5000,
         peakFMin = 50,
         returnPeaks = False
     ):
 
     doDebug = False
 
     if doDebug: print (f0, numPartials, peakDetectionThresholdAboveNoiseLevel)
 
     # calculate the FFT
     windowSize = len(data)
     fftWindow = createLookupTable(windowSize, LOOKUP_TABLE_HANN)
     dataTmp = data * fftWindow
     fftBinWidth = fs / (float(windowSize))
     X = numpy.fft.rfft(dataTmp)
     # get the power spectrum
     spectrumY = numpy.real(X*numpy.conjugate(X))
     spectrumX = numpy.zeros(len(spectrumY))
     spectrumY /= (windowSize)
     for i in range(len(spectrumX)):
         spectrumX[i] = i * fftBinWidth
         spectrumY[i] = math.sqrt(spectrumY[i]) # amplitude spectrum
         
     # normalize
     offset = int(peakFMax / float(fftBinWidth)) + 1
     averageAmplitude = spectrumY[:offset].mean()
     for i in range(len(spectrumY)):
         # convert to dB
         if spectrumY[i] > 0:
             spectrumY[i] = rmsToDb(spectrumY[i])
         else:
             spectrumY[i] = numpy.nan
     spectrumYmax = spectrumY.max()
     noiseFloor = rmsToDb(averageAmplitude) - spectrumYmax
     spectrumY -= spectrumYmax # normalize
     if doDebug: print ("noise floor:", noiseFloor)
     
     # calculate peaks
     c4 = 440 * 2 ** (-7/12.0)
     spectrumSize = len(spectrumY)
     arrPeaks = []
     numBins = int(float(peakFMax) / f0)
     for bin in range(numBins):
         binFreq = f0 * (bin + 1)
         binFMin = binFreq - f0 / 2.0
         binFMax = binFreq + f0 / 2.0
         lBound = int(binFMin / fftBinWidth) + 1
         rBound = int(binFMax / fftBinWidth)
         if rBound >= len(spectrumY):
             rBound = len(spectrumY) - 1
         #print binFMin, binFMax, lBound, rBound
         
         xOfMax = lBound
         valMax = spectrumY[lBound]
         for i in range(rBound - lBound):
             if valMax < spectrumY[i + lBound]:
                 valMax = spectrumY[i + lBound]
                 xOfMax = lBound + i
         freqOfMax = spectrumX[xOfMax]
         if freqOfMax <= peakFMax and freqOfMax >= peakFMin:
             #print "\t\tSpectral peak @", freqOfMax, "Hz:", valMax, "dB", 
             #   alpha, beta, gamma
             cents = hertzToCents(freqOfMax, c4)
             if len(arrPeaks) < numPartials:
                 noiseFloorTmp = spectrumY[lBound:rBound].mean()
                 if valMax >= peakDetectionThresholdAboveNoiseLevel + noiseFloorTmp:
                     arrPeaks.append([freqOfMax, cents, valMax])
         
     if doDebug: print ("\t\t", len(arrPeaks), "peak(s) found")
     if len(arrPeaks) < 1:
         if returnPeaks:
             return numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan, [], []
         else:
             return numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan
 
     fMax = arrPeaks[-1][0] + 100
     if fMax < 5000: fMax = 5000
     for bin in range(numBins):
         binFreq = f0 * (bin + 1)
         binFMin = binFreq - f0 / 2.0
         binFMax = binFreq + f0 / 2.0
 
     spectrumOct = numpy.zeros(spectrumSize - 1)
     for i in range(spectrumSize - 1):
         spectrumOct[i] = hertzToCents(spectrumX[i + 1], c4) / 1200.0
     numPeaks = len(arrPeaks)
     peaksX = numpy.zeros(numPeaks)
     peaksY = numpy.zeros(numPeaks)
     for i in range(numPeaks):
         peaksX[i] = arrPeaks[i][1] / 1200.0 # convert from cents to octave
         peaksY[i] = arrPeaks[i][2]
         if doDebug: print ('\t', arrPeaks[i][1], arrPeaks[i][2])
         
     for bin in range(numBins):
         binFreq = f0 * (bin + 1)
         binFMin = binFreq - f0 / 2.0
         binFMax = binFreq + f0 / 2.0
         
     # calculate the regression line
     if len(peaksX) > 1:
         xMin = peaksX.min() 
         xMax = peaksX.max()
         gradient, intercept, r_value, p_value, std_err = \
             stats.linregress(peaksX, peaksY)
         #print "\t\t", gradient, intercept, r_value ** 2
         if returnPeaks:
             harmFreq = []
             harmAmp = []
             for i, tmp in enumerate(arrPeaks):
                 harmFreq.append(tmp[0])
                 harmAmp.append(tmp[2])
             return gradient, intercept, r_value, p_value, std_err, harmFreq, harmAmp
         else:
             return gradient, intercept, r_value, p_value, std_err
     
     raise Exception("less than two partials detected. unable to calculate " \
         + "spectral slope")
 
 
 
 
 def movingAverager(data, width):
     sum = 0
     size = len(data)
     dataOut = numpy.zeros(size)
     halfWidth = int(width / 2)
     for i in range(size):
         offset1 = i - halfWidth
         offset2 = offset1 + width
         if offset1 < 0: offset1 = 0
         if offset2 >= size: offset2 = size
         n = offset2 - offset1
         if n > 0:
             tmp =numpy.nanmean(data[offset1:offset2])
             dataOut[i] = tmp
         else:
             dataOut[i] = numpy.nan
     return dataOut
 
 
 
 # def computeWeightedMovingAverage(arrT, arrData, windowSize):
 #   """
 #   compute the weighted moving average of an unregularly sampled time series
 #   :param arrT: a numpy array containing the time offsets
 #   :param arrData: a numpy array containing the data values
 #   :param windowSize: the window size (given in same units as the time offset
 #       array) over which the weighting should be applied
 #   :return: a numpy array containing the weighted moving average data
 #   """
 #
 #   arrValAvg = []
 #   offsetTmp = 0
 #   for idx, t in enumerate(arrT):
 #
 #       valTmp = 0
 #       weighting = 0
 #
 #       code = """
 #       float val = 0;
 #       float weighting = 0;
 #       for (int i2 = 0; i2 < n; i2++) {
 #           float t2 = (float)arrT[i2];
 #           float tDiff = t2 - (float)t;
 #           if (fabs(tDiff) <= windowSize / 2.0) {
 #               float w = 1.0 - fabs((float)tDiff / ((float)windowSize / 2.0));
 #               val += arrData[i2] * w;
 #               weighting += w;
 #           }
 #       }
 #       arrP[0] = weighting;
 #       arrP[1] = val;
 #       """
 #       support = "#include <math.h>"
 #       n = len(arrT)
 #       arrP = [0.0, 0.0]
 #       arrParams = ['t', 'arrT', 'arrData', 'n', 'windowSize', 'arrP']
 #       weave.inline(code, arrParams, verbose=0, support_code=support)
 #       weighting, valTmp = arrP
 #
 #       if weighting > 0:
 #           arrValAvg.append(valTmp / float(weighting))
 #       else:
 #           arrValAvg.append(numpy.nan)
 #
 #   #arrTavg = numpy.array(arrTavg, dtype=numpy.float32)
 #   arrValAvg = numpy.array(arrValAvg, dtype=numpy.float32)
 #   return arrValAvg
 
 
 
 def computeWeightedMovingAverage(arrT, arrData, windowSize, timeStep, tMin = None, tMax = None):
     if tMin is None: tMax = arrT.min()
     if tMax is None: tMax = arrT.max()
     def weightingFunction(tDiff, windowSize):
         assert (abs(tDiff) <= windowSize / 2.0)
         x = abs(tDiff / float(windowSize / 2.0))
         assert (x <= 1)
         assert (x >= 0)
         return 1 - x
     arrTavg, arrValAvg = [], []
     t = tMin
     while t < tMax + timeStep:
         valTmp = 0
         weighting = 0
         for idx, t2 in enumerate(arrT):
             tDiff = t2 - t
             if abs(tDiff) <= windowSize / 2.0:
                 w = weightingFunction(tDiff, windowSize)
                 valTmp += arrData[idx] * w
                 weighting += w
                 # if t2 > t + windowSize / 2.0:
                 #   break
         arrTavg.append(t)
         if weighting > 0:
             arrValAvg.append(valTmp / float(weighting))
         else:
             arrValAvg.append(numpy.nan)
         t += timeStep
     arrTavg = numpy.array(arrTavg, dtype=numpy.float32)
     arrValAvg = numpy.array(arrValAvg, dtype=numpy.float32)
     return arrTavg, arrValAvg
 
 
 
 
 def applyBandpassFilter(signal, fs, lowcut, highcut, order, doPreservePhase = True):
     nyq = 0.5 * fs
     low = lowcut / nyq
     high = highcut / nyq
     b, a = scipy.signal.butter(order, [low, high], btype='band')
     y = scipy.signal.lfilter(b, a, signal)
     if doPreservePhase:
         y = numpy.fliplr([y])[0]
         y = scipy.signal.lfilter(b, a, y)
         y = numpy.fliplr([y])[0]
     return y
 
 
 
 
 def applyCombFilter(signal, fs, fComb):
     dt = 0.5 / fComb
     di = int(round(dt * float(fs)))
     sig2 = signal[:-di] + signal[di:]
     return sig2 / 2.0
 
 
 
 
 def calculateDerivative(data):
     raise Exception("deprecated. use dspUtil.toDerivative(...) instead")
     dataOut = numpy.zeros(len(data))
     for i in range(len(data) - 1):
         dataOut[i] = data[i + 1] - data[i]
     return dataOut
 
 
 
 DERIVATIVE_TYPE_FORWARD = 1
 DERIVATIVE_TYPE_BACKWARD = 2
 DERIVATIVE_TYPE_CENTRAL = 3
 
 
 def toDerivative(
         data, 
         derivativeType = DERIVATIVE_TYPE_BACKWARD,
         normalize = -1,
         errorIfValMaxIsZero = False,
         shortenArrayByOne = False
     ):
     numFrames = len(data)
     drv = numpy.zeros(numFrames)
     if derivativeType == DERIVATIVE_TYPE_FORWARD:
         for i in range(numFrames - 1):
             drv[i] = data[i + 1] - data[i]
     elif derivativeType == DERIVATIVE_TYPE_BACKWARD:
         for i in range(numFrames - 1):
             drv[i + 1] = data[i + 1] - data[i]
     elif derivativeType == DERIVATIVE_TYPE_CENTRAL:
         for i in range(numFrames - 2):
             drv[i + 1] = data[i + 1] - data[i - 1]
     else:
         raise Exception("specified derivative type not valid")
     if shortenArrayByOne:
         if derivativeType == DERIVATIVE_TYPE_FORWARD:
             drv = drv[0:-1]
         elif derivativeType == DERIVATIVE_TYPE_BACKWARD:
             drv = drv[0:-1]
         elif derivativeType == DERIVATIVE_TYPE_CENTRAL:
             raise Exception("must not shorten array if central drv is computed")
     if normalize > 0:
         valMax = getAbsMax(drv)
         if valMax == 0:
             if errorIfValMaxIsZero:
                 raise Exception("maximum value of drv is 0 - can't normalize")
         else:
             scaling = normalize / valMax
             drv *= scaling
     return drv
 
 
 
 def integrate(signal, dcOffset = 0):
     n = len(signal)
     val = dcOffset
     out = numpy.zeros(n)
     for i in range(n):
         val += signal[i]
         out[i] = val
     return out
 
 
 
 
 def getHistogramEntropy(
         histogram,
         normalizeDistribution = True
     ):
 
     nHist = len(histogram)
     if nHist == 0:
         raise Exception("histogram is empty")
     H = 0
     divisor = sum(histogram)
     #print "Divisor:", divisor
     for binIdx in range(nHist):
         p = histogram[binIdx]
         if normalizeDistribution and divisor > 0:
             p /= float(divisor)
             pass
         #print binIdx, p
         if p > 0:
             H += (-1.0 * p * numpy.log2(p))
     return H
 
 
 
 
 def rotate(x, y, alpha, xCenter = 0, yCenter = 0):
     sinAlpha = math.sin(alpha)
     cosAlpha = math.cos(alpha)
     dx = x - xCenter
     dy = y - yCenter
     return xCenter + dx * cosAlpha - dy * sinAlpha, \
         yCenter + dx * sinAlpha + dy * cosAlpha 
 
 
 
 
 def calculateJitterPercent(data):
     return calculateJitterRatio(data) / 10.0
 
 
 
 
 def calculateJitterRatio(data):
     n = len(data)
     sum1 = 0
     sum2 = 0
     for i in range(n):
         if i > 0:
             sum1 += abs(data[i-1] - data[i])
         sum2 += data[i]
     sum1 /= float(n - 1)
     sum2 /= float(n)
     return 1000.0 * sum1 / sum2
 
 
 
 
 def calculateJitterFactor(data):
     n = len(data)
     dataF = numpy.zeros(n)
     for i in range(n):
         # convert from periods to F0 per cycle
         dataF[i] = 1.0 / data[i]
     sum1 = 0
     sum2 = 0
     for i in range(n):
         if i > 0:
             sum1 += abs(dataF[i] - dataF[i-1])
         sum2 += dataF[i]
     sum1 /= float(n - 1)
     sum2 /= float(n)
     return 100.0 * sum1 / sum2
 
 
 
 
 def calculatePeriodVariabilityIndex(data):
     data = numpy.array(data)
     n = len(data)
     sum = 0
     mean = data.mean()
     for i in range(n):
         tmp = data[i] - mean
         sum += tmp * tmp
     return 1000.0 * (sum / float(n)) / (mean*mean)
 
 
 
 
 def calculateRelativeAveragePerturbation(data):
     n = len(data)
     if n < 3:
         raise Exception("need at least three data points")
     sum1 = 0
     sum2 = 0
     for i in range(n):
         if i > 0 and i < (n-1):
             sum1 += abs((data[i-1] + data[i] + data[i+1]) / 3 - data[i])
         sum2 += data[i]
     sum1 /= float(n-2)
     sum2 /= float(n)
     return sum1 / sum2
 
 
 
 
 class CSeededRegionGrowingAlgorithm:
         
         
     class CCoord:
         def __init__(self, x, y):
             self.x = x
             self.y = y
 
     PX_EVALUATED = 1
     PX_INSIDE = 2
     PX_OUTSIDE = 3
     PX_INVALID = 4
 
     def __init__(self):
         pass
         
     
     def run(self,
         data, 
         seedPointX = None,
         seedPointY = None,
         threshold = None
     ):
             
         self.data = data    
         self.height = len(data)
         self.width = len(data[0])
         if seedPointX is None:
             seedPointX = int(self.width / 2.0)
         if seedPointY is None:
             seedPointY = int(self.height / 2.0)
         if type(data[0][0]).__name__ != 'float64':
             raise Exception("we expect to receive a 2D numpy array, where " \
                 + "each pixel is represented by exactly one grayscale value " \
                 + "[so no RGB data!]")
         
         self.threshold = threshold
         self.seedVal = data[seedPointY][seedPointX]
         self.arrProcessed = numpy.zeros((self.height, self.width))
         self.arrRegion = numpy.zeros((self.height, self.width))
         self.arrBorder = numpy.zeros((self.height, self.width))
         self.arrQueue = []
         
         coord = self.CCoord(seedPointX, seedPointY)
         self.arrQueue.append(coord)
         while len(self.arrQueue) > 0:
             self.processQueue()
         
     
     def processQueue(self):
         
         if len(self.arrQueue) < 1:
             raise Exception("list is empty")
         coord = self.arrQueue[-1]
         del self.arrQueue[-1]
         
         x = coord.x
         y = coord.y
         arrCoord = [[x-1,y], [x,y+1], [x+1,y], [x,y-1]]
         for c in arrCoord:
             pxStatus = self.evaluatePixel(c[0], c[1])
             if pxStatus == self.PX_INSIDE:
                 self.arrRegion[c[1]][c[0]] = 1
                 self.arrQueue.append(self.CCoord(c[0], c[1]))
             if pxStatus == self.PX_OUTSIDE:
                 self.arrBorder[y][x] = 1
         self.arrProcessed[y][x] = 1
         
     
     def evaluatePixel(self, x, y):
         if x < 0 or x >= self.width:
             return self.PX_INVALID
         if y < 0 or y >= self.height:
             return self.PX_INVALID
         if self.arrProcessed[y][x]:
             return self.PX_EVALUATED
         if self.threshold is None:
             if self.data[y][x] == self.seedVal:
                 return self.PX_INSIDE
         else:
             if self.data[y][x] < self.threshold:
                 return self.PX_INSIDE
         return self.PX_OUTSIDE
         
     def superimposeBorder(self, inputData = None):
         if inputData is None:
             inputData = self.data
         dataOut = numpy.zeros((self.height, self.width, 3))
         for x in range(self.width):
             for y in range(self.height):    
                 val = inputData[y][x]
                 if type(val).__name__ == 'ndarray':
                     val = (float(val[0]) + float(val[1]) + float(val[2])) / 3.0
                 if self.arrBorder[y][x] == 1:
                     val = [1, 0, 0]
                 else:
                     val = [val, val, val]
                 for z in range(len(val)):
                     dataOut[y][x][z] = val[z]
         return dataOut
 
 # ---------------------------------------------------------------------------- #
     
 
 def calculateFormant(
     F, # formant center frequency, Hz
     B, # formant bandwidth, Hz
     f, # frequency for which the gain factor is evaluated
     convertToRms = False
 ):
     
 
     halfBSquared = (B / 2.0) * (B / 2.0)
     tmp = (
         (F * F  + halfBSquared) /
         (numpy.sqrt((f - F)*(f - F) + halfBSquared)
         * numpy.sqrt((f + F)*(f + F) + halfBSquared)))
     if convertToRms:
         return tmp #math.pow(10.0, (tmp / 20.0))
     else:
         return 20.0 * numpy.log10(tmp)
 
 # ---------------------------------------------------------------------------- #
 
 
 def calculateVTTF(
         arrFormantFrequencies, 
         bandwidth,
         fMax,
         numDataPoints,
         lipDiameter = None,
         c = 350,
         rho = 1.14,
         convertToRms = False
     ):
     
     arrVTTF = numpy.zeros(numDataPoints)
     if convertToRms:
         arrVTTF = numpy.ones(numDataPoints)
     binWidth = fMax / float(numDataPoints) # [Hz]
     arrF = None
     dType = type(bandwidth).__name__
     arrBandwidth = []
     if dType in ['list', 'ndarray']:
         if len(bandwidth) != len(arrFormantFrequencies):
             raise Exception("length of formant frequency and bandwidth arrays does not match")
         arrBandwidth = bandwidth
     else:
         for i in range(len(arrFormantFrequencies)):
             arrBandwidth.append(float(bandwidth))
     for idx, formantFreq in enumerate(arrFormantFrequencies):
         arrF = numpy.zeros(numDataPoints)
         arrA = numpy.zeros(numDataPoints)
         B = arrBandwidth[idx]
         for i in range(numDataPoints):
             f = (1 + i) * binWidth
             arrF[i] = f
             arrA[i] = calculateFormant(formantFreq, B, f, convertToRms = convertToRms)
         if convertToRms:
             arrVTTF *= arrA
         else:
             arrVTTF += arrA
     arrVTTF -= arrVTTF.max()
 
     if lipDiameter > 0:
         arrF, arrRad = calculateLipRadiation(d = lipDiameter, fMax = fMax,
             freqSpacing = binWidth, c = c, rho = rho)
         arrVTTF += arrRad[1:]
     return arrVTTF
 
 # ---------------------------------------------------------------------------- #
 
 
 def calculateLipRadiation(d = 1, fMax = 5000, freqSpacing = 1, c = 350, rho = 1.14):
 
 
     A = numpy.pi * pow(d * 0.01 / 2.0, 2)
     #print d, A * 10000
     Rr = 128.0 * rho * c / (9 * pow(numpy.pi, 2) * A)
     Ir = 8.0 * rho / (3 * pow(numpy.pi, 1.5)* pow(A, 0.5))
     j = complex(0, 1)
 
     arrF = []
     arrA = []
     for f in numpy.arange(1, fMax + freqSpacing * 0.5, freqSpacing):
         omega = 2.0 * numpy.pi * f
         CON1 = j * omega * Ir * Rr
         CON2 = (rho * c / A) * (j * omega * Ir + Rr)
         rl = (CON1 - CON2) / (CON1 + CON2)
         LRch = abs(1 + rl)
         T = 20.0 * numpy.log10(LRch)
         #print f, T
         arrF.append(f)
         arrA.append(T)
     arrF = numpy.array(arrF, dtype=numpy.float32)
     arrA = numpy.array(arrA, dtype=numpy.float32)
     return arrF, arrA
 
 # ---------------------------------------------------------------------------- #
 
 
 
 
 
 def removeTimeVaryingDcOffset(data, windowDuration, fps):
     n = len(data)
     dataFiltered = numpy.zeros(n)
     T = 0.1 # duration of averaging window [s]
     windowLength = int(round(float(windowDuration) * float(fps)))
     dataTmp = numpy.array(data)
     #print "applying averager"
     for i in range(n):
         offsetL = i - windowLength / 2
         offsetU = offsetL + windowLength
         if offsetL < 0: offsetL = 0
         if offsetU >= n: offsetU = n - 1
         """
         arrTmp = numpy.array(copy.deepcopy(GAW[offsetL:offsetU]))
         window = dspUtil.createLookupTable(offsetU - offsetL, type = dspUtil.LOOKUP_TABLE_HANN)
         print len(arrTmp), len(window)
         arrTmp *= window
         """
         dataFiltered[i] = dataTmp[i] - dataTmp[offsetL:offsetU].mean()
     return dataFiltered
 
 # ---------------------------------------------------------------------------- #
 
 
 def calculateAnalyticSignal(data):
     # do the hilbert transform
     h = scipy.signal.hilbert(data)
     
     n = len(data)
     hReal = numpy.zeros(n)
     hImg = numpy.zeros(n)
     hAmp = numpy.zeros(n)
     hPhase = numpy.zeros(n)
     for i in range(n):
         re = h[i].real
         im = h[i].imag
         hReal[i] = re
         hImg[i] = im
         hAmp[i] = numpy.sqrt(re * re + im * im)
         ph = numpy.math.atan2(im, re)
         hPhase[i] = ph
     return hReal, hImg, hAmp, hPhase
 
 # ---------------------------------------------------------------------------- #
 
 def unwrapPhase(signal, threshold = numpy.pi):
     n = len(signal)
     arrUnwrapped = numpy.zeros(n)
     arrUnwrapped[0] = signal[0]
     offset = 0
     for i in range(1, n):
         y1 = signal[i-1]
         y2 = signal[i]
         dY = y2 - y1
         if dY < -threshold:
             offset += numpy.pi * 2
         if dY > threshold:
             offset -= numpy.pi * 2
         arrUnwrapped[i] = y2 + offset
     return arrUnwrapped
 
 # ---------------------------------------------------------------------------- #
 
 
 def detectCyclesAnalytic(data, minDistanceConsecutiveCycles = 3):
     
     hReal, hImg, hAmp, hPhase = calculateAnalyticSignal(data)
     hPhaseDrv = toDerivative(hPhase, 2)
     arrCycle = []
     n = len(data)
     recentCycle = -minDistanceConsecutiveCycles * 2
     for i in range(n):
         if hPhaseDrv[i] < -numpy.pi:
             if i - recentCycle >= minDistanceConsecutiveCycles:
                 arrCycle.append(i)
                 recentCycle = i
     #for i in range(n-1):
     #   if hPhase[i] < 0:
     #       if hPhase[i-1] > 0:
     #           arrCycle.append(i)
     return arrCycle
     
 # ---------------------------------------------------------------------------- #
 
 
 def detectCyclesUnwrappedPhase(signal,  fs, phaseUnwrappingThreshold = numpy.pi,
         phaseOffset = 0,
         filterLowerCutoff = None, filterUpperCutoff = None, filterBandwidth = 10,
         movingAveragerDuration = None,
         butterworthBandpassFilterOrder = 3,
         verbose = False, graphOutputPath = None, label = None, returnAllData = False
     ):
 
     
     if verbose: print ("\t", label)
     
     # apply filter?
     signalOriginal = signal
     if filterLowerCutoff and filterUpperCutoff:
         if verbose: print ("\t\tapplying filter [%d..%dHz] ..." \
             % (filterLowerCutoff, filterUpperCutoff))
         # signal = praatUtil.applyBandPassFilterToSignal(signalOriginal * 0.01, fs,
         #   filterLowerCutoff, filterUpperCutoff, filterBandwidth,
         #   preservePhase = True, tmpDataPath = None,
         #   tmpFileName = 'tmp.wav', keepPraatScriptFile = False)
         order = butterworthBandpassFilterOrder
         nyq = 0.5 * fs
         low = filterLowerCutoff / nyq
         high = filterUpperCutoff / nyq
         b, a = scisig.butter(order, [low, high], btype='band')
         signal = scisig.filtfilt(b, a, signalOriginal, padlen=100, method='gust')
 
     if movingAveragerDuration:
         if verbose: print ("\t\tremoving time-varying DC offset ...")
         signalTmp = copy.deepcopy(signal)
         signal = removeTimeVaryingDcOffset(signalTmp, movingAveragerDuration, fs)
         # width = int(round(float(movingAveragerDuration) * float(fs)))
         # signal = movingAverager(signalTmp, width)
 
     # normalize signal
     signal = normalize(signal, 0.5, -0.5)
     #signal -= signal.mean()
     signal -= numpy.percentile(signal, 50)
     
     # apply hilbert transform
     hReal, hImg, hAmp, hPhase = calculateAnalyticSignal(signal)
     
     # find cycles based on unwrapped phase information
     hPhaseUnwrapped = unwrapPhase(hPhase, threshold = phaseUnwrappingThreshold)
     hPhase /= numpy.pi
     hPhaseUnwrapped /= numpy.pi
     phaseOffset /= numpy.pi
     arrCycle = []
     for i, phase in enumerate(hPhaseUnwrapped):
         if phase >= phaseOffset:
             arrCycle.append(i)
             phaseOffset += 2
     
     def findPhasorIntersections(arrX, arrY, numBins):
         arrResults = [] 
         
         #arrIdx, arrAngle, arrR = nonLinearDynamics.polarInterpolation(x1, y1, x2, y2, numBins)
         return arrResults
     #arrPhasorIntersections = findPhasorIntersections(hReal, hImg, numPhasorBins)
     
     
     # create figure
     if graphOutputPath:
     
         def getAx(idx, numSubplots, arrAx):
             ax = plt.subplot(numSubplots * 100 + 10 + idx)
             arrAx.append(ax)
             return ax
     
         numSubplots = 4
         fig = plt.figure(figsize=(20, 3 * numSubplots))
         plt.clf()
         arrAx= []
         n = len(signal)
         arrT = numpy.zeros(n)
         for i in range(n):
             arrT[i] = float(i) / float(fs)
         
         # plot original signal
         ax = getAx(1, numSubplots, arrAx)
         ax.plot(arrT, signal, color='darkblue', label = 'signal filtered')
         ax.plot(arrT, normalize(signalOriginal, 0.5, -0.5), color='red', label='signal orig.')
         leg = ax.legend(loc='best', fancybox=True, framealpha=0.5, fontsize=10)
         
         
         # plot hilbert-transformed data
         ax = getAx(2, numSubplots, arrAx)
         ax.plot(arrT, hReal, label='Re')
         ax.plot(arrT, hImg, label='Im')
         leg = ax.legend(loc='best', fancybox=True, framealpha=0.5, fontsize=10)
         
         # plot analytic signal phase and unwrapped phase
         ax = getAx(3, numSubplots, arrAx)
         ax.plot(arrT, hPhase, label='Phase')
         ax.plot(arrT, hPhaseUnwrapped, label='Phase unwrapped')
         #ax.set_xlabel("Time [s]")
         ax.set_ylabel("Phase [$\\pi$ radians]")
         
         # plot phase-space embedding Re vs Img
         ax = getAx(4, numSubplots, arrAx)
         ax.plot(hReal, hImg)
         ax.set_xlabel('Re')
         ax.set_ylabel('Img')
         ax.plot(0, 0, 'o', color='orange', markersize=7)
         
         # plot phase-space embedding EGG vs dEGG
         #ax = getAx(5, numSubplots, arrAx)
         #ax.plot(signal, toDerivative(signal))
         #ax.set_xlabel('EGG')
         #ax.set_ylabel('dEGG')
         #ax.plot(0, 0, 'o', color='orange', markersize=5)
         
         # plot cycle information
         for idx, ax in enumerate(arrAx):
             if idx <= 1:
                 yMin, yMax = ax.get_ylim()
                 for cycleIdx in arrCycle:
                     t = float(cycleIdx) / float(fs)
                     ax.plot([t, t], [yMin, yMax], '-', 
                         color='gray', linewidth=1, alpha=1)
         
         
         # finalize and save
         for idx, ax in enumerate(arrAx):
             ax.grid()
         plt.tight_layout()
         plt.savefig("%s%s_cycleExtraction.png" % (graphOutputPath , label.replace(' ', '_')))
     
     if verbose: print ("\t\tdone.")
 
     if returnAllData:
         return [arrCycle, signal, hReal, hImg, hAmp, hPhase, hPhaseUnwrapped]
     
     return arrCycle
 
 # ---------------------------------------------------------------------------- #
 
 
 def convertF0DataToCycles(arrT, arrF0, timeStep = None, returnAll = False):
 
     if len(arrT) == 0:
         if returnAll:
             return [], [], []
         return [], []
 
     if timeStep is None:
         arrTmp = toDerivative(arrT)
         timeStep = numpy.nanmax(arrTmp)
         for dt in arrTmp:
             if dt > 0:
                 if timeStep > dt: timeStep = dt
     if timeStep < 0.00001 or timeStep > 0.1:
         raise Exception("timeStep (%s) is out of range" % (str(timeStep)))
 
     # helper function
     def getInterpolated(arrT, arrF0, t):
         n = len(arrT)
         for i in range(n):
             t1 = arrT[i]
             if t1 == t:
                 return arrF0[i]
             if i < n-1:
                 t2 = arrT[i+1]
                 if t <= t2:
                     tRel = (t - t1) / float(t2 - t1)
                     #print tRel
                     return generalUtility.interpolateLinear(arrF0[i], arrF0[i+1], tRel)
             else:
                 #print t, t2, i, n
                 raise Exception("t out of range")
 
     # determine consecutive f0 data portions
     arrF0dataChunks = []
     arrTtmp = []
     arrF0tmp = []
     recentT = timeStep * -10.0
     for i, t in enumerate(arrT):
         if t - recentT < timeStep * 1.1:
             # we're still within a consecutive portion
             pass
         else:
             # new chunk started
             if len(arrTtmp) > 0:
                 arrF0dataChunks.append([arrTtmp, arrF0tmp])
             arrTtmp = []
             arrF0tmp = []
         arrTtmp.append(t)
         arrF0tmp.append(arrF0[i])
         recentT = t
     if len(arrTtmp) > 1:
         arrF0dataChunks.append([arrTtmp, arrF0tmp])
 
     # determine glottal cycles
     arrCycleT, arrCycleDuration = [], []
     for idx, tmp in enumerate(arrF0dataChunks):
         arrT = tmp[0]
         arrF0 = tmp[1]
         i = 0
         tCycle = arrT[0]
         #t0 = arrT[0]
         #dur = arrT[-1] - arrT[0]
         n = len(arrT)
         #print n
         while tCycle <= arrT[-1]:
             # get new cycle
             f0 = arrF0[i]
             proceed = True
             try:
                 f0 = getInterpolated(arrT, arrF0, tCycle)
             except Exception as e:
                 print (e)
                 proceed = False
                 tCycle = arrT[-1] + timeStep * 100
             if numpy.isnan(f0):
                 tCycle += timeStep * 0.1
             else:
                 T = 1.0 / f0
                 #print i, tCycle, f0, T, arrT[0], arrT[-1]
                 tTmp = tCycle
                 while proceed:
                     i += 1
                     if i >= n:
                         proceed = False
                         tCycle = arrT[-1] + 1
                     else:
                         tTmp = arrT[i]
                         if tTmp >= tCycle + T:
                             # OK, cycle covered by data
                             arrCycleT.append(tCycle)
                             arrCycleDuration.append(1.0 / f0)
                             tCycle += T
                             proceed = False
                             #if tCycle != arrT[i]: i -= 1
                             while arrT[i] > tCycle: i -= 1
 
     if 1 == 2:
         # DEBUG graphs
         plt.clf()
         for idx, tmp in enumerate(arrF0dataChunks):
             col = ['blue', 'green', 'cyan', 'brown'][idx]
             arrT = tmp[0]
             arrF0 = tmp[1]
             plt.plot(arrT, arrF0, '-', color=col, linewidth=0.5, alpha=0.3)
             plt.plot(arrT, arrF0, 'o', color=col)
         arrX, arrY = [], []
         for i, t in enumerate(arrCycleT):
             fo = 1.0 / arrCycleDuration[i]
             arrX.append(t)
             arrY.append(fo)
         col='orange'
         plt.plot(arrX, arrY, '-', color=col, linewidth=0.5, alpha=0.3)
         plt.plot(arrX, arrY, 'o', color=col)
         plt.grid()
         plt.show()
         exit(1)
 
     if returnAll:
         return arrCycleT, arrCycleDuration, arrF0dataChunks
     return arrCycleT, arrCycleDuration
 
 # ---------------------------------------------------------------------------- #
 
 def convertCycleDataToF0(arrCycleT, arrPeriod, timeStep, duration):
     n = int(round(duration / timeStep))
     arrT = numpy.zeros(n)
     arrF0 = numpy.zeros(n)
     for i in range(n):
         arrT[i] = float(i) * timeStep
         arrF0[i] = numpy.nan
     if len(arrCycleT) < 1:
         return arrT, arrF0
     for i, t1 in enumerate(arrCycleT):
         T = arrPeriod[i]
         t2 = t1 + T
         idx = int(round(t1 / float(timeStep)))
         t = idx * float(timeStep)
         #print i, t, T, t1, t2
         while t < t1:
             t += timeStep
             idx += 1
             if idx >= n:
                 t = t2
         while t < t2:
             if idx < len(arrF0):
                 arrF0[idx] = 1.0 / T
             idx += 1
             t += timeStep
 
     if 1 == 2:
         # debugging
         plt.plot(arrCycleT, 1.0 / arrPeriod, 'o')
         plt.plot(arrT, arrF0, '.', color='red')
         plt.show()
         exit(1)
     return arrT, arrF0
 
 # ---------------------------------------------------------------------------- #
 
 
 def findVoicedSegments(arrT, arrFo, timeStep, minSegLength = 3):
     arrVoicedSegments = []
     segCnt = 0
     segStart = None
     for i, t in enumerate(arrT):
         fo = arrFo[i]
         if fo > 0:
             if segCnt == 0:
                 segStart = i
                 segCnt = 1
             else:
                 segCnt += 1
         else:
             if segCnt > minSegLength:
                 arrVoicedSegments.append([segStart, i])
             segCnt = 0
         if i > 0:
             if t - arrT[i - 1] > timeStep * 1.5:
                 if segCnt > minSegLength:
                     arrVoicedSegments.append(
                         [segStart, i - 1])
                 segCnt = 0
     if segCnt > minSegLength:
         arrVoicedSegments.append([segStart, len(arrT) - 1])
     return arrVoicedSegments
 
 # ---------------------------------------------------------------------------- #
 
 
 def calculateLinReg(dataX, dataY, degrees):
 
     if len(dataX) < 2:
         raise Exception("data count must be 2 or larger")
 
     #if dspUtil.containsNanInf(dataX):
     #   raise Exception("x-axis data contains NaN or Inf values. aborting.")
     #if dspUtil.containsNanInf(dataY):
     #   raise Exception("y-axis data contains NaN or Inf values. aborting.")
 
 
     # remove NaN and Inf values
     dataX, dataY = generalUtility.removeNanInf(dataX, dataY)
     if len(dataX) < 2:
         return [], numpy.nan
     p = numpy.polyfit(dataX, dataY, degrees)
     #print "\t\t", p
     y1 = numpy.polyval(p,dataX)
     #plt.plot(x, y1, "k-", color='red', linewidth = 2)
     def getY(p, x):
         y = 0
         for i in range(len(p)):
             y += p[len(p) - (i + 1)] * (x ** float(i))
         return y
 
 
     # calculate the variance and R2
     SSerr = 0
     SStot = 0
     mean = sum(dataY) / float(len(dataY))
     for i in range(len(dataX)):
         y_i = dataY[i]
         f_i = getY(p, dataX[i])
         SSerr += (y_i - f_i) * (y_i - f_i)
         SStot += (y_i - mean) * (y_i - mean)
     R2 = 1 - (SSerr / SStot)
     #print "\t\tR2:", R2
 
     return p, R2
 
 # ---------------------------------------------------------------------------- #
 
 
 def detectSubharmonics(signal, fs, timeStep, fMin, fMax, voicingThreshold = 0.3,
     tolerancePercent = 5, maxOctaveCost = 0.25, maxOctaveJumpCost = 0.3,
     minOctaveCost = 0, minOctaveJumpCost = 0):
 
 
     #signal /= numpy.nanmax(numpy.absolute(signal)) * 1.5
     n = len(signal)
     duration = float(n) / float(fs)
     arrMetaData = [
         {
             'octaveCost': maxOctaveCost,
             'octaveJumpCost': maxOctaveJumpCost,
         },
         {
             'octaveCost': minOctaveCost,
             'octaveJumpCost': minOctaveJumpCost,
         },
     ]
     arrResults = []
     for idx, metaData in enumerate(arrMetaData):
         octaveCost = metaData['octaveCost']
         octaveJumpCost = metaData['octaveJumpCost']
         # print fs, timeStep, fMin, fMax, voicingThreshold, octaveCost, \
         #       octaveJumpCost
         arrT, arrFo = praatUtil.calculateF0OfSignal(signal, fs,
             readProgress = timeStep,
             acFreqMin = fMin, fMax = fMax,
             voicingThreshold = voicingThreshold,
             octaveCost = octaveCost, octaveJumpCost = octaveJumpCost)
         arrResults.append([arrT, arrFo])
     numDataPoints = duration / float(timeStep)
     arrT = numpy.arange(0, duration, timeStep)
     n = len(arrT)
     arrFo = [numpy.ones(n) * numpy.nan, numpy.ones(n) * numpy.nan]
     for i in range(2):
         arrIdx = getCommonTimeOffsets(arrT, arrResults[i][0], timeStep)
         for j, tmp in enumerate(arrIdx):
             idx1, idx2 = tmp
             arrFo[i][idx1] = arrResults[i][1][idx2]
 
     # detect subharmonic portions
     arrPeriod = numpy.ones(n) * numpy.nan
     arrFoFinal = numpy.ones(n) * numpy.nan
     subharmonicsFound = False
     for i, t in enumerate(arrT):
         f1 = arrFo[0][i]
         f2 = arrFo[1][i]
         if not numpy.isnan(f1) and not numpy.isnan(f2):
             if f1 > 0 and f2 > 0:
 
                 # check if data points match
                 diff = abs(f1 - f2)
                 mean = (f1 + f2) / 2.0
                 diffPercent = diff * 100.0 / float(mean)
                 if diffPercent <= tolerancePercent:
                     arrFoFinal[i] = mean
                     arrPeriod[i] = 1.0
 
                 else:
 
                     # check if its subharmonic
                     factor = f1 / float(f2)
                     for base in range(2, 9):
                         boundary1 = base + base * (1 - (100 + tolerancePercent) / 100.0)
                         boundary2 = base + base * (1 - (100 - tolerancePercent) / 100.0)
 
                         if factor >= boundary1 and factor <= boundary2:
                             #print "\t\t", i, base, factor, boundary1, boundary2
                             # it's a subharmonic data point
                             arrFoFinal[i] = f1
                             #if f2 > f1:
                             arrPeriod[i] = float(base)
                             subharmonicsFound = True
                             break
 
     if 1 == 2 and subharmonicsFound:
         ms = 8
         plt.plot(arrT, arrFo[0], '+', markersize = ms * 1.8, color='green', alpha=0.8)
         plt.plot(arrT, arrFo[1], 'x', markersize = ms* 1.8, color='yellow', alpha=0.4)
         plt.plot(arrT, arrFoFinal, 'D', markersize = ms, color='violet', alpha=0.8)
         for i, t in enumerate(arrT):
             p = arrPeriod[i]
             if p > 1:
                 plt.plot(t, arrFoFinal[i] / float(p), 'o', markersize = ms, color='red', alpha=1)
         plt.grid()
         plt.show()
         exit(1)
 
     return arrT, arrFoFinal, arrPeriod, arrFo
 
 # ---------------------------------------------------------------------------- #
 
 
 def detectSubharmonicSequences(arrT, arrSubharmonicPeriod,
         minimumConsecutiveDataPoints = 5):
     n = len(arrT)
     arrSubharmonicSequence = numpy.ones(n) * numpy.nan
     if n < 0:
         return arrSubharmonicSequence
     insideSeq = False
     seqStart = None
     for i, val in enumerate(arrSubharmonicPeriod):
         if insideSeq:
             if val > 1:
                 # all OK, just continue collecting sequence data point
                 pass
             else:
                 # end of sequence. store.
                 m = i - seqStart
                 if m >= minimumConsecutiveDataPoints:
                     for j in range(m):
                         arrSubharmonicSequence[j+seqStart] = 1
                 insideSeq = False
                 seqStart = None
         else:
             # inside sequence
             if val > 1:
                 # mark the beginning of a new sequence
                 seqStart = i
                 insideSeq = True
             else:
                 # nothing happens
                 pass
     if insideSeq:
         m = i - seqStart
         if m >= minimumConsecutiveDataPoints:
             for j in range(m):
                 arrSubharmonicSequence[j+seqStart] = 1
 
     # cntTotal = arrSubharmonicSequence.sum()
     # if cntTotal > 0:
     #   plt.plot(arrT, arrSubharmonicPeriod, 'o')
     #   plt.plot(arrT, arrSubharmonicSequence, '.')
     #   plt.show()
     #   exit(1)
 
     return arrSubharmonicSequence
 
 # ---------------------------------------------------------------------------- #