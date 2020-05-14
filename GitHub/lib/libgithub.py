# 2020/05/14 Initial 
######################################################
from logger import logger
from github import Github

class LibGithub:
    def __init__(self,github_username,github_password,opt_verbose='OFF'):
        self.github_username = github_username
        self.github_password = github_password
        self.opt_verbose = opt_verbose 

        self.g_token = Github(self.github_username, self.github_password)       

    def user_get_repos(self):
        repo  = []
        
        for repo in self.g_token.get_user().get_repos():
            
            if self.opt_verbose.lower() == 'on':
                msg = 'repositorie: {}.'
                logger.info(msg.format(repo)) 

        return self.g_token.get_user().get_repos()

    '''
    https://pygithub.readthedocs.io/en/latest/github.html?highlight=search_repositories#github.MainClass.Github.search_repositories
    query – string
    sort – string (‘stars’, ‘forks’, ‘updated’)
    order – string (‘asc’, ‘desc’)
    '''

    def search_repos(self, str_query='language:python',str_sort='stars',str_order='desc'):
        repositories = []
        
        repositories = self.g_token.search_repositories(str_query,str_sort,str_order)

        for rank_idx,repo in enumerate(repositories):            

            if self.opt_verbose.lower() == 'on':
                rank_idx +=1
                msg = '{ } Ranking: {}; Repositorie id:{} full_name:{}.'
                logger.info( msg.format(str_sort.upper(), rank_idx ,repo.id ,repo.full_name) ) 

        return repositories        

    def get_repo(self, str_repo_id=''):

        repo = self.g_token.get_repo(str_repo_id)

        if self.opt_verbose.lower() == 'on':
            msg = 'repositorie contents: {}.'
            logger.info(msg.format(repo))

        return repo    


