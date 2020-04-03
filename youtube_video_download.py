from __future__ import unicode_literals
import youtube_dl
import time


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading')
        print('sleeping...')
        for num in range(0, 20):
            time.sleep(99999)
        print('sleep end')
    if d['status'] == 'downloading':
        # print('downloading')
        pass


class MyLogger(object):
    def debug(self, msg):
        print(msg)
        pass

    def warning(self, msg):
        print(msg)
        pass

    def error(self, msg):
        print(msg)
        print('error,sleep then try again')
        time.sleep(60)
        mydownload()


def mydownload():
    youtube_url = r'https://www.youtube.com/watch?v=K0vSCCAM2ss'
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except youtube_dl.utils.DownloadError:
        pass
        print('except timesleep5s')
        time.sleep(60)
    print('mydownload timesleep5s')
    time.sleep(60)

ydl_opts = {}
ydl_opts['format'] = 'bestvideo+bestaudio'
# ydl_opts['format'] = 'bestaudio'
# ydl_opts['ignoreerrors'] = True
ydl_opts['progress_hooks'] = [my_hook]
ydl_opts['logger'] = MyLogger()


# 下载后如需转码，需要cmd语句：ffmpeg -i 冯提莫-小倔强.webm 冯提莫-小倔强.mp3, ，也可运行webm2mp3.py文件进行转换
mydownload()

#视频和声音合并步骤
# # 1：去掉视频声音
# # ffmpeg -i Python.mp4 -vcodec copy -an Python2.mp4
# # 2：视频和声音合并
# # ffmpeg -i Python2.mp4 -i Python.mp3 -vcodec copy -acodec copy result.mp4