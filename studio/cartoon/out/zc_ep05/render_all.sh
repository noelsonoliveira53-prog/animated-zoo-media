#!/bin/bash
cd /home/claude/animated-zoo-media/studio/cartoon
L=out/zc_ep05/render.log
echo "START lesson $(date)" > $L; python3 toon.py zc_ep05 >> $L 2>&1; echo "EXIT lesson $? $(date)" >> $L
rm -f out/zc_ep05/zc_ep05_silent.mp4.tmp
for n in 0 1 2; do echo "START short $n $(date)" >> $L; python3 toon.py zc_ep05 --short $n >> $L 2>&1; echo "EXIT short $n $? $(date)" >> $L; done
echo "START av1 $(date)" >> $L
ffmpeg -y -loglevel error -i out/zc_ep05/zc_ep05.mp4 -c:v libsvtav1 -preset 9 -b:v 2150k -svtav1-params tune=0 -g 240 -pix_fmt yuv420p10le -c:a copy -movflags +faststart ../../cartoon/zc_ep05.mp4 >> $L 2>&1; echo "EXIT av1 $? $(date)" >> $L
echo ALLDONE >> $L
