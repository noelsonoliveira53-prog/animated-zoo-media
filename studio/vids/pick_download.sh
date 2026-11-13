#!/bin/bash
# pick_download.sh <staged_file> <out.mp4> [min_seconds]
# Checks a file staged from the PC's Downloads folder (a finished .mp4, or the browser's
# <uuid>.tmp / .crdownload that already holds the full video while the save prompt waits)
# and copies it to <out.mp4> only if it decodes fully. No click on the save prompt is needed.
set -e
IN=$1; OUT=$2; MIN=${3:-9}
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN" 2>/dev/null || echo 0)
awk -v d="$DUR" -v m="$MIN" 'BEGIN{exit !(d+0>=m)}' || { echo "NOT_READY duration=$DUR"; exit 2; }
ffmpeg -v error -i "$IN" -f null - 2>&1 | grep -q . && { echo "NOT_READY decode errors (still writing?)"; exit 3; }
cp "$IN" "$OUT"; echo "OK $OUT duration=$DUR"
