# note of_HTTPS Proxy_
Take some note of HTTPS Proxy, ex: mitmproxy, Charles

# Table of Content

[Reference](#reference)  

# 
[iOSアプリのAPIリクエストのトレースはどうするのが効率的か？ 2016-02-11](https://qiita.com/WorldDownTown/items/42d9ab6c746fe7a6bc9c)  

ライブラリ | メリット | デメリット
------------------------------------ | ------------------------------------ | ---------------------------------------------
ResponseDetective | カスタマイズ性が高い | アプリ実装多め
Wireshark | アプリ実装不要 | https不可
Charles | アプリ実装不要・設定が簡単・高機能 | 有料
PonyDebugger | ChromeのDeveloper Toolが見やすい | 古い・メンテ少ない
netfox | アプリ実装は一行だけ | リアルタイムに通信を見れない
mitmproxy | アプリ実装不要・CUI・無料でSSLも確認できる | なし

# 
[【Ruby, Python】開発時に通信傍受プロキシを設置した時、ルート証明書を与えて、ハンドシェイクエラーを回避する 2018-02-12](https://qiita.com/dogwood008/items/3e17ef73800bee7adbb0)  

どうやって覗くの？  
```
この辺を使ってください。私はcharles大好き人間なので課金して使っています。今回はcharlesを使いますが、mitm-pythonの場合もほぼ同様です。
```
* [daniel4x/mitm-python](https://github.com/daniel4x/mitm-python)

# Reference  

* [通信系のデバッグには Charles が便利 2017-11-27](https://qiita.com/usagimaru/items/d340e87da98e62f99b60)  

* [AndroidのSSL通信をCharlesで確認する方法 2017-03-23](https://qiita.com/Capotasto/items/a51a76a8670e67798861)  
```

```

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