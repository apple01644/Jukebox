#!/usr/bin/env bash
sudo rm -rf /etc/jukebox
sudo mkdir /etc/jukebox

cp start.mp3 /etc/jukebox/start.mp3
cp start.mp3 /var/music/start.mp3
cp controller.py /etc/jukebox/controller.py
cp jukebox.py /etc/jukebox/jukebox.py
sudo cp jukebox.service /etc/systemd/system/jukebox.service
sudo systemctl enable jukebox
sudo systemctl start  jukebox