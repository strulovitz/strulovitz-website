/*
================================================================================
 fourd.selftest.js  --  PROOF THAT THE 4D MATHEMATICS IS ACTUALLY CORRECT
================================================================================

 Run it with plain node, no dependencies, no build step:
     node site/src/lib/fourd.selftest.js

 It prints one line per check and exits with code 1 if anything failed, so it
 can go into a pre-commit hook or a build later.

 WHY THIS FILE EXISTS. Nir cannot read code and will never check it, so an
 agent's claim of "the 4D works" is worth nothing on its own. These checks are
 the evidence. They test the properties that MATTER perceptually: that a
 rotation is a true rigid rotation and not a slow shear, that it never mirrors
 the map, that four ninety-degree snaps bring the world exactly home, that a
 hyper-rotation genuinely moves things through the fourth coordinate while an
 ordinary rotation genuinely does not, and that nothing can ever divide by zero
 and blow a node up to infinity in someone's face inside a headset.

 If you change fourd.js, run this. If a check fails, the 4D is broken even if
 the picture on screen still looks pretty.
================================================================================
*/

import {
  PLANES, HYPER_PLANES, identity4, at, planeRotation, multiply4,
  orthonormalize4, determinant4, projectScale, View4D, slabVisibility, FOG_FLOOR,
  DEFAULT_EYE_DISTANCE, W_MIN, leftMultiplyMatrix, rightMultiplyMatrix,
} from './fourd.js';

let passed = 0;
let failed = 0;

function check(name, condition, detail = '') {
  if (condition) {
    passed++;
    console.log(`  PASS  ${name}`);
  } else {
    failed++;
    console.log(`  FAIL  ${name}${detail ? '  --  ' + detail : ''}`);
  }
}

function near(a, b, tolerance = 1e-9) {
  return Math.abs(a - b) <= tolerance;
}

/** How far a matrix is from being a perfect rotation matrix. Should be ~0. */
function orthonormalityError(m) {
  let worst = 0;
  for (let c1 = 0; c1 < 4; c1++) {
    for (let c2 = 0; c2 < 4; c2++) {
      let dot = 0;
      for (let r = 0; r < 4; r++) dot += at(m, r, c1) * at(m, r, c2);
      const expected = c1 === c2 ? 1 : 0;
      worst = Math.max(worst, Math.abs(dot - expected));
    }
  }
  return worst;
}

console.log('\nAI PANORAMA -- 4D mathematics self-test (bible parts 03 and 05)\n');

// -----------------------------------------------------------------------------
console.log('1. The identity and the six planes');
// -----------------------------------------------------------------------------

check('there are exactly six coordinate planes', PLANES.length === 6);
check('three of them are hyper-planes', HYPER_PLANES.length === 3);
check('identity has determinant +1', near(determinant4(identity4()), 1));

// The ZW formula written in bible/part-03.md 3.6, checked literally.
{
  const theta = 0.371;
  const R = planeRotation('zw', theta);
  const p = [0.2, -0.5, 0.7, 0.3];
  const out = [0, 0, 0, 0];
  for (let r = 0; r < 4; r++) {
    out[r] = at(R, r, 0) * p[0] + at(R, r, 1) * p[1] + at(R, r, 2) * p[2] + at(R, r, 3) * p[3];
  }
  const expectedZ = p[2] * Math.cos(theta) - p[3] * Math.sin(theta);
  const expectedW = p[2] * Math.sin(theta) + p[3] * Math.cos(theta);
  check('ZW rotation matches the Bible formula exactly',
    near(out[2], expectedZ) && near(out[3], expectedW),
    `got z=${out[2]} w=${out[3]}, expected z=${expectedZ} w=${expectedW}`);
  check('ZW rotation leaves x and y completely untouched',
    near(out[0], p[0]) && near(out[1], p[1]));
}

