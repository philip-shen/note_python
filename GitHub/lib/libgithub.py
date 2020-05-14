# 2020/05/14 Initial 
######################################################
from logger import logger
from github import Github

import urllib.request; #用來建立請求
import json
import sys, time, os
import codecs

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
                msg = '{} Ranking: {}; Repositorie id:{} full_name:{}.'
                logger.info( msg.format(str_sort.upper(), rank_idx ,repo.id ,repo.full_name) ) 

        return repositories        

    def get_repo(self, str_repo_id=''):

        repo = self.g_token.get_repo(str_repo_id)

        if self.opt_verbose.lower() == 'on':
            msg = 'repositorie contents: {}.'
            logger.info(msg.format(repo))

        return repo    

class WebAPI_JSON:
    def __init__(self,opt_verbose='OFF'):
        
        self.opt_verbose = opt_verbose 
        # URI Schema
        self.url = 'https://unpkg.com/@wcj/github-rank@'+'20.5.14'+'/dist/repos.json'

    '''
    https://stackoverflow.max-everyday.com/2018/06/python-3-urllib/

    python 3 筆記 – 利用urllib來存取網頁

    錯誤訊息：

    Import error: No module name urllib2
    解法：

    from urllib.request import urlopen
    html = urlopen("http://www.google.com/")
    print(html)
    
    python3 基本款式：

    import urllib.request; #用來建立請求

    存取網頁Ex 1:
    x = urllib.request.urlopen('https://www.google.com');
    print(x.read());
    
    存取網頁Ex 2:
    url = 'https://www.google.com';
    values = {'s':'basic',
              'submit':'search'}; #參數及參數值
    data = urllib.parse.urlencode(values); #解析並轉為url編碼格式
    data = data.encode('utf-8'); #將所有網址用utf8解碼
    req = urllib.request.Request(url, data); #建立請求
    resp = urllib.request.urlopen(req); #開啟網頁
    respData = resp.read();
    print(respData);
    '''

    '''
    [Convert bytes to a string](https://stackoverflow.com/questions/606191/convert-bytes-to-a-string) 

    >>> b"abcde"
    b'abcde'

    # utf-8 is used here because it is a very common encoding, but you
    # need to use the encoding your data is actually in.
    >>> b"abcde".decode("utf-8") 
    'abcde'

    https://medium.com/better-programming/strings-unicode-and-bytes-in-python-3-everything-you-always-wanted-to-know-27dc02ff2686
    1.str can be encoded into bytes using the encode() method.
    2.bytes can be decoded to str using the decode() method.
    '''
    def dataGet(self):
        # URI parameter
        #paramStr = urllib.urlencode(param)

        # Read
        readObj = urllib.request.urlopen(self.url)

        # webAPIからのJSONを取得
        response = readObj.read()

        '''
        Type of response: <class 'bytes'>.
        '''
        '''
        b'[\n  {\n    "id": 28457823,\n    "node_id": "MDEwOlJlcG9zaXRvcnkyODQ1NzgyMw==",\n    
        "name": "freeCodeCamp",\n    "full_name": "freeCodeCamp/freeCodeCamp",\n    "private": false,\n    
        "owner": {\n      "login": "freeCodeCamp",\n      "id": 9892522,\n      "node_id": "MDEyOk9yZ2FuaXphdGlvbjk4OTI1MjI=",\n      "avatar_url": "https://avatars0.githubusercontent.com/u/9892522?v=4",\n      "gravatar_id": "",\n      "url": "https://api.github.com/users/freeCodeCamp",\n      "html_url": "https://github.com/freeCodeCamp",\n      "followers_url": "https://api.github.com/users/freeCodeCamp/followers",\n      "following_url": "https://api.github.com/users/freeCodeCamp/following{/other_user}",\n      "gists_url": "https://api.github.com/users/freeCodeCamp/gists{/gist_id}",\n      "starred_url": "https://api.github.com/users/freeCodeCamp/starred{/owner}{/repo}",\n      "subscriptions_url": "https://api.github.com/users/freeCodeCamp/subscriptions",\n      "organizations_url": "https://api.github.com/users/freeCodeCamp/orgs",\n      "repos_url": "https://api.github.com/users/freeCodeCamp/repos",\n      "events_url": "https://api.github.com/users/freeCodeCamp/events{/privacy}",\n      "received_events_url": "https://api.github.com/users/freeCodeCamp/received_events",\n      "type": "Organization",\n      "site_admin": false\n    },\n    "html_url": "https://github.com/freeCodeCamp/freeCodeCamp",\n    "description": "freeCodeCamp.org\'s open source codebase and curriculum. Learn to code at home.",\n    "fork": false,\n    "url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp",\n    "forks_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/forks",\n    "keys_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/keys{/key_id}",\n    "collaborators_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/collaborators{/collaborator}",\n    "teams_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/teams",\n    "hooks_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/hooks",\n    "issue_events_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/issues/events{/number}",\n    "events_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/events",\n    "assignees_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/assignees{/user}",\n    "branches_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/branches{/branch}",\n    "tags_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/tags",\n    "blobs_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/blobs{/sha}",\n    "git_tags_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/tags{/sha}",\n    "git_refs_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/refs{/sha}",\n    "trees_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/trees{/sha}",\n    "statuses_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/statuses/{sha}",\n    "languages_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/languages",\n    "stargazers_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/stargazers",\n    "contributors_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/contributors",\n    "subscribers_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/subscribers",\n    "subscription_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/subscription",\n    "commits_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/commits{/sha}",\n    "git_commits_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/commits{/sha}",\n    "comments_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/comments{/number}",\n    "issue_comment_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/issues/comments{/number}",\n    "contents_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/contents/{+path}",\n    "compare_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/compare/{base}...{head}",\n    "merges_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/merges",\n    "archive_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/{archive_format}{/ref}",\n    "downloads_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/downloads",\n    "issues_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/issues{/number}",\n    "pulls_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/pulls{/number}",\n    "milestones_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/milestones{/number}",\n    "notifications_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/notifications{?since,all,participating}",\n    "labels_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/labels{/name}",\n    "releases_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/releases{/id}",\n    "deployments_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/deployments",\n    "created_at": "2014-12-24T17:49:19Z",\n    "updated_at": "2020-05-13T21:47:08Z",\n    "pushed_at": "2020-05-13T21:24:24Z",\n    "git_url": "git://github.com/freeCodeCamp/freeCodeCamp.git",\n    "ssh_url": "git@github.com:freeCodeCamp/freeCodeCamp.git",\n    "clone_url": "https://github.com/freeCodeCamp/freeCodeCamp.git",\n    "svn_url": "https://github.com/freeCodeCamp/freeCodeCamp",\n    "homepage": "https://contribute.freecodecamp.org",\n    "size": 126597,\n    "stargazers_count": 310682,\n    "watchers_count": 310682,\n    "language": "JavaScript",\n    "has_issues": true,\n    "has_projects": false,\n    "has_downloads": true,\n    "has_wiki": false,\n    "has_pages": true,\n    "forks_count": 24060,\n    "mirror_url": null,\n    "archived": false,\n    "disabled": false,\n    "open_issues_count": 272,\n    "license": {\n      "key": "bsd-3-clause",\n      "name": "BSD 3-Clause \\"New\\" or \\"Revised\\" License",\n      "spdx_id": "BSD-3-Clause",\n      "url": "https://api.github.com/licenses/bsd-3-clause",\n      "node_id": "MDc6TGljZW5zZTU="\n    },\n    "forks": 24060,\n    "open_issues": 272,\n    "watchers": 310682,\n    "default_branch": "master",\n    "score": 1\n  },\n  {\n    "id": 177736533,\n    "node_id": "MDEwOlJlcG9zaXRvcnkxNzc3MzY1MzM=",\n    "name": "996.ICU",\n    "full_name": "996icu/996.ICU",\n    "private": false,\n    "owner": {\n      "login": "996icu",\n      "id": 48942249,\n      "node_id": "MDQ6VXNlcjQ4OTQyMjQ5",\n      "avatar_url": "https://avatars3.githubusercontent.com/u/48942249?v=4",\n      "gravatar_id": "",\n      "url": "https://api.github.com/users/996icu",\n      "html_url": "https://github.com/996icu",\n      "followers_url": "https://api.github.com/users/996icu/followers",\n      "following_url": "https://api.github.com/users/996icu/following{/other_user}",\n      "gists_url": "https://api.github.com/users/996icu/gists{/gist_id}",\n      "starred_url": "https://api.github.com/users/996icu/starred{/owner}{/repo}",\n      "subscriptions_url": "https://api.github.com/users/996icu/subscriptions",\n      "organizations_url": "https://api.github.com/users/996icu/orgs",\n      "repos_url": "https://api.github.com/users/996icu/repos",\n      "events_url": "https://api.github.com/users/996icu/events{/privacy}",\n      "received_events_url": "https://api.github.com/users/996icu/received_events",\n      "type": "User",\n      "site_admin": false\n    },\n    "html_url": "https://github.com/996icu/996.ICU",\n    "description": "Repo for counting stars and contributing. Press F to pay respect to glorious developers.",\n    "fork": false,\n    "url": "https://api.github.com/repos/996icu/996.ICU",\n    "forks_url": "https://api.github.com/repos/996icu/996.ICU/forks",\n    "keys_url": "https://api.github.com/repos/996icu/996.ICU/keys{/key_id}",\n    "collaborators_url": "https://api.github.com/repos/996icu/996.ICU/collaborators{/collaborator}",\n    "teams_url": "https://api.github.com/repos/996icu/996.ICU/teams",\n    "hooks_url": "https://api.github.com/repos/996icu/996.ICU/hooks",\n    "issue_events_url": "https://api.github.com/repos/996icu/996.ICU/issues/events{/number}",\n    "events_url": "https://api.github.com/repos/996icu/996.ICU/events",\n    "assignees_url": "https://api.github.com/repos/996icu/996.ICU/assignees{/user}",\n    "branches_url": "https://api.github.com/repos/996icu/996.ICU/branches{/branch}",\n    "tags_url": "https://api.github.com/repos/996icu/996.ICU/tags",\n    "blobs_url": "https://api.github.com/repos/996icu/996.ICU/git/blobs{/sha}",\n    "git_tags_url": "https://api.github.com/repos/996icu/996.ICU/git/tags{/sha}",\n    "git_refs_url": "https://api.github.com/repos/996icu/996.ICU/git/refs{/sha}",\n    "trees_url": "https://api.github.com/repos/996icu/996.ICU/git/trees{/sha}",\n    "statuses_url": "https://api.github.com/repos/996icu/996.ICU/statuses/{sha}",\n    "languages_url": "https://api.github.com/repos/996icu/996.ICU/languages",\n    "stargazers_url": "https://api.github.com/repos/996icu/996.ICU/stargazers",\n    "contributors_url": "https://api.github.com/repos/996icu/996.ICU/contributors",\n    "subscribers_url": "https://api.github.com/repos/996icu/996.ICU/subscribers",\n    "subscription_url": "https://api.github.com/repos/996icu/996.ICU/subscription",\n    "commits_url": "https://api.github.com/repos/996icu/996.ICU/commits{/sha}",\n    "git_commits_url": "https://api.github.com/repos/996icu/996.ICU/git/commits{/sha}",\n    "comments_url": "https://api.github.com/repos/996icu/996.ICU/comments{/number}",\n    "issue_comment_url": "https://api.github.com/repos/996icu/996.ICU/issues/comments{/number}",\n    "contents_url": "https://api.github.com/repos/996icu/996.ICU/contents/{+path}",\n    "compare_url": "https://api.github.com/repos/996icu/996.ICU/compare/{base}...{head}",\n    "merges_url": "https://api.github.com/repos/996icu/996.ICU/merges",\n    "archive_url": "https://api.github.com/repos/996icu/996.ICU/{archive_format}{/ref}",\n    "downloads_url": "https://api.github.com/repos/996icu/996.ICU/downloads",\n    
        "issues_url": "https://api.github.com/repos/996icu/996.ICU/issues{/number}",\n    
        "pulls_url": "https://api.github.com/repos/996icu/996.ICU/pulls{/number}",\n    
        "milestones_url": "https://api.github.com/repos/996icu/996.ICU/milestones{/number}",\n    
        "notifications_url": "https://api.github.com/repos/996icu/996.ICU/notifications{?since,all,participating}",\n    
        "labels_url": "https://api.github.com/repos/996icu/996.ICU/labels{/name}",\n    
        "releases_url": "https://api.github.com/repos/996icu/996.ICU/releases{/id}",\n    
        "deployments_url": "https://api.github.com/repos/996icu/996.ICU/deployments",\n    
        "created_at": "2019-03-26T07:31:14Z",\n    "updated_at": "2020-05-13T23:50:14Z",\n    
        "pushed_at": "2020-05-08T03:45:15Z",\n    "git_url": "git://github.com/996icu/996.ICU.git",\n    "ssh_url": "git@github.com:996icu/996.ICU.git",\n    "clone_url": "https://github.com/996icu/996.ICU.git",\n    "svn_url": "https://github.com/996icu/996.ICU",\n    "homepage": "https://996.icu",\n    "size": 183401,\n    "stargazers_count": 249514,\n    "watchers_count": 249514,\n    "language": "Rust",\n    "has_issues": false,\n    "has_projects": false,\n    "has_downloads": true,\n    "has_wiki": false,\n    "has_pages": false,\n    "forks_count": 21127,\n    "mirror_url": null,\n    "archived": false,\n    "disabled": false,\n    "open_issues_count": 16771,\n    "license": {\n      "key": "other",\n      "name": "Other",\n      "spdx_id": "NOASSERTION",\n      "url": null,\n      "node_id": "MDc6TGljZW5zZTA="\n    },\n    "forks": 21127,\n    "open_issues": 16771,\n    "watchers": 249514,\n    "default_branch": "master",\n    "score": 1\n  },\n
        '''

        '''
        Type of response: <class 'bytes'>.
        '''
        '''
        Type of decode(ut-f8) of response: <class 'str'>.
        '''

        '''
        Response: [
  {
    "id": 28457823,
    "node_id": "MDEwOlJlcG9zaXRvcnkyODQ1NzgyMw==",
    "name": "freeCodeCamp",
    "full_name": "freeCodeCamp/freeCodeCamp",
    "private": false,
    "owner": {
      "login": "freeCodeCamp",
      "id": 9892522,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjk4OTI1MjI=",
      "avatar_url": "https://avatars0.githubusercontent.com/u/9892522?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/freeCodeCamp",
      "html_url": "https://github.com/freeCodeCamp",
      "followers_url": "https://api.github.com/users/freeCodeCamp/followers",
      "following_url": "https://api.github.com/users/freeCodeCamp/following{/other_user}",
      "gists_url": "https://api.github.com/users/freeCodeCamp/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/freeCodeCamp/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/freeCodeCamp/subscriptions",
      "organizations_url": "https://api.github.com/users/freeCodeCamp/orgs",
      "repos_url": "https://api.github.com/users/freeCodeCamp/repos",
      "events_url": "https://api.github.com/users/freeCodeCamp/events{/privacy}",
      "received_events_url": "https://api.github.com/users/freeCodeCamp/received_events",
      "type": "Organization",
      "site_admin": false
    },
    "html_url": "https://github.com/freeCodeCamp/freeCodeCamp",
    "description": "freeCodeCamp.org's open source codebase and curriculum. Learn to code at home.",
    "fork": false,
    "url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp",
    "forks_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/forks",
    "keys_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/teams",
    "hooks_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/hooks",
    "issue_events_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/issues/events{/number}",
    "events_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/events",
    "assignees_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/assignees{/user}",
    "branches_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/branches{/branch}",
    "tags_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/tags",
    "blobs_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/languages",
    "stargazers_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/stargazers",
    "contributors_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/contributors",
    "subscribers_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/subscribers",
    "subscription_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/subscription",
    "commits_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/contents/{+path}",
    "compare_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/merges",
    "archive_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/downloads",
    "issues_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/issues{/number}",
    "pulls_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/labels{/name}",
    "releases_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/releases{/id}",
    "deployments_url": "https://api.github.com/repos/freeCodeCamp/freeCodeCamp/deployments",
    "created_at": "2014-12-24T17:49:19Z",
    "updated_at": "2020-05-13T21:47:08Z",
    "pushed_at": "2020-05-13T21:24:24Z",
    "git_url": "git://github.com/freeCodeCamp/freeCodeCamp.git",
    "ssh_url": "git@github.com:freeCodeCamp/freeCodeCamp.git",
    "clone_url": "https://github.com/freeCodeCamp/freeCodeCamp.git",
    "svn_url": "https://github.com/freeCodeCamp/freeCodeCamp",
    "homepage": "https://contribute.freecodecamp.org",
    "size": 126597,
    "stargazers_count": 310682,
    "watchers_count": 310682,
    "language": "JavaScript",
    "has_issues": true,
    "has_projects": false,
    "has_downloads": true,
    "has_wiki": false,
    "has_pages": true,
    "forks_count": 24060,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 272,
    "license": {
      "key": "bsd-3-clause",
      "name": "BSD 3-Clause \"New\" or \"Revised\" License",
      "spdx_id": "BSD-3-Clause",
      "url": "https://api.github.com/licenses/bsd-3-clause",
      "node_id": "MDc6TGljZW5zZTU="
    },
    "forks": 24060,
    "open_issues": 272,
    "watchers": 310682,
    "default_branch": "master",
    "score": 1
  },
  {
    "id": 177736533,
    "node_id": "MDEwOlJlcG9zaXRvcnkxNzc3MzY1MzM=",
    "name": "996.ICU",
    "full_name": "996icu/996.ICU",
    "private": false,
    "owner": {
      "login": "996icu",
      "id": 48942249,
      "node_id": "MDQ6VXNlcjQ4OTQyMjQ5",
      "avatar_url": "https://avatars3.githubusercontent.com/u/48942249?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/996icu",
      "html_url": "https://github.com/996icu",
      "followers_url": "https://api.github.com/users/996icu/followers",
      "following_url": "https://api.github.com/users/996icu/following{/other_user}",
      "gists_url": "https://api.github.com/users/996icu/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/996icu/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/996icu/subscriptions",
      "organizations_url": "https://api.github.com/users/996icu/orgs",
      "repos_url": "https://api.github.com/users/996icu/repos",
      "events_url": "https://api.github.com/users/996icu/events{/privacy}",
      "received_events_url": "https://api.github.com/users/996icu/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/996icu/996.ICU",
    "description": "Repo for counting stars and contributing. Press F to pay respect to glorious developers.",
    "fork": false,
    "url": "https://api.github.com/repos/996icu/996.ICU",
    "forks_url": "https://api.github.com/repos/996icu/996.ICU/forks",
    "keys_url": "https://api.github.com/repos/996icu/996.ICU/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/996icu/996.ICU/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/996icu/996.ICU/teams",
    "hooks_url": "https://api.github.com/repos/996icu/996.ICU/hooks",
    "issue_events_url": "https://api.github.com/repos/996icu/996.ICU/issues/events{/number}",
    "events_url": "https://api.github.com/repos/996icu/996.ICU/events",
    "assignees_url": "https://api.github.com/repos/996icu/996.ICU/assignees{/user}",
    "branches_url": "https://api.github.com/repos/996icu/996.ICU/branches{/branch}",
    "tags_url": "https://api.github.com/repos/996icu/996.ICU/tags",
    "blobs_url": "https://api.github.com/repos/996icu/996.ICU/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/996icu/996.ICU/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/996icu/996.ICU/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/996icu/996.ICU/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/996icu/996.ICU/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/996icu/996.ICU/languages",
    "stargazers_url": "https://api.github.com/repos/996icu/996.ICU/stargazers",
    "contributors_url": "https://api.github.com/repos/996icu/996.ICU/contributors",
    "subscribers_url": "https://api.github.com/repos/996icu/996.ICU/subscribers",
    "subscription_url": "https://api.github.com/repos/996icu/996.ICU/subscription",
    "commits_url": "https://api.github.com/repos/996icu/996.ICU/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/996icu/996.ICU/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/996icu/996.ICU/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/996icu/996.ICU/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/996icu/996.ICU/contents/{+path}",
    "compare_url": "https://api.github.com/repos/996icu/996.ICU/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/996icu/996.ICU/merges",
    "archive_url": "https://api.github.com/repos/996icu/996.ICU/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/996icu/996.ICU/downloads",
    "issues_url": "https://api.github.com/repos/996icu/996.ICU/issues{/number}",
    "pulls_url": "https://api.github.com/repos/996icu/996.ICU/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/996icu/996.ICU/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/996icu/996.ICU/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/996icu/996.ICU/labels{/name}",
    "releases_url": "https://api.github.com/repos/996icu/996.ICU/releases{/id}",
    "deployments_url": "https://api.github.com/repos/996icu/996.ICU/deployments",
    "created_at": "2019-03-26T07:31:14Z",
    "updated_at": "2020-05-13T23:50:14Z",
    "pushed_at": "2020-05-08T03:45:15Z",
    "git_url": "git://github.com/996icu/996.ICU.git",
    "ssh_url": "git@github.com:996icu/996.ICU.git",
    "clone_url": "https://github.com/996icu/996.ICU.git",
    "svn_url": "https://github.com/996icu/996.ICU",
    "homepage": "https://996.icu",
    "size": 183401,
    "stargazers_count": 249514,
    "watchers_count": 249514,
    "language": "Rust",
    "has_issues": false,
    "has_projects": false,
    "has_downloads": true,
    "has_wiki": false,
    "has_pages": false,
    "forks_count": 21127,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 16771,
    "license": {
      "key": "other",
      "name": "Other",
      "spdx_id": "NOASSERTION",
      "url": null,
      "node_id": "MDc6TGljZW5zZTA="
    },
    "forks": 21127,
    "open_issues": 16771,
    "watchers": 249514,
    "default_branch": "master",
    "score": 1
  },

中略
  
  {
    "id": 18351848,
    "node_id": "MDEwOlJlcG9zaXRvcnkxODM1MTg0OA==",
    "name": "lowdb",
    "full_name": "typicode/lowdb",
    "private": false,
    "owner": {
      "login": "typicode",
      "id": 5502029,
      "node_id": "MDQ6VXNlcjU1MDIwMjk=",
      "avatar_url": "https://avatars2.githubusercontent.com/u/5502029?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/typicode",
      "html_url": "https://github.com/typicode",
      "followers_url": "https://api.github.com/users/typicode/followers",
      "following_url": "https://api.github.com/users/typicode/following{/other_user}",
      "gists_url": "https://api.github.com/users/typicode/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/typicode/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/typicode/subscriptions",
      "organizations_url": "https://api.github.com/users/typicode/orgs",
      "repos_url": "https://api.github.com/users/typicode/repos",
      "events_url": "https://api.github.com/users/typicode/events{/privacy}",
      "received_events_url": "https://api.github.com/users/typicode/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/typicode/lowdb",
    "description": "⚡️ lowdb is a small local JSON database powered by Lodash (supports Node, Electron and the browser)",
    "fork": false,
    "url": "https://api.github.com/repos/typicode/lowdb",
    "forks_url": "https://api.github.com/repos/typicode/lowdb/forks",
    "keys_url": "https://api.github.com/repos/typicode/lowdb/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/typicode/lowdb/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/typicode/lowdb/teams",
    "hooks_url": "https://api.github.com/repos/typicode/lowdb/hooks",
    "issue_events_url": "https://api.github.com/repos/typicode/lowdb/issues/events{/number}",
    "events_url": "https://api.github.com/repos/typicode/lowdb/events",
    "assignees_url": "https://api.github.com/repos/typicode/lowdb/assignees{/user}",
    "branches_url": "https://api.github.com/repos/typicode/lowdb/branches{/branch}",
    "tags_url": "https://api.github.com/repos/typicode/lowdb/tags",
    "blobs_url": "https://api.github.com/repos/typicode/lowdb/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/typicode/lowdb/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/typicode/lowdb/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/typicode/lowdb/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/typicode/lowdb/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/typicode/lowdb/languages",
    "stargazers_url": "https://api.github.com/repos/typicode/lowdb/stargazers",
    "contributors_url": "https://api.github.com/repos/typicode/lowdb/contributors",
    "subscribers_url": "https://api.github.com/repos/typicode/lowdb/subscribers",
    "subscription_url": "https://api.github.com/repos/typicode/lowdb/subscription",
    "commits_url": "https://api.github.com/repos/typicode/lowdb/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/typicode/lowdb/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/typicode/lowdb/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/typicode/lowdb/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/typicode/lowdb/contents/{+path}",
    "compare_url": "https://api.github.com/repos/typicode/lowdb/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/typicode/lowdb/merges",
    "archive_url": "https://api.github.com/repos/typicode/lowdb/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/typicode/lowdb/downloads",
    "issues_url": "https://api.github.com/repos/typicode/lowdb/issues{/number}",
    "pulls_url": "https://api.github.com/repos/typicode/lowdb/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/typicode/lowdb/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/typicode/lowdb/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/typicode/lowdb/labels{/name}",
    "releases_url": "https://api.github.com/repos/typicode/lowdb/releases{/id}",
    "deployments_url": "https://api.github.com/repos/typicode/lowdb/deployments",
    "created_at": "2014-04-02T02:16:06Z",
    "updated_at": "2020-05-13T19:33:54Z",
    "pushed_at": "2020-04-18T01:06:31Z",
    "git_url": "git://github.com/typicode/lowdb.git",
    "ssh_url": "git@github.com:typicode/lowdb.git",
    "clone_url": "https://github.com/typicode/lowdb.git",
    "svn_url": "https://github.com/typicode/lowdb",
    "homepage": "",
    "size": 1263,
    "stargazers_count": 12990,
    "watchers_count": 12990,
    "language": "JavaScript",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": true,
    "forks_count": 601,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 91,
    "license": {
      "key": "mit",
      "name": "MIT License",
      "spdx_id": "MIT",
      "url": "https://api.github.com/licenses/mit",
      "node_id": "MDc6TGljZW5zZTEz"
    },
    "forks": 601,
    "open_issues": 91,
    "watchers": 12990,
    "default_branch": "master",
    "score": 1
  }
].
        '''

        str_response = response.decode("utf-8");# return string

        if self.opt_verbose.lower() == 'on':
            msg = 'Type of response: {}.'
            logger.info(msg.format(type(response)))
            
            msg = 'Type of decode(ut-f8) of response: {}.'
            logger.info(msg.format( type(str_response )))
            
            
            msg = 'Length of str_response {}.'
            logger.info(msg.format( len(str_response) ))           

        return str_response

    # Data from webAPI then change to JSON format
    def jsonConversion(self,jsonStr):

        # webAPIから取得したJSONデータをpythonで使える形に変換する
        json_data = json.loads(jsonStr)
        
        if self.opt_verbose.lower() == 'on':
            msg = 'jsonStr: {}.'
            logger.info(msg.format(jsonStr))

            msg = 'json_data: {}.'
            logger.info(msg.format(json_data))

        return json_data    


        
