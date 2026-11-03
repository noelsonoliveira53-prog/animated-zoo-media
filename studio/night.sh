#!/bin/bash
# Overnight render queue: renders each item, then pushes the MP4 to the media repo.
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome
cd /root/zoo
R=/home/claude/animated-zoo-media
push() { mkdir -p $R/${SUBDIR:-.}; cp "$1" $R/${SUBDIR:-.}/ && cd $R && git add -A && git commit -qm "Add $(basename $1)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_014CFVfVuQKcnZwKkabBsmrF" && git push -q origin main; cd /root/zoo; echo "PUSHED $(basename $1) $(date +%T)"; }
for s in "$@"; do
  if [[ $s == *ep0* ]]; then python3 long.py eps/$s.json && push out/$s.mp4 || echo "FAIL $s";
  else python3 build.py $s && push out/$s.mp4 || echo "FAIL $s"; fi
done
echo QUEUE_DONE
