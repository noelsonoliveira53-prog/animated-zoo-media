# Gizmo Explains: production run (owner, Nov 19 2026, 12:37 AM)

> "Gizmo Explains channel is the second better performing channel now; let's incorporate that channel on our posting starting tonight:
> create 2 new videos for that channel and post, also change channel description, create a nice banner for the channel and follow same
> principles we are following for The Animated Zoo, however with one 3D explainer a day, minimum 5 mins, and Shorts come from that,
> + create a cartoon version of that and let's test it."

Channel: Gizmo Explains, @GizmoExplainsHQ, channel id UCJaMYOrKCEA54kaOMyYNiKQ, ages 4-8, made for kids. Host: Gizmo, a small round
silver robot with a screen face and an antenna that lights up when he has an idea (3D: `studio/zoo3d/chars/gizmo.py`; flat cartoon:
`studio/cartoon/gizmo/gizmo_flat.svg.part`). Brand: background #1d3a8a to #3561d9, text white, accent #5ff3ff.

Done Nov 19, 12:50 AM: new channel description and banner (`brand/gizmo/banner.png`, safe area checked in Studio's crop view), both read
back after a reload of the customization page.

## What the channel posts

- ONE 3D explainer a day, 5:00 to 6:30 long, built like an Animated Zoo 3D lesson (interactive: questions with answer signs and thinking
  time, on-screen examples of the exact thing explained, every word in sync, a quiz at the end) but with Gizmo as the host and science
  examples instead of animals. Three parts of 83-90 s, each cut whole into one vertical Short (85-95 s, 2160x3840, framed again for 9:16).
- Slots (ET): explainer 2:10 PM; its Shorts on the next days at 8:10 AM, 12:10 PM and 7:10 PM. Always scheduled, never published at once.
- The cartoon version (2D, `studio/cartoon/toon.py`, Gizmo cast) is a TEST: it is a new format for this channel, so it is never uploaded
  until Noelson has watched one full video and approved it (plan status "hold_review"; send him the file).
- Every rule of CLAUDE.md "Working preferences" applies to Gizmo too: 4K native, watermark (Gizmo's channel picture + "Gizmo Explains",
  not Milo), custom thumbnail with at most 3 words and none of the title's words, facts read at the source the same day (line taken out
  if the source cannot be read), stills before the render, frames after, listen.py, review.py, no voice sung or hummed onto notes,
  no '<' or '>' in titles or descriptions, every defect in docs/IMPROVE.md.
- Writing: warm, simple words, short sentences, one true idea per video, questions to the viewer; no danger, fear, anyone hurt, lost,
  crying or trapped, nothing unsafe a child could copy (no fire, electricity at home, chemicals, climbing), no calls to action aimed at kids.
  Description ends with the channel boilerplate: "Gizmo Explains makes gentle, colorful videos for little learners. New videos every day!
  Made with care for ages 4-8. Characters and visuals are animated with the help of AI tools and reviewed for kid safety before publishing."

## Topics

Already on the channel (songs, do not repeat as explainers): magnets, day and night, the 5 senses, rainbows, why the sky is blue, sink or
float, weather, the planets. Explainer topics in order (take the first one with no plan entry): How Do Rockets Fly?; Where Does Rain Come
From? (the water cycle, not weather); How Does a Seed Grow Into a Plant?; How Does Your Heart Work?; Why Do Things Fall Down? (gravity);
How Do Bees Make Honey?; Why Does Ice Melt? (solid, liquid); How Does Sound Travel?; Where Do Shadows Come From?; Why Does the Moon
Change Shape?; How Do Birds Fly?; How Do Our Teeth Help Us?; How Does a Bicycle Move?; Where Does Light Come From?

## Never upload twice, on the RIGHT channel

- Plan file: `studio/upload_plan_gizmo_v3.json`. Guard: `python3 studio/upload_guard.py <file> --channel gizmo` (and `--audit --channel gizmo`).
- Studio's active channel is shared with The Animated Zoo's runs. Switch: Studio avatar menu > Switch account > "Gizmo Explains" (the
  youtube.com/account list does NOT switch Studio reliably, seen Nov 19). Before arming any file read the drawer's channel name
  (`document.querySelector('.entity-name').innerText` must be "Gizmo Explains") and the URL's channel id UCJaMYOrKCEA54kaOMyYNiKQ;
  `zlive("<title>")` on Gizmo's content list must give live = []. Read the channel name again on the upload dialog's page before
  clicking Schedule. When done, switch back to The Animated Zoo the same way and read its name in the drawer.
- Never drive Studio while another run is using it (the Zoo daily run 6:31 AM until it finishes; check the commit log for a run note
  in the last 30 minutes).

## Engine

The 3D lesson tools (`studio/zoo3d/teach.py`, `lesson_shorts.py`, `teachprops.py`, `finish.py`, `watermark.py`) were written for the Zoo:
the host is Milo and the cast are animals. The first Gizmo build adds a channel switch (`"channel": "gizmo"` in the spec: host char gizmo,
Gizmo's lab and outdoor sets, science example props, Gizmo watermark, `gizmo/` output folder) without changing anything a Zoo spec
produces (prove it: a Zoo spec's job JSON is byte-identical before and after). The PC renders the 3D jobs (worker, Blender) as for the Zoo.