// Every one of the six planes must be a proper rotation: determinant +1, never
// -1. A determinant of -1 is a mirror, and a mirrored map would silently
// destroy every reader's spatial memory (part-03.md 3.2, alignment rule 1).
for (const plane of PLANES) {
  const R = planeRotation(plane, 0.7);
  check(`plane ${plane} is a proper rotation, no mirroring`,
    near(determinant4(R), 1) && near(orthonormalityError(R), 0),
    `det=${determinant4(R)}`);
}

// -----------------------------------------------------------------------------
console.log('\n2. Rotation is rigid: nothing stretches, nothing shears');
// -----------------------------------------------------------------------------

{
  // A rotation must preserve the 4D distance of every point from the pivot.
  // If it does not, the graph is being slowly stretched, which would look like
  // "the 4D feels wrong" and be nearly impossible to diagnose by eye.
  const view = new View4D({ pivot: [0.1, -0.2, 0.05, 0.3] });
  const p = [0.6, -0.4, 0.9, -0.7];
  const before = Math.hypot(
    p[0] - view.pivot[0], p[1] - view.pivot[1], p[2] - view.pivot[2], p[3] - view.pivot[3]);
  for (let i = 0; i < 500; i++) {
    view.rotate(PLANES[i % 6], 0.137);
  }
  const out = [0, 0, 0, 0];
  view.rotatePoint(p, out);
  const after = Math.hypot(
    out[0] - view.pivot[0], out[1] - view.pivot[1], out[2] - view.pivot[2], out[3] - view.pivot[3]);
  check('distance from the pivot survives 500 rotations', near(before, after, 1e-9),
    `before=${before} after=${after}`);
  check('Q is still perfectly orthonormal after 500 rotations',
    orthonormalityError(view.Q) < 1e-12, `error=${orthonormalityError(view.Q)}`);
  check('Q still has determinant +1 after 500 rotations',
    near(determinant4(view.Q), 1, 1e-9), `det=${determinant4(view.Q)}`);
}

{
  // The same test with a hostile number of composes, to prove that
  // re-orthonormalizing really does stop drift instead of merely slowing it.
  const view = new View4D();
  for (let i = 0; i < 100000; i++) {
    view.rotate(PLANES[i % 6], 0.011 * ((i % 7) - 3));
  }
  check('Q is still orthonormal after one hundred thousand composes',
    orthonormalityError(view.Q) < 1e-12, `error=${orthonormalityError(view.Q)}`);
  check('no NaN anywhere in Q after one hundred thousand composes',
    Array.from(view.Q).every(Number.isFinite));
}

{
  // The pivot itself must never move. Rotation is "turn the world around this
  // thing"; if the pivot drifts, the focused node slides out from under the
  // reader's attention.
  const view = new View4D({ pivot: [0.4, -0.1, 0.2, -0.6] });
  view.rotate('xw', 1.1).rotate('yz', -0.4).rotate('zw', 2.2);
  const out = [0, 0, 0, 0];
  view.rotatePoint(view.pivot, out);
  check('the pivot point maps exactly onto itself',
    near(out[0], view.pivot[0]) && near(out[1], view.pivot[1]) &&
    near(out[2], view.pivot[2]) && near(out[3], view.pivot[3]));
}

// -----------------------------------------------------------------------------
console.log('\n3. Four snaps come home (the w-gym lesson 3 promise)');
// -----------------------------------------------------------------------------

// bible/part-05.md 5.7 lesson 3 promises the reader, in words: hyper-rotation
// is a LOOP, not a fall. Snap four times and the tesseract turns inside out and
// comes home. If this check fails, that lesson is a lie.
for (const plane of HYPER_PLANES) {
  const view = new View4D();
  for (let i = 0; i < 4; i++) view.rotate(plane, Math.PI / 2, true);
  let worst = 0;
  const I = identity4();
  for (let k = 0; k < 16; k++) worst = Math.max(worst, Math.abs(view.Q[k] - I[k]));
  check(`four 90-degree snaps in ${plane} return exactly to the canonical view`,
    worst < 1e-12, `worst element error=${worst}`);
}

