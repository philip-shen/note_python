import dspUtil, numpy, math, os, generalUtility, myWave
import praatTextGrid
 
PRAAT_SHORT_TEXT_FILE = 1
PRAAT_TEXT_FILE = 0
 
 
def convertToVector(dataX, dataY, duration, timeStep, valMin, valMax):
     data = []
     size = int(round(duration / float(timeStep)))
     for i in range(size):
         data.append(None)
     for i in range(len(dataX)):
         t = dataX[i]
         idx = int(t / timeStep)
         if dataY[i] >= valMin and dataY[i] <= valMax:
             data[idx] = dataY[i]
     return data
 
 
 
 
def readHarmonicityData(fileName):
     dataX, dataY, metaData = readPraatShortTextFile(fileName, 'Harmonicity 2')
     return dataX, dataY
 
 
 
 
def readIntensityTier(fileName):
     dataX, dataY, metaData = readPraatShortTextFile(fileName, 'Intensity')
     return dataX, dataY
 
 
 
 
def readPitchTier(fileName):
     dataX, dataY, metaData = readPraatShortTextFile(fileName, 'PitchTier')
     return dataX, dataY
 
 
 
 
def readLtas(fileName):
     
     fs = None
     bandwidth = None
     f = open(fileName, 'r')
     arrData = []
     for i, line in enumerate(f):
         line = line.strip()
         #print i, line
         if i == 0:
             if line != 'File type = "ooTextFile"':
                 raise Exception("not a LTAS short text file")
         if i == 1:
             if line != 'Object class = "Ltas 2"':
                 raise Exception("not a LTAS short text file")
         if i == 4:
             fs = float(line)
         if i == 6:
             bandwidth = float(line)
         if i > 12:
             arrData.append(float(line))
     return fs, bandwidth, numpy.array(arrData)
     
 
 
 
def readSpectrum(fileName, convertToDb = True, fileType = PRAAT_TEXT_FILE):
     
     def parseLine(line, fileType):
         tmp = line.split('=')[-1]
         tmp2 = tmp.split('e')
         val = 0
         if len(tmp2) == 1: val = float(tmp2[0])
         elif len(tmp2) == 2:
             val = float(tmp2[0]) * math.pow(10.0, float(tmp2[1]))
         else:
             raise ("unable to read data value")
         if fileType == PRAAT_SHORT_TEXT_FILE:
             return val # float(line.strip())
         elif fileType == PRAAT_TEXT_FILE:
             return val # float(line.split('=')[1])
         else:
             raise Exception("Praat file type not recignized")
 
     if fileType == PRAAT_SHORT_TEXT_FILE:
         dataX, dataY, metaData = readPraatShortTextFile(fileName, 'Spectrum 2')
         fs = float(metaData[1])
         windowSize = float(metaData[2])
 
     file = open(fileName, "r")
     cnt = 0
     offset = 0
     data = None # real and imaginary data
     fs = None
     windowSize = None
     idx = 0 # only used for short text file
 
     for line in file:
         line = line.strip()
         cnt += 1
         #print cnt, line # debug information
         
         if cnt == 1:
             # 1 File type = "ooTextFile"
             if line != 'File type = "ooTextFile"':
                 raise Exception ("file " + fileName \
                     + " is not a Praat short text file")
                 
         elif cnt == 2:
             # 2 Object class = "Spectrum 2"
             if line != 'Object class = "Spectrum 2"':
                 raise Exception ("file " + fileName \
                     + " is not a Praat spectrum file")
         
         elif cnt == 5:
             # 5 xmax = 22050
             #try:
                 fs = parseLine(line, fileType) * 2.0
             #except:
             #   raise Exception('unable to determine sampling frequency')
     
         elif cnt == 6:
             # window size is incremented by 1 in the Praat short text file
             # 6 nx = 4097       
             #try:
                 windowSize = parseLine(line, fileType)
                 data = numpy.zeros((2, windowSize))
             #except:
             #   raise Exception('unable to determine windowSize')
         
         elif (fileType == PRAAT_SHORT_TEXT_FILE and cnt > 13) \
                 or (fileType == PRAAT_TEXT_FILE and cnt > 15):
             try:
                 if fileType == PRAAT_SHORT_TEXT_FILE:
                     idx1 = int(idx / windowSize)
                     idx2 = int(idx % windowSize)
                     val = parseLine(line, fileType)
                     data[idx1][idx2] = val
                     #print idx1, idx2, val
                     idx += 1
                 elif fileType == PRAAT_SHORT_TEXT_FILE:
                     if line != 'z [2]:':
                         val = float(line.split('=')[1])
                         tmp = line.split('=')[0].split('[')
                         idx1 = int(tmp[1].strip().strip(']')) - 1
                         idx2 = int(tmp[2].strip().strip(']')) - 1
                         #print idx1, idx2, val
                         #z [1] [1] = -0.00026495086386186666
                         data[idx1][idx2] = val
             except:
                 raise Exception('unable to read data value in line ' \
                     + str(cnt) + ' ("' + line + '")')
                 
     file.close()    
         
     # some basic testing
     if len(data[0]) != len(data[1]):
         raise Exception('ERROR when reading Praat spectrum file ' + fileName \
             + ': size of real and imaginary data arrays does not match')
     if len(data[0]) != windowSize:
         raise Exception ('ERROR when reading Praat spectrum file ' + fileName \
             + ': expected ' + str(windowSize) + ' data points, but read ' \
             + len(data))    
             
     # convert to power spectrum
     dataOut = numpy.zeros(windowSize)
     for i in range(len(data[0])):
         val = math.sqrt(data[0][i] * data[0][i] + data[1][i] * data[1][i])
         # convert to dB
         if convertToDb:
             if val > 0:
                 val = dspUtil.rmsToDb(val)
             else:
                 val = -300
         dataOut[i] = val        
     
     return fs, windowSize, dataOut
 
