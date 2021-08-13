import numpy as np
 
#リニア値からdBへ変換
def db(x, dBref):
    y = 20 * np.log10(x / dBref)     #変換式
    return y                         #dB値を返す
 
#dB値からリニア値へ変換
def idb(x, dBref):
    y = dBref * np.power(10, x / 20) #変換式
    return y   