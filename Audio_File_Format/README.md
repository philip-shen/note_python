
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Python Mutagenで、複数の楽曲から情報（楽曲の長さなど）を高速に抽出](#pythonmutagenで複数の楽曲から情報楽曲の長さなどを高速に抽出)
      * [速度比較（Mutagen v.s. librosa.load）](#速度比較mutagen-vs-librosaload)
   * [Mutagenチートシート: MP3, AAC (.m4a), FLACのタグ・メタデータ抽出](#mutagenチートシート-mp3-aac-m4a-flacのタグメタデータ抽出)
      * [mutagen.mp3.MP3.tags](#mutagenmp3mp3tags)
      * [mutagen.mp3.MP3.info](#mutagenmp3mp3info)
      * [mutagen.flac.FLAC.tags](#mutagenflacflactags)
      * [mutagen.flac.FLAC.info](#mutagenflacflacinfo)
      * [mutagen.mp4.MP4.tags](#mutagenmp4mp4tags)
      * [mutagen.mp4.MP4.info](#mutagenmp4mp4info)
   * [手持ちの音楽ファイルからアニソンのプレイリストを自動的に作れるようにした話](#手持ちの音楽ファイルからアニソンのプレイリストを自動的に作れるようにした話)
   * [Python: PyTagLibで音楽ファイル (wav, flac, mp3, m4a, aac) のタグ情報抽出](#python-pytaglibで音楽ファイル-wav-flac-mp3-m4a-aac-のタグ情報抽出)
      * [インストール方法](#インストール方法)
         * [2. ver. 1.4.1をインストール](#2-ver-141をインストール)
   * [「米津玄師の似た曲データベース」作成のための類似曲検索システム設計](#米津玄師の似た曲データベース作成のための類似曲検索システム設計)
      * [構成・処理フロー](#構成処理フロー)
   * [soundfile](#soundfile)
      * [soundfileでのオーディオファイル読み込み（ブロック単位）](#soundfileでのオーディオファイル読み込みブロック単位)
      * [soundifleでのRawファイルの読み込み](#soundifleでのrawファイルの読み込み)
   * [PyFilterBank](#pyfilterbank)
      * [PyFilterBank の概要](#pyfilterbank-の概要)
   * [PyQtで作るdB単位の音量フェーダー](#pyqtで作るdb単位の音量フェーダー)
   * [PyQt Qsound でオーディオファイルを再生／停止](#pyqt-qsound-でオーディオファイルを再生停止)
   * [PyQt でアプリの背景色やテキスト文字の色などの属性を設定する方法](#pyqt-でアプリの背景色やテキスト文字の色などの属性を設定する方法)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose
Leave some tracks of Audio File Format(.wav, .flac, .aiff, .raw, etc.) 

# Python+Mutagenで、複数の楽曲から情報（楽曲の長さなど）を高速に抽出
[Python+Mutagenで、複数の楽曲から情報（楽曲の長さなど）を高速に抽出  2019-11-16](https://www.wizard-notes.com/entry/python/extract-length-with-mutagen)

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/K/Kurene/20191116/20191116075330.png" width="300" height="100">  

## 速度比較（Mutagen v.s. librosa.load）
```
librosa.loadでFLACファイル52曲の波形を読み込んで長さを算出した場合と比べました*1。

    Mutagen: 0.027 sec
    librosa.load: 28.764 sec
```

# Mutagenチートシート: MP3, AAC (.m4a), FLACのタグ・メタデータ抽出  
[Mutagenチートシート: MP3, AAC (.m4a), FLACのタグ・メタデータ抽出  2019-10-19](https://www.wizard-notes.com/entry/python/mutagen-cheatsheet)

## mutagen.mp3.MP3.tags
## mutagen.mp3.MP3.info

## mutagen.flac.FLAC.tags
```
flac.tags["artist"]             artist
flac.tags["albumartist"]        album_artist
flac.tags["composer"]           composer
flac.tags["tracktotal"]         total_track_number
flac.tags["disctotal"]          disc_number
flac.tags["date"]               year
flac.tags["tracknumber"]        track_number
flac.tags["comment"]            comments
flac.tags["title"]              title
flac.tags["genre"]              genre
flac.tags["discnumber"]         disc_number
flac.tags["album"]              album
```

## mutagen.flac.FLAC.info
```
flac.info.min_blocksize
flac.info.max_blocksize
flac.info.min_framesize
flac.info.max_framesize
flac.info.sample_rate
flac.info.channels
flac.info.bits_per_sample
flac.info.total_samples
flac.info.length
flac.info.md5_signature
flac.info.code
flac.info.bitrate
```

## mutagen.mp4.MP4.tags
## mutagen.mp4.MP4.info

# 手持ちの音楽ファイルからアニソンのプレイリストを自動的に作れるようにした話 
[手持ちの音楽ファイルからアニソンのプレイリストを自動的に作れるようにした話 posted at 2020-03-04](https://qiita.com/temple1026/items/c02846c796751e72b0d9#%E5%AE%9F%E8%A3%85%E3%81%97%E3%81%9F%E3%82%82%E3%81%AE)

<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F504018%2Facaa32f2-d3af-6c8b-195c-685b959410a2.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=6c5ae8e10186752ebd7b4a6cc50ad521" width="600" height="400">  

```
ソースコードと実行ファイル(Windows用)はGitHubに置いてあるので，併せて確認していただければ幸いです．
```
[ temple1026 /Anison Playlist Generator Pub](https://github.com/temple1026/AnisonPlaylistGenerator/blob/master/src/apg.py)

```
a. Pythonのファイルから実行する場合

    git clone https://github.com/temple1026/AnisonPlaylistGenerator apg

    cd apg

    pip install -r requirements.txt

    python main.py
```

# Python: PyTagLibで音楽ファイル (wav, flac, mp3, m4a, aac) のタグ情報抽出  
[Python: PyTagLibで音楽ファイル (wav, flac, mp3, m4a, aac) のタグ情報抽出  2021-02-14](https://www.wizard-notes.com/entry/python-pytablib)

## インストール方法 
### 2. ver. 1.4.1をインストール  
```
以下のStack Overflowの回答では、Ubuntu 16.04 and Python 2で pip install pytaglib==1.4.1とすることでpipによるインストールができたという報告がありました。


私のWin10環境でもインストールできました。
```
[python - Pip installing pytaglib error - Stack Overflow](https://stackoverflow.com/questions/48511211/pip-installing-pytaglib-error)

# 「米津玄師の似た曲データベース」作成のための類似曲検索システム設計
[「米津玄師の似た曲データベース」作成のための類似曲検索システム設計 2021-07-31](https://www.wizard-notes.com/entry/music-analysis/similar-songs-search-system-202107)

## 構成・処理フロー  
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/K/Kurene/20210731/20210731131236.png" width="400" height="500">  


# soundfile
[Python：soundfile を使ったオーディオファイル (.wav, .flac, .aiff, .raw, etc.) の読み書き  2021-01-28](https://www.wizard-notes.com/entry/python/soundfile)

```
    様々なOSで動いてほしい
    オーディオファイルをNumPy配列として扱いたい
    ファイル形式は wav, aiff, flac, raw など（mp3, aacなどは利用しない）
    ブロック（フレーム）ごとに信号を読み込みたい
    処理は軽いほうがよい
```
場合、 soundfile がお勧めです。

[SoundFile — PySoundFile 0.10.3post1-1-g0394588 documentation](https://pysoundfile.readthedocs.io/en/latest/)

```
# https://github.com/bastibe/python-soundfile/blob/master/soundfile.py#L38
_formats = {
    'WAV':   0x010000,  # Microsoft WAV format (little endian default).
    'AIFF':  0x020000,  # Apple/SGI AIFF format (big endian).
    'AU':    0x030000,  # Sun/NeXT AU format (big endian).
    'RAW':   0x040000,  # RAW PCM data.
    'PAF':   0x050000,  # Ensoniq PARIS file format.
    'SVX':   0x060000,  # Amiga IFF / SVX8 / SV16 format.
    'NIST':  0x070000,  # Sphere NIST format.
    'VOC':   0x080000,  # VOC files.
    'IRCAM': 0x0A0000,  # Berkeley/IRCAM/CARL
    'W64':   0x0B0000,  # Sonic Foundry's 64 bit RIFF/WAV
    'MAT4':  0x0C0000,  # Matlab (tm) V4.2 / GNU Octave 2.0
    'MAT5':  0x0D0000,  # Matlab (tm) V5.0 / GNU Octave 2.1
    'PVF':   0x0E0000,  # Portable Voice Format
    'XI':    0x0F0000,  # Fasttracker 2 Extended Instrument
    'HTK':   0x100000,  # HMM Tool Kit format
    'SDS':   0x110000,  # Midi Sample Dump Standard
    'AVR':   0x120000,  # Audio Visual Research
    'WAVEX': 0x130000,  # MS WAVE with WAVEFORMATEX
    'SD2':   0x160000,  # Sound Designer 2
    'FLAC':  0x170000,  # FLAC lossless file format
    'CAF':   0x180000,  # Core Audio File format
    'WVE':   0x190000,  # Psion WVE format
    'OGG':   0x200000,  # Xiph OGG container
    'MPC2K': 0x210000,  # Akai MPC 2000 sampler
    'RF64':  0x220000,  # RF64 WAV file
}

_subtypes = {
    'PCM_S8':    0x0001,  # Signed 8 bit data
    'PCM_16':    0x0002,  # Signed 16 bit data
    'PCM_24':    0x0003,  # Signed 24 bit data
    'PCM_32':    0x0004,  # Signed 32 bit data
    'PCM_U8':    0x0005,  # Unsigned 8 bit data (WAV and RAW only)
    'FLOAT':     0x0006,  # 32 bit float data
    'DOUBLE':    0x0007,  # 64 bit float data
    'ULAW':      0x0010,  # U-Law encoded.
    'ALAW':      0x0011,  # A-Law encoded.
    'IMA_ADPCM': 0x0012,  # IMA ADPCM.
    'MS_ADPCM':  0x0013,  # Microsoft ADPCM.
    'GSM610':    0x0020,  # GSM 6.10 encoding.
    'VOX_ADPCM': 0x0021,  # OKI / Dialogix ADPCM
    'G721_32':   0x0030,  # 32kbs G721 ADPCM encoding.
    'G723_24':   0x0031,  # 24kbs G723 ADPCM encoding.
    'G723_40':   0x0032,  # 40kbs G723 ADPCM encoding.
    'DWVW_12':   0x0040,  # 12 bit Delta Width Variable Word encoding.
    'DWVW_16':   0x0041,  # 16 bit Delta Width Variable Word encoding.
    'DWVW_24':   0x0042,  # 24 bit Delta Width Variable Word encoding.
    'DWVW_N':    0x0043,  # N bit Delta Width Variable Word encoding.
    'DPCM_8':    0x0050,  # 8 bit differential PCM (XI only)
    'DPCM_16':   0x0051,  # 16 bit differential PCM (XI only)
    'VORBIS':    0x0060,  # Xiph Vorbis encoding.
    'ALAC_16':   0x0070,  # Apple Lossless Audio Codec (16 bit).
    'ALAC_20':   0x0071,  # Apple Lossless Audio Codec (20 bit).
    'ALAC_24':   0x0072,  # Apple Lossless Audio Codec (24 bit).
    'ALAC_32':   0x0073,  # Apple Lossless Audio Codec (32 bit).
}
```

## soundfileでのオーディオファイル読み込み（ブロック単位）
```
import soundfile as sf
filepath = "xxx.wav" #"xxxx.flac"
for block in sf.blocks(filepath, blocksize=1024):
    pass  # your_processing(block)
```

例：RMS算出
```
import numpy as np
import soundfile as sf

rms = [np.sqrt(np.mean(block**2)) for block in
       sf.blocks('myfile.wav', blocksize=1024, overlap=512)]
```

## soundifleでのRawファイルの読み込み  
```
import soundfile as sf
filepath = 'xxxx.raw'
data, samplerate = sf.read(filepath, channels=1, samplerate=44100,subtype='FLOAT')
```

# PyFilterBank  
[ Python PyFilterBankで環境音をオクターブバンド分析 NumPy matplotlib Python Programming 音響音楽信号処理 ディジタルフィルタ  2020-12-23](https://www.wizard-notes.com/entry/music-analysis/pyfilterbank-octaveband)

## PyFilterBank の概要  
```
PyFilterBank は、様々なフィルタバンクを提供するPython向けライブラリです。

以下のフィルタバンクを利用できます。

    オクターブバンド
    メルフィルタバンク
    ガンマトーン
    周波数重み付けフィルタ
        A特性
        B特性
        C特性
```
[Welcome to PyFilterbank’s documentation! — PyFilterbank devN documentation](http://siggigue.github.io/pyfilterbank/index.html)

```
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from pyfilterbank import FractionalOctaveFilterbank


# オーディオファイル読み込み
filepath = "stream.wav"
x, sr = sf.read(filepath)

# 1/3 オクターブバンド分析
# y.shape = (サンプル数, バンド数)
ofb = FractionalOctaveFilterbank(sample_rate=sr, order=4, nth_oct=3.0)
y, states = ofb.filter(x)

# 時間方向に加算、対数(dB)に変換
L_sum = np.sum(y**2, axis=0)
L = 10 * np.log10(L_sum/np.max(L_sum))

# 各バンドの中心周波数
freqs = np.array(list(states.keys()))

# プロット
plt.subplot(2,1,1)
plt.plot(freqs, L, marker="o", color="c")
plt.grid()
plt.title("Octave-band analysis")
plt.subplot(2,1,2)
plt.plot(freqs, L, marker="o", color="m")
plt.grid()
plt.xscale('log')
plt.title("Octave-band analysis (xscale is \'log\')")
plt.tight_layout()
plt.show()
```

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/K/Kurene/20201223/20201223131505.png" width="500" height="300">  

# PyQtで作るdB単位の音量フェーダー  
[PyQtで作るdB単位の音量フェーダー](https://www.wizard-notes.com/entry/python/pyqt-dB-volume-fader)

信号に乗算するゲイン係数は、音量フェーダーのdB値 x から、 として算出しています。
<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/K/Kurene/20201223/20201223085908.png" width="300" height="100">  

[volume - Convert dB value to linear scale - Sound Design Stack Exchange](https://sound.stackexchange.com/questions/38722/convert-db-value-to-linear-scale)


# PyQt Qsound でオーディオファイルを再生／停止
[PyQt Qsound でオーディオファイルを再生／停止  2020-12-20](https://www.wizard-notes.com/entry/python/pyqt-qsound)

# PyQt でアプリの背景色やテキスト文字の色などの属性を設定する方法
[PyQt でアプリの背景色やテキスト文字の色などの属性を設定する方法  2020-12-09](https://www.wizard-notes.com/entry/python/dev/pyqt-palette-and-stylesheet)


* []()  
![alt tag]()
<img src="" width="300" height="200">  

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
