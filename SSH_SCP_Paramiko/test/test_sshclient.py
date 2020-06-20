
import paramiko
import scp
import json

import os,sys,time

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger

# you can also use progress4, which adds a 4th parameter to track IP and port
# useful with multiple threads to track source
# https://github.com/jbardin/scp.py#tracking-progress-of-your-file-uploadsdownloads
def progress4(filename, size, sent, peername):
    sys.stdout.write("(%s:%s) %s\'s progress: %.2f%%   \r" % (peername[0], peername[1], filename, float(sent)/float(size)*100) )


with open('config.json') as f:
    config = json.load(f)


'''
config["SSH_Client"][0]: {'hostname': '192.168.1.104', 'port': 22, 'username': 'test', 'password': '123456'}
config["SSH_Client"][0]["hostname"]: 192.168.1.104
'''

msg = 'config["SSH_Client"][0]["hostname"]: {}'
logger.info(msg.format(config["SSH_Client"][0]["hostname"]))

# サーバに繋ぐ
with paramiko.SSHClient() as sshc:
    sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #sshc.load_system_host_keys()
    sshc.connect(hostname=config["SSH_Client"][0]["hostname"], \
                    port=config["SSH_Client"][0]["port"], \
                    username=config["SSH_Client"][0]["username"], \
                    password=config["SSH_Client"][0]["password"])

# SSHClient()の接続設定を合わせてあげる
with scp.SCPClient(sshc.get_transport()) as scpc:
    scpc.get('docker_registry/certs/hyperv-ubuntu18.local.crt')

#scp = SCPClient(ssh.get_transport(), progress4=progress4)

sshc.close()
scpc.close()    