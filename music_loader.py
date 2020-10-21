import os
import time



def get_music_list(base_dir):
    music_list = []

    def _find_music(music_dir):
        for file_name in os.listdir(music_dir):
            abs_path = f'{music_dir}/{file_name}'
            if abs_path.find('.mp3') != -1:
                print('Add music', abs_path)
                music_list.append(abs_path)
            elif os.path.isdir(abs_path):
                print('Explore', abs_path)
                _find_music(abs_path)
            else:
                print('What is it', abs_path)

    try:
        _find_music(base_dir)
    finally:
        return music_list
