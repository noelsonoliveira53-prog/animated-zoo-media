# Growth test drafts: The Animated Zoo (Nov 19 2026)

Drafts only. Nothing here is built, scheduled, uploaded or changed on the channel; no setting, schedule, automation, render preset or
budget was touched. Existing videos, assets, prompts and production files are unchanged.

## Files
| Path | What it is |
|---|---|
| `drafts/growth_test_2026-11/01_audit.md` | What was inspected, the verified baseline, the top-3 long-form comparison, the 0-10 s dips, thumbnail notes |
| `drafts/growth_test_2026-11/02_improvements.md` | Five ranked improvements with before/after examples and how each will be measured; settings notes |
| `drafts/growth_test_2026-11/03_test_plan.md` | The 4-episode test (Nov 23-29, 3:30 PM slots): titles, thumbnails, first shots and lines, outlines, hypotheses |
| `drafts/growth_test_2026-11/05_scorecard.csv` | The four-row scorecard to fill in at day 7 |
| `drafts/growth_test_2026-11/pilot/zool_g01.json` | Pilot lesson spec, teach.py format (same schema as `studio/zoo3d/lessons/zool_ep16.json`) |
| `drafts/growth_test_2026-11/pilot/script.md` | Timed script: every line, answer pauses, music and sound cues (estimated 5:36) |
| `drafts/growth_test_2026-11/pilot/shotlist.md` | 22-shot list for the Blender lesson workflow, plus the new prop and animation needed |
| `drafts/growth_test_2026-11/pilot/thumbnail_and_description.md` | Final title, thumbnail brief, thumbnail render prompt, YouTube description |
| `drafts/growth_test_2026-11/pilot/qa.md` | Fact table (14 claims, each read at source today), kid safety, Milo continuity, mobile, narration; what is not checked yet |
| `drafts/growth_test_2026-11/pilot/make_pilot.py` | Regenerates the spec and the timed script |
| `drafts/growth_test_2026-11/data/` | The Studio table and retention readings this is based on |

## Scorecard (fill in after 7 days public)
Columns: impressions, CTR, % still watching at 30 s, average view duration, watch hours, each against the same-length videos already on the
channel (values in the CSV). **Sample rule:** with under 1,000 impressions at day 7, CTR and retention are noise, so read again at day 14.
With one episode per arm, the test can show a direction, not a winner. A format "wins" only if both of its episodes beat their comparison.

## Qualified watch hours (Earn tab, tracked separately from Analytics watch time)
- Latest reading: **71 qualified hours** (data as of Nov 14; the Earn tab still showed Nov 14 on Nov 19). One reading only, so no weekly pace
  can be measured yet. The next dated Earn reading gives the first real weekly number.
- Your historical estimate: ~36 qualified h/week. A rough check from the analytics: about 31 long-form h/week (69.9 h of all watch time
  in Nov 12-18, times the 45% long-form share of lifetime watch time). This is an estimate, not an Earn-tab figure.
- Planning targets (not forecasts): **77 h/week** reaches 4,000 in about a year; **150-155 h/week** is the six-month pace from the 71 h
  baseline (3,929 h ÷ 26 weeks = 151). The 90-day plan's Jan 31, 2027 application date would need **~377 h/week** (3,929 h ÷ 10.4 weeks),
  far above any pace seen so far.
- Track it weekly in `docs/YPP_PROGRESS.md` (already logged every daily run).

## Three decisions
1. **Produce first: the pilot, "Whose Feet Are These? Guess With Milo".** It is the longest test episode (~5:36, about twice the watch time per
   viewer of a 2:51 song at the same retention) and it tests the biggest leak (lessons lose 61-68% of viewers by 10 s). It must be built and
   approved by you before Nov 25. Sing With Milo #1 (Nov 23) runs inside the current rules regardless.
2. **Test first: the cold open.** The first shot and the first line deliver the title's promise, and Milo's name comes after the hook. It costs
   nothing, works in every format (2D lessons, adventures, 3D songs), and is measured by 10 s and 30 s retention.
3. **A sequel is justified when** the pilot, at day 7 with at least 1,000 impressions, keeps **30% or more of viewers at 30 s** and earns
   **more watch hours in 7 days than the best 2D lesson had after 11-14 days** (5.1 h, Amazing Animal Bodies, in the Nov 16 Studio read; the
   others were 4.2-4.4 h). If impressions are under 1,000, decide at day 14.

## Needs your decision (settings, not changed)
- Guess With Milo episodes are 3D lessons; the Nov 18 rule stopped new 3D lessons. They can use the 3:30 PM one-3D-a-day slot only if you allow
  that exception. Otherwise they port to the 2D fact-lesson engine with the same scripts.
- New format: nothing of it posts until you've watched one full episode and approved it.

## No more evidence needed now
Everything above came from Studio pages this session could read. The Earn tab's next "data as of" reading is the one number that would change
the watch-hour math, and the daily run reads it.
