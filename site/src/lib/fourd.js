/*
================================================================================
 fourd.js  --  THE FOUR-DIMENSIONAL MATHEMATICS OF AI PANORAMA
================================================================================

 Owned by: bible/part-03.md sections 3.6 (rotation) and 3.7 (projection).
 Comfort caps and control tiers that USE this file: bible/part-05.md.

 This file contains NO rendering, NO browser APIs and NO three.js. It is pure
 arithmetic, so it can be tested by plain node (see fourd.selftest.js). If you
 are an agent editing this file: keep it that way. The renderer may import this
 file; this file may never import the renderer.

 THE FIVE THINGS YOU MUST UNDERSTAND BEFORE EDITING

 1. In four dimensions you do NOT rotate around an axis. You rotate inside a
    PLANE. There are exactly six coordinate planes: XY, XZ, YZ (the three
    ordinary rotations a human already knows) and XW, YW, ZW (the three
    "hyper-rotations" that are the whole point of this project).

 2. A rotation by angle theta in a plane mixes the two coordinates named by
    that plane and leaves the other two completely alone. For the ZW plane:
        z_new = z * cos(theta) - w * sin(theta)
        w_new = z * sin(theta) + w * cos(theta)
    Every other plane is the same two lines with different letters.

 3. There is only ever ONE piece of orientation state in the whole program: the
    4x4 matrix Q. Every user gesture, from a thumbstick nudge to the expert
    two-handed twist, is composed onto Q by Q = R * Q. Because there is only
    one state, Undo is "pop the previous Q off a stack" and Reset is
    "Q = identity". Never invent a second orientation variable anywhere.

 4. Repeated multiplication of matrices slowly accumulates floating point
    error, and a drifted rotation matrix quietly turns into a shear that
    stretches the whole graph. So after every compose we re-orthonormalize Q
    (Gram-Schmidt). This is not optional politeness; it is what keeps the map
    honest over a long session.

 5. Matrices here are COLUMN-MAJOR, the same convention three.js uses, stored
    in a flat array of 16 numbers. The element in row r, column c lives at
    index c * 4 + r. Write it down; index mistakes here are invisible bugs
    that look like "the 4D feels weird".

 LAW 2 REMINDER, because this is where the temptation lives: the fourth
 coordinate w is NEVER turned into a colour. This file returns a projection
 SCALE for w. Size, stems, gauges and slabs are how w becomes visible. Hue is
 reserved for identity. An agent that maps w to hue has failed the task.
================================================================================
*/

// The six coordinate planes, in the fixed order used by the whole project.
// The first three are ordinary 3D rotations, the last three are hyper-rotations.
export const PLANES = ['xy', 'xz', 'yz', 'xw', 'yw', 'zw'];

// The three hyper-planes, in the order the left thumbstick click cycles them
// (bible/part-05.md 5.4, Tier 1 control 2).
export const HYPER_PLANES = ['xw', 'yw', 'zw'];

// Which coordinate index each letter means. x=0, y=1, z=2, w=3.
const AXIS_INDEX = { x: 0, y: 1, z: 2, w: 3 };

// Default 4D eye distance for the projection (bible/part-03.md 3.7.1).
export const DEFAULT_EYE_DISTANCE = 3.0;

// The floor of the unit box. Every published coordinate lives in [-1, +1]
// (bible/part-03.md 3.1.2), so the lowest possible w is -1.
export const W_MIN = -1;


// -----------------------------------------------------------------------------
// BASIC MATRIX ARITHMETIC
// -----------------------------------------------------------------------------

/** A fresh 4x4 identity matrix: the canonical, un-rotated view. */
export function identity4() {
  const m = new Float64Array(16);
  m[0] = 1; m[5] = 1; m[10] = 1; m[15] = 1;
  return m;
}

/** Read the element at row r, column c out of a column-major 4x4. */
export function at(m, r, c) {
  return m[c * 4 + r];
}

/**
 * Build the rotation matrix for one plane.
 *
 * plane: one of the six strings in PLANES, for example 'zw'.
 * theta: the angle in RADIANS.
 *
 * The result is a proper rotation: its determinant is +1 and it never mirrors
 * anything. Mirroring would silently flip the reader's whole mental map, which
 * bible/part-03.md 3.2 forbids by name.
 */