def readPointProcessData(fName):
     if not os.path.isfile(fName):
         raise Exception("file '%s' does not exist" % (str(fName)))
     f = open(fName, 'r')
     arrData = []
     for idx, line in enumerate(f):
         if idx > 5:
             arrData.append(float(line))
     f.close()
     return numpy.array(arrData, dtype=numpy.float32)
 
 
def generateEmptyPraatTextGrid(fName, arrIntervalTierNames, 
         arrPointTierNames = None, overwriteExistingTextGrid = False,
         duration = None):
     path, fileNameOnly, suffix = generalUtility.splitFullFileName(fName)
     outputFileName = path + fileNameOnly + '.TextGrid'
     if not overwriteExistingTextGrid:
         if os.path.isfile(outputFileName):
             raise Exception("TextGrid %s already exists" % outputFileName)
     if duration is None:
         numChannels, numFrames, fs, data = myWave.readWaveFile(\
             fName, useRobustButSlowAlgorithm = False)
         duration = float(numFrames) / float(fs)
     
     textGrid = praatTextGrid.PraatTextGrid(0, duration)
     if not arrIntervalTierNames is None:
         for label in arrIntervalTierNames:
             intervalTier = praatTextGrid.PraatIntervalTier(label)
             intervalTier.add(0, duration, "")
             textGrid.add(intervalTier)
     if not arrPointTierNames is None:
         for label in arrPointTierNames:
             pointTier = praatTextGrid.PraatPointTier(label)
             textGrid.add(pointTier)
     textGrid.save(outputFileName)
 
 
 
 
