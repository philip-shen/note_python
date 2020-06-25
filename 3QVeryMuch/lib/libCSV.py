import os,sys,glob
from logger import logger

def walk_in_dir(dir_path,file_type,opt_verbose='OFF'):
    ret_listOfFileNames = []
    #ret_list_ZipFolder_TxtCsvFiles =[]

    for filename in glob.glob(os.path.join(dir_path, file_type)):
        listOfFileNames = []

        listOfFileNames = filename
        ret_listOfFileNames.append(listOfFileNames)

        '''
        fileName:..\logs\boommic_SWout\dut.3quest\Results\output.csv in directory:..\logs\boommic_SWout\dut.3quest\Results
        fileName:..\logs\Intermic_SWin\dut.3quest\Results\output.csv in directory:..\logs\Intermic_SWin\dut.3quest\Results
        '''        
        '''
        listOfFileNames:..\logs\boommic_SWout\dut.3quest\Results\output.csv in walk_in_dir
        listOfFileNames:..\logs\boommic_SWout\dut.3quest\Results\output_02.csv in walk_in_dir

        listOfFileNames:..\logs\Intermic_SWin\dut.3quest\Results\output.csv in walk_in_dir
        '''
        if opt_verbose.lower() == "on":
            msg = "fileName:{} in directory:{}"
            logger.info(msg.format(filename, dir_path))
             
            msg = "listOfFileNames:{} in walk_in_dir"
            logger.info(msg.format(listOfFileNames))        

    for dirname in (d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d)) ):
        walk_in_dir(os.path.join(dir_path, dirname))
    
    '''
    ret_listOfFileNames:['..\\logs\\boommic_SWout\\dut.3quest\\Results\\output.csv', '..\\logs\\boommic_SWout\\dut.3quest\\Results\\output_02.csv'] in walk_in_dir

    ret_listOfFileNames:['..\\logs\\Intermic_SWin\\dut.3quest\\Results\\output.csv'] in walk_in_dir    
    '''
    msg = "ret_listOfFileNames:{} in walk_in_dir"
    logger.info(msg.format(ret_listOfFileNames))        

    return ret_listOfFileNames