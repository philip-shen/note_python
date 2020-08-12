# -*- coding:utf-8 -*-
import numpy as np
import scipy.signal
import wave
import array
import struct
from scipy.io import wavfile

def wav_read(file_path, mmap=False):
    """
    return sample value between range(-1,1)
    Note" librosa.load use aioread, which may truncate the precision of the audio data to 16 bits.
    :param file_path:
    :param mmap: False read all data directly, True read data memory mapping
    :return:  samples ,fs
    """

    fs, samples = wavfile.read(file_path, mmap=mmap)
   
    # transfer samples from fixed to float
    if samples.dtype == np.int16:
        samples = np.array(samples, dtype=np.float32)
        samples /= 2 ** 15
    elif samples.dtype == np.float32:
        samples = np.array(samples)
    else:
        raise NotImplementedError

    return samples, fs

def wav_write(file_path, samples, fs, wav_type='int16'):
    # scipy.io.wavfile.write cannot process np.float16 data
    if wav_type == 'float32':
        wavfile.write(file_path, fs, samples.astype(np.float32))
    elif wav_type == 'int16':
        output_samples = samples * (2 ** 15)
        wav_type_iinfo = np.iinfo(wav_type)
        output_samples.clip(min=wav_type_iinfo.min, max=wav_type_iinfo.max,
                            out=output_samples)
        output_samples = output_samples.astype(wav_type)
        wavfile.write(file_path, fs, output_samples)
    else:
        raise NotImplementedError

def readWav(filename):
    """
    wavファイルを読み込んで，データ・サンプリングレートを返す関数
    """
    try:
        wf = wave.open(filename)
        fs = wf.getframerate()
        # -1 ~ 1までに正規化した信号データを読み込む
        data = np.frombuffer(wf.readframes(wf.getnframes()),dtype="int16")/32768.0
        return (data,fs)
    except Exception as e:
        print(e)
        exit()


def writeWav(filename,data,fs):
    """
    入力されたファイル名でwavファイルを書き出す．
    """
    # データを-32768から32767の整数値に変換
    data = [int(x * 32767.0) for x in data]
    #バイナリ化
    binwave = struct.pack("h" * len(data), *data)
    wf = wave.Wave_write(filename)
    wf.setparams((
                    1,                          # channel
                    2,                          # byte width
                    fs,                         # sampling rate
                    len(data),                  # number of frames
                    "NONE", "not compressed"    # no compression
                ))
    wf.writeframes(binwave)
    wf.close()



def upsampling(conversion_rate,data,fs):
    """
    アップサンプリングを行う．
    入力として，変換レートとデータとサンプリング周波数．
    アップサンプリング後のデータとサンプリング周波数を返す．
    """
    # 補間するサンプル数を決める
    interpolationSampleNum = conversion_rate-1

    # FIRフィルタの用意をする
    nyqF = (fs*conversion_rate)/2.0     # 変換後のナイキスト周波数
    cF = (fs/2.0-500.)/nyqF             # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
    taps = 511                          # フィルタ係数（奇数じゃないとだめ）
    b = scipy.signal.firwin(taps, cF)   # LPFを用意

    # 補間処理
    upData = []
    for d in data:
        upData.append(d)
        # 1サンプルの後に，interpolationSampleNum分だけ0を追加する
        for i in range(interpolationSampleNum):
            upData.append(0.0)

    # フィルタリング
    resultData = scipy.signal.lfilter(b,1,upData)
    return (resultData,fs*conversion_rate)


def downsampling(conversion_rate,data,fs):
    """
    ダウンサンプリングを行う．
    入力として，変換レートとデータとサンプリング周波数．
    アップサンプリング後のデータとサンプリング周波数を返す．
    """
    # 間引くサンプル数を決める
    decimationSampleNum = conversion_rate-1

    # FIRフィルタの用意をする
    nyqF = (fs/conversion_rate)/2.0             # 変換後のナイキスト周波数
    cF = (fs/conversion_rate/2.0-500.)/nyqF     # カットオフ周波数を設定（変換前のナイキスト周波数より少し下を設定）
    taps = 511                                  # フィルタ係数（奇数じゃないとだめ）
    b = scipy.signal.firwin(taps, cF)           # LPFを用意

    #フィルタリング
    data = scipy.signal.lfilter(b,1,data)

    #間引き処理
    downData = []
    for i in range(0,len(data),decimationSampleNum+1):
        downData.append(data[i])

    return (downData,fs/conversion_rate)


FILENAME = "D:/project/FeqResp/Asus/asus_S54C_0807_Igo_Speech_FR_BandG/dut.wav"
#FILENAME = "../src_wav/3Quest_Standmic.wav"

if __name__ == "__main__":
    # 何倍にするかを決めておく
    up_conversion_rate = 2
    # 何分の1にするか決めておく．ここではその逆数を指定しておく（例：1/2なら2と指定）
    down_conversion_rate = 2
    down_conversion_wave = "D:/project/FeqResp/Asus/asus_S54C_0807_Igo_Speech_FR_BandG/dut_16k.wav"

    # テストwavファイルを読み込む
    #data,fs = readWav(FILENAME)
    data,fs = wav_read(FILENAME)
    print('fs {}',fs)
    upData,upFs = upsampling(up_conversion_rate,data,fs)
    downData,downFs = downsampling(down_conversion_rate,data,fs)

    #writeWav("../src_wav/up.wav",upData,upFs)
    writeWav(down_conversion_wave,downData,downFs)
    
    #wav_write("../src_wav/up.wav",upFs,upData)
    #wav_write("../src_wav/down.wav",downFs,downData)
