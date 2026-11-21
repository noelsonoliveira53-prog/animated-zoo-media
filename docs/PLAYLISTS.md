# The Animated Zoo: playlists and the channel's Home tab

Owner, Nov 20 2026: "Start to create playlist on YouTube and organizing the channel better".
Rules and ids: `studio/playlists.json`. Helper: `studio/playlists.py`. Only The Animated Zoo; Gizmo Explains and the other channels have none here.

## The playlists (Studio > Content > Playlists, read Nov 20 after the last change)

| Playlist | id | holds | on Nov 20 |
|---|---|---|---|
| Milo's Zoo - Every Episode! Animal Songs & Facts for Kids | PLeHpynHKDtC4 | every long video | 56 |
| Sing With Milo: Animal Songs for Kids | PLTugpo-ZdpEU | every song | 16 |
| Milo's Zoo Adventures: Animal Stories for Kids | PLA91qj59yfSM | every cartoon adventure, oldest first | 8 |
| Animal Facts with Milo: Why? How? Who? | PLaz7XgQN0n20 | every cartoon lesson (2D Guess With Milo too) | 9 |
| Learn About Animals with Milo: Lessons for Kids | PLe_JOBipvKqo | every 3D lesson | 23 |
| Guess With Milo: Animal Guessing Games for Kids | PLBBdQkNsgYjs | long guessing games and quizzes (by title) | 4 |
| Elephants for Kids: Songs, Stories and Facts with Milo | PLfYs2HDgA_To | long videos about elephants (by title) | 7 |
| Camels and Desert Animals for Kids with Milo | PLWmeYY_QldD4 | long videos about camels and the desert (by title) | 6 |
| Monkeys and Rainforest Animals for Kids with Milo | PLJrUt_nMvHRM | long videos about monkeys and the rainforest (by title) | 8 |
| Baby Animals for Kids: Songs and Stories with Milo | PLb5gnQZhfWCQ | long videos about baby animals (by title) | 9 |
| Quick Animal Facts: Shorts with Milo | PLTPsc-7PMrYY | every Short, and nothing else | 78 |

All public. A video that is scheduled sits in its playlists already and shows there when it goes public.
Descriptions: what is in the playlist, the ages (2-6), "Every fact is checked against trusted sources." where facts are named; never "AI", never a call to action, never '<' or '>'.
A playlist's description names only things its videos show (Nov 20: "joeys" was typed into Baby Animals with no kangaroo in any video, and taken out before saving).
Eight long videos from before the plans existed (the "5 ... with Milo" lessons) are in their playlists on YouTube and in no plan: `playlists.py --audit` counts 8 fewer than Studio for Every Episode and Learn, 1 fewer for Camels, Monkeys and Baby.

## A new upload goes into its playlists (every run that uploads)

1. `python3 studio/playlists.py <plan file>` prints the playlists (a format decides the series playlists, the title decides the topic playlists).
2. Studio > Content, tick the video's row, "Add to playlist", tick those playlists, Save; the toast reads "Playlists edited". (The upload dialog's own "Playlists" field does the same during the upload.)
3. `python3 studio/playlists.py --done <plan file>` records `"playlists"` in the plan entry. `--todo` lists what is still missing; a run ends with it empty.
A fix of a live video (`--replace`): the new upload goes into the same playlists; the old one leaves them when it is set to Private (Studio hides a private video from a public playlist; remove its row from the playlist page once it is deleted).

## The duplicate trap (found Nov 20: Every Episode read 71 for 56 videos)

In the bulk "Add to playlist" dialog a box with a DASH means "some of the ticked videos are already in". Ticking it and saving adds the ones already in a SECOND time.
- Never tick a dashed box. Tick only rows that are not in the playlist yet (box empty), or untick the box for all of them, Save, then tick it, Save.
- The repair that worked: every row ticked, the playlist's box set to empty, Save (all copies leave); again with the box ticked, Save (one copy each). Then the playlist page: one row per video.
- A "[Deleted video]" row on a playlist's page has its own "Remove" button (a real click; a scripted click does nothing).
- Check afterwards on Content > Playlists: the count equals the number of videos that belong there.

## Driving the dialog from the built-in browser

- When the Browser pane is hidden the page gets no animation frames (a `requestAnimationFrame` callback never runs): the dialog opens in the data and never on screen, and a wait for it runs out. Screenshots are white.
  `window.requestAnimationFrame = cb => setTimeout(() => cb(performance.now()), 16)` (set after testing that a real frame does not come) lets the dialogs open; clicks made by script on the row boxes, the dialog's boxes and Save work; typing a new playlist's title needs real clicks and keys.
- With six or more playlists the dialog gets a search field and its "New playlist" button moves down: click buttons by their text, never by a remembered position.
- Wait about 5 s after a Save before opening the dialog again: the list reloads and closes it.
- A script that takes longer than 45 s is cut off by the tool but keeps running in the page: start it, keep its result in `window.__last`, read that in the next call.

## Home tab (Studio > Customization > Home tab, published Nov 20)

"Show Home Tab" was OFF: visitors landed on the Videos tab and saw no shelves. It is ON now, with 12 sections (the maximum):
For You, Videos, Posts (empty), Collaborations (empty), Sing With Milo, Milo's Zoo Adventures, Animal Facts with Milo, Learn About Animals with Milo, Guess With Milo, Short videos, Baby Animals for Kids, Created playlists.
A section's menu only removes it and a new section lands at the bottom: to move one up, remove the ones that must sit below it and add them again.
Not changed: the channel description (it still says "ages 3-8" and "5-minute zoo adventures every Monday, Wednesday and Friday"; the playlists say 2-6 and the grid is daily), the banner, the picture, the trailer spots. The owner decides those.
