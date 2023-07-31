"""
pythonでyoutube動画をダウンロード
https://qiita.com/mino211/items/f43553f669d09c3b431f
"""

"""
How can I convert MP4 video to MP3 audio with FFmpeg?
https://superuser.com/questions/332347/how-can-i-convert-mp4-video-to-mp3-audio-with-ffmpeg

ffmpeg -i video.mp4 -b:a 192K -vn music.mp3
"""
import os,sys
import tempfile
import pathlib
from scipy import fft
from scipy.io import wavfile
from pytube import YouTube

#global
ax = None
take = 20
normalize = False
denoise = False
lowpass = 0
mp4tomp3 = True

ffmpegwav = 'ffmpeg -i "{}" -t %s -c:a pcm_s16le -map 0:a "{}"'
ffmpegnormalize = ('ffmpeg -y -nostdin -i "{}" -filter_complex ' +
"'[0:0]loudnorm=i=-23.0:lra=7.0:tp=-2.0:offset=4.45:linear=true:print_format=json[norm0]' " +
"-map_metadata 0 -map_metadata:s:a:0 0:s:a:0 -map_chapters 0 -c:v copy -map '[norm0]' " +
'-c:a:0 pcm_s16le -c:s copy "{}"')
ffmpegdenoise = 'ffmpeg -i "{}" -af'+" 'afftdn=nf=-25' "+'"{}"'
ffmpeglow = 'ffmpeg -i "{}" -af'+" 'lowpass=f=%s' "+'"{}"'
ffmpegmp3 = 'ffmpeg -i "{}" -b:a 192k -vn "{}"'

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
      in_out(ffmpegmp3, infile,outfile)
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
    print(f'dl_fname:{ dl_fname }')
    out_fname = f"{os.path.splitext(os.path.basename(dl_fname))[0]}"
    print(f'out_fname:{ out_fname }')
    
    normalize_denoise_mp4tomp3(dl_fname, out_fname)

    #global video
    #yt=YouTube(url,on_progress_callback=progress)
    #video=yt.streams.first()
    #video.get_by_itag(int(itag)).download()

def set(url):
    #url = input("urlを指定してください")
    for y in YouTube(url).streams:
        print(y)
    itag = input("itagを入力してください")
    return url, itag

def startdownload(url, itag):
    try:
        download(url, itag)
        print("ダウンロードが終了しました")
    except TimeoutError:
        print("タイムアウトしました")

def main(in_urls):
    for in_url in in_urls:
        url, itag = set(in_url)
        startdownload(url, itag)

if __name__ == '__main__':
    video_url =[
        'https://www.youtube.com/watch?v=hN5MBlGv2Ac',
        'https://www.youtube.com/watch?v=vdAUcGGDKNM'
    ]
    main(video_url)