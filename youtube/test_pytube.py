"""
pythonでyoutube動画をダウンロード
https://qiita.com/mino211/items/f43553f669d09c3b431f
"""

"""
How can I convert MP4 video to MP3 audio with FFmpeg?
https://superuser.com/questions/332347/how-can-i-convert-mp4-video-to-mp3-audio-with-ffmpeg

ffmpeg -i video.mp4 -b:a 192K -vn music.mp3
"""
"""
Convert mp4 to WAV with ffmpeg 
https://gist.github.com/Bonno/73873ed4ac523adc9611

ffmpeg -i <infile> -af "pan=stereo|c0=c0|c1=c1" -f wav <outfile>
"""
"""
Manipulating audio channels 
https://trac.ffmpeg.org/wiki/AudioChannelManipulation#:~:text=ffmpeg%20integrates%20a%20default%20down,you%20have%20very%20specific%20needs.
"""

import os,sys,time
import tempfile
import pathlib
from scipy import fft
from scipy.io import wavfile
from pytube import YouTube
import argparse

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

from logger_setup import *
from GetCsvColumn import CsvFile,EXCLUDE

#global
ax = None
take = 20
normalize = False
denoise = False
lowpass = 0
mp4tomp3 = False
mp4towav_48k_mono = True

ffmpegwav = 'ffmpeg -i "{}" -t %s -c:a pcm_s16le -map 0:a "{}"'
ffmpegnormalize = ('ffmpeg -y -nostdin -i "{}" -filter_complex ' +
"'[0:0]loudnorm=i=-23.0:lra=7.0:tp=-2.0:offset=4.45:linear=true:print_format=json[norm0]' " +
"-map_metadata 0 -map_metadata:s:a:0 0:s:a:0 -map_chapters 0 -c:v copy -map '[norm0]' " +
'-c:a:0 pcm_s16le -c:s copy "{}"')
ffmpegdenoise = 'ffmpeg -i "{}" -af'+" 'afftdn=nf=-25' "+'"{}"'
ffmpeglow = 'ffmpeg -i "{}" -af'+" 'lowpass=f=%s' "+'"{}"'
ffmpegmp3 = 'ffmpeg -i "{}" -b:a 192k -vn -y "{}"'
ffmpegwav_48k_mono = 'ffmpeg.exe  -i "{}" -af pan=mono  -sample_fmt s16 -ar 48000 -y "{}"'

o = lambda x: '%s%s'%(x,'.wav')
o_mp3 = lambda x: '%s%s'%(x,'.mp3')

def in_out(command,infile,outfile):
    hdr = '-'*len(command)
    print("%s\n%s\n%s"%(hdr,command,hdr))
    ret = os.system(command.format(infile,outfile))
    if 0 != ret:
      sys.exit(ret)

def normalize_denoise_mp4tomp3(infile,outname):
  with tempfile.TemporaryDirectory() as tempdir:
    #outfile = o(pathlib.Path(tempdir)/outname)
    if not os.path.isdir(pathlib.Path('mp3')):
       os.makedirs(pathlib.Path('mp3'), exist_ok=True)
    
    #outfile = o(pathlib.Path('mp3')/outname)
    #in_out(ffmpegwav%take,infile,outfile)
    if normalize:
      infile, outfile = outfile,o(outfile)
      in_out(ffmpegnormalize,infile,outfile)
    if denoise:
      infile, outfile = outfile,o(outfile)
      in_out(ffmpegdenoise,infile,outfile)
      infile, outfile = outfile,o(outfile)
      in_out(ffmpegdenoise,infile,outfile)
    if int(lowpass):
      infile, outfile = outfile,o(outfile)
      in_out(ffmpeglow%lowpass,infile,outfile)
    if mp4tomp3:
      infile, outfile = infile, o_mp3(pathlib.Path('mp3')/outname)
      #print(f'infile:{ infile }')
      #print(f'outfile:{ outfile }')
      logger.info(f'infile:{ infile }')
      logger.info(f'outfile:{ outfile }')
      in_out(ffmpegmp3, infile,outfile)
    if mp4towav_48k_mono:
      infile, outfile = infile, o(pathlib.Path('mp3')/outname)
      #print(f'infile:{ infile }')
      #print(f'outfile:{ outfile }')
      
      logger.info(f'infile:{ infile }')
      logger.info(f'outfile:{ outfile }')
      in_out(ffmpegwav_48k_mono, infile, outfile)
        
    #r,s = wavfile.read(outfile)
    #if len(s.shape)>1: #stereo
    #  s = s[:,0]
    #return r,s
  
