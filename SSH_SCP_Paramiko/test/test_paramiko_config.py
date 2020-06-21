#!/usr/bin/python
#Py2/Py3 are supported
#https://qiita.com/cielavenir/items/6aa9e6dc1166ae947c6f

import os,sys,subprocess,glob
import paramiko
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

with open('config.json') as f:
    config = json.load(f)

def getlist(h,k):
    if k not in h:
        return []
    if not isinstance(h[k],list):
        return [h.pop(k)]
    return h.pop(k)

def bash_expand(s):
    return subprocess.check_output(['bash','-c','echo "%s"'%s]).decode('utf-8')

def parse_config(hostname, password, username=None, configfile='~/.ssh/config'):
    configfile = os.path.expanduser(configfile)
    cfg = {
        'hostname':hostname,
        'username':username if username is not None else os.environ['USER'],
        'password':password,
        'port':22,
        'compress':False,
    }
    configfile_dir = os.path.dirname(configfile)
    configfiles = [configfile]
    configfiles_added = {configfile}
    while configfiles:
        configfile = configfiles.pop(0)
        if os.path.exists(configfile):
            print('Loading '+configfile)
            with open(configfile) as f:
                for line in f:
                    args=line.split()
                    if args and args[0].lower()=='include':
                        for incl in args[1:]:
                            if incl[0]=='~':
                                incl = os.path.expanduser(incl)
                            elif incl[0]!='/':
                                incl = os.path.join(configfile_dir,incl)
                            for e in sorted(glob.glob(incl)):
                                if e not in configfiles_added:
                                    configfiles_added.add(e)
                                    configfiles.append(e)
                f.seek(0)
                ssh_config = paramiko.SSHConfig()
                ssh_config.parse(f)
                user_config = ssh_config.lookup(hostname)
                print(user_config)
                cfg['hostname'] = user_config.pop('hostname') # hostname could be alias(?)
                cfg['username'] = user_config.pop('user',cfg['username'])
                cfg['password'] = int(user_config.pop('password',cfg['password']))
                cfg['port'] = int(user_config.pop('port',cfg['port']))
                if 'compression' in user_config:
                    v = user_config.pop('compression')
                    if v.lower()=='yes':
                        cfg['compress'] = True
                    elif v.lower()=='no':
                        cfg['compress'] = False
                if 'certificatefile' in user_config or 'identityfile' in user_config:
                    if 'key_filename' not in cfg:
                        cfg['key_filename'] = []
                    cfg['key_filename'] += [os.path.expanduser(e) for e in getlist(user_config,'certificatefile')+getlist(user_config,'identityfile')]
                if 'proxycommand' in user_config:
                    cfg['sock'] = paramiko.ProxyCommand(bash_expand(user_config.pop('proxycommand')))
    #print('[paramiko config]')
    #print(cfg)
    msg = '[paramiko config]: {}'
    logger.info(msg.format(cfg))
    return cfg

with open('config.json') as f:
    config = json.load(f)

msg = 'config["SSH_Client"][0]["hostname"]: {}'
logger.info(msg.format(config["SSH_Client"][0]["hostname"]))

with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(**parse_config(config["SSH_Client"][0]["hostname"], \
                               config["SSH_Client"][0]["password"],\
                               config["SSH_Client"][0]["username"]))
    with ssh.open_sftp() as sftp:
        with sftp.file('.ssh/authorized_keys','r') as f:
            sys.stdout.write(f.read().decode('utf-8'))