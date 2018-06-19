#!/bin/sh
sudo apt-get install alsa-utils
sudo apt-get install ffmpeg
chmod 777 bootstrap
./bootstrap
./configure
make
sudo make install
exit 0