def extractSegments(wavFileName, label = None, tierIndex = 0, 
         textGridFileName = None, outputPath = None):
     
     path, fileNameOnly, suffix = generalUtility.splitFullFileName(wavFileName)
     if textGridFileName is None:
         textGridFileName = "%s%s.TextGrid" % (path, fileNameOnly)
     if outputPath is None:
         outputPath = path
     numChannels, numFrames, fs, channelData = myWave.readWaveFile(wavFileName)
     textGrid = praatTextGrid.PraatTextGrid(0, 0)
     arrTiers = textGrid.readFromFile(textGridFileName)
     tier = arrTiers[tierIndex]
     cnt = 0
     arrSegmentInfo = []
     for i in range(tier.getSize()):
         doExtract = False
         if label is None:
             if tier.getLabel(i).strip() != '':
                 doExtract = True
         else:
             if tier.getLabel(i).strip() != label:
                 doExtract = True
         if doExtract:
             cnt += 1
             interval = tier.get(i)
             tStart = interval[0]
             tEnd = interval[1]
             offset1 = int(round(tStart * float(fs)))
             offset2 = int(round(tEnd * float(fs)))
             arrDataTmp = []
             for chIdx in range(numChannels):
                 arrDataTmp.append(channelData[chIdx][offset1:offset2])
             outputFileName = "%s%s_%04d.wav" % (outputPath, fileNameOnly, cnt)
             myWave.writeWaveFile(arrDataTmp, outputFileName, SRate = fs, 
                 normalize = False, removeDcWhenNormalizing = True)
             arrSegmentInfo.append((tStart, tEnd))
     return arrSegmentInfo
 
 
 
 
def readPraatShortTextFile(fileName, obj):
     file = open(fileName, "r")
     cnt = 0
     numDataPoints = 0
     offset = 0
     dataX = []
     dataY = []
     dataIdx = 0
     timeStep = 0
     timeOffset = 0
     
     arrFileTypes = [
         'Harmonicity 2', 'PitchTier', 'Intensity', 'SpectrumTier', \
             'Spectrum 2', 'Cepstrum 1'
     ]
     
     if not obj in arrFileTypes:
         raise Exception('readPraatShortTextFile - file type must be: ' 
             + ', '.join(arrFileTypes))
     metaData = []
     for line in file:
         line = line.strip()
         cnt += 1
         #print cnt, line # debug information
         if cnt > 6:
             if obj == 'Harmonicity 2' or obj == 'Intensity 2':
                 if cnt > 13:
                     val = float(line)
                     if val > -100:
                         dataY.append(val)
                     else:
                         dataY.append(None)
                     dataX.append(timeOffset + float(dataIdx) * timeStep)
                     dataIdx += 1
                 else:
                     if cnt == 7:
                         timeStep = float(line)
                     if cnt == 8:
                         timeOffset = float(line)
             else:
             # read data here
                 if cnt % 2 == 0:
                     dataY.append(float(line))
                     dataIdx += 1
                 else:
                     dataX.append(float(line))
         else:
             if cnt > 3:
                 metaData.append(line)
             # error checking and loop initialization
             if cnt == 1:
                 if line != "File type = \"ooTextFile\"":
                     raise Exception ("file " + fileName \
                         + " is not a Praat pitch" + " tier file")
             if cnt == 2:
                 err = False
                 #print line 
                 if obj == 'Harmonicity':
                     if line != "Object class = \"Harmonicity\"" \
                             and line != "Object class = \"Harmonicity 2\"":
                         err = True
                 elif obj == 'Intensity':
                     if line != "Object class = \"IntensityTier\"" \
                             and line != "Object class = \"Intensity 2\"":
                         err = True
                 else:
                     if line != "Object class = \"" + obj + "\"":
                         err = True
                 if err == True:
                     raise Exception ("file " + fileName + " is not a Praat "    
                         + obj + " file")
             if cnt == 6:
                 if line[0:15] == 'points: size = ':
                     numDataPoints = int(line.split('=')[1].strip())
                     raise Exception (\
                         "only the 'short text file' type is supported. " \
                         + " Save your Praat " + obj \
                         + " with 'Write to short text file.") 
                 else:
                     numDataPoints = int(line)
     return (numpy.array(dataX), numpy.array(dataY), metaData)