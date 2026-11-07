// Procedural background music on WebAudio: a lookahead scheduler plays a soft pad, bass and
// pentatonic arpeggio over a 4-chord loop. Moods change tempo, scale brightness and drums.

export type Mood = 'calm' | 'battle' | 'boss';

interface MoodDef {
  bpm: number;
  chords: number[][]; // semitone offsets from root per chord
  root: number; // MIDI note
  drums: boolean;
  arpOctave: number;
}

const MOODS: Record<Mood, MoodDef> = {
  calm: { bpm: 78, root: 57, chords: [[0, 4, 7], [-3, 0, 4], [5, 9, 12], [7, 11, 14]], drums: false, arpOctave: 12 },
  battle: { bpm: 112, root: 55, chords: [[0, 3, 7], [-4, 0, 3], [5, 8, 12], [7, 10, 14]], drums: true, arpOctave: 12 },
  boss: { bpm: 132, root: 52, chords: [[0, 3, 7], [1, 4, 8], [0, 3, 7], [-2, 2, 5]], drums: true, arpOctave: 12 },
};

const midiToHz = (m: number) => 440 * Math.pow(2, (m - 69) / 12);

export class Music {
  private ctx: AudioContext | null = null;
  private out: GainNode | null = null;
  private mood: Mood = 'calm';
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
    const def = MOODS[this.mood];
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
      this.note(def.root + n, t, len * 1.6, 'square', 0.025, 0.005);
    }
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
