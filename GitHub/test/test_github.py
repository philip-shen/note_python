# 2020/05/14 Initial 
######################################################
import os,sys,time

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from logger import logger
from github import Github

if __name__ == "__main__":
    t0 = time.time()

    args = sys.argv
    try:
        if( len(args) == 3 ):
            username = args[1]
            password = args[2]
            g = Github(username, password)

            for repo in g.get_user().get_repos():
                msg = 'repositories: {}.'
                logger.info(msg.format(repo))        

    except IndexError:
        print('IndexError: Usage "python %s github_username github_password"' % ( args[0]))
    
    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))        