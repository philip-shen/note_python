
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [The Most Popular and The Most Fork Repositories](#the-most-popular-and-the-most-fork-repositories)
      * [Most Forks](#most-forks)
      * [Most Starred](#most-starred)
   * [Get GitHub Information by PyGithub](#get-github-information-by-pygithub)
      * [GitHub Instance](#github-instance)
      * [GitHub Repositories List](#github-repositories-list)
      * [GitHub Repositories Starts](#github-repositories-starts)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
      * [Script to list all repos for a github organization](#script-to-list-all-repos-for-a-github-organization)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of GitHub stuffs

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


# Troubleshooting


# Reference

## Script to list all repos for a github organization  
[Script to list all repos for a github organization · GitHub](https://gist.github.com/ralphbean/5733076)
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


