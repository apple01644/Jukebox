#!python3

import os
import sys
import time

import pygame

from controller import Controller


class MP3Player:
    RUN_DIR = '/etc/jukebox/'
    MUSIC_DIR = '/etc/jukebox/album/'
    music_list = []
    music_volume = 0.5
    music_index = 0
    controller = None
    music_paused = False

    def __init__(self):
        print('[TRY] file loaded')
        while True:
            if os.path.isdir(self.MUSIC_DIR):
                for f in os.listdir(self.MUSIC_DIR):
                    if f.find('.mp3') != -1:
                        self.music_list.append(f)
            if len(self.music_list) > 0:
                break
            else:
                time.sleep(0.1)
        print('[SUCC] file loaded')

        print('[TRY] Load music index')
        try:
            with open('music_index.dat', 'r') as f:
                data = f.read()
                if data:
                    self.music_index = int(data)
                    if self.music_index >= len(self.music_list):
                        self.music_index = 0
            print('[SUCC] Load music index')
        except:
            print('[FAIL] Load music index')

    def volume_up(self):
        self.music_volume += 0.01
        if self.music_volume > 1:
            self.music_volume = 1
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except:
            pass

    def volume_down(self):
        self.music_volume -= 0.01

        if self.music_volume < 0:
            self.music_volume = 0
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except:
            pass

    def prev_song(self):
        self.music_index = (self.music_index - 1 + len(self.music_list)) % len(self.music_list)
        path = self.MUSIC_DIR + self.music_list[self.music_index]
        print(self.music_list[self.music_index], path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play()
        self.music_paused = False
        with open('music_index.dat', 'w') as f:
            f.write(str(self.music_index))

    def next_song(self):
        self.music_index = (self.music_index + 1) % len(self.music_list)
        path = self.MUSIC_DIR + self.music_list[self.music_index]
        print(self.music_list[self.music_index], path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play()
        self.music_paused = False
        with open('music_index.dat', 'w') as f:
            f.write(str(self.music_index))

    def big_button(self):
        if self.music_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.music_paused = not self.music_paused

    def main_loop(self):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load(self.RUN_DIR + '/start.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        self.controller = Controller(self)
        while True:
            self.controller.loop()
        pygame.mixer.quit()
        pygame.quit()


mp3_player = MP3Player()

if __name__ == '__main__':
    mp3_player.main_loop()
