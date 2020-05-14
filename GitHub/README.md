
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Environment](#environment)
   * [Prerequirment](#prerequirment)
   * [Test Results](#test-results)
      * [Start Search Top 100 Star Ranking by Login Username and password](#start-search-top-100-star-ranking-by-login-username-and-password)
      * [List All Elements of Top 10 Star Ranking Repository](#list-all-elements-of-top-10-star-ranking-repository)
   * [The Most Popular and The Most Fork Repositories](#the-most-popular-and-the-most-fork-repositories)
      * [Most Forks](#most-forks)
      * [Most Starred](#most-starred)
   * [Get GitHub Information by PyGithub](#get-github-information-by-pygithub)
      * [GitHub Instance](#github-instance)
      * [GitHub Repositories List](#github-repositories-list)
      * [GitHub Repositories Starts](#github-repositories-starts)
   * [GitHub Repositories Starts Search](#github-repositories-starts-search)
      * [Example](#example)
   * [Github Repositories Ranking.](#github-repositories-ranking)
      * [UNPKG](#unpkg)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
      * [Script to list all repos for a github organization](#script-to-list-all-repos-for-a-github-organization)
      * [GitHub Repositories Starts Ranking](#github-repositories-starts-ranking)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Purpose
Take note of GitHub stuffs

# Environment  
* OS: Win 10 Home 64bit
* Python:3.6+ 


# Prerequirment  
```
pip3 install -r requirements.txt
```


# Test Results  
```
cd E:\note_python\GitHub\test
e:

python test_github.py xxxx(github_usernamt) xxxx(github_password)
```
## Start Search Top 100 Star Ranking by Login Username and password  
![alt tag](https://i.imgur.com/eeyheBk.jpg)  

![alt tag](https://i.imgur.com/KIB0MQt.jpg)  

## List All Elements of Top 10 Star Ranking Repository
![alt tag](https://i.imgur.com/MgCfvqu.png)  

![alt tag](https://i.imgur.com/e6zGAdp.png)  


# The Most Popular and The Most Fork Repositories  
[How to find out “The most popular repositories” on Github? [closed] edited Jun 12 '16](https://stackoverflow.com/questions/19855552/how-to-find-out-the-most-popular-repositories-on-github)  

## Most Forks  
```
https://github.com/search?o=desc&p=1&q=stars%3A%3E1&s=forks&type=Repositories
```

```
https://github.com/search?o=desc&p=2&q=stars%3A%3E1&s=forks&type=Repositories
```

```
https://github.com/search?o=desc&p=3&q=stars%3A%3E1&s=forks&type=Repositories
```

## Most Starred  
```
https://github.com/search?p=1&q=stars%3A%3E100&s=stars&type=Repositories
```

```
https://github.com/search?p=2&q=stars%3A%3E100&s=stars&type=Repositories
```

```
https://github.com/search?p=3&q=stars%3A%3E100&s=stars&type=Repositories
```

# Get GitHub Information by PyGithub  
[PyGithubを使って、GitHubの情報を取得する Mar 17, 2020](https://qiita.com/yshr10ic/items/a416ba6fbea7637be552)  

## GitHub Instance  
[GitHubインスタンスの作成](https://qiita.com/yshr10ic/items/a416ba6fbea7637be552#github%E3%82%A4%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%B3%E3%82%B9%E3%81%AE%E4%BD%9C%E6%88%90)  
```
create_instance.py

from github import Github

# ユーザ名、パスワードによるインスタンス生成
g = GitHub('username', 'password')

# アクセストークンによるインスタンス生成
g = Github('access_token')

# カスタムホストによるGitHubエンタープライズのインスタンス生成
g = Github(base_url='https://{hostname}/api/v3', login_or_token='access_token')
```

## GitHub Repositories List  
```
get_repos.py

for repo in g.get_user().get_repos():
    print(repo)

```

```
Repository(full_name="yshr10ic/deep-learning-from-scratch")
Repository(full_name="yshr10ic/deep-learning-from-scratch-2")
...
```

## GitHub Repositories Starts  
```
get_count_of_stars.py

repo = g.get_repo('yshr10ic/deep-learning-from-scratch-2')
print(repo.stargazers_count)
```

```
1
```

# GitHub Repositories Starts Search  
[https://qiita.com/mazu/items/dd5042d22ef0d52ab0e1 updated at 2018-06-22](https://qiita.com/mazu/items/dd5042d22ef0d52ab0e1)  

## Example  
検索の例 | 説明 | urlクエリー
------------------------------------ | --------------------------------------------- | --------------------------------------------- 
crud stars:>=100 | CRUDを含むスター100以上 | https://github.com/search?q=crud+stars%3A%3E100
crud language:python stars:>=100 | CRUDを含むpython言語のスター100以上 | https://github.com/search?q=crud+language%3Apython+stars%3A%3E%3D100
crud stars:>=100 created:>2016-04-01 | crudを含むスター100以上で作成日2016年4/1以降のもの | https://github.com/search?q=crud+stars%3A%3E%3D100+created%3A%3E2015-04-01

[https://help.github.com/articles/understanding-the-search-syntax/](https://help.github.com/articles/understanding-the-search-syntax/)

# Github Repositories Ranking.
[Github Repositories Ranking. - 小弟调调](https://wangchujiang.com/github-rank/repos.html)
![alt tag](https://i.imgur.com/IfoSd3s.png)  

[jaywcjlove/github-rank](https://github.com/jaywcjlove/github-rank)
> Github 中国和全球用户排名，全球仓库 Star 最多排名(自动日更)。 http://jaywcjlove.github.io/github-rank/  

## UNPKG  
```
https://unpkg.com/@wcj/github-rank@20.5.14/dist/repos.json
```
![alt tag](https://i.imgur.com/8YaYOJI.png)  


# Troubleshooting


# Reference



## Script to list all repos for a github organization  
[Script to list all repos for a github organization · GitHub](https://gist.github.com/ralphbean/5733076)



## GitHub Repositories Starts Ranking  
[GitHubリポジトリのスター数ランキングを表示する updated at 2019-06-09](https://qiita.com/notakaos/items/e344bbeca52e41df443a)  
```
curl -H "Accept: application/vnd.github.mercy-preview+json" "https://api.github.com/search/repositories?q=stars:%3E1&s=stars&type=Repositories"
```

```
1curl -H "Accept: application/vnd.github.mercy-preview+json" "https://api.github.com/search/repositories?q=stars:%3E1&s=stars&type=Repositories" | jq '.items[] | [.full_name, .html_url, .language // "-", .stargazers_count] | @tsv' -r | awk '{printf("%d|[%s](%s)|%s|%'"'"'d\n", NR, $1, $2, $3, $4)}'
```


[github3.py: A Library for Using GitHub's REST API](https://github3py.readthedocs.io/en/master/)

* []()  
![alt tag]()  

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3



