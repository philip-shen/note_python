"""
date: 2020/12/23
author: @_kurene
"""
import sys
import pyaudio
import threading
import numpy as np
import librosa
import warnings
from numba import jit

warnings.simplefilter('ignore')


@jit
def process_block(input, output, n_ch, n_chunk, gain):
    for c in range(0, n_ch):
        for n in range(0, n_chunk):
            output[c, n] = gain * input[c, n]


class AudioPlayer():
    def __init__(self, sr=44100, n_chunk=1024, format="float32", loop_on=True):
        self.sr      = sr
        self.n_ch    = 2
        self.n_chunk = n_chunk
        self.loop_on = loop_on
        self.length  = 0
        self.offset  = 0
        self.format  = pyaudio.paInt16 if format == "int16" else pyaudio.paFloat32
        self.dtype   = np.float32
        self.gain    = 1.0
        
        self.signal = None
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format, channels=self.n_ch, rate=self.sr, frames_per_buffer=self.n_chunk, 
                                  input=False, output=True)
        self.stream.stop_stream()

    def set_audiofile(self, filepath):
        self.stop()
        
        signal, self.sr = librosa.load(filepath, sr=self.sr, mono=False)
        length = signal.shape[0] if signal.ndim == 1 else signal.shape[1]
 
        self.length = (length // self.n_chunk)*self.n_chunk + (self.n_chunk if length % self.n_chunk > 0 else 0)
        self.signal = np.zeros((self.n_ch, self.length))
        
        for k in range(0, self.n_ch):
            self.signal[k, 0:length] = signal / self.n_ch if signal.ndim == 1 else signal[k]
 
    def __run(self):
        output = np.zeros((self.n_ch, self.n_chunk))
        while self.stream.is_active():
            input = self.signal[:, self.offset : self.offset + self.n_chunk]
            
            process_block(input, output, self.n_ch, self.n_chunk, self.gain)
            
            # Convert nd-array into stream chunk
            chunk_data = np.reshape(output.T, (self.n_chunk * self.n_ch))
            chunk = chunk_data.astype(self.dtype).tostring()
            self.stream.write(chunk)

            # Update offset
            self.offset += self.n_chunk
            if self.offset >= self.length:
                if self.loop_on:
                    self.offset = 0
                else:
                    self.stop()
        return True
    #==========================================================
    # Control funcs
    #==========================================================
    def pause(self):
        self.stream.stop_stream()
        
    def stop(self):
        self.stream.stop_stream()
        self.offset = 0
        
    def play(self):
        self.stream.start_stream()
        t = threading.Thread(target=self.__run)
        t.start()
        
    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()