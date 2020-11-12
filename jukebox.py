import time
import pygame
import random
import traceback
import os

from controller import Controller
from music_loader import get_music_list

if os.name == 'posix':
    music_dir = '/var/music/'
    run_dir = '/etc/jukebox/'
elif os.name == 'nt':
    music_dir = 'C:/Users/apple/Desktop/as/'
    run_dir = 'F:/Repositories/Jukebox/'


def print_except_trace():
    traceback.format_exc()


class MP3Player:
    music_list = []
    music_volume = 1.0
    controller = None
    music = None

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music_list = get_music_list(music_dir)
        if len(self.music_list) == 0:
            self.play_error_sound(2)

    def play_error_sound(self, times):
        for _ in range(times):
            self.music.load(run_dir + 'error.mp3')
            self.music.play()
            time.sleep(0.77)

    def volume_up(self):
        self.music_volume = min(self.music_volume + 0.003, 1)
        self.music.set_volume(self.music_volume)

    def volume_down(self):
        self.music_volume = max(self.music_volume - 0.003, 0)
        self.music.set_volume(self.music_volume)

    def get_music_index(self):
        try:
            with open(run_dir + 'music_index.dat', 'r') as f:
                return int(f.read())
        except:
            print_except_trace()
            return 0

    def set_music_index(self, new_music_index):
        while new_music_index < 0:
            new_music_index += len(self.music_list)
        while new_music_index >= len(self.music_list):
            new_music_index -= len(self.music_list)
        with open(run_dir + 'music_index.dat', 'w') as f:
            f.write(str(new_music_index))

    music_index = property(get_music_index, set_music_index)

    @property
    def now_music_path(self):
        if os.name == 'nt':
            return self.music_list[self.music_index].replace('/', '\\')
        else:
            return self.music_list[self.music_index]

    def play_song_by_index(self):
        print('Play', self.now_music_path)
        try:
            self.music.load(self.now_music_path)
            self.music.play()
            print('Success Play', self.now_music_path)
        except:
            self.play_error_so
            und(1)
            print_except_trace()

    def prev_song(self):
        self.music_index = self.music_index - 1
        self.play_song_by_index()

    def next_song(self):
        self.music_index = self.music_index + 1
        self.play_song_by_index()

    def big_button(self):
        self.music_index = random.randint(0, len(self.music_list) - 1)
        self.play_song_by_index()

    def main_loop(self):
        self.music.load(run_dir + 'start.mp3')
        self.music.set_volume(self.music_volume)
        print('start')
        self.music.play()
        time.sleep(3)
        self.play_song_by_index()

        self.controller = Controller(self)
        while True:
            self.controller.loop()
            if self.music.get_busy() == 0:
                self.next_song()

    def __del__(self):
        pygame.mixer.quit()
        pygame.quit()


mp3_player = MP3Player()

if __name__ == '__main__':
    mp3_player.main_loop()
