Table of Contents
=================

   * [Purpose](#purpose)
   * [Chromebookにpyenvでpython3.7.4をインストールするまで](#chromebookにpyenvでpython374をインストールするまで)
      * [環境](#環境)
      * [pyenvのインストール](#pyenvのインストール)
      * [Vim編集部分は、下記記事に助けてもらう](#vim編集部分は下記記事に助けてもらう)
      * [profileの再度読み込み](#profileの再度読み込み)
      * [pythonインストール](#pythonインストール)
      * [①pythonインストールのためのCコンパイラがない](#pythonインストールのためのcコンパイラがない)
      * [②zlibライブラリがインストールされていない](#zlibライブラリがインストールされていない)
      * [③libffi-devライブラリがインストールされていない](#libffi-devライブラリがインストールされていない)
      * [④上記対処だけでは、ワーニングがでてしまう](#上記対処だけではワーニングがでてしまう)
      * [デフォルトバージョンの変更](#デフォルトバージョンの変更)
      * [pipもインストールします](#pipもインストールします)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of Chromebook/ChromeOS

# Chromebookにpyenvでpython3.7.4をインストールするまで  
[Chromebookにpyenvでpython3.7.4をインストールするまで updated at 2019-12-01](https://qiita.com/DaikichiDaze/items/3a0382228d387f7615b3)

## 環境  
```
    Acer Chromebook R13
    ARM Cortex-A72 2.0GHz
    ChromeOS: 76.0.3809.136
        開発者モードへは切り替えていません
    git: 2.11.0 (標準インストール)
```

## pyenvのインストール  
()[https://qiita.com/shigechioyo/items/198211e84f8e0e9a5c18]
```
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv  
```

## Vim編集部分は、下記記事に助けてもらう 
()[https://qiita.com/kon_yu/items/b8864ff566b8b67a9810]
```
sudo vim ~/.profile
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
```

## profileの再度読み込み  
```
source ~/.profile
```

## pythonインストール
```
$ pyenv install 3.7.4
```

## ①pythonインストールのためのCコンパイラがない   
エラー 	configure: error: no acceptable C compiler found in $PATH
対処 	$ apt-get install build-essential
参考 	https://stackoverflow.com/questions/19816275/no-acceptable-c-compiler-found-in-path-when-installing-python

## ②zlibライブラリがインストールされていない  
エラー 	ZipImportError: can't decompress data; zlib not available
対処 	$ sudo apt-get install zlib1g-dev
参考 	https://qiita.com/banaoh/items/00aea13fe045fab7e8ba

## ③libffi-devライブラリがインストールされていない  
エラー 	ModuleNotFoundError: No module named '_ctypes'
対処 	$ sudo apt install libffi-dev
参考 	https://qiita.com/hitochan777/items/941d4422c53978b275f8

## ④上記対処だけでは、ワーニングがでてしまう  
```
WARNING: The Python bz2 extension was not compiled. Missing the bzip2 lib?```
WARNING: The Python readline extension was not compiled. Missing the GNU readline lib?
WARNING: The Python sqlite3 extension was not compiled. Missing the SQLite3 lib?
```

対処 	$ sudo apt-get install libbz2-dev libreadline-dev libsqlite3-dev
参考 	https://qiita.com/utgwkk/items/bf282ca95f64ef7dd594

## デフォルトバージョンの変更  
```
$ pyenv global 3.6.5
```

## pipもインストールします  
```
$ sudo apt-get install python3-pip
```


# Troubleshooting


# Reference

 


* []()  
![alt tag]()
<img src="" width="400" height="500">  

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



