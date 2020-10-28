# -*- coding: utf-8 -*-

import numpy as np
import wave

chunk = 1024

fname = 'audio_sample.wav'
foname = 'audio_sample_out.wav'

waveInFile = wave.open(fname, 'r')

# wavファイルの情報を取得
# チャネル数：monoなら1, stereoなら2, 5.1chなら6(たぶん)
nchannles = waveInFile.getnchannels()

# 音声データ1サンプルあたりのバイト数。2なら2bytes(16bit), 3なら24bitなど
samplewidth = waveInFile.getsampwidth()

# サンプリング周波数。普通のCDなら44.1k
framerate = waveInFile.getframerate()

# 音声のデータ点の数
nframes = waveInFile.getnframes()

print("Channel num : ", nchannles)
print("Sample width : ", samplewidth)
print("Sampling rate : ", framerate)
print("Frame num : ", nframes)


# chunk毎に処理、最後のあまりは無視
wav_len = int(nframes / chunk)

# wavの全データを読み込む
wav_in_bytes = waveInFile.readframes(nframes)

# byte型で読み込まれるのでint16に変換
wav_in_buf = np.frombuffer(wav_in_bytes, dtype='int16')

# Lchは偶数番目、Rchは奇数番目にあるので、振り分ける
wav_in_l_buf = wav_in_buf[::nchannles]
wav_in_r_buf = wav_in_buf[1::nchannles]

# audio chunkのリストの初期化
audio_data = []

for i in range(wav_len):
    # ミックスしてモノラルにするため2で割る
    data_l = wav_in_l_buf[i * chunk:(i+1) * chunk] / 2.0
    data_r = wav_in_r_buf[i * chunk:(i+1) * chunk] / 2.0
    # 左右チャンネルを足しaudio_dataに追加
    audio_data.append(np.add(data_l, data_r))

waveInFile.close()

# 書き込み用ファイルのオープン
waveOutFile = wave.open(foname, 'w')

# 各種パラメータ設定
waveOutFile.setnchannels(1)
waveOutFile.setsampwidth(samplewidth)
waveOutFile.setframerate(framerate)

# audio_dataを結合しwaveファイルに書き出し
waveOutFile.writeframes(np.concatenate(audio_data).astype(np.int16))

waveOutFile.close()