import Phaser from 'phaser';

/** How much of `full` is showing after `t` seconds at `cps` characters per second (line breaks are free). */
export function typeSlice(full: string, t: number, cps: number): string {
  if (t <= 0) return '';
  let budget = Math.floor(t * cps);
  let i = 0;
  while (i < full.length && budget > 0) {
    if (full[i] !== '\n') budget--;
    i++;
  }
  return full.slice(0, i);
}

/**
 * Reveal a text object's string a few characters at a time. A tap anywhere finishes it at once; `still` (Reduce
 * Motion) shows it straight away. Returns a function that completes it immediately.
 */
export function typewriter(scene: Phaser.Scene, text: Phaser.GameObjects.Text, full: string, opts: { cps?: number; delay?: number; still?: boolean; onDone?: () => void } = {}): () => void {
  const cps = opts.cps ?? 45;
  let done = false;
  const finish = () => {
    if (done) return;
    done = true;
    ev?.remove();
    if (text.active) text.setText(full).setAlpha(1);
    scene.input.off('pointerdown', finish);
    opts.onDone?.();
  };
  if (opts.still) {
    text.setText(full).setAlpha(1);
    done = true;
    opts.onDone?.();
    return () => undefined;
  }
  text.setText('').setAlpha(1);
  const start = scene.time.now + (opts.delay ?? 0);
  const ev = scene.time.addEvent({
    delay: 30,
    loop: true,
    callback: () => {
      if (!text.active) return finish();
      const t = (scene.time.now - start) / 1000;
      const shown = typeSlice(full, t, cps);
      text.setText(shown);
      if (shown.length >= full.length) finish();
    },
  });
  scene.input.on('pointerdown', finish);
  return finish;
}
