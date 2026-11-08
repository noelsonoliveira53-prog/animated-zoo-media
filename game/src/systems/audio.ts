// Tiny procedural sound engine on WebAudio. No audio files: every sound is synthesized.
import { music } from './music';

type Wave = OscillatorType;

class Sfx {
  private ctx: AudioContext | null = null;
  private master: GainNode | null = null;
  private volume = 0.6;
  private muted = false;
  private lastPlayed: Record<string, number> = {};

  setVolume(v: number, muted: boolean): void {
    this.volume = v;
    this.muted = muted;
    if (this.master) this.master.gain.value = muted ? 0 : v * 0.5;
  }

  /** Must be called from a user gesture on some browsers. */
  unlock(): void {
    try {
      if (!this.ctx) {
        const Ctor = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (!Ctor) return;
        this.ctx = new Ctor();
        this.master = this.ctx.createGain();
        this.master.gain.value = this.muted ? 0 : this.volume * 0.5;
        this.master.connect(this.ctx.destination);
        // Music bypasses the SFX master so it has its own on/off switch.
        music.attach(this.ctx, this.ctx.destination);
      }
      if (this.ctx.state === 'suspended') void this.ctx.resume();
    } catch {
      this.ctx = null;
    }
  }

  private throttle(key: string, ms: number): boolean {
    const now = performance.now();
    if ((this.lastPlayed[key] ?? 0) + ms > now) return false;
    this.lastPlayed[key] = now;
    return true;
  }

