# coding: utf-8 

"""
以下のURLを参考にさせていただきました
http://d.hatena.ne.jp/mohayonao/20110121/1295611356  
http://aidiary.hatenablog.com/entry/20110607/1307449007 
"""
"""
https://gist.github.com/taogawa/4586999
"""
import math
import array
import pyaudio
import random

def sin_wave(freq, sec=1, velocity=0.2, rate=44100):
    def gen():
        n = int(rate * sec)
        for i in range(n):
            yield math.sin(2.0 * math.pi * i / rate * freq) * velocity 
    return array.array('f', gen()).tobytes()

def square_wave(freq, sec=1, velocity=0.2, rate=44100):
    def gen():
        n = int(rate * sec)
        for i in range(n):
             yield sum([math.sin(2.0 * math.pi * i /rate * freq * (2 * j - 1)) * (velocity / (2 * j - 1))
                                                                                        for j in range(10)])
    return array.array('f', gen()).tobytes()

def triangle_wave(freq, sec=1, velocity=0.2, rate=44100):
    def gen():
        n = int(rate * sec)
        for i in range(n):
            yield sum([(velocity / (2 * j + 1) ** 2) * math.sin((2 * j + 1) * 2.0 * math.pi * i / rate * freq)
                                                                                        for j in range(10)])
    return array.array('f', gen()).tobytes()

def saw_wave(freq, sec=1, velocity=0.2, rate=44100):
    def gen():
        n = int(rate * sec)
        for i in range(n):
            yield sum([(velocity / j) * math.sin(2.0 * math.pi * j * i / rate * freq)
                                                                for j in range(1, 10)])
    return array.array('f', gen()).tobytes()

p = pyaudio.PyAudio()
stream = p.open(rate=44100, channels=1, format=pyaudio.paFloat32, output=True)

scale = [ 261.63, # C
          293.66, # D
          329.63, # E
          349.23, # F
          392.00, # G
          440.00, # A
          493.88, # H
          261.63 * 2, # C
          ]

for freq in scale:
    stream.write(sin_wave(freq))
    stream.write(square_wave(freq))
    stream.write(triangle_wave(freq))
    stream.write(saw_wave(freq))

stream.close()
p.terminate()

