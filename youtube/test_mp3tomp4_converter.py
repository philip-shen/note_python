'''
slanacpizzagomilicafesb/YouTube-to-mp3-or-mp4-converter 
https://github.imc.re/slanacpizzagomilicafesb/YouTube-to-mp3-or-mp4-converter

This is a converter I made for myself for when I download videos from YouTube.
'''
import tkinter as tk
import tkinter.ttk as ttk
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import *
from tkinter.filedialog import askdirectory
import moviepy.editor as mpe

window = tk.Tk()
window.title("YT to mp3 converter")
save_path = "D:/Music/converter_music/"

def convert_command():
    error_msg_lbl["text"] = ""

    if mp3_flag.get() == 1:
        if default_folder.get() == 1:
            # Use pytube to download the video
            yt = YouTube(url_entry.get())

            try:
                video = yt.streams.filter(only_audio=True).first()
                # Download the video to a file
                out_file = video.download(output_path=save_path)

            except FileExistsError:
                error_msg_lbl["text"] = "ERROR: That file already exists."

            else:
                # Set up new filename for the MP3
                new_file = out_file.replace(".mp4", ".mp3")
                # Use moviepy to convert video audio to mp3
                video_clip = AudioFileClip(out_file)
                video_clip.write_audiofile(new_file)
                
                # Remove the original video file
                os.remove(out_file)
                
                url_entry.delete(0, tk.END)

        elif default_folder.get() == 0:
            # Ask for a different save path
            new_save_path = askdirectory()
            # Use pytube to download the video
            yt = YouTube(url_entry.get())

            try:
                video = yt.streams.filter(only_audio=True).first()
                # Download the video to a file
                out_file = video.download(output_path=new_save_path)
            
            except FileExistsError:
                error_msg_lbl["text"] = "ERROR: That file already exists."

            else:
                # Set up new filename for the MP3
                new_file = out_file.replace(".mp4", ".mp3")
                # Use moviepy to convert video audio to mp3
                video_clip = AudioFileClip(out_file)
                video_clip.write_audiofile(new_file)
                
                # Remove the original video file
                os.remove(out_file)
                
                url_entry.delete(0, tk.END)

    elif mp4_flag.get() == 1:
        if default_folder.get() == 1:
            # Use pytube to download the video
            yt = YouTube(url_entry.get())
            
            try:
                audio = yt.streams.filter(only_audio=True).first().download(output_path=save_path)
                aname = audio[:-4] + ".mp3"
                os.rename(audio, aname)

                video = yt.streams.filter(subtype='mp4', res=resolution.get()).first().download(output_path=save_path)
                vname = video[:-4] + "1.mp4"
                os.rename(video, vname)

            except AttributeError:
                error_msg_lbl["text"] = "ERROR: Requested resolution not found, please try a different one."
                os.remove(aname)

            except FileExistsError:
                error_msg_lbl["text"] = "ERROR: That file already exists."
            
            else:
                # Setting the audio to the video
                video = mpe.VideoFileClip(vname)
                audio = mpe.AudioFileClip(aname)
                final = video.set_audio(audio)
                # Output result
                final.write_videofile(vname[:-5] + vname[-4:])

                # Remove the original video file
                os.remove(aname)
                os.remove(vname)
                
                url_entry.delete(0, tk.END)
            

        elif default_folder.get() == 0:
            # Ask for a different save path
            new_save_path = askdirectory()
            # Use pytube to download the video
            yt = YouTube(url_entry.get())
            
            try:
                audio = yt.streams.filter(only_audio=True).first().download(output_path=save_path)
                aname = audio[:-4] + ".mp3"
                os.rename(audio, aname)

                video = yt.streams.filter(subtype='mp4', res=resolution.get()).first().download(output_path=new_save_path)
                vname = video[:-4] + "1.mp4"
                os.rename(video, vname)

            except AttributeError:
                error_msg_lbl["text"] = "ERROR: Requested resolution not found, please try a different one."
                os.remove(aname)

            except FileExistsError:
                error_msg_lbl["text"] = "ERROR: That file already exists."
            
            else:
                # Setting the audio to the video
                video = mpe.VideoFileClip(vname)
                audio = mpe.AudioFileClip(aname)
                final = video.set_audio(audio)
                # Output result
                final.write_videofile(vname[:-5] + vname[-4:])

                # Remove the original video file
                os.remove(aname)
                os.remove(vname)
                
                url_entry.delete(0, tk.END)

mp3_flag = tk.IntVar(window, value=1, name="mp3")
mp4_flag = tk.IntVar(window, value=0, name="mp4")

def mp3_command():
    window.setvar(name = "mp3", value=1)
    window.setvar(name = "mp4", value=0)
    mp3_btn["relief"] = tk.SUNKEN
    mp4_btn["relief"] = tk.RAISED
    mp4_btn["borderwidth"] = 2
    mp3_btn["borderwidth"] = 5
    res_144p_btn.configure(state='disabled')
    res_240p_btn.configure(state='disabled')
    res_360p_btn.configure(state='disabled')
    res_480p_btn.configure(state='disabled')
    res_720p_btn.configure(state='disabled')
    res_1080p_btn.configure(state='disabled')
    res_1440p_btn.configure(state='disabled')
    res_2160p_btn.configure(state='disabled')
 

