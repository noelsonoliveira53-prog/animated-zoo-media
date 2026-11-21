# 1. Channel audit and baseline (The Animated Zoo), Nov 19 2026

## What was inspected (read-only, nothing changed on the channel)
- **YouTube Studio > Insights > Content**, lifetime table (Mar 5 2025 to Nov 18 2026), read Nov 19 5:25 PM ET: views, watch hours,
  thumbnail impressions, CTR, average view duration and % viewed for the top 48 videos by watch time (`data/studio_table_2026-11-19.txt`).
- **Per-video Insights pages** for 9 videos: Studio's key metrics, plus the audience-retention curve, read point by point off the drawn
  chart (`data/retention_2026-11-19.md`; values ±2 points).
- **Earn tab**: eligibility box (data as of Nov 14).
- **Content list** through Studio's own data (122 videos: ids, lengths, publish times, public or scheduled).
- **Project files**: the opening lines of every 2D lesson (`studio/eps/*.json`), the song lyrics (`studio/zoo3d/songs/make_specs_b3/b4.py`),
  the 3D lesson specs (`studio/zoo3d/lessons/`), the thumbnails in `brand/`, and the earlier analytics log (`docs/ANALYTICS.md`).

**Not inspected:** I did not watch the videos. The "scene at the dip" notes below come from the scripts and specs of the opening seconds and
from the thumbnail files, not from playback. Studio's new Insights pages show only "since published" figures per video, so a true
first-7-days window (impressions, CTR and retention by date) was not available. The same-age comparison uses the dated lifetime reads in
`docs/ANALYTICS.md` instead (Nov 13 read: each video 4-8 days old). Traffic-source splits were read only for Where Is My Mama?.

## Baseline (verified)
| Measure | Value | Source and date |
|---|---|---|
| Lifetime views | 37,640 | Studio Insights, data through Nov 18 (your screenshot: 37.7K) |
| Lifetime watch time (all, Shorts included) | 171.2 h | same (your screenshot: 172 h) |
| Thumbnail impressions / CTR / avg view | 440,046 / 2.0% / 0:25 | same |
| Subscribers | 89 | Earn tab, data as of Nov 14 |
| **Qualified public watch hours (365 d)** | **71** | Earn tab, data as of Nov 14 (unchanged on Nov 19) |
| Qualified Shorts views (90 d) | 11K | Earn tab, data as of Nov 14 |
| Long-form watch time in the table | 76.1 h across 19 long videos | Insights table (Shorts: 93.2 h, which does not count toward the 4,000 hours) |
| All watch time, last 7 days (Nov 12-18) | 69.9 h (Shorts included) | `docs/ANALYTICS.md`, Nov 19 7 AM read |

Qualified hours and Analytics watch time are kept apart: the Earn tab counts only public long-form hours after YouTube's validation, so
71 h is the only number that moves YPP. There is one Earn reading so far, so the weekly qualified pace cannot be computed yet.

The three uploads in your screenshot (Panda Loves Bamboo!, Amazing Animal Feet!, Is a Koala a Bear?) went public on Nov 19 and have no
mature data. They are left out of every comparison.

## The three public full-length episodes earning the most watch time
| | Where Is My Mama? (3D song, 2:51) | Amazing Animal Bodies (2D lesson, 4:58) | Animal Sounds Song (3D song, 2:51) |
|---|---|---|---|
| Published | Nov 9 | Nov 5 | Nov 8 |
| Watch hours (lifetime) | **31.3** (41% of all long-form hours) | 5.1 | 5.0 |
| Impressions | 120.4K | 21.7K | 31.9K |
| CTR | 2.9% | 2.8% | 1.9-2.0% |
| Avg view duration | 0:28 (16.8%) | 0:26 (9.0%) | 0:22 (13.0%) |
| Still watching at 10 s / **30 s** | 46% / **23%** | 36% / **20%** | 39% / **19%** |
| Same age (Nov 13 read) | 3,788 views at ~4 days, 119K impr., 2.9% CTR | 676 views at 8 days, 21.7K impr., 2.8% | 738 views at 5 days, 34.1K impr., 1.8% |
| Main traffic | Suggested 93%; 98% new viewers; India 45% | Suggested 95% | Suggested 86% |

For comparison: Milo Had a Zoo! E-I-E-I-O (familiar tune) **6.1% CTR, 32% at 30 s** (the best curve read) but only 2.8K impressions.
Ocean & Ice and Treetop (2D lessons) hold best in the long run (0:45 and 0:39 average, 26-27% at 30 s, 12% and 9% at 2:00) but have the
weakest CTR (1.5% and 1.4%). The two newest guessing-style 3D lessons (Who Am I?, Stripes or Spots?) show 9.9% and 7.0% CTR on only
111 and 86 impressions: too small to read.

## What the dips show
No curve rises anywhere (nothing re-watched). Every curve loses most of its viewers in the **first 10 seconds** (lessons 61-68% gone,
songs 42-61%), then decays smoothly. So the biggest single lever is the opening, not the middle.

| Priority | At the dip (0:00-0:10) | Diagnosis (hypothesis unless stated) |
|---|---|---|
| Where Is My Mama? | Opens straight on the chorus: "Where is my mama? Where can she be?" with the title words on screen. | **Discovery win, opening limit.** Suggested traffic gave it about 4-5x the impressions of any other song (120.4K vs 31.9K and 23.8K, verified). It delivers its promise in second 1, so the 54% lost by 10 s is most likely suggested-feed sampling by viewers who wanted a different baby song (hypothesis). Its question-and-reveal shape (each verse finds a mama) is the model for the test. |
| Amazing Animal Bodies | Opens: "Hi, friends! I'm Milo the bluebird, and welcome to The Animated Zoo! Today we're looking at amazing animal bodies..." The first animal clue comes only after the greeting, the topic list and a count. | **Opening issue (strong hypothesis).** Every 2D lesson and every 3D lesson so far opens with this greeting (verified in all 9 2D lesson files and in zool_ep16). All four 2D lessons with a drawn curve lost 61-68% by 10 s. |
| Animal Sounds Song | Opens on the chorus "What does the animal say?". Thumbnail is the same Milo-with-lion-giraffe-zebra picture as Where Is My Mama?, only the words differ. | **Title/thumbnail issue.** Lowest CTR of the three (1.9%) on 31.9K impressions (verified). The title "Animal Sounds Song for Kids! Roar, Toot, Neigh..." is cut on a phone after "Roar, Toot," and the thumbnail can't be told apart from another video. |

## Thumbnails (looked at the files in `brand/`)
- Where Is My Mama? and Animal Sounds: the same composition (Milo centre, lion, giraffe, zebra), text = the title. A pre-reader sees the same
  picture twice.
- Amazing Animal Bodies: five small flat animals in a row plus "AMAZING BODIES!" and a "5": many small things, no single focus.
- Amazing Animal Feet (zool_ep16, new): "GRIP GRIP!" with a white polar bear on white snow and a small magnifier. The example (feet) is not
  visible at feed size.
