# 01/27/2020 Initial, Chinese New Year 初三
#

import os,sys,platform
import subprocess
import random

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
from readConfig import *

def ps_exec(cmd, adminPriv=False):
    """ 使用 Windows PowerShell Start-Process 執行程式, 回傳 STDOUT, 並且支援以系統管理員身分執行 """

    # 產生隨機檔名, 用來儲存 stdout
    existed = True
    while existed:
        r = random.randint(0,65535)
        stdout_path = os.path.expanduser('~\\stdout-%04x.txt' % r)
        existed = os.path.isfile(stdout_path)
    open(stdout_path, 'w').close()

    if adminPriv:
        # 產生底層參數
        deep_args = list(map(lambda n: "'{}'".format(n), cmd[1:]))
        deep_args = ','.join(deep_args)

        # 產生表層參數
        surface_args = [
            'Start-Process',
            '-FilePath', cmd[0],
            '-ArgumentList', deep_args,
            '-RedirectStandardOutput', stdout_path,
            '-NoNewWindow'
        ]
        surface_args = list(map(lambda n: '"{}"'.format(n), surface_args))
        surface_args = ','.join(surface_args)

        # 產生完整執行程式指令
        cmd = [
            'powershell.exe', 'Start-Process',
            '-FilePath', 'powershell.exe',
            '-ArgumentList', surface_args,
            '-Verb', 'RunAs',
            '-Wait'
        ]
    else:
        # 產生表層參數
        surface_args = list(map(lambda n: '"{}"'.format(n), cmd[1:]))
        surface_args = ','.join(surface_args)

        # 產生完整執行程式指令
        cmd = [
            'powershell.exe', 'Start-Process',
            '-FilePath', cmd[0],
            '-ArgumentList', surface_args,
            '-RedirectStandardOutput', stdout_path,
            '-NoNewWindow',
            '-Wait'
        ]

    # 取 stdout
    completed = subprocess.run(cmd)
    stdout_content = ''
    with open(stdout_path, 'r') as stdout_file:
        stdout_content = stdout_file.read()
    os.remove(stdout_path)

    return stdout_content

def main():
    #cmd = [ 'netstat.exe', '-a', '-n', '-p', 'tcp' ]

    cmd = ['PowerShell.exe', 'Remove-VpnConnection', \
           '-Name', 'Test4', \
           '-Force', '-PassThru'] 
    #stdout = ps_exec(cmd, adminPriv=True)
    #print(stdout)

    cmd = ['PowerShell.exe', 'Set-VpnConnection', \
           '-Name', 'Test4', '-ServerAddress', "10.1.1.1", \
            '-TunnelType', "L2tp", \
            '-EncryptionLevel', "Optional", \
            '-AuthenticationMethod', 'Eap', \
            '-SplitTunneling', 0, \
            '-AllUserConnection', \
            '-L2tpPsk', "password", \
            '-Force', '-RememberCredential', 1, \
            '-PassThru']
             
    stdout = ps_exec(cmd, adminPriv=True)
    print(stdout)

    cmd = ['PowerShell.exe', 'Get-VpnConnection']
    stdout = ps_exec(cmd, adminPriv=True)
    print(stdout)

if __name__ == '__main__':

    # Read json file
    with open('config.json') as f:
        config_para = json.load(f)

    main()