"""
抓YT音樂影片且轉成mp3 （Python）- 2022
https://hackmd.io/@brad84622/Hk_71R7-v
"""
def progress(chunk,file_handle,bytes_remaining):
    global video
    contentSize=video.filesize
    size=contentSize-bytes_remaining
    print('\r' + '[Download progress]:%.2f%%;\n' % (' ' * int(size*20/contentSize), \
            ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')
        
def download(url, itag):
    
    dl_fname = YouTube(url).streams.get_by_itag(int(itag)).download()
    #print(f'dl_fname:{ dl_fname }')
    logger.info(f'dl_fname:{ dl_fname }')

    out_fname = f"{os.path.splitext(os.path.basename(dl_fname))[0]}"
    #print(f'out_fname:{ out_fname }')
    logger.info(f'out_fname:{ out_fname }')
    
    normalize_denoise_mp4tomp3(dl_fname, out_fname)

    return dl_fname
    #global video
    #yt=YouTube(url,on_progress_callback=progress)
    #video=yt.streams.first()
    #video.get_by_itag(int(itag)).download()

def set(url, itag):
    #url = input("urlを指定してください")
    for y in YouTube(url).streams:
        print(y)
    if itag == '':
       itag = input("itagを入力してください")

    return url, itag

def startdownload(url, itag):
    try:
        dl_video_fname = download(url, itag)
        #print("ダウンロードが終了しました")
        logger.info('Donwload complete!')

        return dl_video_fname
    except TimeoutError:
        #print("タイムアウトしました")
        logger.info('Donwload time out!')

def remove_dl_video_file(fname):
   # Try to delete the file.
  try:  
    os.remove(fname)
  except OSError as e:
    # If it fails, inform the user.
    #print("Error: %s - %s." % (e.filename, e.strerror))
    logger.info("Error: %s - %s." % (e.filename, e.strerror))

def get_url_from_csv(dir_csv_url, opt_verbose='OFF'):
  list_yt_urls = []

  csvfile = CsvFile(dir_csv_url)

  list_csvfile_folders_column= csvfile.get_column('folder')
  list_csvfile_yt_urls_column= csvfile.get_column('YT_url')

  if opt_verbose.lower() == 'on':
      logger.info(f'list_csvfile_folders_column: {list_csvfile_folders_column}\n' )
      logger.info(f'list_csvfile_yt_urls_column: {list_csvfile_yt_urls_column}\n' )

  for idx, folder in enumerate(list_csvfile_folders_column):
     if '#' in folder:
        continue
     else:
        list_yt_urls.append(list_csvfile_yt_urls_column[idx])
  
  logger.info(f'list_yt_urls: {list_yt_urls}\n' )

  return list_yt_urls
      
def main(in_urls):
    list_dl_fnames = []

    for in_url in in_urls:
        url, itag = set(in_url, itag='139')
        list_dl_fnames.append(startdownload(url, itag))

    for dl_fname in list_dl_fnames:
       #print(f'list_dl_fname: {list_dl_fname}')
       logger.info(f'dl_fname: {dl_fname}')
       remove_dl_video_file(dl_fname)

if __name__ == '__main__':
    logger_set(strdirname)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', action='store', default=None, help='keyin csv url file')
    
    opt_verbose='OFF'
    results = parser.parse_args()
    csv_file  = results.conf
    video_url = get_url_from_csv(csv_file, opt_verbose)
    main(video_url)

    
    '''
    video_url =[
      #  'https://youtu.be/gr67C2vRIxg?si=k4grk5lUt5BIBooU',
      #  'https://www.youtube.com/live/G7jwsT3V2oY?si=ivZEOiGfg8EWNy59',
      #  'https://youtu.be/j9EOoxPHBp8',
      #  'https://www.youtube.com/watch?v=hN5MBlGv2Ac',
      #  'https://www.youtube.com/watch?v=vdAUcGGDKNM',
      #  'https://youtu.be/ZgLFuJyeUTg?si=sa_HH3ETrzimTpX0',
      #  'https://www.youtube.com/live/eA-fP8jBlZA?si=qdzsh4ohXpd9elnS',
      #  'https://www.youtube.com/live/5agP0JjMl-w?si=BvFpnv7wRfqVvA9_'
      #    'https://www.youtube.com/live/yjEE3lHhQ6o?si=spFDVRlPtJaYlj46',
      #    'https://www.youtube.com/live/yjEE3lHhQ6o?si=UJ0OomAXY8Oh34te',
      #    'https://www.youtube.com/live/yjEE3lHhQ6o?si=od8yEg-3c2KPB928',
          'https://www.youtube.com/live/Rqme2qJ3lXI?si=Xz8EGAF02VRAI3_f',
          'https://www.youtube.com/live/wTnTfGMqF00?si=sDB0aPpFFOPzSQcQ',
    ]
    '''