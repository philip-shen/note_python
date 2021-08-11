
Table of Contents
=================

   * [Purpose](#purpose)
   * [Installation](#installation)
   * [command line](#command-line)
   * [CODEX FFMPEG](#codex-ffmpeg)
   * [ytdl-org / youtube-dl](#ytdl-org--youtube-dl)
   * [How can i find all ydl_opts](#how-can-i-find-all-ydl_opts)
   * [youtube-dl](#youtube-dl)
      * [下載 mp4 格式的影片](#下載-mp4-格式的影片)
      * [下載 mp3 檔](#下載-mp3-檔)
      * [下載不同畫質與格式](#下載不同畫質與格式)
   * [Troubleshooting](#troubleshooting)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Take note of Youtube

# Installation  
```
沒特別裝管控pkg的話 .. 
通常虛擬環境會在
C:\Users\windows user\Envs
```

```
將ffmpeg的full包的bin資料夾下 3個exe
，放進去剛建立的環境內Scripts分類下
```


# command line
```
youtube-dl --extract-audio --audio-format wav  https://www.youtube.com/watch?v=3FBijeNg_Gs
```

# CODEX FFMPEG  
[CODEX FFMPEG](https://www.gyan.dev/ffmpeg/builds/)


#  ytdl-org / youtube-dl 
[ ytdl-org /youtube-dl ](https://github.com/ytdl-org/youtube-dl)


# How can i find all ydl_opts 
[How can i find all ydl_opts](https://stackoverflow.com/questions/38658046/how-can-i-find-all-ydl-opts)

All options for the Python Module are listed in [YoutubeDL.py](https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278)


# youtube-dl
[youtube-dl](https://ianwu.tw/press/topic/command_line_program/youtube-dl)

## 下載 mp4 格式的影片  
```
預設的下載格式是 webm (opens new window)，
如果要下載 mp4 格式可以用 -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' 指定聲音與影像的格式
```

```
youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' https://www.youtube.com/watch?v=rkAfWfZkfyo
```

## 下載 mp3 檔
```
youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=rkAfWfZkfyo
```


## 下載不同畫質與格式 
```
youtube-dl -F https://www.youtube.com/watch?v=rkAfWfZkfyo  
```


[](html#%E4%B8%8B%E8%BC%89-mp4-%E6%A0%BC%E5%BC%8F%E7%9A%84%E5%BD%B1%E7%89%87)


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






