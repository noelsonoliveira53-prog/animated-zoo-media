import type { EnemyDef } from '../data/types';

/** How an enemy moves on screen; purely visual. */
export type Gait = 'march' | 'waddle' | 'hop' | 'scuttle' | 'flap';

export function gaitFor(def: EnemyDef): Gait {
  if (def.flying) return 'flap';
  if (def.armor >= 0.35 || def.radius >= 18) return 'waddle';
  if (def.radius <= 11) return 'scuttle';
  if (def.speed >= 42) return 'hop'; // the quick ones (roughly the fastest fifth of walkers) bound along
  return 'march';
}

export interface Pose {
  /** pixels lifted off the ground */
  lift: number;
  sx: number;
  sy: number;
  /** radians */
  rot: number;
}

/** The pose at walk phase `b` (radians, grows with distance walked). */
export function poseFor(gait: Gait, b: number): Pose {
  const s = Math.sin;
  switch (gait) {
    case 'waddle': // heavy side-to-side rock with a small lift
      return { lift: Math.abs(s(b)) * 2, sx: 1 + s(2 * b) * 0.03, sy: 1 - s(2 * b) * 0.03, rot: s(b) * 0.09 };
    case 'hop': {
      // bounding hops: stretch in the air, squash on landing
      const ph = (((b % Math.PI) + Math.PI) % Math.PI) / Math.PI; // 0..1 per hop
      const air = s(ph * Math.PI);
      const land = ph < 0.12 || ph > 0.92;
      return { lift: air * 9, sx: land ? 1.12 : 0.97, sy: land ? 0.86 : 1.05, rot: 0 };
    }
    case 'scuttle': // quick little steps with a jitter
      return { lift: Math.abs(s(2 * b)) * 1.5, sx: 1 + s(4 * b) * 0.05, sy: 1 - s(4 * b) * 0.05, rot: s(3 * b) * 0.05 };
    case 'flap': // wings beat: the body stretches and squeezes quickly, with a slow drift tilt
      return { lift: 0, sx: 1 - s(3 * b) * 0.05, sy: 1 + s(3 * b) * 0.12, rot: s(b * 0.7) * 0.06 };
    default: // march: the original gentle bob
      return { lift: Math.abs(s(b)) * 4, sx: 1 + s(2 * b) * 0.04, sy: 1 - s(2 * b) * 0.04, rot: 0 };
  }
}

/** What a soldier or hero is doing this frame, for its idle/walk/fight animation. */
export type UnitState = 'idle' | 'walk' | 'fight';

/**
 * Pose for soldiers and heroes at scene time `t` (ms). `seed` offsets each unit so a squad doesn't move in lockstep;
 * `facing` is +1 right / −1 left (walkers lean and fighters swing toward it).
 */
export function unitPose(state: UnitState, t: number, seed: number, facing: number): Pose {
  const s = Math.sin;
  switch (state) {
    case 'walk': {
      const p = t / 85 + seed;
      return { lift: Math.abs(s(p)) * 3, sx: 1, sy: 1 + Math.abs(s(p)) * 0.03, rot: facing * 0.08 + s(p) * 0.04 };
    }
    case 'fight': {
      // a chopping arc: rock forward into the swing, then back
      const p = t / 70 + seed;
      const swing = Math.max(0, s(p));
      return { lift: 0, sx: 1 + swing * 0.04, sy: 1 - swing * 0.03, rot: facing * swing * 0.2 - facing * 0.03 };
    }
    default: {
      // breathing
      const p = t / 520 + seed;
      return { lift: 0, sx: 1 - s(p) * 0.012, sy: 1 + s(p) * 0.03, rot: 0 };
    }
  }
}
