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
import libgithub as lib_github

if __name__ == "__main__":
    t0 = time.time()

    args = sys.argv
    try:
        if( len(args) == 1 ):
            msg = 'IndexError: Usage "python {} github_username github_password"'
            logger.info( msg.format(args[0]) ) 

        if( len(args) == 3 ):
            msg = 'Start Search Star Ranking Top 100 on GitHub.'
            logger.info(msg) 

            #opt_verbose='ON'
            opt_verbose='OFF'

            username = args[1]
            password = args[2]
            list_star_rank_id = []  
            list_star_rank_full_name = []  

            ## Initaize 
            local_lib_github = lib_github.LibGithub(username, password, opt_verbose)

            #list_repos = local_lib_github.user_get_repos()
            
            ## start ranking over 43k   
            str_query='stars:>43000'
            str_sort='stars'
            list_repos = local_lib_github.search_repos(str_query,str_sort)

            ## Show Star Ranking Top 100 Repo id and full name
            for rank_idx,repo in enumerate(list_repos):
                rank_idx +=1
                #list_repo_info = local_lib_github.get_repo(repo.full_name)
                msg = '{} Ranking: {}; Repositorie id:{} full_name:{}.'
                logger.info( msg.format(str_sort.upper(), rank_idx, repo.id,repo.full_name) ) 

                list_star_rank_id.append(repo.id)
                list_star_rank_full_name.append(repo.full_name)

                if rank_idx == 100: break        

            # Get Star Ranking Top 1 Repo data  
            #star_ranking_top_1_id = list_star_rank_id[0]
            #repo = local_lib_github.get_repo(star_ranking_top_1_id)            
            #print('\n')
            #msg = 'Top 1 Star Ranking: Repositorie id:{} full_name:{} Star_Count:{}.'
            #logger.info( msg.format( list_star_rank_id[0], list_star_rank_full_name[0], repo.stargazers_count) ) 
            
            # Get GitHub Repo from UNPKG in JSON fromat  
            local_webapi_json = lib_github.WebAPI_JSON(opt_verbose)
            str_data = local_webapi_json.dataGet()            
            json_data = local_webapi_json.jsonConversion(str_data)
            
            print('\n')            
            msg = 'Top 1 Star Ranking, key: ; value:'
            logger.info(msg) 
            
            for key, value in json_data[0].items():
                msg = '{}; {}.'
                logger.info( msg.format( key, value) ) 
                
    except IndexError:
        print('IndexError: Usage "python %s github_username github_password"' % ( args[0]))
    
    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))        