import scipy
import pytest
from mock import patch
from scipy.io.wavfile import read
import os, sys
import numpy as np
import matplotlib.pyplot as plt

strabspath=os.path.abspath(sys.argv[0])
sys.path.append(strabspath)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
print(prevdirname)
sys.path.append(prevdirname)


from spafe.features.spfeats import extract_feats
from spafe.frequencies.fundamental_frequencies import compute_yin
from spafe.frequencies.dominant_frequencies import get_dominant_frequencies
from spafe.features.mfcc import mel_spectrogram
from spafe.utils.vis import show_spectrogram


fpath = os.path.join(prevdirname, 'test.wav')#"../../../test.wav"
fs, sig = read(fpath)
mSpec, _ = mel_spectrogram(sig,
                                fs=fs,
                                pre_emph=0,
                                pre_emph_coeff=0.97,
                                win_len=0.030,
                                win_hop=0.015,
                                win_type="hamming",
                                nfilts=128,
                                nfft=2048,
                                low_freq=0,
                                high_freq=fs/2)


show_spectrogram(mSpec.T,
                 fs,
                 xmin=0,
                 xmax=len(sig)/fs,
                 ymin=0,
                 ymax=(fs/2)/1000,
                 dbf=80.0,
                 xlabel="Time (s)",
                 ylabel="Frequency (kHz)",
                 title="Mel spectrogram (dB)",
                 cmap="jet")