"""
pip install yt-dlp
"""
import os
import re
import os,sys, time
import tempfile
import pathlib
import argparse
import yt_dlp

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

from logger_setup import *
from GetCsvColumn import CsvFile,EXCLUDE

def download_and_convert_video(video_url, output_folder, output_filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, output_filename),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def clean_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r'[\/:*?"<>|]', '_', filename)

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

def main(csv_info, opt_verbose='OFF'):    
    list_dl_fnames = []
    video_urls, video_paths, video_renames = get_url_from_csv(csv_info, opt_verbose)
    
    for idx, in_url in enumerate(video_urls):
        
        if not os.path.isdir(video_paths[idx]):
            os.makedirs(video_paths[idx], exist_ok=True)
        elif video_paths[idx].lower() == '':
            pass
        
        download_and_convert_video(in_url, video_paths[idx], video_renames[idx])
        list_dl_fnames.append(f"{video_paths[idx]}\{video_renames[idx]}")
        
    return list_dl_fnames
    
if __name__ == "__main__":
    t0 = time.time()
    
    logger_set(strdirname)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', action='store', default=None, help='keyin csv url file')
    
    opt_verbose='Off'
    results = parser.parse_args()
    csv_file  = results.conf
    
    main(csv_file, opt_verbose)

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))