export function planeRotation(plane, theta) {
  const i = AXIS_INDEX[plane[0]];
  const j = AXIS_INDEX[plane[1]];
  if (i === undefined || j === undefined || i === j) {
    throw new Error(`fourd: not a coordinate plane: ${plane}`);
  }
  const c = Math.cos(theta);
  const s = Math.sin(theta);
  const m = identity4();
  // Column-major writes. Reading these four lines against note 2 at the top
  // of this file is the fastest way to convince yourself they are right.
  m[i * 4 + i] = c;   // row i, col i
  m[j * 4 + i] = -s;  // row i, col j
  m[i * 4 + j] = s;   // row j, col i
  m[j * 4 + j] = c;   // row j, col j
  return m;
}

/** Matrix product a * b, returned as a new matrix. */
export function multiply4(a, b) {
  const out = new Float64Array(16);
  for (let c = 0; c < 4; c++) {
    for (let r = 0; r < 4; r++) {
      let sum = 0;
      for (let k = 0; k < 4; k++) sum += at(a, r, k) * at(b, k, c);
      out[c * 4 + r] = sum;
    }
  }
  return out;
}

/**
 * Gram-Schmidt: force the four columns to be unit length and mutually
 * perpendicular again, in place. Call this after every compose (note 4 above).
 * The columns are processed in order, so column 0 keeps its direction exactly
 * and later columns are nudged; that makes the correction stable rather than
 * jittery.
 */
export function orthonormalize4(m) {
  for (let c = 0; c < 4; c++) {
    // Subtract from this column everything it shares with the earlier columns.
    for (let e = 0; e < c; e++) {
      let dot = 0;
      for (let r = 0; r < 4; r++) dot += m[c * 4 + r] * m[e * 4 + r];
      for (let r = 0; r < 4; r++) m[c * 4 + r] -= dot * m[e * 4 + r];
    }
    // Then make it exactly one unit long.
    let len = 0;
    for (let r = 0; r < 4; r++) len += m[c * 4 + r] * m[c * 4 + r];
    len = Math.sqrt(len);
    if (len < 1e-12) {
      // Should never happen with a real rotation. If it somehow does, refuse to
      // divide by zero and put a clean basis vector back, so the view stays
      // usable instead of filling with NaN.
      for (let r = 0; r < 4; r++) m[c * 4 + r] = (r === c) ? 1 : 0;
      continue;
    }
    for (let r = 0; r < 4; r++) m[c * 4 + r] /= len;
  }
  return m;
}

/** The determinant of a 4x4. Used only by the self-test and the debug HUD. */
export function determinant4(m) {
  // Laplace expansion along the first row. Written out longhand on purpose:
  // it is easier for a future reader to check than a clever loop.
  const s = (r0, r1, c0, c1) =>
    at(m, r0, c0) * at(m, r1, c1) - at(m, r0, c1) * at(m, r1, c0);
  const d0 = at(m, 0, 0) * (
    at(m, 1, 1) * s(2, 3, 2, 3) - at(m, 1, 2) * s(2, 3, 1, 3) + at(m, 1, 3) * s(2, 3, 1, 2));
  const d1 = at(m, 0, 1) * (
    at(m, 1, 0) * s(2, 3, 2, 3) - at(m, 1, 2) * s(2, 3, 0, 3) + at(m, 1, 3) * s(2, 3, 0, 2));
  const d2 = at(m, 0, 2) * (
    at(m, 1, 0) * s(2, 3, 1, 3) - at(m, 1, 1) * s(2, 3, 0, 3) + at(m, 1, 3) * s(2, 3, 0, 1));
  const d3 = at(m, 0, 3) * (
    at(m, 1, 0) * s(2, 3, 1, 2) - at(m, 1, 1) * s(2, 3, 0, 2) + at(m, 1, 2) * s(2, 3, 0, 1));
  return d0 - d1 + d2 - d3;
}


// -----------------------------------------------------------------------------
// THE PROJECTION FROM FOUR DIMENSIONS DOWN TO THREE
// -----------------------------------------------------------------------------

