# -*- coding: UTF-8 -*-
import pygame
import vlc 
import requests
import json
import time
import os

# 初始化pygame
pygame.mixer.init()
# pygame设置音量
pygame.mixer.music.set_volume(1.0)

instance = vlc.Instance() 
player = instance.media_player_new() 

media = None

while True:
    # 判断是否正在播放
    if pygame.mixer.music.get_busy() or (media is not None and (vlc.State.Ended != media.get_state() and vlc.State.Error != media.get_state())):
        time.sleep(2)
        continue;

    # get ramdon music
    ramdonMusicResult = requests.get("https://puluter.cn/server.php?s=App.Table.FreeRandOne&model_name=bgmList")
    if ramdonMusicResult.status_code != 200:
        continue;
    ramdonMusicJsonResult = json.loads(ramdonMusicResult.text)
    ramdonMusicJsonResult = ramdonMusicJsonResult[u'data'][u'data']
    musicName = ramdonMusicJsonResult[u'music_name']
    musicAddr = ramdonMusicJsonResult[u'music_src']
    print musicName
    print musicAddr

    # download mp3
    musicName = musicName + ".mp3"
    if not os.path.exists(musicName):
        musicFile = requests.get(musicAddr) 
        with open(musicName, "wb") as code:
            code.write(musicFile.content)

    # play mp3
    try:
        media = instance.media_new(musicName)
        player.set_media(media)
        player.play()
        continue
    except:
        print "发生了异常，进行下一首！"

    try:
        pygame.mixer.music.load(musicName)
        pygame.mixer.music.play()
    except:
        print "pygame发生了异常，进行下一首！"
