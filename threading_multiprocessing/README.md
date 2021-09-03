
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [threading and multiprocessing](#threading-and-multiprocessing)
      * [threading](#threading)
         * [インスタンス化(Instance)](#インスタンス化instance)
         * [カスタマイズ(Classes)](#カスタマイズclasses)
         * [スレッド数を計算(thread)](#スレッド数を計算thread)
         * [デーモンスレッド(Dameo)](#デーモンスレッドdameo)
      * [multiprocessing](#multiprocessing)
      * [multiprocessing](#multiprocessing-1)
         * [subprocess.run](#subprocessrun)
         * [subprocess.Popen](#subprocesspopen)
      * [concurrent.futures](#concurrentfutures)
         * [ExecutorとFuture](#executorとfuture)
         * [map、as_completedとwait](#mapas_completedとwait)
   * [subprocessの使い方(Python3.6)](#subprocessの使い方python36)
      * [Pip of shell script](#pip-of-shell-script)
   * [Python 好用模組教學 - concurrent.futures](#python-好用模組教學---concurrentfutures)
   * [Python multiprocessing 模組進階說明與範例](#python-multiprocessing-模組進階說明與範例)
      * [Process 類別(class)](#process-類別class)
      * [join() 方法](#join-方法)
      * [多個 Processes](#多個-processes)
      * [封裝複雜邏輯](#封裝複雜邏輯)
      * [Processes 之間的溝通](#processes-之間的溝通)
         * [Queues](#queues)
         * [Pipe](#pipe)
      * [shared memory 共享記憶體](#shared-memory-共享記憶體)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take some note of threading and multiprocessing  

# threading and multiprocessing  
[Pythonのthreadingとmultiprocessingを完全理解 updated at 2020-11-04](https://qiita.com/kaitolucifer/items/e4ace07bd8e112388c75#threading%E3%81%A8multiprocessing)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F246522%2F9db33432-ebde-4226-849c-543708a98f9a.jpeg?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&w=1400&fit=max&s=ccc9e36388dddc4d14bddc896ad3fd53" width="600" height="400">  

## threading  
関数  | 説明
------------------------------------ | ---------------------------------------------
start()	 |  スレッドを開始する
setName() | スレッドに名前をつける 
getName() | スレッドの名前を取得
setDaemon(True) | スレッドをデーモンにする
join() | スレッドの処理が終わるまで待機
run() | スレッドの処理をマニュアルで実行する

### インスタンス化(Instance)  
```
　関数などを導入してThreadのインスタンスを作成し、startで開始させると、スレッドを立ち上げられます。
```


```
import threading
import time


def run(n):
    # threading.current_thread().nameはgetName()を呼び出す
    print("task: {} (thread name: {})".format(n, threading.current_thread().name))
    time.sleep(1)
    print('2s')
    time.sleep(1)
    print('1s')
    time.sleep(1)
    print('0s')
    time.sleep(1)


t1 = threading.Thread(target=run, args=("t1",))
t2 = threading.Thread(target=run, args=("t2",), name='Thread T2') # ここではsetName()が呼び出される
# start()
t1.start()
t2.start()
# join()
t1.join()
t2.join()
# join()を呼び出したため
# メインスレッドは上記のスレッドが終わるまで待機し
# 全部終わったらprintする
print(threading.current_thread().name)
```

```
task: t1 (thread name: Thread-1)
task: t2 (thread name: Thread T2)
2s
2s
1s
1s
0s
0s
MainThread
```

```
t1とt2が交替で実行されていることが確認できます。交替ルールの1つはIO操作（ここではprint操作が該当する）の後で、1.5 GILのところでまた詳しく説明します。
```

### カスタマイズ(Classes)  
```
　Threadを継承して、スレッドクラスのrunメソッドをカスタマイズした上での利用も可能です。
```

```
import threading
import time


class MyThread(threading.Thread):
    def __init__(self, n):
        super(MyThread, self).__init__()
        self.n = n

    # run()を書き直す
    def run(self):
        print("task: {}".format(self.n))
        time.sleep(1)
        print('2s')
        time.sleep(1)
        print('1s')
        time.sleep(1)
        print('0s')
        time.sleep(1)


t1 = MyThread("t1")
t2 = MyThread("t2")

t1.start()
t2.start()

```

```
task: t1
task: t2
2s
2s
1s
1s
0s
0s
```

### スレッド数を計算(thread)  

```
import threading
import time


def run(n):
    print("task: {}".format(n))
    time.sleep(1)


for i in range(1, 4):
    t = threading.Thread(target=run, args=("t{}".format(i),))
    t.start()

time.sleep(0.5)
print(threading.active_count())
```

```
task: t1
task: t2
task: t3
4
```

###  デーモンスレッド(Dameo)
```
import threading
import time


def run(n):
    print("task: {}".format(n))
    time.sleep(1)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')


for i in range(1, 4):
    t = threading.Thread(target=run, args=("t{}".format(i),))
    # setDaemon(True)
    t.setDaemon(True) 
    t.start()

time.sleep(1.5)
print('スレッド数: {}'.format(threading.active_count()))
```

```
task: t1
task: t2
task: t3
3
3
3
スレッド数: 4
```


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

# Python 好用模組教學 - concurrent.futures  
[Python 好用模組教學 - concurrent.futures 2020年8月15日](https://myapollo.com.tw/zh-tw/python-concurrent-futures/) 

```
Python 關於平行處理的模組除了 multiprocessing 與 threading 之外，其實還提供 1 個更為簡單易用的 concurrent.futures 可以使用。

該模組提供 ThreadPoolExecutor 與 ProcessPoolExecutor 2 個經過封裝的 classes ，讓人方便上手之外，也讓程式看起來更加簡潔。

個人認為是相當值得學習＆使用的模組之一，可以應付絕大多數日常關於平行處理的使用場景。

本文將透過幾個範例學習 concurrent.futures 模組。
```

# Python multiprocessing 模組進階說明與範例  
[Python multiprocessing 模組進階說明與範例 2021年5月2日](https://myapollo.com.tw/zh-tw/more-about-python-multiprocessing/)

## Process 類別(class)  
```
實際上，絕大多數需要平行處理的情況，都可以透過將平行處理的部分轉成函式(function)後，交由 Pool 進行執行即可。

不過，仍有少數情況不適合用 Pool 執行，例如我們只需要 1 個 process 在背景執行一些工作達成類似非同步(asynchronous)執行的效果。

此時就可以考慮使用 Process 類別(class) 。

只要繼承該類別並且實作 run() 方法(method)即可將需要在背景執行的工作放在另 1 個 process 中執行，例如以下範例實作 1 個能夠每 3 秒監控某網站的 process ，並且在監控 5 次後結束執行：
```

```
透過繼承 Process 類別實作完 ChildProcess 類別之後，ChildProcess 就具有在不同 process 中執行的能力，當我們呼叫 start() 方法之後， ChildProcess 類別就會在另 1 個 process 中執行。

例如以下範例，我們在 22 行實例化該類別，接著在第 23 行呼叫 start() 方法，此時就會讓 ChildProcess 在另外的 process 中執行 run() 方法，同時為了證明 ChildProcess 不會阻礙 main process 的執行，我們在第 25 - 27 行執行其他工作：
```

```
mport time

import requests

from multiprocessing import Process, current_process


class ChildProcess(Process):
    def run(self):
        p = current_process()
        print("New process -> [%s] %s" % (p.pid, p.name))
        for _ in range(5):
            resp = requests.get('https://example.com')
            print('example.com [%d]' % resp.status_code) 
            time.sleep(3)
        print("[%s] %s terminated" % (p.pid, p.name))


parent_p = current_process()
print("I'm main process -> [%s] %s" % (parent_p.pid, parent_p.name))

child_p = ChildProcess()
child_p.start()

for _ in range(5):
    print("I'm main process, doing a job now")
    time.sleep(2)

print("[%s] %s terminated" % (parent_p.pid, parent_p.name))
```

```
上述範例的執行結果如下，可以看到 2 個不同 PID 的 processes 各自執行其工作，而且互不影響，其中 main process 51090 執行完其工作後就先結束，直到 child process 51106 執行完監控網站的任務後，整個 python process 才結束執行：

```

```

$ python test.py
I'm main process -> [51090] MainProcess
I'm main process, doing a job now
New process -> [51106] ChildProcess-1
example.com [200]
I'm main process, doing a job now
I'm main process, doing a job now
example.com [200]
I'm main process, doing a job now
example.com [200]
I'm main process, doing a job now
[51090] MainProcess terminated
example.com [200]
example.com [200]
[51106] ChildProcess-1 terminated
```

## join() 方法 
```
前述章節中提到 main process 比 child process 先結束執行的情況，
如果有些情況是需要先等 child process 執行完的情況，那麼可以額外針對 child process 呼叫 join() 方法，
如此一來 main process 就會先停在呼叫 join() 的地方等待，直到 child process 結束後才繼續執行 main process, 
例如以下範例：
```

```
import time

from multiprocessing import Process, current_process


class ChildProcess(Process):
    def run(self):
        p = current_process()
        print("New process -> [%s] %s" % (p.pid, p.name))
        time.sleep(10)
        print("[%s] %s terminated" % (p.pid, p.name))


parent_p = current_process()
print("I'm main process -> [%s] %s" % (parent_p.pid, parent_p.name))

child_p = ChildProcess()
child_p.start()
child_p.join()

print("[%s] %s terminated" % (parent_p.pid, parent_p.name))
```

```
上述範例執行結果如下，可以發現不管執行幾次， MainProcess 總是會等 child process 結束後才結束：
```

```
$ python test.py
I'm main process -> [13420] MainProcess
New process -> [13436] ChildProcess-1
[13436] ChildProcess-1 terminated
[13420] MainProcess terminated
```

```
如果把 child_p.join() 刪掉，就會發現 MainProcess 總是先結束執行。

以上就是 join() 方法的功效。
```

## 多個 Processes  
## 封裝複雜邏輯  

## Processes 之間的溝通  
### Queues  
### Pipe
```
另 1 個 processes 之間溝通的方式為 Pipe （或稱為管道），有別於 Queue 單向溝通的限制，Pipe 具有雙向溝通的能力，當我們呼叫 Pipe() 時會回傳 2 個 Connection ，代表一個管道的 2 端，可以理解為一條水管的 2 端開口，2 個開口都具有傳送與接收資料的能力(稱為 duplex )，因此 main process 與 child process 可以透過這個管道進行雙向溝通。

例如以下範例程式，第 21 行建立 1 個管道，我們將 2 個 connections 分別命名為 parent_conn 與 child_conn 代表管道一端是 main process, 另一端是 child process, 接著將 10 透過 parent_conn 送進管道內，所以要取得這筆資料就得在 child_conn 接收才行，也就是第 12 行接收資料的部分，再來將資料運算完之後，同樣透過 child_conn 將資料送進管道，因此要接收結果就得在 parent_conn 那端接收，也就是第 27 行的部分：
```

## shared memory 共享記憶體  

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



