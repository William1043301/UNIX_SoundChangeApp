#!/bin/sh
sudo apt-get install alsa-utils
sudo apt-get install ffmpeg
echo "Please enter the time(sec) you want to record."
read n
ffmpeg -f alsa -ar 44100 -i hw:0 -t $n out.wav
exit 0
