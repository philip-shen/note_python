'''
【pytube】HTTP Error 400: Bad Request のエラーの対処法
https://itechblog.hatenablog.com/entry/2024/09/30/200132
'''
'''
JuanBindez/pytubefix 
https://github.com/JuanBindez/pytubefix
'''
"""
pytubefix.exceptions.VideoUnavailable:
https://github.com/JuanBindez/pytubefix/issues/242
"""
import os,sys, time
import tempfile
import pathlib
import argparse

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

from logger_setup import *
from GetCsvColumn import CsvFile,EXCLUDE

from pytubefix import YouTube
from pytubefix.cli import on_progress
from termcolor import colored

CLIENTS = {
    1: "WEB",
    2: "WEB_EMBED",
    3: "WEB_MUSIC",
    4: "WEB_CREATOR",
    5: "WEB_SAFARI",
    6: "ANDROID",
    7: "ANDROID_MUSIC",
    8: "ANDROID_CREATOR",
    9: "ANDROID_VR",
    10: "ANDROID_PRODUCER",
    11: "ANDROID_TESTSUITE",
    12: "IOS",
    13: "IOS_MUSIC",
    14: "IOS_CREATOR",
    15: "MWEB",
    16: "TV_EMBED",
    17: "MEDIA_CONNECT",
}


def download_client(url: str, settings: dict, filetype: str):
    """Download filetype (video or audio) with one of the clients from the CLIENTS list."""
    for _, client in CLIENTS.items():
        try:
            # Try to reach filetype and create YouTube object
            print(colored(f'Trying to reach {filetype} with "{client}" client', "yellow"))
            yt = (
                YouTube(url=url, client=client, on_progress_callback=on_progress)
                .streams.filter(**settings["params"])
                .order_by(settings["order_by"])
                .desc()
                .first()
            )

            # Download filetype (video or audio)
            print(colored(f'Downloading "{yt.title}" ' f'{settings["intro_message"]}') )
            yt.download(filename=f"{filetype}.mp3", skip_existing=False, timeout=10, max_retries=5)
            print(f'\n{settings["out_message"]}', "blue")

            # Return from function if success
            return
        except Exception as e:
            print(colored(f'Error occured while downloading via "{client}" client: {e}\n', "red") )

    raise Exception("Failed to download asset with all available clients")

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
ffmpegwav_48k_mono_00 = 'ffmpeg.exe  -i "{}" -af pan=mono  -sample_fmt s16 -ar 48000 -y "{}"'
ffmpegwav_48k_mono = 'ffmpeg.exe  -i "{}" -map ? -acodec pcm_s16le -ar 48000 -y "{}"'

o = lambda x: '%s%s'%(x,'.wav')
o_mp3 = lambda x: '%s%s'%(x,'.mp3')

def in_out(command,infile,outfile):
    hdr = '-'*len(command)
    #print("%s\n%s\n%s"%(hdr,command,hdr))
    logger.info(f'{hdr}\n{command}\n{hdr}')
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
      #infile, outfile = infile, o(pathlib.Path('mp3')/outname)
      infile, outfile = infile, o(outname)

      logger.info(f'infile:{ infile }')
      logger.info(f'outfile:{ outfile }')

      in_out(ffmpegwav_48k_mono, infile, outfile)
        
      
def download(url, out_wav_path, out_video_name, client_option):
    
    #dl_fname = YouTube(url).streams.get_by_itag(int(itag)).download()
    yt = YouTube(url, client=client_option, on_progress_callback = on_progress)
    
    # 最高品質のオーディオストリームを選択
    #audio_stream = yt.streams.filter(only_audio=True).first()
    # オーディオを一時ファイルとしてダウンロード
    #temp_file = audio_stream.download()

    audio_stream = yt.streams.get_audio_only()
    temp_file = audio_stream.download(mp3=True)
    # MoviePyを使用してオーディオをMP3に変換
    #audio_clip = AudioFileClip(temp_file)
    #audio_clip.write_audiofile("test.mp3", codec="libmp3lame")

    dl_fname = temp_file
    #print(f'dl_fname:{ dl_fname }')
    logger.info(f'dl_fname:{ dl_fname }')

    #out_fname = f"{os.path.splitext(os.path.basename(dl_fname))[0]}"
    out_fname = f'{out_wav_path}/{out_video_name}'
    
    logger.info(f'out_fname:{ out_fname }')

    normalize_denoise_mp4tomp3(dl_fname, out_fname)
    
    
    return dl_fname

