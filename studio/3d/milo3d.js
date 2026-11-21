// 3D Milo: the Animated Zoo's round blue bird host, built from simple shapes so it renders anywhere (no model files).
// build(THREE) -> { group, pose(t, opts) }   opts: { talk: 0..1, flap: 0..1, blink: bool, look: radians, hop: 0..1 }
export function buildMilo(THREE) {
  const toy = (color, extra = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.45, clearcoat: 0.6, clearcoatRoughness: 0.35, ...extra });
  const M = {
    blue: toy(0x2f80ed), dark: toy(0x1c5fc4), belly: toy(0xa7d3ff), white: toy(0xffffff, { roughness: 0.2 }),
    pupil: toy(0x1a1a2e, { roughness: 0.15, clearcoat: 1 }), beak: toy(0xff9f1c), cheek: toy(0xff9ab0, { transparent: true, opacity: 0.8 }),
  };
  const S = (r, m, w = 32) => { const o = new THREE.Mesh(new THREE.SphereGeometry(r, w, w), m); o.castShadow = true; o.receiveShadow = true; return o; };
  const root = new THREE.Group();          // moves around the world
  const body = new THREE.Group();          // squash/stretch + bob
  root.add(body);

  const torso = S(1, M.blue, 48); torso.scale.set(1, 0.95, 0.95); body.add(torso);
  const belly = S(0.78, M.belly, 48); belly.position.set(0, -0.22, 0.38); belly.scale.set(1, 0.92, 0.7); body.add(belly);

  // eyes
  const eyes = [];
  for (const sx of [-1, 1]) {
    const eye = new THREE.Group(); eye.position.set(0.34 * sx, 0.3, 0.78); eye.rotation.y = 0.28 * sx;
    const white = S(0.27, M.white); white.scale.z = 0.6; eye.add(white);
    const pupil = S(0.14, M.pupil); pupil.position.set(0.02 * sx, -0.01, 0.15); eye.add(pupil);
    const glint = S(0.045, M.white, 12); glint.position.set(0.06 * sx + 0.02, 0.06, 0.25); eye.add(glint);
    body.add(eye); eyes.push(eye);
    const cheek = S(0.13, M.cheek, 16); cheek.position.set(0.58 * sx, 0.02, 0.72); cheek.scale.set(1, 0.6, 0.35); cheek.rotation.y = 0.6 * sx; body.add(cheek);
  }

  // beak: upper + lower halves so it can talk
  const beak = new THREE.Group(); beak.position.set(0, 0.06, 0.9); body.add(beak);
  const cone = (r, h) => { const g = new THREE.ConeGeometry(r, h, 24); g.rotateX(Math.PI / 2); g.translate(0, 0, h / 2); return g; };
  const upper = new THREE.Mesh(cone(0.27, 0.55), M.beak); upper.scale.y = 0.6; upper.position.y = 0.05; upper.castShadow = true; beak.add(upper);
  const lowerPivot = new THREE.Group(); lowerPivot.position.set(0, -0.02, 0); beak.add(lowerPivot);
  const lower = new THREE.Mesh(cone(0.22, 0.4), M.beak); lower.scale.y = 0.5; lower.position.y = -0.04; lower.castShadow = true; lowerPivot.add(lower);

  // crest feathers
  for (const [x, z, rz, h] of [[-0.12, 0.05, 0.25, 0.42], [0.04, 0.12, -0.05, 0.52], [0.18, 0.02, -0.35, 0.36]]) {
    const f = new THREE.Mesh(new THREE.ConeGeometry(0.1, h, 16), M.blue); f.position.set(x, 0.95 + h / 2 - 0.08, z); f.rotation.z = rz; f.castShadow = true; body.add(f);
  }

  // wings (pivot at the shoulder)
  const wings = [];
  for (const sx of [-1, 1]) {
    const pivot = new THREE.Group(); pivot.position.set(0.86 * sx, 0.05, -0.05); body.add(pivot);
    const w = S(0.5, M.dark); w.scale.set(0.28, 0.75, 0.55); w.position.set(0.1 * sx, -0.3, 0); w.rotation.z = 0.25 * sx; pivot.add(w);
    wings.push({ pivot, sx });
  }

  // tail
  const tail = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.7, 20), M.dark); tail.rotation.x = -2.1; tail.position.set(0, -0.1, -0.98); tail.scale.x = 1.5; tail.castShadow = true; body.add(tail);

  // legs + feet
  const legs = [];
  for (const sx of [-1, 1]) {
    const leg = new THREE.Group(); leg.position.set(0.3 * sx, -0.82, 0.1); root.add(leg);
    const shin = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 0.42, 12), M.beak); shin.position.y = -0.21; shin.castShadow = true; leg.add(shin);
    for (const a of [-0.45, 0, 0.45]) { const toe = S(0.07, M.beak, 12); toe.scale.set(0.8, 0.5, 2.2); toe.position.set(Math.sin(a) * 0.12, -0.42, 0.1 + Math.cos(a) * 0.08); toe.rotation.y = a; leg.add(toe); }
    legs.push(leg);
  }

  function pose(t, o = {}) {
    const talk = o.talk || 0, flap = o.flap || 0, hop = o.hop || 0;
    const breathe = Math.sin(t * 2.4) * 0.025;
    const hopY = hop > 0 ? Math.abs(Math.sin(t * 7)) * 0.45 * hop : 0;
    const squash = hop > 0 ? 1 - Math.max(0, Math.cos(t * 14)) * 0.08 * hop : 1;
    body.position.y = 0.06 + breathe + hopY;
    body.scale.set(1 / Math.sqrt(squash) * (1 - breathe * 0.3), squash * (1 + breathe), 1 / Math.sqrt(squash));
    body.rotation.y = o.look || 0;
    body.rotation.z = Math.sin(t * 1.3) * 0.04 + (o.tilt || 0);
    for (const l of legs) l.position.y = -0.82 + hopY * 0.9;
    legs[0].rotation.x = hop > 0 ? Math.sin(t * 7) * 0.4 : 0; legs[1].rotation.x = -legs[0].rotation.x;
    lowerPivot.rotation.x = talk * 0.55;
    upper.rotation.x = -talk * 0.08;
    const fl = Math.sin(t * (flap > 0.5 ? 16 : 3)) * (0.12 + flap * 0.9);
    for (const w of wings) w.pivot.rotation.z = w.sx * (0.15 + fl + flap * 0.6);
    const b = o.blink ? 0.1 : 1; for (const e of eyes) e.scale.y = b;
    tail.rotation.z = Math.sin(t * 3) * 0.12;
  }
  pose(0);
  return { group: root, pose };
}
