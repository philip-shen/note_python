import os,sys,time,platform
import json
from pandas.io.json import json_normalize

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from libCSV import *
from logger import logger

import myWave
import dspUtil
import numpy
import copy
import generalUtility


if __name__ == "__main__":
    # Get present time
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))         
    args = sys.argv
    
    with open('config.json') as f:
        data = json.load(f)

    try:
        
        #for i,_corpus in enumerate(data["Corpus"]):            
        for i in range(len(data["Corpus"])):

            msg = 'i:{}'
            logger.info(msg.format(i) )
            
            # Check path if exists or not
            if(os.path.isdir(data["Corpus"][i]['path_dut'])):    
                
                opt_verbose='ON'
                #opt_verbose='OFF'
                
                file_type = '*.wav'
                ret_list_DUTFolder_wavFiles = walk_in_dir(data["Corpus"][i]['path_dut'],file_type)  

                for DUTFolder_wavFiles in ret_list_DUTFolder_wavFiles:

                    """
                    # normalize the left channel, leave the right channel untouched
                    # load the input file
                    #numChannels, numFrames, fs, wav_data = myWave.readWaveFile(DUTFolder_wavFiles)
                    numFrames, fs, wav_data = myWave.readMonoWaveFile(DUTFolder_wavFiles)

                    # data is a list of numpy arrays, one for each channel
                    #wav_data = dspUtil.normalize(wav_data)

                    # save the normalized file (both channels)
                    # this is the explicit code version, to make clear what we're doing. since we've
                    # treated the data in place, we could simple write: 
                    # myWave.writeWaveFile(data, outputFileName, fs) and not declare dataOut
                    dataOut = wav_data 
                    fileNameOnly = generalUtility.getFileNameOnly(DUTFolder_wavFiles)
                    outputFileName = fileNameOnly + "_processed.wav"
                    myWave.writeWaveFile(dataOut, outputFileName, fs)
                    """
                    path_dut_dutoffsec_wave= myWave.wavDCOffes(DUTFolder_wavFiles,opt_verbose, True, True)

                    if opt_verbose.lower() == "on":
                        #msg = 'len(wav_data):{}'
                        #logger.info(msg.format(len(wav_data)) )

                        msg = '{}th DUTFolder DUTFolder_wavFiles:{}'
                        logger.info(msg.format(i, DUTFolder_wavFiles) )

                        #msg = 'numFrames:{}; fs:{}'
                        #logger.info(msg.format(numFrames, fs) )

                        msg = 'path_dut_dutoffsec_wave:{}'
                        logger.info(msg.format(path_dut_dutoffsec_wave) )


    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))     



# just for kicks, reverse (i.e., time-invert) all channels
#for chIdx in range(numChannels):
#    n = len(data[chIdx])
#    dataTmp = copy.deepcopy(data[chIdx])
#    for i in range(n):
#        data[chIdx][i] = dataTmp[n - (i + 1)]


