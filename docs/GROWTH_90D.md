# The Animated Zoo: 90-day operating rules (Noelson, Nov 18, 2026)

Source: Claude Doc "The Animated Zoo — 90-Day Operating System" (https://claude.ai/artifact/NDJNhHpmJW8hu7FoEm54v8), read Nov 19, 2026.
Saved here so every run can read the rules without the connector. Where this file and the doc differ, the doc wins; where the
daily-run prompt's step 3a differs from docs/DAILY_RUN.md, step 3a wins.

Day 1 = Wed Nov 18, 2026. Day 90 = Sun Feb 15, 2027.

## Goal and deadline
- Goal: The Animated Zoo accepted into the YouTube Partner Program (ad revenue) inside 90 days.
- Bar: 1,000 subscribers + 4,000 public long-form watch hours (last 365 days), OR 1,000 subscribers + 10M Shorts views (last 90 days).
  The routes do not combine; Shorts watch time never counts toward hours.
- From Feb 1, 2027 the bar doubles for new applicants (8,000 h or 20M Shorts views). Application submitted no later than
  Sat Jan 31, 2027 (Day 75; the cut-off is stated by AIR Media-Tech, not on YouTube's own help pages). Stretch: Dec 31, 2026.
- Review takes about a month; before acceptance the channel earns $0 from YouTube.
- Made for kids: personalized ads, comments, bell, cards, end screens, memberships, merch, Super Chat/Thanks, Save to playlist are off.
  Ads still run (contextual only).

## Production (effective Nov 18)
| Format | Style | Per day | Status |
|---|---|---|---|
| Music video | 3D | 1, the only 3D upload of the day | keep |
| Adventure story (5:00-6:30) | 2D cartoon | 1+ (daily builds) | keep, top priority |
| Fact lesson (5:00-6:30) | 2D cartoon | 1+ (daily builds) | keep |
| Lesson / story Shorts (85-95 s) | 2D cartoon | 3 | keep |
| 3D teaching lessons | 3D | 0, stopped | no new builds, no new uploads |
| Compilation (20-40 min, own 2D episodes) | 2D | 1 every 2 days, after Noelson approves the first | new |

- 3D lessons already scheduled or public stay (never deleted). Built but not uploaded: status `hold_3d_cap`, not posted; PC jobs not started are cancelled.
- A long slot with no 2D video ready stays EMPTY. An empty slot beats a weak or repetitive video.
- [Superseded Nov 20 2026 11:13 PM] 2D ONLY (Noelson: "Let's keep just 2d cartons on the channel suspend all 3d uploads of songs and fill the spaces with the same carton model we have"): no 3D upload at all on The Animated Zoo, the daily song included; no medley. 3D videos that are public stay; the seven that were scheduled were set Private (`hold_2d_only`), not deleted.

## Positioning and pillars
Milo and his zoo friends go on little adventures and every story teaches one true animal fact. Story-first, fact-proven, sing-along breaks, never scary.
Copy: recurring cast, song hooks, compilations. Do not: nursery-rhyme covers, other brands' characters or songs, toy content.
1. Adventures (2D), growth engine: series with Milo + 5-7 friends; one goal, three obstacles, a solution the friends find, warm ending, 2-3 true facts on screen.
2. Fact lessons (2D), trust engine: question, thinking time, answer sign, on-screen example, say-it-with-me, quiz; facts read at source the day written.
3. Music (3D, 1 a day), discovery engine.
4. Compilations (2D), watch-hour engine: 20-40 min (40+ in the Dec 20-Jan 3 holiday window), one theme, new title, own thumbnail, a new 2D opening
   under 10 s and short 2D bridges; only our own episodes already public; no 3D footage; 4K; review.py PASS; plan format "compilation", slot 5:30 AM.
   Start once 6+ public cartoon episodes share a theme. The first one is "hold_review" until Noelson has watched and approved it (record it in PLAYBOOK.md).

## Daily grid (ET, every slot 2 h apart)
5:30 AM adventure (or compilation) | 7:30 AM Short | 9:30 AM fact lesson | 11:30 AM Short | 1:30 PM adventure | 3:30 PM adventure (it was the 3D song's slot until Nov 20 11:13 PM) | 5:30 PM fact lesson | 7:30 PM Short.
Never two uploads on the same animal or topic on the same day. Multilingual audio tracks stay on the same upload, no duplicates.

## Retention (every long video)
0-5 s problem or question on screen, no logo intro; a new shot/place/action every 8-12 s; a viewer moment every 45-60 s; song or tune break at the midpoint;
last 15 s name the next adventure. Thumbnails: one animal, one emotion, max 3 words; titles Title Case under 60 characters, no clickbait.

## Growth systems
Series arcs of 5-7 adventures; compilations; Shorts as funnel (whole lesson or story moments); weekly double-down (one slot toward the best pillar by watch
time per view); language test (a track with 20%+ of watch time for 4 weeks earns localized titles); variety guard (no same animal/topic per day; own script,
scenes and thumbnail; Noelson's approvals and edits logged in the repo as human creative input).

## Monetization
Not used: sponsorships / paid placement (removes from YouTube Kids), affiliate, Amazon or book links, memberships. Off-YouTube ideas (Noelson's call): KDP
coloring books, library licensing after 100 episodes, song distribution depending on Suno rights.

## YPP checklist
Noelson only: 2-Step Verification; AdSense for YouTube; accepting the YPP base terms in Studio > Earn. Never done by a run.
Daily run checks: no strikes or open claims; Advanced features on; Made for kids = yes and the fact-checked boilerplate (no AI line) on every upload; no reused or near-identical content;
Earn-tab progress logged in docs/YPP_PROGRESS.md; notify Noelson the same day both thresholds of one route are met.
If rejected: appeal within 21 days or reapply after 30 days.

## Milestones (Earn tab)
| Checkpoint | Qualified hours | Subscribers |
|---|---|---|
| Day 30, Dec 17 | >= 1,400 | >= 400 |
| Day 60, Jan 16 | >= 3,000 | >= 800 (below 3,000 h: rescue mode, a compilation every day) |
| Day 75, Jan 31 | 4,000 | 1,000, application submitted |
| Day 90, Feb 15 | - | accepted or pending with a clean channel |
Every run: hours still needed / days left to Jan 31 = hours per day required; flag when the 7-day average is below it. If hours are out of reach but Shorts views
trend above ~110k/day, focus on the 10M Shorts route.

## Reviews
- Mondays, docs/REVIEW_WEEKLY.md (last 7 days): impressions, CTR, AVD / % viewed, retention drops (>10 points in 5 s = fix in the next build), subs per video,
  traffic sources, likes as tie-breaker, each against the channel's own median. Top 3 and what they share; bottom 3 with a new title or thumbnail (applied in
  Studio, never a re-upload) or an intro note in docs/IMPROVE.md; at most one long slot moved toward the best pillar.
- 1st of the month: pillar table by watch time per view, audio-language split, compilation share of watch hours, near-duplicate check, milestone status,
  rescue-mode decision; summary sent to Noelson.

## Calendar
W1 Nov 18-24 cap in force, first compilation to Noelson | W2 Nov 25-Dec 1 first arc named, first weekly review, Noelson's checklist | W3 Dec 2-8 compilations
every 2 days | W4 Dec 9-15 one slot shifted, 3 weakest fixed | W5 Dec 16-22 Day 30 checkpoint | W6 Dec 23-29 holiday compilations 40+ min, winter arc |
W7 Dec 30-Jan 5 apply by Dec 31 if eligible | W8 Jan 6-12 second arc, language read-out | W9 Jan 13-19 Day 60 checkpoint | W10 Jan 20-26 policy audit |
W11 Jan 27-Feb 2 apply no later than Jan 31 | W12 Feb 3-9 keep cadence | W13 Feb 10-15 Day 90.
