#!/bin/bash
# Splice a Vids hook clip onto the start of a finished 4K Blender episode, keeping the episode's song.
# hybrid_splice.sh <episode.mp4> <hook.mp4> <hook_seconds (must be a keyframe in the episode)> <lyrics.txt> <out.mp4>
# lyrics.txt: lines "start end text" (seconds) burned on the hook like the karaoke lyrics.
set -e
EP=$1; HOOK=$2; T=$3; LY=$4; OUT=$5
D=$(dirname "$0"); FONT=$D/../zoo3d/fonts/Baloo2-ExtraBold.ttf; W=$(mktemp -d)
DT=""; i=0
while read -r s e txt; do [ -z "$s" ] && continue; i=$((i+1))
  printf '%s' "$txt" > "$W/l$i.txt"
  DT="$DT,drawtext=fontfile=$FONT:textfile=$W/l$i.txt:fontsize=104:fontcolor=white:borderw=9:bordercolor=0x2a1a10:x=(w-tw)/2:y=h*0.885:enable=between(t\\,$s\\,$e)"
done < "$LY"
FPS=$(ffprobe -v error -select_streams v -show_entries stream=r_frame_rate -of csv=p=0 "$EP")
ffmpeg -v error -y -i "$HOOK" -t "$T" -an -vf "fps=$FPS,scale=3840:2160:flags=lanczos,unsharp=5:5:0.35$DT,format=yuv420p10le" \
  -c:v libsvtav1 -preset 10 -b:v 8000k -g 240 -video_track_timescale 12288 "$W/hook.mp4"
ffmpeg -v error -y -ss "$T" -i "$EP" -map 0:v -c copy -video_track_timescale 12288 "$W/tail.mp4"
printf "file '%s'\nfile '%s'\n" "$W/hook.mp4" "$W/tail.mp4" > "$W/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$W/list.txt" -c copy "$W/video.mp4"
ffmpeg -v error -y -i "$W/video.mp4" -i "$EP" -map 0:v -map 1:a -c copy -movflags +faststart -shortest "$OUT"
rm -rf "$W"
