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
  l50: {
    title: 'The Stars Come Home',
    lines: [
      'Velumbra sinks back into the deep, and its thousand eyes go dark.',
      'The glowing pools brighten, one by one, like stars coming home.',
      'The Murkhorde is broken. The Keepers can finally rest a while.',
    ],
    sky: [0x080a18, 0x3a3a6a],
    accent: 0x5ae8d0,
  },
  l55: {
    title: 'The Orchard Wakes',
    lines: [
      'Mawbloom crumbles into black mulch, and the stumps lie down again.',
      'By morning, green buds are pushing through the rot between the rows.',
      'The Keepers fill their baskets and carry the first clean harvest home.',
    ],
    sky: [0x5a8aa8, 0xd8c890],
    accent: 0xd8642a,
  },
  l60: {
    title: 'The Sky Clears',
    lines: [
      'Thrumhorn sinks to its knees, and the thunder rolls away east.',
      'For the first time in years, real rain falls soft on the steppe.',
      'The herds scatter, calm again, and the grass turns green behind them.',
    ],
    sky: [0x2a3040, 0x7a8a6a],
    accent: 0xfff07a,
  },
  l65: {
    title: 'The Sands Fall Still',
    lines: [
      'Scourmaw sinks beneath the dunes with a long, dry sigh, and does not rise.',
      'The heat haze clears, and the false shapes on the horizon fade away.',
      'Somewhere past the last dune, the Keepers hear the sea for the first time.',
    ],
    sky: [0x3a8aa8, 0xf0dca8],
    accent: 0xd8a060,
  },
  l70: {
    title: 'The Tide Turns',
    lines: [
      'Brinecrown sinks into the deep water, its coral crown settling on the sand.',
      'The reef glows softly in the evening light, and the crabs go quiet.',
      'Far out at sea, a strange dark sail is turning toward the Keepers.',
    ],
    sky: [0x1a5a9a, 0x5ac0c8],
    accent: 0xf07a6a,
  },
  l75: {
    title: 'The Black Sails Fall',
    lines: [
      'Dreadmast lists, groans, and sinks beneath the waves, its black sails last to go.',
      'The rest of the flotilla scatters into the night, rudderless and afraid.',
      'The Keepers stand on a borrowed deck and watch the dawn come up over open sea.',
    ],
    sky: [0x0a1a2a, 0x2a5a7a],
    accent: 0xffb040,
  },
  l80: {
    title: 'The Last Leaf Falls',
    lines: [
      'Rustantler sinks to its knees, and the fire in its antlers gutters out like a candle.',
      'For the first time in an age, the leaves of the Amberwood stop falling.',
      'In the hush, the Keepers hear birdsong, and somewhere far ahead, the sound of the sea.',
    ],
    sky: [0x5a3a2a, 0xd8a050],
    accent: 0xe87a1a,
  },
  l85: {
    title: 'The Fog Lifts',
    lines: [
      'Veilwhisker\'s lantern gutters out, and the old fox spirit fades into the morning like the last of the mist.',
      'One by one, the thousand lanterns go dark. Below them, the terraces shine green in the sun.',
      'From the summit the Keepers can see the whole road home, and the long road still ahead.',
    ],
    sky: [0x8aa8b8, 0xe8f0e0],
    accent: 0xffd27a,
  },
  l90: {
    title: 'The King Steps Down',
    lines: [
      'Crownmane sits back on his throne of branches, and for the first time in a hundred years he is quiet.',
      'The hawks circle once and settle in their nests. The howlers stop howling. The whole canopy holds its breath.',
      'Then the Old King lifts his vine crown, sets it at the Keepers\' feet, and points a long arm toward the horizon.',
    ],
    sky: [0x3a6a3a, 0xd8e8a0],
    accent: 0xe8a040,
  },
  l95: {
    title: 'The Hive Goes Quiet',
    lines: [
      'Goldwing settles on the roof of her great hive, her wings folded, the last of her wax shield cracking away.',
      'The humming of the hills falls to a gentle murmur. The beetles go back to their burrows; the cubs fall asleep in the clover.',
      'Before the Keepers leave, the old queen sends them off with a jar of her finest honey, and points them down the road.',
    ],
    sky: [0xe8a030, 0xfff0c0],
    accent: 0xffd040,
  },
  l100: {
    title: 'The Lantern Dims',
    lines: [
      'Glowmaw sinks down into the black pool, and her great lantern dims to the soft glow of a single firefly.',
      'All across the bog the croaking stops. Then, one by one, the fireflies come back out to dance over the water.',
      'The Keepers have walked a hundred battles from the Grovelands. Somewhere beyond the bog, the road keeps going.',
    ],
    sky: [0x0e2230, 0x3a6a5a],
    accent: 0xe8ff8a,
  },
  l105: {
    title: 'The Wind Lies Down',
    lines: [
      'Galestag stops at the top of the hill, breathing hard, and for the first time in an age the prairie wind falls still.',
      'The thistledown drifts slowly to the ground like summer snow, and the tumbleweeds roll to a stop in the grass.',
      'The old elk bows its great crowned head to the Keepers, then turns and walks away into the tall purple grass.',
    ],
    sky: [0x8a9ac8, 0xf0e0f0],
    accent: 0xb88ad0,
  },
};
