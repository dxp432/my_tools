from __future__ import unicode_literals
import time
import youtube_dl
import os

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading')
        path_data = '.'
        # 在当前路径找文件
        for i in os.listdir(path_data):
            # 当前文件夹的下面的所有东西的绝对路径
            file_data = path_data + "\\" + i
            print(file_data)
            if os.path.isfile(file_data) and file_data.find('webm') >= 0:
                # 获取当前文件夹的下面的所有文件名字
                print(file_data)

                # 重命名为name
                os.rename(file_data,'name.webm')
                my_cmd = r'ffmpeg -i name.webm name.mp3'
                os.system(my_cmd)

                # 把下面两个文件改名字
                os.rename('name.webm',file_data)
                os.rename('name.mp3',file_data[2:-5]+'.mp3')
                os.remove(file_data)
            else:
                pass
                # print('no webm file  dxp')
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
    youtube_url = r'https://www.youtube.com/watch?v=GEAUExnkHek'


    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except youtube_dl.utils.DownloadError:
        pass
        print('except timesleep5s')
        time.sleep(60)
    print('done....')
    time.sleep(60)

ydl_opts = {}
# ydl_opts['format'] = 'bestvideo+bestaudio'
ydl_opts['format'] = 'bestaudio'
# ydl_opts['ignoreerrors'] = True
ydl_opts['progress_hooks'] = [my_hook]
ydl_opts['logger'] = MyLogger()


# 下载后如需转码，需要cmd语句：ffmpeg -i 冯提莫-小倔强.webm 冯提莫-小倔强.mp3, ，也可运行webm2mp3.py文件进行转换
mydownload()