/**
 * The normalized projection scale of bible/part-03.md 3.7.1:
 *     s = (d - w_min) / (d - w)
 *
 * Why this exact form and not the textbook 4D perspective divide: because w
 * can never reach d (w is at most +1, d defaults to 3), the denominator can
 * never reach zero, so nothing can ever explode to infinity on screen. And
 * because the numerator uses w_min, s is close to 1 across the whole unit box
 * instead of being an arbitrary small number.
 *
 * What the reader experiences: a node with a HIGH w looks BIGGER and nearer,
 * exactly like the outer cube in the classic drawing of a tesseract, while low
 * w nests small and inward. Under the default meaning of w that is also
 * editorially true: the settled encyclopedia looms large and enclosing, this
 * week's raw news hangs small and outward.
 */
export function projectScale(w, d = DEFAULT_EYE_DISTANCE, wMin = W_MIN) {
  return (d - wMin) / (d - w);
}


// -----------------------------------------------------------------------------
// THE VIEW: THE ONE PIECE OF 4D STATE IN THE PROGRAM
// -----------------------------------------------------------------------------

/**
 * View4D holds the single orientation matrix Q, the pivot that rotation happens
 * about, the 4D eye distance, and the small undo stack. Both the VR body and
 * the flat-screen body of the site drive this same object, which is how
 * bible/part-05.md can promise "one interaction model, two bodies".
 */
export class View4D {
  constructor(options = {}) {
    this.Q = identity4();
    // Rotation happens about the focused node, or the graph centroid when
    // nothing is focused (bible/part-03.md 3.6.2). Never about the world origin.
    this.pivot = new Float64Array(options.pivot || [0, 0, 0, 0]);
    this.eyeDistance = options.eyeDistance ?? DEFAULT_EYE_DISTANCE;
    // Undo history of previous Q values. Small on purpose: this is a courage
    // aid for experimenting, not a document history.
    this.history = [];
    this.historyLimit = options.historyLimit ?? 32;
    // Which hyper-plane the left thumbstick currently drives.
    this.activeHyperPlane = 'xw';
    // How many times a full projection pass has run. The renderer's debug
    // assert uses this to prove the one-projection-per-frame rule.
    this.projectionCount = 0;
  }

  /** Remember the current Q so that undo() can come back to it. */
  pushHistory() {
    this.history.push(Float64Array.from(this.Q));
    if (this.history.length > this.historyLimit) this.history.shift();
  }

  /**
   * Rotate by theta radians in one plane, composing onto Q and immediately
   * re-orthonormalizing.
   *
   * recordUndo should be FALSE for the continuous frame-by-frame rotation of a
   * held thumbstick (otherwise one gesture would fill the undo stack with
   * hundreds of entries) and TRUE for a discrete act such as a 90 degree snap.
   */
  rotate(plane, theta, recordUndo = false) {
    if (theta === 0) return this;
    if (recordUndo) this.pushHistory();
    this.Q = orthonormalize4(multiply4(planeRotation(plane, theta), this.Q));
    return this;
  }

  /** Cycle the active hyper-plane XW -> YW -> ZW -> XW (part-05.md 5.4). */
  cycleHyperPlane(direction = 1) {
    const i = HYPER_PLANES.indexOf(this.activeHyperPlane);
    const n = HYPER_PLANES.length;
    this.activeHyperPlane = HYPER_PLANES[(i + direction + n) % n];
    return this.activeHyperPlane;
  }

  /** Undo one recorded rotation. Returns true if there was something to undo. */
  undo() {
    const previous = this.history.pop();
    if (!previous) return false;
    this.Q = previous;
    return true;
  }

  /** Back to the canonical view: Q = identity (part-03.md 3.6.3). */
  reset() {
    this.pushHistory();
    this.Q = identity4();
    return this;
  }

  /** Move the pivot, for example onto a newly focused node. */
  setPivot(x, y, z, w) {
    this.pivot[0] = x; this.pivot[1] = y; this.pivot[2] = z; this.pivot[3] = w;
    return this;
  }

  /**
   * Rotate ONE 4D point into the current view basis.
   *   p_rotated = Q * (p - pivot) + pivot
   * out must be a length-4 array; it is written in place and returned, so that
   * the render loop can run without allocating (bible/part-04.md).
   */
  rotatePoint(p, out) {
    const Q = this.Q, pv = this.pivot;
    const dx = p[0] - pv[0], dy = p[1] - pv[1], dz = p[2] - pv[2], dw = p[3] - pv[3];
    for (let r = 0; r < 4; r++) {
      out[r] = Q[0 * 4 + r] * dx + Q[1 * 4 + r] * dy + Q[2 * 4 + r] * dz + Q[3 * 4 + r] * dw + pv[r];
    }
    return out;
  }

