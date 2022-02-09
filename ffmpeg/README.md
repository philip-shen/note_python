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