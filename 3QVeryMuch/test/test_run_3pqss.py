#!/usr/bin/env python2.7

# from __future__ import print_function
import sys
import glob
import os
import time
import getpass
import json
from pandas.io.json import json_normalize

sys.path.append('/share/tools/batch_processor_3quest')
import gen_3pass_bat
import parse_3pass_log

#arg_num = len(sys.argv);

t0 = time.time()
local_time = time.localtime(t0)
print('Start Time is %s/%s/%s %s:%s:%s'%(local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                        local_time.tm_hour,local_time.tm_min,local_time.tm_sec))    

bat_out_posi_base = '/share/data/users/chenchu/3q_bp_temp/3pass'
bat_out_posi2_base = '/share/data/Exchange/chenchu.hsu/3q_bp_temp/3pass'

curr_dir = os.getcwd()
curr_usr = getpass.getuser()
bat_out_posi = os.path.join(bat_out_posi_base, curr_usr)
if not os.path.isdir(bat_out_posi):
    bat_out_posi = os.path.join(bat_out_posi2_base, curr_usr)

proc_posi = os.path.join(bat_out_posi, 'proc_files')
print('bat_out_posi = %s'%bat_out_posi)

with open('config.json') as f:
    data = json.load(f)

'''
#if(arg_num > 1):
#    for k in xrange(arg_num-1):
#        folder_proc = sys.argv[k+1]
'''

for i,_3quest in enumerate(data["3Quest"]):

    if (data["3Quest"][i]['label_dut'] != '' and data["3Quest"][i]['label_standmic'] != ''\
        and os.path.isfile(data["3Quest"][i]['mic_dut']) \
        and os.path.isfile(data["3Quest"][i]['mic_standmic'])):#bypass without labels and dut, standmic wav file

        folder_proc= data["3Quest"][i]['path_dut']

        print('process %s ---- \n'%folder_proc)
        cmd_txt = 'rm %s/*.wav'%proc_posi
        print(cmd_txt)
        os.system(cmd_txt)

        print('copy files to %s \n'%proc_posi)
        cmd_txt = 'octave --eval "addpath "/share/tools/batch_processor_3quest"; func_convert_wav_(\'%s\', \'%s\');"'%(folder_proc, proc_posi)
        print(cmd_txt)
        os.system(cmd_txt)

        config = {}
        # to decide mode
        wav_list = glob.glob(os.path.join(proc_posi, '*.wav'))        

        '''
        data["3Quest"][28]['path_dut']: /home/philip.shen/3Quest/Logitech/logitech_0710_debussy-debug-0701/dut

        How to get the home directory in Python?
        https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
        os.path.expanduser('~')        
        '/home/philip.shen'
        '''

        if('dut' in wav_list[0]):
            config['run_case'] = 143   # 3quest mode for HS
            config['case_mode'] = 1 # 0 for NB, 1 for WB
            config['type_name'] = '3quest'
            #config['unproc_posi_base'] = '/share/data/users/philip.shen/3Quest/Logitech/logitech_0710_debussy-debug-0701/standmic'
            config['unproc_posi_base'] = data["3Quest"][i]['path_standmic'].replace(os.path.expanduser('~'), '/share/data/users/'+getpass.getuser() )
            print('config[\'unproc_posi_base\']: %s \n'%config['unproc_posi_base'])
        
            config['noise_3q_list'] = ['pub', 'road', 'crossroad', 'train', 'car', 'cafeteria', 'mensa', 'callcenter', 'voice_distractor','nobgn']
            config['avg_taken_ind'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        run_case = config['run_case']
        run_txt = config['type_name']
        run_num = len(config['noise_3q_list'])
        print('run_num=%d'%run_num)
        
        # gen test bat file
        print('config.type_name = %s, run_case = %d'%(config['type_name'], run_case))
        gen_3pass_bat.gen_3pass_bat(config, proc_posi, bat_out_posi)

        
        # cmd_txt = 'touch %s/%s_bp.go'%(bat_out_posi, run_txt)
        # print(cmd_txt)
        # os.system(cmd_txt)
        fid_3p_go = open('%s/%s_bp.go'%(bat_out_posi, run_txt), 'w+')
        fid_3p_go.write('%d'%run_num)
        fid_3p_go.close()

        cmd_txt = 'chmod 777 %s/%s_bp.go'%(bat_out_posi, run_txt)
        print(cmd_txt)
        os.system(cmd_txt)

        # wait 3quest batch processor finish
        print('waiting ')
        for t in xrange(720):
            time.sleep(3)   # Delays for 5 seconds. 
            if os.path.isfile('%s/%s_bp.go'%(bat_out_posi, run_txt)) or os.path.isfile('%s/%s_bp.running'%(bat_out_posi, run_txt)):  # still running
                if(t>12): # pass 5*12 sec
                    if((t%6) == 0):
                        print('waited cnt%d (%d sec)'%(t, t*3))
            else:
                log_result_posi = os.path.join(bat_out_posi, 'Results')
                parse_3pass_log.parse_3pass_log(folder_proc, config, bat_out_posi, log_result_posi)
                break;
            
        # copy result
        if(folder_proc[-1] == '/'):
            folder_proc = folder_proc[:-1]
        out_3pass = folder_proc + '.%s'%run_txt
        cmd_txt = 'mkdir %s'%out_3pass
        print(cmd_txt)
        os.system(cmd_txt)

        cmd_txt = 'cp -rf %s/ini %s'%(bat_out_posi, out_3pass)
        os.system(cmd_txt)
        cmd_txt = 'cp -rf %s/Results %s'%(bat_out_posi, out_3pass)
        os.system(cmd_txt)

print('Time duration: %.2f seconds.'%(time.time() - t0))                 