{
  // And the honest structural version of the same claim, on a real tesseract:
  // ONE ninety-degree hyper-rotation must map the sixteen vertices of the
  // tesseract onto the sixteen vertices of the tesseract -- a symmetry of the
  // object, not a random smear. This is the strongest single check in the file:
  // it proves the object being rotated really is a four-dimensional cube.
  const vertices = [];
  for (let i = 0; i < 16; i++) {
    vertices.push([
      (i & 1) ? 1 : -1,
      (i & 2) ? 1 : -1,
      (i & 4) ? 1 : -1,
      (i & 8) ? 1 : -1,
    ]);
  }
  const view = new View4D();
  view.rotate('zw', Math.PI / 2);
  const out = [0, 0, 0, 0];
  let allLandOnVertices = true;
  const hit = new Set();
  for (const v of vertices) {
    view.rotatePoint(v, out);
    const key = out.map((n) => (Math.abs(n - 1) < 1e-9 ? '+' : Math.abs(n + 1) < 1e-9 ? '-' : '?')).join('');
    if (key.includes('?')) allLandOnVertices = false;
    hit.add(key);
  }
  check('a 90-degree ZW hyper-rotation maps the tesseract onto itself',
    allLandOnVertices && hit.size === 16, `distinct images=${hit.size}`);
}

// -----------------------------------------------------------------------------
console.log('\n4. The fourth dimension is genuinely the fourth dimension');
// -----------------------------------------------------------------------------

{
  // An ordinary 3D rotation must NEVER change a node's w. If it does, we have
  // accidentally smeared the fourth dimension into the first three and the
  // whole premise of the project is fake.
  const p = [0.5, 0.2, -0.3, 0.8];
  const out = [0, 0, 0, 0];
  for (const plane of ['xy', 'xz', 'yz']) {
    const view = new View4D();
    view.rotate(plane, 0.9);
    view.rotatePoint(p, out);
    check(`ordinary rotation ${plane} leaves w untouched`, near(out[3], p[3]),
      `w went from ${p[3]} to ${out[3]}`);
  }
  // And a hyper-rotation must genuinely MOVE things in w, otherwise the
  // hyper-rotation is decorative and the reader is being fooled.
  for (const plane of HYPER_PLANES) {
    const view = new View4D();
    view.rotate(plane, 0.9);
    view.rotatePoint(p, out);
    check(`hyper-rotation ${plane} really does move the node in w`,
      Math.abs(out[3] - p[3]) > 0.05, `w barely moved: ${p[3]} -> ${out[3]}`);
  }
}

// -----------------------------------------------------------------------------
console.log('\n5. The projection can never explode in someone\'s headset');
// -----------------------------------------------------------------------------

check('at the floor of the box the scale is exactly 1', near(projectScale(W_MIN), 1));
check('higher w gives a larger scale, so high w looms nearer',
  projectScale(0.9) > projectScale(0) && projectScale(0) > projectScale(-0.9));

{
  // Sweep the entire legal range of w, plus a margin outside it in case a
  // rotation pushes a corner of the unit box slightly past +1, and demand that
  // the scale stays finite, positive and modest. A node whose size suddenly
  // multiplied by a million inside a headset would be genuinely painful.
  let worstScale = 0;
  let allSane = true;
  for (let w = -2; w <= 2.0001; w += 0.001) {
    const s = projectScale(w);
    if (!Number.isFinite(s) || s <= 0) allSane = false;
    worstScale = Math.max(worstScale, s);
  }
  check('the scale stays finite and positive across w from -2 to +2', allSane);
  check('the scale never grows beyond a comfortable factor of four',
    worstScale < 4, `worst scale=${worstScale}`);
  check('the 4D eye is far enough away that the denominator can never reach zero',
    DEFAULT_EYE_DISTANCE > 2);
}

// -----------------------------------------------------------------------------
console.log('\n6. One projection pass, and it agrees with the single-point path');
// -----------------------------------------------------------------------------

