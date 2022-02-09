Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [ffmpeg-pythonで動画編集する](#ffmpeg-pythonで動画編集する)
      * [ffmpegをインストールする](#ffmpegをインストールする)
      * [ffmpeg-pythonをインストールする](#ffmpeg-pythonをインストールする)
      * [音声を保存する](#音声を保存する)
         * [wavで保存する](#wavで保存する)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Leave some tracks of ffmpeg.


# ffmpeg-pythonで動画編集する
* [ffmpeg-pythonで動画編集する 2021-03-13](https://qiita.com/studio_haneya/items/a2a6664c155cfa90ddcf)

## ffmpegをインストールする
公式サイトからインストーラーをダウンロードしてきて入れます
https://ffmpeg.org/download.html

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F277233%2F4b34d399-8a3c-bb11-38b0-ccecca54f757.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=90d431c2053a48f20c78f46a5795c6d1" width="500" height="300">  

落としてきた圧縮ファイルを適当なフォルダに展開して、binフォルダにPATHを通せばインストール完了です
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F277233%2F34f968b2-b473-32d4-b0a7-9ff5298d1cfc.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=978c8de88ba9f67373b36b78b1562b57" width="300" height="200">  

PATHが通ってれば以下のようにterminalから呼べるようになっている筈です
```
> ffmpeg

ffmpeg version 2021-03-07-git-a7f841718f-full_build-www.gyan.dev Copyright (c) 2000-2021 the FFmpeg developers
  built with gcc 10.2.0 (Rev6, Built by MSYS2 project)
```

## ffmpeg-pythonをインストールする
```
pip install ffmpeg-python
```

```
>>> import ffmpeg
>>> path = './movie.mp4'
>>> video_info = ffmpeg.probe(path)
>>> video_info

{'streams': [{'index': 0,
   'codec_name': 'h264',
   'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10',
   'profile': 'High',
   'codec_type': 'video',
   'codec_tag_string': 'avc1',
   'codec_tag': '0x31637661',
   'width': 1920,
   'height': 1080,
   'coded_width': 1920,
   'coded_height': 1080, 
   ...
```

## 音声を保存する 
### wavで保存する

```
stream = ffmpeg.input('movie.mp4')
stream = ffmpeg.output(stream, 'audio.wav', format='wav')
ffmpeg.run(stream)
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