  /**
   * THE ONE PROJECTION PASS. Read this comment before changing anything here.
   *
   * bible/part-03.md 3.7.4 and part-05.md 5.9.1 make this a red-letter rule:
   * the 4D-to-3D projection is computed ONCE per frame, producing ONE 3D scene,
   * which the VR compositor then draws twice, once per eye. It is very tempting
   * to "improve" stereo by projecting separately for the left and right eye.
   * That produces disparity no human brain can fuse, and it makes people sick.
   * One pass. Both eyes consume the same result. Always.
   *
   * Inputs
   *   points4  Float32Array or Float64Array of length 4 * n: x,y,z,w per node.
   *   out3     Float32Array of length 3 * n, filled with the projected 3D
   *            positions.
   *   outW     Float32Array of length n, filled with each node's ROTATED w.
   *            The slab, the stems and the wrist gauge all need the rotated w,
   *            never the stored w.
   *   outScale Float32Array of length n, filled with the projection scale s.
   *            The renderer multiplies the node's base radius by s, and that
   *            is the ONLY thing allowed to set node size (part-03.md 3.7.5).
   *
   * Returns the number of nodes processed.
   */
  projectAll(points4, out3, outW, outScale) {
    const n = points4.length / 4;
    const Q = this.Q, pv = this.pivot;
    const d = this.eyeDistance;
    const numerator = d - W_MIN;
    // Pull the sixteen matrix entries into locals: this loop is the hottest
    // code in the whole site and property lookups inside it are not free.
    const q00 = Q[0], q10 = Q[1], q20 = Q[2], q30 = Q[3];
    const q01 = Q[4], q11 = Q[5], q21 = Q[6], q31 = Q[7];
    const q02 = Q[8], q12 = Q[9], q22 = Q[10], q32 = Q[11];
    const q03 = Q[12], q13 = Q[13], q23 = Q[14], q33 = Q[15];
    const pvx = pv[0], pvy = pv[1], pvz = pv[2], pvw = pv[3];

    for (let i = 0; i < n; i++) {
      const b = i * 4;
      const dx = points4[b] - pvx;
      const dy = points4[b + 1] - pvy;
      const dz = points4[b + 2] - pvz;
      const dw = points4[b + 3] - pvw;

      const x = q00 * dx + q01 * dy + q02 * dz + q03 * dw + pvx;
      const y = q10 * dx + q11 * dy + q12 * dz + q13 * dw + pvy;
      const z = q20 * dx + q21 * dy + q22 * dz + q23 * dw + pvz;
      const w = q30 * dx + q31 * dy + q32 * dz + q33 * dw + pvw;

      const s = numerator / (d - w);
      const o = i * 3;
      out3[o] = x * s;
      out3[o + 1] = y * s;
      out3[o + 2] = z * s;
      outW[i] = w;
      outScale[i] = s;
    }
    this.projectionCount++;
    return n;
  }
}


// -----------------------------------------------------------------------------
// THE SLAB (SLICE MODE)
// -----------------------------------------------------------------------------

/**
 * How visible a node is, given its rotated w and the slab the reader is
 * currently looking at (bible/part-05.md 5.2, mode 1).
 *
 * Returns a number from 0 to 1:
 *   1.0        the node is inside the slab, fully solid
 *   0 to 1     the node is in the ghost band just outside the slab, and the
 *              renderer draws it as a faint wireframe ghost
 *   0.0        the node is beyond the ghost band
 *
 * The ghost band exists because of a red-letter rule: NOTHING VANISHES WITHOUT
 * A TRACE (part-05.md 5.9.4). A reader must always be able to see that more
 * world exists in the direction they have not swum yet. "My article
 * disappeared" is a design failure, not a user error.
 */
export function slabVisibility(w, w0, epsilon) {
  const distance = Math.abs(w - w0);
  const half = epsilon * 0.5;
  if (distance <= half) return 1;
  const ghost = distance - half;
  if (ghost >= epsilon) return 0;
  // Linear fade across the ghost band, strongest nearest the slab.
  return 1 - (ghost / epsilon);
}