{
  // The bulk projection used by the renderer must give exactly the same answer
  // as the plainly-written single point version. Two code paths that disagree
  // would mean the picture and the picking do not match, which feels like the
  // headset is lying to you.
  const n = 64;
  const points4 = new Float64Array(n * 4);
  for (let i = 0; i < n * 4; i++) points4[i] = Math.sin(i * 1.7) * 0.9;
  const out3 = new Float32Array(n * 3);
  const outW = new Float32Array(n);
  const outScale = new Float32Array(n);

  const view = new View4D({ pivot: [0.05, -0.1, 0.2, 0.0] });
  view.rotate('xw', 0.6).rotate('yz', -1.2).rotate('zw', 0.3);

  const before = view.projectionCount;
  view.projectAll(points4, out3, outW, outScale);
  check('one call to projectAll counts as exactly one projection pass',
    view.projectionCount === before + 1);

  let worst = 0;
  const rotated = [0, 0, 0, 0];
  for (let i = 0; i < n; i++) {
    view.rotatePoint(points4.subarray(i * 4, i * 4 + 4), rotated);
    const s = projectScale(rotated[3], view.eyeDistance);
    worst = Math.max(worst,
      Math.abs(out3[i * 3] - rotated[0] * s),
      Math.abs(out3[i * 3 + 1] - rotated[1] * s),
      Math.abs(out3[i * 3 + 2] - rotated[2] * s),
      Math.abs(outW[i] - rotated[3]),
      Math.abs(outScale[i] - s));
  }
  // Float32 output arrays, so the tolerance is float32 precision, not float64.
  check('the fast bulk projection agrees with the plain single-point version',
    worst < 1e-6, `worst disagreement=${worst}`);
  check('every projected value is a real number, no NaN and no infinity',
    Array.from(out3).every(Number.isFinite) && Array.from(outScale).every(Number.isFinite));
}

// -----------------------------------------------------------------------------
console.log('\n7. Undo, reset, and the hyper-plane cycle');
// -----------------------------------------------------------------------------

{
  const view = new View4D();
  view.rotate('xw', 0.5, true);
  const afterFirst = Float64Array.from(view.Q);
  view.rotate('zw', 1.0, true);
  check('undo restores the previous orientation exactly',
    view.undo() && Array.from(view.Q).every((v, i) => near(v, afterFirst[i])));
  view.reset();
  const I = identity4();
  check('reset returns to the canonical view',
    Array.from(view.Q).every((v, i) => near(v, I[i])));
  check('undo eventually reports that there is nothing left to undo', (() => {
    const v = new View4D();
    return v.undo() === false;
  })());
  // A held thumbstick must not fill the undo stack with hundreds of entries.
  const cont = new View4D();
  for (let i = 0; i < 200; i++) cont.rotate('xw', 0.01);
  check('continuous rotation records no undo entries', cont.history.length === 0);
}

{
  const view = new View4D();
  check('the hyper-plane cycle starts at XW', view.activeHyperPlane === 'xw');
  check('clicking cycles XW to YW', view.cycleHyperPlane() === 'yw');
  check('clicking cycles YW to ZW', view.cycleHyperPlane() === 'zw');
  check('clicking cycles ZW back to XW', view.cycleHyperPlane() === 'xw');
}

// -----------------------------------------------------------------------------
console.log('\n8. The slab, and the promise that nothing vanishes without a trace');
// -----------------------------------------------------------------------------

check('a node in the middle of the slab is fully solid', slabVisibility(0, 0, 0.25) === 1);
check('a node at the slab edge is still fully solid', slabVisibility(0.125, 0, 0.25) === 1);
check('a node just outside the slab is a visible ghost, not gone',
  slabVisibility(0.2, 0, 0.25) > 0 && slabVisibility(0.2, 0, 0.25) < 1);
check('a node far outside the ghost band is fog, never fully gone (Nir 2026-09-04: "not disappearing!!!")',
  slabVisibility(0.9, 0, 0.25) === FOG_FLOOR);