def mp4_command():
    window.setvar(name = "mp4", value=1)
    window.setvar(name = "mp3", value=0)
    mp4_btn["relief"] = tk.SUNKEN
    mp3_btn["relief"] = tk.RAISED
    mp4_btn["borderwidth"] = 5
    mp3_btn["borderwidth"] = 2
    res_144p_btn.configure(state='normal')
    res_240p_btn.configure(state='normal')
    res_360p_btn.configure(state='normal')
    res_480p_btn.configure(state='normal')
    res_720p_btn.configure(state='normal')
    res_1080p_btn.configure(state='normal')
    res_1440p_btn.configure(state='normal')
    res_2160p_btn.configure(state='normal')

#window_frame = tk.Frame(master=window)
url_lbl_frame = tk.Frame(master=window)
url_entry_convert_btn_frame = tk.Frame(master=window)
#convert_btn_frame = tk.Frame()
mp34_default_btns_frame = tk.Frame(master=window)
mp3_4_btn_frame = tk.Frame(master=mp34_default_btns_frame)
blank_lbl_frame = tk.Frame(master=mp34_default_btns_frame)
default_folder_frame = tk.Frame(master=mp34_default_btns_frame)
resolution_btns_frame = tk.Frame(master=window)
res_btns_frame = tk.Frame(master=resolution_btns_frame)
blank_lbl_res_frame = tk.Frame(master=resolution_btns_frame)
error_msg_frame = tk.Frame(master=window)



url_lbl = tk.Label(master=url_lbl_frame,
                   text="Paste the URL here:                                                                                              ")
url_lbl.pack(side=tk.TOP)


url_entry = tk.Entry(master=url_entry_convert_btn_frame,
                     width=50
                     )
url_entry.pack(side=tk.LEFT)



convert_btn = tk.Button(master=url_entry_convert_btn_frame,
                        text="Convert",
                        width=10,
                        height=1,
                        command=convert_command
                        )
convert_btn.pack(side=tk.RIGHT)



mp3_btn = tk.Button(master=mp3_4_btn_frame,
                    text=".mp3",
                    width=10,
                    height=1,
                    command=mp3_command,
                    borderwidth=5,
                    relief=tk.SUNKEN
                    )
mp3_btn.pack(side=tk.LEFT)

mp4_btn = tk.Button(master=mp3_4_btn_frame,
                    text=".mp4",
                    width=10,
                    height=1,
                    command=mp4_command
                    )
mp4_btn.pack(side=tk.LEFT)

# label full of spaces used to position the .mp3 and .mp4 buttons along with the default folder checkbox
blank_lbl = tk.Label(master=blank_lbl_frame,
                     text="                                       ")
blank_lbl.pack(side=tk.LEFT)

default_folder = tk.IntVar(value=1)
default_folder_btn = ttk.Checkbutton(master=default_folder_frame,
                                     text="Default folder",
                                     variable=default_folder,
                                     onvalue=1,
                                     offvalue=0
                                     )
default_folder_btn.pack(side=tk.RIGHT)



res_lbl = tk.Label(master=res_btns_frame,
                   text="Resolution:")
res_lbl.pack(side=tk.TOP)

resolution = tk.StringVar(value='720p')
res_144p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='144p',
                               variable=resolution,
                               value='144p')
res_144p_btn.pack(side=tk.TOP)
res_144p_btn.configure(state='disabled')

res_240p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='240p',
                               variable=resolution,
                               value='240p')
res_240p_btn.pack(side=tk.TOP)
res_240p_btn.configure(state='disabled')

res_360p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='360p',
                               variable=resolution,
                               value='360p')
res_360p_btn.pack(side=tk.TOP)
res_360p_btn.configure(state='disabled')

res_480p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='480p',
                               variable=resolution,
                               value='480p')
res_480p_btn.pack(side=tk.TOP)
res_480p_btn.configure(state='disabled')

res_720p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='720p',
                               variable=resolution,
                               value='720p')
res_720p_btn.pack(side=tk.TOP)
res_720p_btn.configure(state='disabled')

res_1080p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='1080p',
                               variable=resolution,
                               value='1080p')
res_1080p_btn.pack(side=tk.TOP)
res_1080p_btn.configure(state='disabled')

res_1440p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='1440p',
                               variable=resolution,
                               value='1440p')
res_1440p_btn.pack(side=tk.TOP)
res_1440p_btn.configure(state='disabled')

res_2160p_btn = ttk.Radiobutton(master=res_btns_frame,
                               text='2160p',
                               variable=resolution,
                               value='2160p')
res_2160p_btn.pack(side=tk.TOP)
res_2160p_btn.configure(state='disabled')


# label full of spaces used to position the resolution radio buttons
blank_lbl_res = tk.Label(master=blank_lbl_res_frame,
                         text="                                          ")
blank_lbl_res.pack(side=tk.RIGHT)



error_msg_lbl = tk.Label(master=error_msg_frame,
                         text="")
error_msg_lbl.pack()



url_lbl_frame.pack(side=tk.TOP)
url_entry_convert_btn_frame.pack(side=tk.TOP)
mp34_default_btns_frame.pack(side=tk.TOP)
mp3_4_btn_frame.pack(side=tk.LEFT)
blank_lbl_frame.pack(side=tk.LEFT)
default_folder_frame.pack(side=tk.RIGHT)
res_btns_frame.pack(side=tk.LEFT)
blank_lbl_res_frame.pack(side=tk.LEFT)
resolution_btns_frame.pack(side=tk.TOP)
error_msg_frame.pack(side=tk.TOP)

"""
url_entry_convert_btn_frame.place()
mp3_4_btn_frame.pack(side=tk.LEFT)
default_folder_frame.pack(side=tk.RIGHT)
mp34_default_btns_frame.place(x=20, y=60)
resolution_btns_frame.place(x=20, y=100)
window_frame.pack()
"""
# Start the event loop.
window.mainloop()