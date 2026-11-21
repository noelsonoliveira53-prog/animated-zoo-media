#!/bin/bash
# Pops the next chunk from queue.txt and renders it (each chunk < 2h). Log: night_q.log
cd /root/zoo
line=$(head -1 queue.txt); [ -z "$line" ] && { echo "QUEUE_EMPTY" >> night_q.log; exit 0; }
sed -i 1d queue.txt
set -- $line; ch=$1; sub=$2; shift 2
echo "CHUNK_START $ch $* $(date +%T)" >> night_q.log
CHANNEL=$ch SUBDIR=$sub GZTITLE=lab bash night.sh "$@" >> night_q.log 2>&1
echo "CHUNK_DONE $ch $(date +%T)" >> night_q.log
