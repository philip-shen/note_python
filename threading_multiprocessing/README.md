
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [threading and multiprocessing](#threading-and-multiprocessing)
      * [threading](#threading)
         * [インスタンス化(Instance)](#インスタンス化instance)
         * [カスタマイズ(Classes)](#カスタマイズclasses)
         * [スレッド数を計算(thread)](#スレッド数を計算thread)
         * [デーモンスレッド(Daemo)](#デーモンスレッドdaemo)
      * [multiprocessing](#multiprocessing)
      * [multiprocessing](#multiprocessing-1)
         * [subprocess.run](#subprocessrun)
         * [subprocess.Popen](#subprocesspopen)
      * [concurrent.futures](#concurrentfutures)
         * [ExecutorとFuture](#executorとfuture)
         * [map、as_completedとwait](#mapas_completedとwait)
   * [pythonで平行処理入門 (threading.Thread)](#pythonで平行処理入門-threadingthread)
      * [平行処理の例](#平行処理の例)
   * [pythonで並列化入門 (multiprocessing.Pool)](#pythonで並列化入門-multiprocessingpool)
      * [一気にまとめて処理する (Pool.map)](#一気にまとめて処理する-poolmap)
      * [Pool.mapで複数引数を渡したい](#poolmapで複数引数を渡したい)
      * [Pool.mapで複数引数を渡す (wrapper経由)](#poolmapで複数引数を渡す-wrapper経由)
   * [[Python] TkinterでYoutube Downloaderを作ってみた。](#python-tkinterでyoutube-downloaderを作ってみた)
      * [生成順番](#生成順番)
      * [2.2.2. 呼び出し](#222-呼び出し)
   * [Pythonでthreadingを使った非同期処理](#pythonでthreadingを使った非同期処理)
   * [Pythonにおける非同期処理: asyncio逆引きリファレンス](#pythonにおける非同期処理-asyncio逆引きリファレンス)
      * [並列で処理を行いたい(固定長)](#並列で処理を行いたい固定長)
      * [並列で処理を行いたい(不定長)](#並列で処理を行いたい不定長)
      * [並列での実行数を制御したい](#並列での実行数を制御したい)
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

###  デーモンスレッド(Daemo)
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


# pythonで平行処理入門 (threading.Thread)  
[pythonで平行処理入門 (threading.Thread) posted at 2019-09-08](https://qiita.com/studio_haneya/items/a3485ea837e17e37bae9)

```
平行処理: 同じCPUコアの同じpythonプロセスで複数の処理を同時にやる
並列処理: 別のCPUコアの別のpythonプロセスで複数の処理を同時にやる
```

## 平行処理の例  
```
threading.Threadを定義してstart()で開始、join()すると終了するまで待機します。
待機するのでなくis_alive()でチェックしながら別の作業をやることも出来ます。

threading.Threadは返り値を受け取れないようなので参照渡しの引数に仕込みます。
ただし、受け取り用の引数を result = x * x のようにすると別の変数になってしまって返ってこないのでlistやdictで渡して書き加えて戻すようにします。
```

```
import time
import threading


def nijou(x, result):
    print('input: %d' % x)
    time.sleep(3)
    result[threading.current_thread().name] = x * x
    print('double:', result)


if __name__ == "__main__":
    result = dict()
    thread = threading.Thread(target=nijou, args=[4, result], name='thread1')

    thread.start()
    for k in range(6):
        time.sleep(1)
        print(thread.is_alive())
    thread.join()
    print(result)
```

```
結果

input: 4
True
True
double: {'thread1': 16}
False
False
False
False
{'thread1': 16}
```


# pythonで並列化入門 (multiprocessing.Pool)  
[pythonで並列化入門 (multiprocessing.Pool) updated at 2019-09-12](https://qiita.com/studio_haneya/items/1cf192a0185e12c7559b)  

```
並列処理: 別のCPUコアの別のpythonプロセスで複数の処理を同時にやる
平行処理: 同じCPUコアの同じpythonプロセスで複数の処理を同時にやる

待機が多いような楽な処理は平行処理で、負荷が重い処理は並列処理でやるのが良いでしょう。
今回は並列処理をmultiprocessing.Pool()でやる話です。
```

## 一気にまとめて処理する (Pool.map)  
http://iatlex.com/python/parallel_first 

```
import time
from multiprocessing import Pool

# 並列処理させる関数
def nijou(x):
    print('input: %d' % x)
    time.sleep(2)
    retValue = x * x
    print('double: %d' % (retValue))
    return(retValue)

if __name__ == "__main__":
    p = Pool(4) # プロセス数を4に設定
    result = p.map(nijou, range(10))  # nijou()に0,1,..,9を与えて並列演算
    print(result)
```

```
上記コードを実行すると下の結果が返ってきます。p = multiprocessing.Pool(4)
で同時実行するプロセス数を指定しておいてp.map()で実行するという使い方です。
p.map()の第1引数に使う関数を渡し第2引数が関数に渡す引数になります。この書き方だと渡せる引数は１つだけです。
```

```
input: 0
input: 1
input: 2
input: 3
double: 0
input: 4
double: 1
input: 5
double: 4
input: 6
double: 9
input: 7
double: 16
input: 8
double: 25
input: 9
double: 36
double: 49
double: 64
double: 81
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

## Pool.mapで複数引数を渡したい  
```
p.map()が渡してくれる引数は1個だけですが、listとかでまとめちゃえば複数の値を渡すことは普通にできます。
```

```
import time
from multiprocessing import Pool

def nijou(inputs):
    x, y = inputs
    print('input: %d, %d' % (x, y))
    time.sleep(2)
    retValue = [x * x, y * y]
    print('double: %d, %d' % (retValue[0], retValue[1]))
    return(retValue)

if __name__ == "__main__":
    p = Pool(4)
    values = [(x, y) for x in range(4) for y in range(4)]
    print(values)
    result = p.map(nijou, values)
    print(result)
```

p.map()がvaluesの中の値を1個ずつ渡してくれるので、(0, 0) → (0, 1) → (0, 2)の順で渡していきます。

```
[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
input: 0, 0
input: 0, 1
input: 0, 2
input: 0, 3
double: 0, 0
input: 1, 0
double: 0, 1
input: 1, 1
double: 0, 4
input: 1, 2
double: 0, 9
input: 1, 3
double: 1, 0
(略)
double: 9, 4
double: 9, 9
[[0, 0], [0, 1], [0, 4], [0, 9], [1, 0], [1, 1], [1, 4], [1, 9], [4, 0], [4, 1], [4, 4], [4, 9], 
```

## Pool.mapで複数引数を渡す (wrapper経由)  
関数が複数引数を受け取るような書き方になってる場合は、複数引数をまとめるwrapper関数をつくります。
既にある関数を利用する場合はこの書き方の方がやりやすいと思います。

```
import time
from multiprocessing import Pool

def nijou(x, y):
    print('input: %d %d' % (x, y))
    time.sleep(2)
    print('double: %d %d' % ((x * x), (y * y)))

def nijou_wrapper(args):
    return nijou(*args)

if __name__ == "__main__":
    p = Pool(4)
    values = [(x, y) for x in range(4) for y in range(4)]
    print(values)
    p.map(nijou_wrapper, values)
```


# [Python] TkinterでYoutube Downloaderを作ってみた。  
[[Python] TkinterでYoutube Downloaderを作ってみた。 posted at 2020-05-26](https://qiita.com/kotai2003/items/6a289b431d167b209b9d)  

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F208980%2Fd54c757e-6f1c-27e7-5cbf-dc5631b10a72.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=d74d37f597a5a54c6b352ece51a1431a" width="600" height="400">  

## 生成順番
```
下記の順番で、Threadを設計します。
StartボタンのCall Back関数　→　Thread生成メソッド　→　実行メソッド
```

```
from threading import Thread

#Call Back関数
def click_me(self):
    self.create_thread()

#Thread生成メソッド
def create_thread(self):
    self.run_thread = Thread( target=self.method_in_a_thread )
    self.run_thread.start()
    print(self.run_thread)

#実行メソッド
def method_in_a_thread(self):
    print('New Thread is Running.')
    self.get_youtube( self.URL_name.get(), self.Folder_name.get())
```

## 2.2.2. 呼び出し  
```
self.btn_Start = tk.Button(self.frame_form, text = 'Start')
self.btn_Start.configure( font= self.font02 )
self.btn_Start.grid( column=1, row=2, padx=20, pady=20, sticky= tk.W + tk.E )
self.btn_Start.configure( command = self.click_me)
```


# Pythonでthreadingを使った非同期処理
[Pythonでthreadingを使った非同期処理 updated at 2020-04-16](https://qiita.com/Gattaca/items/a63707aac2cdcccb6127)
```
worker()はスレッドで実行させる処理です。
q.get()でキューから要素を取り出し、1秒スリープしてから取り出した要素を表示しています。
q.task_done()でキューから取り出した要素の処理が完了したことをキューに知らせます。これらの処理を無限ループします。
```

```
from queue import Queue
from threading import Thread
import time


def worker(q):
    while True:
        result = q.get()
        time.sleep(1)
        print(result)
        q.task_done()

if __name__ == '__main__':
    q = Queue()

    for _ in range(3):
        thread = Thread(target=worker, args=(q,))
        thread.setDaemon(True)
        thread.start()

    a = [1, 2, 3, 4, 5, 6]
    for i in a:
        q.put(i)

    q.join()
```

```
メインの処理では、q = Queue()でキューを作成します。
引数にmaxsizeを指定しない場合はキューの大きさは無限になります。
thread = Thread(target=worker, args=(q,))でスレッドを作成し、上で作成したworker()関数と引数を渡します。
thread.setDaemon(True)でスレッドをデーモンスレッドにする処理です。
デーモンスレッドは残っているスレッドがデーモンスレッドだけの時pythonプログラムを終了させます。
thread.start()でスレッドをスタートさせています。
今回はfor文で3つのスレッドをたてています。

次はキューにaの要素を順次入れていきます。
最後q.join()でキューの処理が全部終わるまで待機します。
```

```
python async.py
# 1秒待機
1
3
2
# 1秒待機
5
6
4
```


# Pythonにおける非同期処理: asyncio逆引きリファレンス 
[Pythonにおける非同期処理: asyncio逆引きリファレンス updated at 2019-03-06](https://qiita.com/icoxfog417/items/07cbf5110ca82629aca0)

```

```


<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F25990%2Fd4f19dcb-140e-beda-4985-a2bbf35b7233.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=c31c617f5252d6644825b156b7925002
" width="400" height="200">

[第1回　マルチスレッドはこんなときに使う (1/2)](https://atmarkit.itmedia.co.jp/ait/articles/0503/12/news025.html) 

```
import asyncio


Seconds = [
    ("first", 5),
    ("second", 0),
    ("third", 3)
]


async def sleeping(order, seconds, hook=None):
    await asyncio.sleep(seconds)
    if hook:
        hook(order)
    return order


async def basic_async():
    # the order of result is nonsequential (not depends on order, even sleeping time)
    for s in Seconds:
        r = await sleeping(*s)
        print("{0} is finished.".format(r))
    return True

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(basic_async())
```

## 並列で処理を行いたい(固定長)  
```
あらかじめ並列で実行したい処理の数が決まっている際は、
それらを並列で一斉に処理させることができます。そのために提供されている機能が、asyncio.gatherとasyncio.waitです。

まず、asyncio.gatherのパターン
```

## 並列で処理を行いたい(不定長)  
```
先ほどの並列処理は並列処理をする数がわかっていましたが、
次々リクエストが来る場合など長さが固定でない場合もあります(ストリームなど)。
そうした場合は、Queueを使った処理が可能です。
```

## 並列での実行数を制御したい 
```
特にスクレイピングなどを行う場合、あるサイト内の1000個のコンテンツのurlを一斉に処理するなどするとと多大な迷惑がかかるため、並列で実行するプロセスの数を制御したい場合があります。
この時に使うのがSemaphoreになります。
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
透過繼承 Process 類別實作完 ChildProcess 類別之後，ChildProcess 就具有在不同 process 中執行的能力，
當我們呼叫 start() 方法之後， ChildProcess 類別就會在另 1 個 process 中執行。

例如以下範例，我們在 22 行實例化該類別，接著在第 23 行呼叫 start() 方法，
此時就會讓 ChildProcess 在另外的 process 中執行 run() 方法，
同時為了證明 ChildProcess 不會阻礙 main process 的執行，我們在第 25 - 27 行執行其他工作：
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
上述範例的執行結果如下，可以看到 2 個不同 PID 的 processes 各自執行其工作，
而且互不影響，其中 main process 51090 執行完其工作後就先結束，
直到 child process 51106 執行完監控網站的任務後，整個 python process 才結束執行：

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
另 1 個 processes 之間溝通的方式為 Pipe （或稱為管道），有別於 Queue 單向溝通的限制，
Pipe 具有雙向溝通的能力，當我們呼叫 Pipe() 時會回傳 2 個 Connection ，代表一個管道的 2 端，
可以理解為一條水管的 2 端開口，2 個開口都具有傳送與接收資料的能力(稱為 duplex )，
因此 main process 與 child process 可以透過這個管道進行雙向溝通。

例如以下範例程式，第 21 行建立 1 個管道，
我們將 2 個 connections 分別命名為 parent_conn 與 child_conn 代表管道一端是 main process, 
另一端是 child process, 接著將 10 透過 parent_conn 送進管道內，
所以要取得這筆資料就得在 child_conn 接收才行，
也就是第 12 行接收資料的部分，再來將資料運算完之後，同樣透過 child_conn 將資料送進管道，因此要接收結果就得在 parent_conn 那端接收，也就是第 27 行的部分：
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




