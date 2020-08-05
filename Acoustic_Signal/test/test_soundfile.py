import soundfile as sf
fname = '../src_wav/1980s-Casio-Celesta-C5.wav' # mono
# fname = 'Alesis-Fusion-Pizzicato-Strings-C4.wav' # stereo

data, samplerate = sf.read(fname)
#sf.write('new_file.wav', data, samplerate)

print(data.shape)

# stereo音源なら
# l_channel = data[:,0]
# r_channel = data[:,1]