  private tone(freq: number, dur: number, type: Wave, gain: number, slideTo?: number, delay = 0): void {
    if (!this.ctx || !this.master || this.muted) return;
    const t0 = this.ctx.currentTime + delay;
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t0);
    if (slideTo) osc.frequency.exponentialRampToValueAtTime(Math.max(20, slideTo), t0 + dur);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(gain, t0 + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g).connect(this.master);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  }

  private noise(dur: number, gain: number, cutoff = 1200): void {
    if (!this.ctx || !this.master || this.muted) return;
    const len = Math.floor(this.ctx.sampleRate * dur);
    const buf = this.ctx.createBuffer(1, len, this.ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < len; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / len);
    const src = this.ctx.createBufferSource();
    src.buffer = buf;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = cutoff;
    const g = this.ctx.createGain();
    g.gain.value = gain;
    src.connect(filter).connect(g).connect(this.master);
    src.start();
  }

  shoot(kind: string): void {
    if (!this.throttle('shoot' + kind, 60)) return;
    if (kind === 'glimmer') this.tone(880, 0.18, 'sine', 0.12, 1400);
    else if (kind === 'boulder') {
      this.tone(140, 0.2, 'triangle', 0.16, 70);
      this.noise(0.1, 0.12, 500);
    }
    else this.tone(520, 0.06, 'triangle', 0.08, 300);
  }
  melee(): void {
    if (!this.throttle('melee', 90)) return;
    this.noise(0.04, 0.1, 3000);
    this.tone(420 + Math.random() * 120, 0.04, 'square', 0.03);
  }
  boom(): void {
    if (!this.throttle('boom', 80)) return;
    this.noise(0.25, 0.25, 400);
    this.tone(90, 0.25, 'sine', 0.2, 40);
  }
  zap(): void {
    if (!this.throttle('zap', 80)) return;
    this.noise(0.12, 0.15, 5000);
    this.tone(1400, 0.1, 'sawtooth', 0.05, 300);
  }
  heal(): void {
    if (!this.throttle('heal', 200)) return;
    this.tone(500, 0.25, 'sine', 0.06, 900);
  }
  shieldBreak(): void {
    this.noise(0.15, 0.2, 2500);
    this.tone(900, 0.12, 'square', 0.05, 300);
  }
  hit(): void {
    if (this.throttle('hit', 50)) this.noise(0.05, 0.12, 2000);
  }
  kill(): void {
    if (this.throttle('kill', 40)) this.tone(300, 0.15, 'square', 0.06, 90);
  }
  coin(): void {
    if (!this.throttle('coin', 70)) return;
    this.tone(1200, 0.07, 'square', 0.04);
    this.tone(1600, 0.09, 'square', 0.04, undefined, 0.05);
  }
  build(): void {
    this.noise(0.12, 0.2, 600);
    this.tone(220, 0.15, 'triangle', 0.15, 440);
  }
  sell(): void {
    this.tone(700, 0.1, 'triangle', 0.1, 350);
  }
  leak(): void {
    this.tone(160, 0.35, 'sawtooth', 0.12, 60);
  }
  click(): void {
    this.tone(660, 0.04, 'square', 0.05);
  }
  /** Short cues for enemy traits, each throttled so a crowd doesn't turn into noise. */
  trait(kind: string): void {
    if (!this.throttle('trait' + kind, kind === 'thorns' ? 160 : 120)) return;
    switch (kind) {
      case 'gust': // airy whoosh
      case 'swoop':
        this.noise(0.28, 0.1, kind === 'gust' ? 1400 : 900);
        this.tone(320, 0.25, 'sine', 0.03, kind === 'gust' ? 180 : 120);
        break;
      case 'revive': // rising golden chime
        [660, 880, 1320].forEach((f, i) => this.tone(f, 0.16, 'sine', 0.05, undefined, i * 0.07));
        break;
      case 'shift': // two-tone flip
        this.tone(560, 0.05, 'triangle', 0.05);
        this.tone(840, 0.06, 'triangle', 0.05, undefined, 0.05);
        break;
      case 'blink': // quick zip up
        this.tone(700, 0.08, 'sine', 0.05, 1500);
        break;
      case 'thorns': // tiny prick
        this.noise(0.03, 0.06, 4000);
        break;
      case 'glare': // bright flash
        this.tone(1800, 0.12, 'sine', 0.05, 2400);
        this.noise(0.08, 0.06, 6000);
        break;
      case 'coral': // shimmering shell
        this.tone(900, 0.2, 'sine', 0.04, 1300);
        break;
      case 'spores': // soft puff
        this.noise(0.18, 0.08, 700);
        break;
      case 'enrage': // low growl
        this.tone(110, 0.35, 'sawtooth', 0.08, 70);
        break;
      case 'burrow': // dirt rumble
        this.noise(0.22, 0.12, 300);
        break;
      case 'charge': // steam hiss
        this.noise(0.2, 0.09, 5000);
        break;
      case 'echo': // ghostly double ping
        this.tone(1200, 0.12, 'sine', 0.04);
        this.tone(900, 0.18, 'sine', 0.03, undefined, 0.1);
        break;
      case 'shock': // electric crackle
        this.noise(0.14, 0.12, 6000);
        this.tone(1600, 0.1, 'sawtooth', 0.04, 400);
        break;
      case 'blast': // blunderbuss pop
        this.noise(0.1, 0.12, 1800);
        this.tone(160, 0.08, 'square', 0.05, 80);
        break;
      case 'snatch': // a hawk's screech and a whoosh
        this.tone(1400, 0.18, 'sawtooth', 0.035, 900);
        this.noise(0.15, 0.06, 3000);
        break;
      case 'rile': // an angry little hoot
        this.tone(520, 0.08, 'square', 0.04, 780);
        break;
      case 'grief': // a low mournful note
        this.tone(220, 0.35, 'sine', 0.05, 165);
        break;
      case 'mist': // a soft breathy hush
        this.noise(0.25, 0.04, 2500);
        this.tone(660, 0.2, 'sine', 0.025, 990);
        break;
      case 'dodge': // a quick whoosh
        this.noise(0.08, 0.06, 4000);
        break;
      case 'leech': // a quick wet gulp
        this.tone(300, 0.08, 'sine', 0.04, 160);
        break;
      case 'drum': // two hollow log thumps
        this.tone(90, 0.12, 'sine', 0.09, 60);
        this.tone(120, 0.1, 'triangle', 0.06, 70);
        this.noise(0.06, 0.05, 400);
        break;
      case 'anchor': // heavy iron clank and a splash
        this.tone(110, 0.25, 'square', 0.06, 70);
        this.noise(0.3, 0.07, 900);
        break;
      case 'ink': // a soft murky squirt
        this.noise(0.18, 0.08, 500);
        this.tone(220, 0.15, 'sine', 0.04, 110);
        break;
      case 'cleanse': // splash of a wave
        this.noise(0.35, 0.09, 1200);
        this.tone(520, 0.2, 'sine', 0.03, 260);
        break;
      case 'crack': // dry clay snap
        this.noise(0.06, 0.12, 2500);
        this.tone(320, 0.05, 'square', 0.04, 180);
        break;
      case 'mirage': // shimmering detune
        this.tone(700, 0.25, 'sine', 0.04, 740);
        this.tone(705, 0.25, 'sine', 0.04, 660, 0.03);
        break;
      case 'pilfer': // jingle of coins running away
        [1400, 1250, 1100].forEach((f, i) => this.tone(f, 0.06, 'square', 0.03, undefined, i * 0.05));
        break;
      case 'bolt': // thunderclap: sharp crack then a low rumble
        this.noise(0.08, 0.16, 7000);
        this.noise(0.5, 0.1, 300);
        break;
      case 'blossom': // a soft rising shimmer of fluff
        [880, 1100, 1320].forEach((f, i) => this.tone(f, 0.14, 'sine', 0.03, undefined, i * 0.05));
        this.noise(0.25, 0.02, 3000);
        break;
      case 'dive': // a wet plop
        this.tone(320, 0.12, 'sine', 0.05, 120);
        this.noise(0.15, 0.04, 700);
        break;
      case 'hex': // a long, sour, wobbling croak
        this.tone(140, 0.4, 'sawtooth', 0.04, 90);
        this.tone(147, 0.4, 'square', 0.02, 95, 0.05);
        break;
      case 'glaze': // a sticky squelch
        this.noise(0.12, 0.04, 500);
        this.tone(220, 0.12, 'sine', 0.035, 160);
        break;
      case 'parry': // a dull waxy tock
        this.tone(420, 0.06, 'square', 0.035, 300);
        break;
      case 'melt': // a soft sliding drip
        this.tone(700, 0.25, 'sine', 0.045, 260);
        this.tone(520, 0.2, 'triangle', 0.03, 200, 0.06);
        break;
      case 'swarm': // an angry buzzing cloud
        this.tone(180, 0.5, 'sawtooth', 0.035, 220);
        this.tone(186, 0.5, 'sawtooth', 0.03, 230);
        this.noise(0.4, 0.05, 2400);
        break;
      case 'mend': // soft bubbling chime
        this.tone(660, 0.18, 'sine', 0.04, 880);
        this.tone(990, 0.14, 'sine', 0.03, undefined, 0.08);
        break;
      case 'feed': // wet gulp
        this.tone(140, 0.16, 'sine', 0.08, 70);
        this.noise(0.08, 0.05, 600);
        break;
      case 'grow': // creaky sprout
        this.tone(180, 0.18, 'triangle', 0.07, 360);
        this.noise(0.1, 0.06, 900);
        break;
      case 'split': // wet pop
        this.tone(260, 0.08, 'sine', 0.07, 520);
        break;
    }
  }
  waveHorn(): void {
    this.tone(196, 0.5, 'sawtooth', 0.08, 220);
    this.tone(294, 0.5, 'sawtooth', 0.06, 330, 0.08);
  }
  victory(): void {
    [523, 659, 784, 1046].forEach((f, i) => this.tone(f, 0.3, 'triangle', 0.12, undefined, i * 0.13));
  }
  defeat(): void {
    [392, 330, 262, 196].forEach((f, i) => this.tone(f, 0.4, 'sawtooth', 0.08, undefined, i * 0.18));
  }
}

export const sfx = new Sfx();
