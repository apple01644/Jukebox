#!/usr/bin/env bash
sudo rm -rf /etc/jukebox
sudo mkdir /etc/jukebox

cp start.mp3 /etc/jukebox/start.mp3
cp error.mp3 /etc/jukebox/error.mp3
cp music_loader.py /etc/jukebox/music_loader.py
cp controller.py /etc/jukebox/controller.py
cp jukebox.py /etc/jukebox/jukebox.py
sudo touch /etc/jukebox/music_index.dat
sudo chmod u=rw /etc/jukebox/music_index.dat
sudo chown pi /etc/jukebox/music_index.dat

sudo cp jukebox.service /etc/systemd/system/jukebox.service
sudo systemctl enable jukebox
sudo systemctl start  jukebox
