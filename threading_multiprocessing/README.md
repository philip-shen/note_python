
Table of Contents
=================

   * [Purpose](#purpose)
   * [threading and multiprocessing](#threading-and-multiprocessing)
      * [threading](#threading)
      * [multiprocessing](#multiprocessing)
      * [multiprocessing](#multiprocessing-1)
         * [subprocess.run](#subprocessrun)
         * [subprocess.Popen](#subprocesspopen)
      * [concurrent.futures](#concurrentfutures)
         * [ExecutorとFuture](#executorとfuture)
         * [map、as_completedとwait](#mapas_completedとwait)
   * [subprocessの使い方(Python3.6)](#subprocessの使い方python36)
      * [Pip of shell script](#pip-of-shell-script)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take some note of threading and multiprocessing  

# threading and multiprocessing  
[Pythonのthreadingとmultiprocessingを完全理解 updated at 2020-11-04](https://qiita.com/kaitolucifer/items/e4ace07bd8e112388c75#threading%E3%81%A8multiprocessing)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F246522%2F9db33432-ebde-4226-849c-543708a98f9a.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=ccc9e36388dddc4d14bddc896ad3fd53" width="600" height="400">  

## threading  

## multiprocessing  

## multiprocessing  
```
Unix系OSではfork()で、子プロセスとして現在のプロセスのコピーを作成するのを説明しました。
つまり、Pythonでos.forkを呼び出すと、Pythonプログラムの子プロセスが作成されます。
しかし、Pythonプログラムではなく、外部コマンドが実行できる子プロセスが必要な時もあります。

Unix系OSにはもう1つexec()というシステムコールが存在します。
Pythonの中ではos.execveとして実装されています。
exec()は現在プロセスを他のプログラムで置き換える関数です。
つまり、os.forkでPythonプログラムの子プロセスを作り、os.execveで他のプログラム（シェルで実行できるls、pingのようなプログラム）で置き換えることができます。

標準ライブラリsubprocessは外部プログラムを実行する子プロセスを作成するためのモジュールです。
そして、subprocessで外部プログラムを実行する時は、
Pythonプロセスと子プロセスの間にプロセス間通信用のパイプ（Pipe）を構築し、パラメータを渡したり、戻り値やエラーを受け取ったりすることが可能になります。
```

### subprocess.run  
```
subprocess.run(args, *, stdin=None, input=None, 
    stdout=None, stderr=None, shell=False, timeout=None, check=False, universal_newlines=False)
```

### subprocess.Popen
```
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, 
    preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False,
    startup_info=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=())
```

メソッド | 説明 
------------------------------------ | --------------------------------------------- 
poll | 子プロセスの実行が終了したらステータスコードを返す；終了してないならNoneを返す
wait | 子プロセスの実行が終了するのを待つ；timeoutになったらTimeoutExpiredエラーを起こす
communicate | 子プロセスと通信を行う
send_signal | 子プロセスにシグナルを送る；例えばsignal.signal(signal.SIGINT)はUNIX系OSのコマンドラインで、Ctrl+Cを押した時のシグナル
terminate | 子プロセスを終了する
kill | 子プロセスを強制終了

```
# 2つの子プロセスをパイプで繋ぐ
p1 = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'Data'], stdin=p1.stdout, stdout=subprocess.PIPE)
out, err = p2.communicate()  # df -h | grep Data
print(out.decode())
```

```
/dev/disk1s1   466Gi  438Gi  8.0Gi    99% 1156881 4881295959    0%   /System/Volumes/Data
map auto_home    0Bi    0Bi    0Bi   100%       0          0  100%   /System/Volumes/Data/home
```

## concurrent.futures  
```

```

### ExecutorとFuture  
```
concurrent.futuresはThreadPoolExecutorとProcessPoolExecutorを提供していて，
これらはExecutorクラスを継承したものになります。

ThreadPoolExecutorとProcessPoolExecutorはmax_workersと
いうスレッド数またはプロセス数を指定する引数を受け取ります。
submitメソッドで1つのタスクを実行して、Futureクラスのインスタンスを返します。
```

```
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests


def load_url(url):
    return requests.get(url)


if __name__ == '__main__':
    url = 'https://www.python.org/'
    executor = ProcessPoolExecutor(max_workers=4)  # ThreadPoolExecutor(max_workers=4)
    future = executor.submit(load_url, url)
    print(future)
    while 1:
        if future.done():
            print('status code: {}'.format(future.result().status_code))
            break

```

### map、as_completedとwait  
```
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests


URLS = ['https://google.com', 'https://www.python.org/', 'https://api.github.com/']


def load_url(url):
    return requests.get(url)


if __name__ == '__main__':
    # with ThreadPoolExecutor(max_workers=4) as executor:
    with ProcessPoolExecutor(max_workers=4) as executor:
        for url, data in zip(URLS, executor.map(load_url, URLS)):
            print('{} - status_code {}'.format(url, data.status_code))
```

```
https://google.com - status_code 200
https://www.python.org/ - status_code 200
https://api.github.com/ - status_code 200
```

```
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import requests


URLS = ['https://google.com', 'https://www.python.org/', 'https://api.github.com/']


def load_url(url):
    return url, requests.get(url).status_code


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as executor:
        tasks = [executor.submit(load_url, url) for url in URLS]
        for future in as_completed(tasks):
            print(*future.result())
```

```
https://google.com 200
https://www.python.org/ 200
https://api.github.com/ 200
```

```
　waitメソッドはメインスレッド、メインプロセスをブロッキングさせます。
return_whenという引数で、3つの条件を設定できます。
```

条件 | 説明 
------------------------------------ | --------------------------------------------- 
ALL_COMPLETED | 全タスクが完成したらブロッキングを解放する
FIRST_COMPLETED | 任意のタスクが完成したらブロッキングを解放する
FIRST_EXCEPTION | 任意のタスクがエラーを起こしたらブロッキングを解放する

```
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, ALL_COMPLETED
import requests


URLS = ['https://google.com', 'https://www.python.org/', 'https://api.github.com/']


def load_url(url):
    requests.get(url)
    print(url)


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as executor:
        tasks = [executor.submit(load_url, url) for url in URLS]
        wait(tasks, return_when=ALL_COMPLETED)
        print('all completed.')  # 3つのprintの後にメインプロセスが解放されprintする
```

```
https://www.python.org/
https://api.github.com/
https://google.com
all completed.
```


# subprocessの使い方(Python3.6)  
[subprocessの使い方(Python3.6) updated at 2020-08-21](https://qiita.com/caprest/items/0245a16825789b0263ad)


## Pip of shell script  
```
p1 = subprocess.Popen(["dmesg"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "hda"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # SIGPIPE if p2 exits.
output = p2.communicate()[0]
```

* []()  
![alt tag]()
<img src="" width="" height="">  

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
