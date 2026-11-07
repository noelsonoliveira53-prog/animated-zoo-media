// Short story cards shown after a region's boss falls (the Emberdeep finale has its own full epilogue).
export interface StoryCard {
  title: string;
  lines: string[];
  sky: [number, number]; // gradient top, bottom
  accent: number; // glow / particle colour
}

export const STORY: Record<string, StoryCard> = {
  l20: {
    title: 'The Weald Wakes',
    lines: [
      "Morrowcap's spores settle, and the glowcaps dim to a gentle light.",
      'Beyond the mist the Keepers smell salt on the wind.',
      'What is left of the Murkhorde has fled toward the sea.',
    ],
    sky: [0x1e2340, 0x5a4a6a],
    accent: 0x9ae8ff,
  },
  l25: {
    title: 'The Tide Turns',
    lines: [
      "Saltjaw's shell cracks on the rocks, and the shoals fall quiet.",
      'Fishers return to the beaches with nets and songs.',
      'Far inland, the sand turns to glass under a violet sky.',
    ],
    sky: [0x1f6a80, 0xf0e2b8],
    accent: 0xffffff,
  },
  l30: {
    title: 'The Light Mends',
    lines: [
      'Kaleidrax shatters, and its shards ring out like a thousand bells.',
      'The Barrens catch the sunrise and throw it back as rainbows.',
      'High above, a stair of wind climbs into the clouds.',
    ],
    sky: [0x241a3a, 0x8a7aa8],
    accent: 0xc0a0f0,
  },
  l35: {
    title: 'The Wind Settles',
    lines: [
      'Zephyrax folds its great wings and drifts away into the clouds.',
      'The Aeries are still for the first time in an age.',
      'Far below the cloud sea, a green jungle hides an old temple.',
    ],
    sky: [0x9ac8e8, 0xf4f8fc],
    accent: 0xe8f4ff,
  },
  l40: {
    title: 'The Idol Sleeps',
    lines: [
      'Ulmaroth sinks back beneath its moss, and the temple goes quiet.',
      'Then, from under the temple floor, something hisses and clanks.',
      'There are machines down there, and they are still running.',
    ],
    sky: [0x1f5a5a, 0x4a8a3a],
    accent: 0x9aff8a,
  },
  l45: {
    title: 'The Engine Stills',
    lines: [
      "Grindmaw's fires gutter out, and the Hollows fall silent.",
      'The Keepers climb back toward the light, tired and proud.',
      'But deep in the dark, something else has started to answer.',
    ],
    sky: [0x1a1a22, 0x8a6a2a],
    accent: 0xff8a3c,
  },
};