check('the ghost band fades smoothly rather than popping', (() => {
  let previous = 1;
  for (let w = 0.125; w <= 0.375; w += 0.005) {
    const v = slabVisibility(w, 0, 0.25);
    if (v > previous + 1e-9) return false;
    previous = v;
  }
  return true;
})());
check('the slab is symmetric above and below the reader\'s position',
  near(slabVisibility(0.3, 0, 0.25), slabVisibility(-0.3, 0, 0.25)));

// -----------------------------------------------------------------------------
console.log('\n9. The two-handed twist really is a rotation of four-dimensional space');
// -----------------------------------------------------------------------------

{
  // Quaternion multiplication, written plainly, to check the matrices against.
  const multiplyQuaternions = (a, b) => ({
    w: a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
    x: a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
    y: a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
    z: a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w,
  });
  const normalise = (q) => {
    const n = Math.hypot(q.w, q.x, q.y, q.z);
    return { w: q.w / n, x: q.x / n, y: q.y / n, z: q.z / n };
  };
  // Our points are (x, y, z, w) and the quaternion is (w, x, y, z), so index 3
  // of a point is the quaternion's w. These two helpers pin that convention.
  const toQuaternion = (p) => ({ w: p[3], x: p[0], y: p[1], z: p[2] });
  const toPoint = (q) => [q.x, q.y, q.z, q.w];

  const l = normalise({ w: 0.3, x: -0.5, y: 0.7, z: 0.2 });
  const r = normalise({ w: -0.4, x: 0.25, y: 0.15, z: 0.8 });
  const p = [0.3, -0.7, 0.2, 0.55];

  // The honest answer, straight from quaternion algebra: l * p * r.
  const expected = toPoint(multiplyQuaternions(multiplyQuaternions(l, toQuaternion(p)), r));

  // The matrices' answer.
  const M = multiply4(leftMultiplyMatrix(l.w, l.x, l.y, l.z),
                      rightMultiplyMatrix(r.w, r.x, r.y, r.z));
  const got = [0, 0, 0, 0];
  for (let row = 0; row < 4; row++) {
    got[row] = at(M, row, 0) * p[0] + at(M, row, 1) * p[1] +
               at(M, row, 2) * p[2] + at(M, row, 3) * p[3];
  }
  let worst = 0;
  for (let i = 0; i < 4; i++) worst = Math.max(worst, Math.abs(got[i] - expected[i]));
  check('the twist matrices agree with plain quaternion multiplication',
    worst < 1e-12, `worst error=${worst}`);

  check('a twist is a proper rotation, no mirroring and no stretching',
    near(determinant4(M), 1, 1e-9) && near(orthonormalityError(M), 0, 1e-12),
    `det=${determinant4(M)} ortho=${orthonormalityError(M)}`);

  // And it must reach where single-plane rotations cannot: a twist should move
  // a point in all four coordinates at once.
  const view = new View4D();
  const out = [0, 0, 0, 0];
  view.twist(l, r);
  view.rotatePoint(p, out);
  let movedInAll = true;
  for (let i = 0; i < 4; i++) if (Math.abs(out[i] - p[i]) < 1e-6) movedInAll = false;
  check('one twist moves a point in all four coordinates at once', movedInAll,
    `${p} -> ${out}`);

  check('Q stays perfectly rigid after a thousand twists', (() => {
    const v = new View4D();
    for (let i = 0; i < 1000; i++) {
      const tiny = normalise({ w: 1, x: 0.01 * Math.sin(i), y: 0.01 * Math.cos(i), z: 0.005 });
      const tiny2 = normalise({ w: 1, x: 0.004, y: -0.008 * Math.sin(i * 0.3), z: 0.006 });
      v.twist(tiny, tiny2);
    }
    return orthonormalityError(v.Q) < 1e-12 && Array.from(v.Q).every(Number.isFinite);
  })());

  check('undo and reset still work after a twist', (() => {
    const v = new View4D();
    v.pushHistory();
    v.twist(l, r);
    if (!v.undo()) return false;
    const I = identity4();
    return Array.from(v.Q).every((value, i) => near(value, I[i]));
  })());

  // The identity twist must do nothing at all, which is what makes "hold both
  // grips still and nothing moves" true, and therefore what makes the gesture
  // trustworthy rather than twitchy.
  check('twisting by nothing changes nothing', (() => {
    const v = new View4D();
    v.rotate('xw', 0.4);
    const before = Float64Array.from(v.Q);
    v.twist({ w: 1, x: 0, y: 0, z: 0 }, { w: 1, x: 0, y: 0, z: 0 });
    return Array.from(v.Q).every((value, i) => near(value, before[i], 1e-12));
  })());
}

