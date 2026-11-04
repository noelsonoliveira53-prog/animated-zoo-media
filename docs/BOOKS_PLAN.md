# Future step: kids coloring books → Amazon links in channel descriptions

Status: PLANNED, not started (Noelson, Nov 3 2026: "this is for future"). Nothing is added to descriptions yet.

## Decisions so far
- New KDP kids coloring books built from each channel's own episode art (one book per channel/episode theme), published under the Terabit Press imprint.
- Descriptions link with PLAIN amazon.com/dp/<ASIN> links to Noelson's own KDP titles. NO Amazon Associates/affiliate tags: Associates policy prohibits sites directed at children (these channels are Made for Kids).

## How it will work
1. `studio/books_lineart.py` turns any scene key into a black-outline coloring page (8.5x11 @ 300 dpi). Proof pages: docs/books/test_firetruck.png, test_excavator.png.
2. Per book: cover + title page + ~40–50 pages (one subject per page, name in outline letters) + a few activity pages (count, match, trace).
3. Export interior PDF + cover PDF, upload-ready for KDP (Noelson uploads/publishes, or approves an upload via the browser).
4. After each book is live: add one parent-facing line to LONG-FORM episode descriptions only, e.g. "For grown-ups: the Tiny Truck Town coloring book → amazon.com/dp/XXXX". Shorts links aren't clickable, so skip Shorts.

## Rules to keep
- The narration never asks kids to buy anything; the line is addressed to grown-ups and lives only in the description.
- Prefer one solid book per channel/theme over dozens of thin per-episode books (KDP quality/spam risk).
