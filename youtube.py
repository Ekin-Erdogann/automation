from pytube import YouTube
import tkinter as tk
from tkinter import filedialog

def download(url,path):
    try:
        yt=YouTube(url)
        streams=yt.streams.filter(progressive=True,file_extension="mp4")
        highest_res=streams.get_highest_resolution()
        highest_res.download(output_path=path)
        print("video downloaded!")
    except Exception as e:
        print(e)

def open_dialog():
    folder=filedialog.askdirectory()
    if folder:
        return folder


if __name__=="__main__":
    root= tk.Tk()
    root.withdraw()
    url=input( "please enter a youtube url: ")
    save_dir=open_dialog()

    if  save_dir:
        download(url,save_dir)
    else:
        print("please select directory")
        


