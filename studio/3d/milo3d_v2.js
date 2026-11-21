// 3D Milo v2: sculpted, film-style toy bird. Procedural feather textures, big glossy eyes with lids, layered wings.
// buildMilo(THREE) -> { group, pose(t, opts) }  opts: { talk, flap, hop, look, tilt, blink }
function canvasTex(THREE, w, h, draw, srgb = true) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c); if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4; return t;
}
// scalloped feather pattern used as a bump map
function featherBump(THREE) {
  return canvasTex(THREE, 512, 512, (g, w, h) => {
    g.fillStyle = "#808080"; g.fillRect(0, 0, w, h);
    const s = 32;
    for (let row = 0; row < h / s * 2 + 2; row++) for (let col = -1; col < w / s + 1; col++) {
      const x = col * s + (row % 2) * s / 2, y = row * s / 2;
      const grd = g.createRadialGradient(x, y - s * 0.2, 2, x, y, s * 0.62);
      grd.addColorStop(0, "#b8b8b8"); grd.addColorStop(0.8, "#7a7a7a"); grd.addColorStop(1, "#555");
      g.fillStyle = grd; g.beginPath(); g.ellipse(x, y, s * 0.55, s * 0.62, 0, 0, Math.PI * 2); g.fill();
    }
  }, false);
}
function eyeTex(THREE) {
  return canvasTex(THREE, 512, 512, (g, w, h) => {
    g.fillStyle = "#fbfdff"; g.fillRect(0, 0, w, h);
    const cx = w / 2, cy = h / 2;
    let grd = g.createRadialGradient(cx, cy, 20, cx, cy, 150);
    grd.addColorStop(0, "#2a1a0c"); grd.addColorStop(0.35, "#6b3f17"); grd.addColorStop(0.8, "#a8692a"); grd.addColorStop(1, "#3a230d");
    g.fillStyle = grd; g.beginPath(); g.arc(cx, cy, 150, 0, Math.PI * 2); g.fill();
    for (let i = 0; i < 90; i++) { const a = i / 90 * Math.PI * 2; g.strokeStyle = `rgba(255,210,150,${0.08 + (i % 3) * 0.04})`; g.lineWidth = 3; g.beginPath(); g.moveTo(cx + Math.cos(a) * 70, cy + Math.sin(a) * 70); g.lineTo(cx + Math.cos(a) * 145, cy + Math.sin(a) * 145); g.stroke(); }
    g.fillStyle = "#0b0706"; g.beginPath(); g.arc(cx, cy, 68, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#fff"; g.beginPath(); g.ellipse(cx + 48, cy - 52, 34, 26, -0.5, 0, Math.PI * 2); g.fill();
    g.globalAlpha = 0.85; g.beginPath(); g.arc(cx - 46, cy + 50, 14, 0, Math.PI * 2); g.fill(); g.globalAlpha = 1;
  });
}
export function buildMilo(THREE) {
  const bump = featherBump(THREE);
  const body = (color, rep = 6) => { const b = bump.clone(); b.needsUpdate = true; b.repeat.set(rep * 0.55, rep * 0.35);
    return new THREE.MeshPhysicalMaterial({ color, roughness: 0.55, bumpMap: b, bumpScale: 0.45, sheen: 0.35, sheenRoughness: 0.5, sheenColor: new THREE.Color(0xcfe6ff), clearcoat: 0.15 }); };
  const M = {
    blue: body(0x1f6fe0), dark: body(0x154fb0, 4), belly: body(0xc4e2ff, 5),
    beak: new THREE.MeshPhysicalMaterial({ color: 0xffa21f, roughness: 0.3, clearcoat: 0.8, clearcoatRoughness: 0.2 }),
    eye: new THREE.MeshPhysicalMaterial({ map: eyeTex(THREE), roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.03 }),
    cheek: new THREE.MeshStandardMaterial({ color: 0xff8fb0, roughness: 0.6, transparent: true, opacity: 0.55, depthWrite: false }),
    leg: new THREE.MeshPhysicalMaterial({ color: 0xff9a14, roughness: 0.4, clearcoat: 0.5 }),
  };
  const mesh = (geo, mat) => { const o = new THREE.Mesh(geo, mat); o.castShadow = true; o.receiveShadow = true; return o; };
  const root = new THREE.Group(), rig = new THREE.Group(); root.add(rig);

  // body: a slightly pear-shaped lathe so it reads as a sculpted character, not a ball
  const prof = []; for (let i = 0; i <= 40; i++) { const a = i / 40 * Math.PI; const r = Math.sin(a) * (1 + 0.1 * Math.sin(a - 0.6)); prof.push(new THREE.Vector2(r, -Math.cos(a) * 1.0)); }
  const torso = mesh(new THREE.LatheGeometry(prof, 72), M.blue); torso.scale.set(1.02, 0.98, 0.96); rig.add(torso);
  const belly = mesh(new THREE.SphereGeometry(0.8, 64, 48), M.belly); belly.position.set(0, -0.26, 0.42); belly.scale.set(0.95, 0.9, 0.62); rig.add(belly);

  // eyes with lids
  const eyes = [], lids = [];
  for (const sx of [-1, 1]) {
    const socket = new THREE.Group(); socket.position.set(0.33 * sx, 0.3, 0.74); socket.rotation.y = 0.32 * sx; rig.add(socket);
    const ball = mesh(new THREE.SphereGeometry(0.3, 48, 32), M.eye); ball.scale.z = 0.72; ball.rotation.y = -Math.PI / 2 - 0.3 * sx; ball.rotation.x = 0.05; socket.add(ball); eyes.push(ball);
    const lidGeo = new THREE.SphereGeometry(0.315, 40, 20, 0, Math.PI * 2, 0, Math.PI / 2);
    const top = mesh(lidGeo, M.blue); top.scale.z = 0.76; top.rotation.x = -2.05; socket.add(top);
    const brow = mesh(new THREE.CapsuleGeometry(0.035, 0.22, 6, 12), M.dark); brow.rotation.z = Math.PI / 2 - 0.12 * sx; brow.position.set(0.0, 0.43, 0.08); socket.add(brow);
    lids.push({ top, brow, sx });
    const cheek = mesh(new THREE.SphereGeometry(0.15, 24, 16), M.cheek); cheek.position.set(0.6 * sx, 0.0, 0.7); cheek.scale.set(1, 0.6, 0.3); cheek.rotation.y = 0.65 * sx; cheek.castShadow = false; rig.add(cheek);
  }

  // beak: rounded upper + lower halves
  const beak = new THREE.Group(); beak.position.set(0, 0.04, 0.9); rig.add(beak);
  const half = (len, wid, up) => { const g = new THREE.SphereGeometry(1, 32, 16, 0, Math.PI * 2, up ? 0 : Math.PI / 2, Math.PI / 2); g.scale(wid, 0.16, len); g.translate(0, 0, len * 0.55); return g; };
  const upper = mesh(half(0.4, 0.24, true), M.beak); beak.add(upper);
  const jaw = new THREE.Group(); beak.add(jaw);
  const lower = mesh(half(0.3, 0.2, false), M.beak); lower.position.y = -0.005; jaw.add(lower);

  // crest: curved feather tubes
  for (const [x, lean, len] of [[-0.11, 0.35, 0.5], [0.02, 0.05, 0.62], [0.15, -0.3, 0.45]]) {
    const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(x, 0.9, 0.05), new THREE.Vector3(x - lean * 0.3, 0.9 + len * 0.55, 0.0), new THREE.Vector3(x - lean * 0.7, 0.9 + len, -0.18)]);
    const tube = new THREE.TubeGeometry(curve, 20, 0.07, 12); const pos = tube.attributes.position;
    for (let i = 0; i < pos.count; i++) { const v = new THREE.Vector3().fromBufferAttribute(pos, i); const tt = Math.min(1, Math.max(0, (v.y - 0.9) / len)); const p = curve.getPoint(tt); v.sub(p).multiplyScalar(1 - tt * 0.85).add(p); pos.setXYZ(i, v.x, v.y, v.z); }
    tube.computeVertexNormals(); rig.add(mesh(tube, M.blue));
  }

  // wings: three layered feathers per side
  const wings = [];
  for (const sx of [-1, 1]) {
    const pivot = new THREE.Group(); pivot.position.set(0.9 * sx, 0.12, 0.05); rig.add(pivot);
    [[0, 0, 1], [0.04, -0.12, 0.85], [0.08, -0.22, 0.7]].forEach(([dx, dy, s], k) => {
      const f = mesh(new THREE.SphereGeometry(0.5, 32, 20), k ? M.dark : M.blue); f.scale.set(0.2, 0.78 * s, 0.5 * s); f.position.set((0.1 + dx) * sx, -0.32 + dy, -0.04 * k); f.rotation.z = (0.28 + k * 0.08) * sx; pivot.add(f);
    });
    wings.push({ pivot, sx });
  }

  // tail feathers
  const tail = new THREE.Group(); tail.position.set(0, -0.15, -0.9); rig.add(tail);
  [-0.35, 0, 0.35].forEach(a => { const f = mesh(new THREE.SphereGeometry(0.3, 24, 16), M.dark); f.scale.set(0.42, 0.18, 1); f.position.set(Math.sin(a) * 0.18, 0, -0.18); f.rotation.set(0.5, a, 0); tail.add(f); });

  // legs + toes
  const legs = [];
  for (const sx of [-1, 1]) {
    const leg = new THREE.Group(); leg.position.set(0.3 * sx, -0.84, 0.1); root.add(leg);
    const shin = mesh(new THREE.CapsuleGeometry(0.06, 0.32, 6, 12), M.leg); shin.position.y = -0.2; leg.add(shin);
    for (const a of [-0.5, 0, 0.5]) { const toe = mesh(new THREE.CapsuleGeometry(0.045, 0.14, 6, 10), M.leg); toe.rotation.set(Math.PI / 2, 0, -a); toe.position.set(Math.sin(a) * 0.1, -0.42, 0.08 + Math.cos(a) * 0.06); leg.add(toe); }
    legs.push(leg);
  }

  function pose(t, o = {}) {
    const talk = o.talk || 0, flap = o.flap || 0, hop = o.hop || 0;
    const breathe = Math.sin(t * 2.4) * 0.022;
    const ph = Math.sin(t * 7), hopY = hop > 0 ? Math.abs(ph) * 0.42 * hop : 0;
    const land = hop > 0 ? Math.max(0, 1 - Math.abs(ph) * 5) : 0;
    const sq = 1 - land * 0.12 * hop;
    rig.position.y = 0.05 + breathe + hopY;
    rig.scale.set(1 / Math.sqrt(sq), sq * (1 + breathe * 0.6), 1 / Math.sqrt(sq));
    rig.rotation.y = o.look || 0;
    rig.rotation.z = Math.sin(t * 1.3) * 0.035 + (o.tilt || 0);
    rig.rotation.x = Math.sin(t * 1.1) * 0.03 - talk * 0.04;
    for (const l of legs) l.position.y = -0.84 + hopY * 0.92;
    legs[0].rotation.x = hop > 0 ? ph * 0.45 : 0; legs[1].rotation.x = -legs[0].rotation.x;
    jaw.rotation.x = talk * 0.5; upper.rotation.x = -talk * 0.06;
    const fl = Math.sin(t * (flap > 0.5 ? 15 : 2.6)) * (0.1 + flap * 0.85);
    for (const w of wings) w.pivot.rotation.z = w.sx * (0.38 + fl + flap * 0.55);
    const close = o.blink ? 1 : 0;
    for (const l of lids) { l.top.visible = close > 0; l.top.rotation.x = -0.35; l.brow.position.y = 0.43 + talk * 0.03 - close * 0.02; }
    tail.rotation.x = Math.sin(t * 3) * 0.08; tail.rotation.y = Math.sin(t * 2.2) * 0.15;
  }
  pose(0);
  return { group: root, pose };
}
