#!/bin/sh
ffmpeg -f alsa -i hw:0 -t $1 out.wav
echo $1
echo $high
echo $low
pitch=$2
if [ "$pitch" = "high" ]; then
	soundstretch out.wav output.wav -pitch=5

elif [ "$pitch" = "low" ]; then
	soundstretch out.wav output.wav -pitch=-5

elif [ "$pitch" = "reverse" ];then
        soundstretch out.wav output.wav -x
fi
exit 0