// -----------------------------------------------------------------------------
console.log('\n10. A double rotation is the one motion three dimensions cannot imitate');
// -----------------------------------------------------------------------------

{
  // Turning in a plane AND in the plane that shares nothing with it, at the same
  // time, is what four dimensions allow and three do not. In three dimensions
  // any two rotations share an axis and therefore add up to one ordinary turn.
  // These checks prove the pair really is independent, because that is the claim
  // lesson 5 makes to the reader.
  const partners = { xw: 'yz', yw: 'xz', zw: 'xy' };
  for (const [plane, partner] of Object.entries(partners)) {
    const sharesNothing = !plane.split('').some((letter) => partner.includes(letter));
    check(`${plane} and ${partner} share no axis at all`, sharesNothing,
      `${plane} vs ${partner}`);
  }

  // Two rotations in planes that share nothing must COMMUTE: doing them in
  // either order gives the same result. That is the mathematical signature of
  // them being genuinely simultaneous rather than one after the other.
  for (const [plane, partner] of Object.entries(partners)) {
    const one = new View4D();
    one.rotate(plane, 0.7).rotate(partner, 1.1);
    const other = new View4D();
    other.rotate(partner, 1.1).rotate(plane, 0.7);
    let worst = 0;
    for (let i = 0; i < 16; i++) worst = Math.max(worst, Math.abs(one.Q[i] - other.Q[i]));
    check(`turning in ${plane} and ${partner} gives the same result in either order`,
      worst < 1e-12, `worst=${worst}`);
  }

  // And a double rotation must leave NOTHING standing still except the centre:
  // every one of the four coordinates of a general point has to move. A single
  // plane rotation always leaves two coordinates untouched, which is exactly
  // why it looks like an ordinary turn.
  const p = [0.4, -0.3, 0.6, 0.2];
  const out = [0, 0, 0, 0];

  const single = new View4D();
  single.rotate('zw', 0.6);
  single.rotatePoint(p, out);
  let untouchedBySingle = 0;
  for (let i = 0; i < 4; i++) if (Math.abs(out[i] - p[i]) < 1e-9) untouchedBySingle++;
  check('one plane at a time leaves two coordinates completely alone',
    untouchedBySingle === 2, `${untouchedBySingle} untouched`);

  const doubled = new View4D();
  doubled.rotate('zw', 0.6).rotate('xy', 0.5);
  doubled.rotatePoint(p, out);
  let untouchedByDouble = 0;
  for (let i = 0; i < 4; i++) if (Math.abs(out[i] - p[i]) < 1e-9) untouchedByDouble++;
  check('a double rotation moves all four coordinates at once',
    untouchedByDouble === 0, `${untouchedByDouble} untouched`);

  // A double rotation with two different angles does not return to the start
  // after a quarter turn, a half turn or a full turn of either plane. This is
  // the honest basis for telling the reader "it never comes back to the same
  // shape".
  check('a double rotation with unequal angles does not repeat early', (() => {
    const v = new View4D();
    const I = identity4();
    for (let step = 1; step <= 8; step++) {
      v.rotate('zw', Math.PI / 2);
      v.rotate('xy', Math.PI / 2 * 0.37);
      let same = true;
      for (let i = 0; i < 16; i++) if (!near(v.Q[i], I[i], 1e-6)) { same = false; break; }
      if (same) return false;
    }
    return true;
  })());
}

// -----------------------------------------------------------------------------
console.log(`\n${passed} checks passed, ${failed} failed.\n`);
process.exit(failed === 0 ? 0 : 1);
