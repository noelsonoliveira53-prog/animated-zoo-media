// Procedural background music on WebAudio: a lookahead scheduler plays a soft pad, bass and
// arpeggio over a 4-chord loop. Moods change tempo, scale brightness and drums; region themes
// (data/musicThemes.ts) transpose the loop, swap waveforms and add a lead motif. Stingers mark wins/losses.

import { motifAt, resolveMood, STINGERS, stingerSeconds, THEMES, type Mood, type MoodDef, type StingerId, type ThemeDef } from '../data/musicThemes';

export type { Mood } from '../data/musicThemes';

const midiToHz = (m: number) => 440 * Math.pow(2, (m - 69) / 12);

export class Music {
  private ctx: AudioContext | null = null;
  private out: GainNode | null = null;
  private mood: Mood = 'calm';
  private theme: ThemeDef = THEMES[0];
  private enabled = true;
  private volume = 0.6;
  private step = 0;
  private nextTime = 0;
  private timer: number | null = null;

  attach(ctx: AudioContext, destination: AudioNode): void {
    if (this.ctx) return;
    this.ctx = ctx;
    this.out = ctx.createGain();
    this.out.gain.value = this.level();
    this.out.connect(destination);
    this.nextTime = ctx.currentTime + 0.1;
    this.timer = window.setInterval(() => this.schedule(), 50);
  }

  private level(): number {
    return this.enabled ? 0.22 * this.volume : 0;
  }

  setVolume(volume: number, enabled: boolean): void {
    this.volume = volume;
    this.enabled = enabled;
    if (this.out && this.ctx) this.out.gain.setTargetAtTime(this.level(), this.ctx.currentTime, 0.2);
  }

  setMood(m: Mood): void {
    if (m === this.mood) return;
    this.mood = m;
    this.step = Math.floor(this.step / 16) * 16; // restart on a bar line
  }

  setTheme(t: ThemeDef): void {
    if (t.id === this.theme.id) return;
    this.theme = t;
    this.step = Math.floor(this.step / 16) * 16;
  }

  getTheme(): ThemeDef {
    return this.theme;
  }

  /** Short fanfare/lament over a paused loop. Returns false (plays nothing) before audio is unlocked or with music off. */
  stinger(id: StingerId): boolean {
    const ctx = this.ctx;
    if (!ctx || !this.out || !this.enabled) return false;
    const s = STINGERS[id];
    const t0 = ctx.currentTime + 0.05;
    const sixteenth = 60 / s.bpm / 4;
    for (const [semi, step, len] of s.notes) this.note(s.root + semi, t0 + step * sixteenth, len * sixteenth * 1.1, s.wave, 0.09, 0.01);
    const last = s.notes[s.notes.length - 1];
    for (const c of s.chord) this.note(s.root - 12 + c, t0 + last[1] * sixteenth, last[2] * sixteenth * 1.3, 'sine', 0.05, 0.05);
    // Rest the loop until the stinger has rung out, then resume on a bar line.
    this.nextTime = Math.max(this.nextTime, t0 + stingerSeconds(id) + 0.6);
    this.step = Math.ceil(this.step / 16) * 16;
    return true;
  }

  getMood(): Mood {
    return this.mood;
  }

  stop(): void {
    if (this.timer !== null) window.clearInterval(this.timer);
    this.timer = null;
  }

  private schedule(): void {
    const ctx = this.ctx;
    if (!ctx || !this.out) return;
    if (!this.enabled) {
      this.nextTime = ctx.currentTime + 0.1;
      return;
    }
    const def = resolveMood(this.mood, this.theme);
    const sixteenth = 60 / def.bpm / 4;
    // Schedule a little ahead of the audio clock.
    while (this.nextTime < ctx.currentTime + 0.25) {
      this.playStep(def, this.step, this.nextTime, sixteenth);
      this.nextTime += sixteenth;
      this.step++;
    }
  }

  private playStep(def: MoodDef, step: number, t: number, len: number): void {
    const bar = Math.floor(step / 16) % def.chords.length;
    const chord = def.chords[bar];
    const s = step % 16;
    // Pad: once per bar, soft and long.
    if (s === 0) for (const n of chord) this.note(def.root + n, t, len * 15, 'sine', 0.05, 0.6);
    // Bass on beats 1 and 3 (plus a pickup in battle moods).
    if (s === 0 || s === 8 || (def.drums && s === 14)) this.note(def.root - 12 + chord[0], t, len * 3, 'triangle', 0.12, 0.02);
    // Arpeggio every other sixteenth, walking up the chord.
    if (s % 2 === 0) {
      const n = chord[(s / 2) % chord.length] + def.arpOctave + (s >= 8 ? 12 : 0);
      this.note(def.root + n, t, len * 1.6, this.theme.arpWave, 0.025, 0.005);
    }
    // Region motif as a lead line (a quieter echo in calm moods).
    const lead = this.mood === 'calm' ? 0.025 : 0.045;
    for (const [semi, , l] of motifAt(this.theme, step)) this.note(def.root + semi, t, len * l * 1.05, this.theme.leadWave, lead, 0.02);
    if (def.drums) {
      if (s % 4 === 0) this.kick(t);
      if (s % 4 === 2) this.hat(t, 0.03);
      if (s === 4 || s === 12) this.hat(t, 0.06, 1800);
    }
  }

  private note(midi: number, t: number, dur: number, type: OscillatorType, gain: number, attack: number): void {
    const ctx = this.ctx!;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = type;
    osc.frequency.value = midiToHz(midi);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + Math.max(0.005, attack));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(this.out!);
    osc.start(t);
    osc.stop(t + dur + 0.05);
  }

  private kick(t: number): void {
    const ctx = this.ctx!;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.frequency.setValueAtTime(120, t);
    osc.frequency.exponentialRampToValueAtTime(40, t + 0.15);
    g.gain.setValueAtTime(0.18, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.18);
    osc.connect(g).connect(this.out!);
    osc.start(t);
    osc.stop(t + 0.2);
  }

  private hat(t: number, gain: number, cutoff = 6000): void {
    const ctx = this.ctx!;
    const len = Math.floor(ctx.sampleRate * 0.05);
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const f = ctx.createBiquadFilter();
    f.type = 'highpass';
    f.frequency.value = cutoff;
    const g = ctx.createGain();
    g.gain.value = gain;
    src.connect(f).connect(g).connect(this.out!);
    src.start(t);
  }
}

export const music = new Music();
