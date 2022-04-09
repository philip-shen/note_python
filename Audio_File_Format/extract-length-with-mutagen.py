import os, sys
from pathlib import Path
from itertools import chain

from mutagen.mp4 import MP4
from mutagen.flac import FLAC 
from mutagen.mp3 import MP3


exts = ["flac", "mp3", "m4a", "aac"]

dirpath = sys.argv[1]
p = Path(dirpath)
filepaths = list(chain.from_iterable([list(p.glob(f"*.{ext}")) for ext in exts]))

print("Sampling Rate\tCh.\tLength\tExt.\tFilename")
for filepath in filepaths:
    filename = os.path.split(filepath)[1]
    filename, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == ".mp3":
        audio_info = MP3(filepath).info
    elif ext in ["aac", ".m4a"]:
        audio_info = MP4(filepath).info
    elif ext == ".flac":
        audio_info = FLAC (filepath).info
    length = audio_info.length
    channels = audio_info.channels
    sample_rate = audio_info.sample_rate
    print(f"{sample_rate}\t\t{channels}\t{length:0.1f}\t{ext}\t{filename}")