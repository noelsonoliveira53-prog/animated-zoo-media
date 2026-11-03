# Week-2 content brief (one agent per channel)

Working dir: /root/zoo (renderer). Media repo: /home/claude/animated-zoo-media (do NOT commit/push; the lead integrates).
Channel bible (READ FIRST, kids-safety + brand rules): /root/.claude/skills/synced/8d1352d6-8642-41f8-8126-9cc465ce64b3_19dd87a2-86b1-429a-b199-0649a374eb38/youtube-network-channels/SKILL.md

## What to deliver for YOUR channel
Per the 4-week ramp, each channel needs:
- 16 Shorts: 1/day on Nov 9 and Nov 10 (at SLOT_A), then 2/day Nov 11–17 (SLOT_A and SLOT_B).
- 6 episodes: one per day Nov 12–17 at SLOT_EP (Nov 11 is already covered by episode 5).

## Files you create (ONLY these — never edit build.py, long.py, fx.py, channel.py, night.sh, queue.txt, runq.sh or another channel's files)
1. `art_<ch>2.py` — NEW scenes, same style/frame as your channel's existing art file (read it: 1080x1100 viewBox, `<g id="animal">`, `<g id="fx" opacity="0">`, `<g id="fx2" opacity="0">`, cute faces, no text-heavy scenes). Export `SCENES_<CH>2` (dict) and `NAMES_<CH>2` (key → on-screen label). EVERY key must start with your prefix + "2_" (e.g. `tt2_`) so nothing collides. You may also reuse existing scene keys from your channel's current art file in scripts. Aim for ~25 new scenes.
2. `shorts_<ch>2.json` — 16 Shorts in exactly the existing format (copy the structure of your channel's existing shorts JSON: id, animal(scene key), title, thumb, top, bg, floor, sources, 6 beats with the same act names). 20–60 s, ~100–125 words. Ids: `<prefix>2_<topic>`.
3. `eps/<prefix>_ep06_<slug>.json` … `<prefix>_ep11_<slug>.json` — 6 episodes in exactly the existing episode format (intro 5 lines, 5 subjects × 12 lines with the same act tags, recap 6 lines with "@key", outro 2). Target 600–720 words so the render lands at 4:30–6:30. Fresh subjects — don't repeat week-1 episode line-ups.
4. `upload_plan_<ch>2.json` — same schema as the existing upload_plan_<ch>.json (file "<subdir>/<id>.mp4", title, description, date YYYY-MM-DD, time "H:MM AM", status "to_upload", thumb for episodes "brand/<subdir>/thumb_<id>.png"). Descriptions follow the existing ones (AI disclosure line, hashtags, #Shorts on Shorts).
5. Episode thumbnails: `brand/<subdir>/thumb_<id>.html` + PNG (1280x720) in the same style as the existing ones (see mkplan.py; screenshot with node + playwright, chromium is preinstalled: require('playwright')).
6. A contact-sheet PNG of all new scenes so the lead can eyeball them: /tmp/claude-0/-home-claude/ef203c51-db22-5edb-be31-9f6eb9bbdf6d/scratchpad/<ch>2_sheet.png — LOOK at it yourself and fix broken/ugly scenes before finishing.

## Rules
- Do NOT render videos (the machine has 2 cores and a render queue running). Quick SVG/HTML screenshots are fine.
- Original characters only; no brands, no real people, no copyrighted characters.
- Kids-safe, true, simple facts; gentle tone; nothing scary.
- Validate: `python3 -c "import json;json.load(open(...))"` for every JSON; every scene key used in scripts exists in your art (new) or the channel's existing art; titles ≤ 70 chars.
- Finish with a short report: files created, scene count, any concerns.
