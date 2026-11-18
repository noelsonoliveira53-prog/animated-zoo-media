#!/bin/bash
cd /home/claude/animated-zoo-media/studio/cartoon; L=out/zc_ep05/render.log
echo "START short 2 again (second start) $(date)" >> $L; python3 toon.py zc_ep05 --short 2 >> $L 2>&1; echo "EXIT short 2 again $? $(date)" >> $L
for n in 1 2 3; do echo "START av1 short $n $(date)" >> $L
ffmpeg -y -loglevel error -i out/zc_ep05/zc_ep05_short$n.mp4 -c:v libsvtav1 -preset 9 -b:v 2150k -svtav1-params tune=0 -g 240 -pix_fmt yuv420p10le -c:a copy -movflags +faststart ../../cartoon/zc_ep05_short$n.mp4 >> $L 2>&1; echo "EXIT av1 short $n $? $(date)" >> $L; done
echo ENCODESDONE >> $L