def startdownload(url, outpath, outvideo, client_option):
    
    try:
        dl_video_fname = download(url, outpath, outvideo, client_option)
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
    print("Error: %s - %s." % (e.filename, e.strerror))

def get_url_from_csv(dir_csv_url, opt_verbose='OFF'):
  list_yt_urls = []
  list_yt_renames = []
  list_folders = []

  csvfile = CsvFile(dir_csv_url)

  list_csvfile_folders_column= csvfile.get_column('folder')
  list_csvfile_renames_column= csvfile.get_column('rename')
  list_csvfile_yt_urls_column= csvfile.get_column('YT_url')

  if opt_verbose.lower() == 'on':
      logger.info(f'list_csvfile_folders_column: {list_csvfile_folders_column}\n' )
      logger.info(f'list_csvfile_renames_column: {list_csvfile_renames_column}\n' )
      logger.info(f'list_csvfile_yt_urls_column: {list_csvfile_yt_urls_column}\n' )

  for idx, folder in enumerate(list_csvfile_folders_column):
     if '#' in folder:
        continue
     else:
        list_yt_urls.append(list_csvfile_yt_urls_column[idx])
        list_folders.append(folder)
        list_yt_renames.append(list_csvfile_renames_column[idx])
  
  logger.info(f'list_yt_urls: {list_yt_urls}\n' )

  return list_yt_urls, list_folders, list_yt_renames

def main(in_urls, in_folders, out_video_names, opt_client):
    list_dl_fnames = []

    for idx, in_url in enumerate(in_urls):
        list_dl_fnames.append(startdownload(in_url, in_folders[idx], out_video_names[idx], opt_client))

    for dl_fname in list_dl_fnames:
       #print(f'list_dl_fname: {list_dl_fname}')
       logger.info(f'dl_fname: {dl_fname}')
       remove_dl_video_file(dl_fname)

if __name__ == '__main__':
    t0 = time.time()
    
    logger_set(strdirname)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', action='store', default=None, help='keyin csv url file')
    
    opt_verbose='Off'
    results = parser.parse_args()
    csv_file  = results.conf
    video_urls, video_paths, video_renames = get_url_from_csv(csv_file, opt_verbose)
    main(video_urls, video_paths, video_renames, CLIENTS[15])

    '''
    video_url =[
      #  'https://www.youtube.com/watch?v=vdAUcGGDKNM',
      #  'https://youtu.be/ZgLFuJyeUTg?si=sa_HH3ETrzimTpX0',
        #'https://www.youtube.com/watch?v=j42eBLuoAfg',
        
        #'https://youtu.be/V5XIFLWec-c?si=A3-p8kPCdNyzZrJl',
        #'https://youtu.be/UyuB5zA-yMM?si=Br120aSx-GJ5jZnS',
        #'https://youtu.be/oUeRCXNmZ88?si=vYCcdZAYTP3A3COd',
        #'https://youtu.be/YUhmu4dBo2Q?si=FKL-PE5I96prJrRL',
        #'https://youtu.be/erhdbjYE1T4?si=Y2cmYz0_-9bxpGOH',
        #'https://youtu.be/GbMQNY3mDNc?si=O_2iRx7ehcqn-rsL',
        #'https://youtu.be/FFVfh9JflOo?si=LXdib6rUT-5fnarE',
        #'https://youtu.be/Ipi7dY7ersw?si=hKf4Wc0nshiYnMiD',
        #'https://youtu.be/ERdBg6LUjSQ?si=wBbig53YvRBiINeh',
        #'https://youtu.be/CUwW8nLSdHA?si=49OyenNMsq4HGXuM',
        'https://youtu.be/mBz7nUxPsCk?si=RlyubU1B_6UpCYSW',
        'https://youtu.be/-wb2PAx6aEs?si=q1Nz0KNrB7EZHHy3',
        ]
    
    main(video_url, CLIENTS[3])
    '''
    '''
    for url in video_url:
       download_client(url, 
                       {"on_progress_callback": on_progress,
                        "mp3": True},
            filetype= "audio")
    '''
    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))