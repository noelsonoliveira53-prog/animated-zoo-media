#!/bin/bash
# Cut a vertical 1080x1920 Short from a finished 3D song: make_short.sh <src.mp4> <start> <end> "<LINE1>" "<LINE2>" <out.mp4>
# Layout: blurred full-frame background, 4:3 center crop of the song (keeps the burned lyrics), big question title on top.
set -e
SRC=$1; S=$2; E=$3; L1=$4; L2=$5; OUT=$6
F=$(dirname "$0")/fonts/Baloo2-ExtraBold.ttf
S2=$(python3 -c "print(min(150,int(1000/(len(\"$L2\")*0.62))))")
D=$(python3 -c "print($E-$S)")
ffmpeg -v error -y -ss "$S" -t "$D" -i "$SRC" -filter_complex "\
[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.08[bg];\
[b]crop=ih*4/3:ih:(iw-ih*4/3)/2:0,scale=1080:810[fg];[bg][fg]overlay=0:(H-h)/2+40,\
drawtext=fontfile=$F:text='$L1':fontsize=110:fontcolor=white:borderw=10:bordercolor=0x402010:x=(w-tw)/2:y=250,\
drawtext=fontfile=$F:text='$L2':fontsize=$S2:fontcolor=0xFFD23F:borderw=12:bordercolor=0x402010:x=(w-tw)/2:y=370,\
drawtext=fontfile=$F:text='Sing along with Milo!':fontsize=64:fontcolor=white:borderw=6:bordercolor=0x402010:x=(w-tw)/2:y=1560,\
fade=t=in:st=0:d=0.25,fade=t=out:st=$(python3 -c "print($D-0.35)"):d=0.35,fps=30,format=yuv420p[v];\
[0:a]afade=t=in:st=0:d=0.3,afade=t=out:st=$(python3 -c "print($D-0.5)"):d=0.5,loudnorm=I=-16:TP=-1.5[au]" \
-map "[v]" -map "[au]" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 192k -movflags +faststart "$OUT"
