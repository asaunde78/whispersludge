


from yt_dlp import YoutubeDL, utils
import random 
import os
import subprocess


def filename_hook(d):
    # print(d)
    if d["status"] == "finished":
        # print(d)

        os.rename(d["filename"], f"videos/outfile.mp4")




mc_url = "https://www.youtube.com/watch?v=n_Dv4JMiwK8"

opts = {
    "default_search":"ytsearch",
}
username = "redditstory"
with YoutubeDL(opts) as infograb:
    info = infograb.extract_info(mc_url, download=False)
    print(info["duration"])
    end = 132
    start = random.uniform(0, info["duration"]- end)
    
    ydl_opts = {
        "paths": {"home": "videos"},
        "format": "mp4",
        "concurrent_fragment_downloads":5,
        "progress_hooks": [filename_hook],
        "default_search":"ytsearch",
        "download_ranges":utils.download_range_func(None, [(start, end+start)]),  
        "force_keyframes_at_cuts": True, 
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(mc_url)
        
        ffmpeg_cmd = ['ffmpeg', "-y",'-i','videos/outfile.mp4', '-vf', 'subtitles=subtitles.srt', f'videos/{username}subtitled.mp4']
        
        subprocess.run(ffmpeg_cmd)
        ffmpeg_cmd = ["ffmpeg", "-y","-i", f"videos/{username}subtitled.mp4", "-i", f"audio/{username}.wav", "-c:v", "copy" , "-map" , "0:v:0", "-map", "1:a:0", "-shortest", f"videos/final{username}.mp4"]
        subprocess.run(ffmpeg_cmd)