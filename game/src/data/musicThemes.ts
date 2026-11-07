// Music data: per-region themes that colour the shared mood loops, plus short end-of-battle stingers.
// Everything is semitones and sixteenth-note steps so the scheduler stays tiny.

export type Mood = 'calm' | 'battle' | 'boss';

export interface MoodDef {
  bpm: number;
  chords: number[][]; // semitone offsets from root per chord (one chord per bar)
  root: number; // MIDI note
  drums: boolean;
  arpOctave: number;
}

/** A motif note: semitone offset from the theme root, start step (0–31 over 2 bars), length in steps. */
export type MotifNote = [semi: number, step: number, len: number];

export interface ThemeDef {
  id: string;
  name: string;
  transpose: number; // semitones added to every mood's root
  tempo: number; // bpm multiplier
  arpWave: OscillatorType;
  leadWave: OscillatorType;
  /** Played as a lead line every 4 bars during battle/boss moods; a softer echo in calm. */
  motif: MotifNote[];
}

export const MOODS: Record<Mood, MoodDef> = {
  calm: { bpm: 78, root: 57, chords: [[0, 4, 7], [-3, 0, 4], [5, 9, 12], [7, 11, 14]], drums: false, arpOctave: 12 },
  battle: { bpm: 112, root: 55, chords: [[0, 3, 7], [-4, 0, 3], [5, 8, 12], [7, 10, 14]], drums: true, arpOctave: 12 },
  boss: { bpm: 132, root: 52, chords: [[0, 3, 7], [1, 4, 8], [0, 3, 7], [-2, 2, 5]], drums: true, arpOctave: 12 },
};

export const THEMES: ThemeDef[] = [
  // Menus, village, map: the plain loops, gentle bell-like lead.
  { id: 'home', name: 'Sanctuary', transpose: 0, tempo: 1, arpWave: 'square', leadWave: 'sine',
    motif: [[12, 0, 4], [14, 4, 4], [19, 8, 8], [16, 20, 4], [14, 24, 8]] },
  // Grovelands: bouncy, woody, rising figure.
  { id: 'grove', name: 'Grovelands', transpose: 2, tempo: 1, arpWave: 'triangle', leadWave: 'triangle',
    motif: [[12, 0, 2], [15, 2, 2], [19, 4, 4], [17, 8, 2], [15, 10, 2], [12, 12, 4], [10, 16, 4], [12, 20, 8]] },
  // Frostfern Highlands: higher, slower, sparse glassy notes.
  { id: 'frost', name: 'Frostfern', transpose: 5, tempo: 0.88, arpWave: 'sine', leadWave: 'sine',
    motif: [[19, 0, 6], [24, 6, 6], [22, 12, 4], [19, 16, 10], [15, 26, 6]] },
  // Emberdeep: low, driving, stabbing falling figure.
  { id: 'ember', name: 'Emberdeep', transpose: -3, tempo: 1.08, arpWave: 'square', leadWave: 'sawtooth',
    motif: [[12, 0, 3], [12, 3, 1], [11, 4, 4], [8, 8, 3], [7, 11, 1], [8, 12, 4], [3, 16, 6], [7, 24, 8]] },
  // Saltmarrow Shoals: a rolling, lilting tune with a square-wave whistle.
  { id: 'shoal', name: 'Saltmarrow', transpose: 3, tempo: 1.04, arpWave: 'triangle', leadWave: 'square',
    motif: [[12, 0, 3], [16, 3, 3], [19, 6, 6], [17, 12, 3], [16, 15, 3], [14, 18, 6], [12, 24, 8]] },
  // Duskcap Weald: hushed, drifting, a little uneasy (whole-tone steps).
  { id: 'dusk', name: 'Duskcap', transpose: 1, tempo: 0.94, arpWave: 'triangle', leadWave: 'sine',
    motif: [[14, 0, 4], [16, 4, 4], [18, 8, 6], [16, 14, 2], [12, 16, 4], [10, 20, 4], [12, 24, 8]] },
];

/** Theme for a battle in a given region (index into REGIONS); clamps to the last themed region. */
export function themeForRegion(region: number): ThemeDef {
  const battleThemes = THEMES.slice(1);
  return battleThemes[Math.max(0, Math.min(battleThemes.length - 1, region))];
}

export function themeById(id: string): ThemeDef {
  return THEMES.find((t) => t.id === id) ?? THEMES[0];
}

/** The mood loop as heard in a theme: transposed and re-tempoed. */
export function resolveMood(mood: Mood, theme: ThemeDef): MoodDef {
  const m = MOODS[mood];
  return { ...m, root: m.root + theme.transpose, bpm: Math.round(m.bpm * theme.tempo) };
}

/** Motif notes that start on this step of a 4-bar (64-step) cycle; the motif plays in the first 2 bars. */
export function motifAt(theme: ThemeDef, step: number): MotifNote[] {
  const s = step % 64;
  if (s >= 32) return [];
  return theme.motif.filter((n) => n[1] === s);
}

export type StingerId = 'victory' | 'defeat';

export interface StingerDef {
  bpm: number;
  wave: OscillatorType;
  root: number; // MIDI
  notes: MotifNote[]; // steps are sixteenths at bpm
  chord: number[]; // held under the final note
}

export const STINGERS: Record<StingerId, StingerDef> = {
  victory: { bpm: 140, wave: 'triangle', root: 60,
    notes: [[0, 0, 2], [4, 2, 2], [7, 4, 2], [12, 6, 4], [9, 10, 2], [12, 12, 2], [16, 14, 10]], chord: [0, 4, 7, 12] },
  defeat: { bpm: 112, wave: 'sawtooth', root: 55,
    notes: [[7, 0, 4], [6, 4, 4], [5, 8, 4], [3, 12, 4], [0, 16, 12]], chord: [0, 3, 6] },
};

/** Total length of a stinger in seconds (used to duck and resume the loop). */
export function stingerSeconds(id: StingerId): number {
  const s = STINGERS[id];
  const end = Math.max(...s.notes.map((n) => n[1] + n[2]));
  return (end * 60) / s.bpm / 4;
}
