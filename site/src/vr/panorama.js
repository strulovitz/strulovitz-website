/*
================================================================================
 panorama.js  --  THE SCENE: HOLOTABLE, NODES, EDGES, STEMS, TESSERACT
================================================================================

 Owned by: bible/part-04.md (rendering discipline) and bible/part-05.md 5.1 to
 5.3 (the holotable and the non-colour cues for the fourth dimension).

 This file knows about three.js. It does NOT know about mice, controllers, or
 WebXR: it is handed a View4D from fourd.js plus the fake data, and its whole
 job is to turn numbers into a picture, once per frame.

 THE FOUR RULES BURNED INTO THIS FILE

 1. ONE PROJECTION PER FRAME. update() calls view.projectAll exactly once and
    both eyes of the headset then draw that same 3D result. Projecting once per
    eye would create a disparity no human brain can fuse and would make people
    sick (bible/part-03.md 3.7.4, part-05.md 5.9.1). There is a debug assert
    for this at the bottom of the file.

 2. SIZE COMES ONLY FROM THE PROJECTION. A node's drawn radius is its base
    radius times the projection scale s, and nothing else ever multiplies it
    (part-03.md 3.7.5). Importance will be shown by glow rings later, never by
    size.

 3. THE FOURTH DIMENSION IS NEVER A COLOUR (LAW 2). Colour here is cluster
    identity, fixed forever. The fourth dimension is made visible by size,
    by the dithered slab, by ghosts, by drop-stems over a fixed floor grid, and
    by the wrist gauge. Search this file for "colour" and you will find it read
    from the data and never computed from w.

 4. NOTHING VANISHES WITHOUT A TRACE. Nodes outside the slab do not disappear;
    they fade through a ghost band so the reader can always see that more world
    exists in the direction they have not swum yet (part-05.md 5.9.4).

 5. THE ROOM NEVER MOVES. Everything the reader can rotate lives inside the
    group called `graph`. The floor, the horizon and the table are outside it
    and never rotate, because a stable peripheral rest frame is the single
    strongest defence against nausea (part-05.md 5.1.2).
================================================================================
*/

import * as THREE from '../../vendor/three.module.min.js';
import { View4D, slabVisibility, PLANES } from '../lib/fourd.js';
import { CLUSTERS, W_BANDS, wHistogram } from '../scenes/synthetic.js';

// How big the graph is in the real world. bible/part-05.md 5.1.1: about 1.6
// metres across, at comfortable chest height, a bit over a metre in front of
// the reader when the session starts.
const GRAPH_DIAMETER = 1.6;
// The Bible fixes the graph at about 1.6 metres across, centred at chest
// height. A 1.6 metre ball centred at 1.3 metres reaches down to half a metre,
// so the table has to sit LOW, at about knee height, for the object to float
// ABOVE it as promised rather than being skewered by it. The reader looks
// slightly down into the whole thing, which is also the friendliest posture.
const TABLE_HEIGHT = 0.45;
const GRAPH_CENTRE_HEIGHT = 1.30;
const GRAPH_DISTANCE = 1.15;

// The slab: how thick the slice of the world is that reads as fully solid.
export const DEFAULT_EPSILON = 0.25;
// In projection mode the slab opens up to swallow the whole world at once.
const PROJECTION_EPSILON = 4.0;
// bible/part-05.md 5.2 mode 2 item 1: the two modes cross over in 600 ms.
const MODE_TRANSITION_MS = 600;

// How many nodes may drop a stem to the floor. A budget, per part-04.md.
const MAX_STEMS = 300;


/**
 * A screen-door dither, patched into whatever standard material we use.
 *
 * Why dithering instead of ordinary transparency: transparent objects must be
 * sorted back to front every frame or they draw over each other wrongly, and
 * with hundreds of moving nodes in a headset that sorting is both slow and
 * unstable (nodes flicker in front of each other). A dither throws away a
 * fraction of the PIXELS instead of blending, so it needs no sorting at all,
 * costs nothing, and reads to the eye as a fade. This is what
 * bible/part-04.md 4.4.5 means by "dithered alpha".
 *
 * The pattern is fixed to the pixel grid, so it does not crawl or shimmer.
 */
function makeDitheredMaterial(baseMaterial) {
  baseMaterial.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>
        attribute float aVisibility;
        varying float vVisibility;`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>
        vVisibility = aVisibility;`);

    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', `#include <common>
        varying float vVisibility;
        // The classic compact ordered dither. Bayer2 gives a 2x2 pattern and
        // nesting it gives the familiar 4x4 one, without needing arrays.
        float panoramaBayer2(vec2 a) { a = floor(a); return fract(a.x / 2.0 + a.y * a.y * 0.75); }
        float panoramaBayer4(vec2 a) { return panoramaBayer2(0.5 * a) * 0.25 + panoramaBayer2(a); }`)
      .replace('#include <clipping_planes_fragment>', `
        if (vVisibility < 0.999) {
          if (vVisibility <= 0.001) discard;
          if (panoramaBayer4(gl_FragCoord.xy) > vVisibility) discard;
        }
        #include <clipping_planes_fragment>`);
  };
  // Changing onBeforeCompile means three.js must be told the program is new.
  baseMaterial.customProgramCacheKey = () => 'panorama-dither-v1';
  return baseMaterial;
}


/**
 * One instanced mesh of identical little shapes, with a per-instance colour and
 * a per-instance visibility. Used for nodes, for edges and for stems, because
 * drawing a thousand separate objects would blow the draw-call budget
 * (bible/part-04.md: under one hundred draw calls) while drawing a thousand
 * COPIES of one object costs a single call.
 */
export class InstancedSet {
  constructor(geometry, capacity, options = {}) {
    // A per-instance colour only reaches the picture if the material has
    // vertexColors switched on, and switching that on makes the shader read a
    // per-VERTEX colour attribute as well. A geometry without one multiplies
    // everything by zero and every instance comes out pure black. So give the
    // geometry a white vertex colour once, here, and never think about it again.
    // (This cost an hour and a screenshot full of black dots. Leave it in.)
    if (!geometry.getAttribute('color')) {
      const vertexCount = geometry.getAttribute('position').count;
      geometry.setAttribute('color',
        new THREE.BufferAttribute(new Float32Array(vertexCount * 3).fill(1), 3));
    }
    const material = makeDitheredMaterial(new THREE.MeshLambertMaterial({
      vertexColors: true,
      emissive: options.emissive ?? 0x000000,
      side: THREE.FrontSide,
    }));
    this.mesh = new THREE.InstancedMesh(geometry, material, capacity);
    this.mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    this.mesh.frustumCulled = false;
    this.capacity = capacity;

    this.visibility = new Float32Array(capacity).fill(1);
    this.visibilityAttribute = new THREE.InstancedBufferAttribute(this.visibility, 1);
    this.visibilityAttribute.setUsage(THREE.DynamicDrawUsage);
    geometry.setAttribute('aVisibility', this.visibilityAttribute);

    this.mesh.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(capacity * 3).fill(1), 3);
    this.mesh.instanceColor.setUsage(THREE.DynamicDrawUsage);

    // Scratch objects reused every frame. Allocating inside a render loop is
    // what causes the garbage-collector stutters that a headset shows as a
    // jolt (bible/part-04.md: zero-allocation loop).
    this.scratchMatrix = new THREE.Matrix4();
    this.scratchPosition = new THREE.Vector3();
    this.scratchQuaternion = new THREE.Quaternion();
    this.scratchScale = new THREE.Vector3();
    this.scratchFrom = new THREE.Vector3();
    this.scratchTo = new THREE.Vector3();
    this.scratchDirection = new THREE.Vector3();
    this.used = 0;
  }

  setColour(index, r, g, b) {
    const a = this.mesh.instanceColor.array;
    a[index * 3] = r; a[index * 3 + 1] = g; a[index * 3 + 2] = b;
  }

  /** Place a sphere-like instance at a point with a uniform size. */
  placePoint(index, x, y, z, size, visible) {
    this.scratchPosition.set(x, y, z);
    this.scratchQuaternion.identity();
    this.scratchScale.set(size, size, size);
    this.scratchMatrix.compose(this.scratchPosition, this.scratchQuaternion, this.scratchScale);
    this.mesh.setMatrixAt(index, this.scratchMatrix);
    this.visibility[index] = visible;
  }

  /**
   * Stretch a cylinder instance so that it runs from one point to another.
   * The base geometry is a unit-height cylinder pointing up the y axis, so we
   * rotate "up" onto the direction we want and scale its height to the length.
   */
  placeSegment(index, ax, ay, az, bx, by, bz, thickness, visible) {
    this.scratchFrom.set(ax, ay, az);
    this.scratchTo.set(bx, by, bz);
    this.scratchDirection.subVectors(this.scratchTo, this.scratchFrom);
    const length = this.scratchDirection.length();
    if (length < 1e-6) {
      this.visibility[index] = 0;
      return;
    }
    this.scratchPosition.addVectors(this.scratchFrom, this.scratchTo).multiplyScalar(0.5);
    this.scratchDirection.divideScalar(length);
    this.scratchQuaternion.setFromUnitVectors(UP, this.scratchDirection);
    this.scratchScale.set(thickness, length, thickness);
    this.scratchMatrix.compose(this.scratchPosition, this.scratchQuaternion, this.scratchScale);
    this.mesh.setMatrixAt(index, this.scratchMatrix);
    this.visibility[index] = visible;
  }

  hide(index) { this.visibility[index] = 0; }

  finish(count) {
    this.mesh.count = count;
    this.mesh.instanceMatrix.needsUpdate = true;
    this.mesh.instanceColor.needsUpdate = true;
    this.visibilityAttribute.needsUpdate = true;
  }
}

const UP = new THREE.Vector3(0, 1, 0);


/**
 * The whole scene. Construct it once, then call update() every frame.
 */
export class Panorama {
  constructor(data, options = {}) {
    this.data = data;
    this.view = new View4D();

    // ---- Reader state that belongs to the interaction, not to the maths ----
    this.mode = 'slice';                  // 'slice' or 'projection'
    // WHERE THE SLAB STARTS, AND WHY IT IS NOT ALWAYS ZERO.
    // A reader must never arrive to an empty world. In the placeholder world
    // content was spread evenly and zero was the sensible middle; in a real
    // young magazine almost everything is either brand-new news or an
    // encyclopedia entry, and w = 0 is the empty gap BETWEEN them. So home is
    // the busiest place in the fourth dimension, computed from the data itself.
    // A SCENE DECIDES ITS OWN HOME. The placeholder world documents that a
    // reader starts among the established news at zero (bible/part-03.md 3.5),
    // and that is left exactly as it was. A real edition supplies its own home,
    // which is wherever its content actually is.
    this.bands = data.bands || W_BANDS;
    this.homeW = (typeof data.homeW === 'number') ? data.homeW : 0;
    this.w0 = this.homeW;                 // where the slab sits, part-05.md 5.2
    this.epsilon = DEFAULT_EPSILON;       // how thick the slab is
    this.targetEpsilon = DEFAULT_EPSILON;
    this.showTesseract = true;
    this.showGraph = true;
    this.hoveredNode = -1;
    this.focusedNode = -1;
    this.idleMilliseconds = 0;
    this.wobbleEnabled = true;
    this.stemsEnabled = true;

    // ---- Scratch arrays for the one projection pass ----
    const n = data.count;
    this.out3 = new Float32Array(n * 3);
    this.outW = new Float32Array(n);
    this.outScale = new Float32Array(n);
    this.nodeVisibility = new Float32Array(n);

    const t = data.tesseract;
    this.tesseractPoints4 = new Float64Array(t.vertices.length * 4);
    t.vertices.forEach((v, i) => {
      this.tesseractPoints4[i * 4] = v[0];
      this.tesseractPoints4[i * 4 + 1] = v[1];
      this.tesseractPoints4[i * 4 + 2] = v[2];
      this.tesseractPoints4[i * 4 + 3] = v[3];
    });
    this.tesseractOut3 = new Float32Array(t.vertices.length * 3);
    this.tesseractOutW = new Float32Array(t.vertices.length);
    this.tesseractOutScale = new Float32Array(t.vertices.length);

    this.histogram = wHistogram(data.points4, data.count);

    // ---- The three.js side ----
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x07090f);
    this.buildRoom();
    this.buildGraphObjects();

    // Extra four-dimensional objects that something else owns -- the gym's
    // toys, for instance. They are projected inside the SAME pass as everything
    // else, in this file, so that nobody can accidentally start projecting
    // somewhere else and break the one-projection rule (part-05.md 5.9.1).
    this.extraSets = new Map();

    // Counters used by the debug assert of the one-projection rule.
    this.projectionsThisFrame = 0;
    this.expectedProjections = 2;
    this.projectionRuleViolated = false;
  }

  // ---------------------------------------------------------------------------
  // THE ROOM. Never rotates. Gives the eye something still to hold on to.
  // ---------------------------------------------------------------------------
  buildRoom() {
    this.scene.add(new THREE.HemisphereLight(0xbfd4ff, 0x1a1a22, 1.15));
    const key = new THREE.DirectionalLight(0xffffff, 1.4);
    key.position.set(1.4, 2.6, 1.6);
    this.scene.add(key);
    const fill = new THREE.DirectionalLight(0x88aaff, 0.5);
    fill.position.set(-1.6, 0.8, -1.4);
    this.scene.add(fill);

    // The floor. A grid whose CELL SIZE NEVER CHANGES, which is exactly what
    // makes the drop-stems informative: a node that is big because it is near
    // in z sits over a near grid cell, while a node that is big because its w
    // is high sits over a far cell. The mismatch is the cue
    // (bible/part-05.md 5.3.3).
    const floor = new THREE.GridHelper(8, 40, 0x2a3550, 0x161d2e);
    floor.position.y = 0;
    this.scene.add(floor);

    // A distant horizon ring: a fixed landmark for the eye, so peripheral
    // vision always has something stationary in it.
    const horizon = new THREE.Mesh(
      new THREE.TorusGeometry(7.5, 0.02, 6, 96),
      new THREE.MeshBasicMaterial({ color: 0x24304a })
    );
    horizon.rotation.x = Math.PI / 2;
    horizon.position.y = 0.6;
    this.scene.add(horizon);

    // The holotable itself: the surface the shadows and stems land on.
    this.table = new THREE.Mesh(
      new THREE.CylinderGeometry(GRAPH_DIAMETER * 0.62, GRAPH_DIAMETER * 0.66, 0.035, 48),
      new THREE.MeshLambertMaterial({ color: 0x161c2b })
    );
    this.table.position.set(0, TABLE_HEIGHT, -GRAPH_DISTANCE);
    this.scene.add(this.table);

    const rim = new THREE.Mesh(
      new THREE.TorusGeometry(GRAPH_DIAMETER * 0.63, 0.008, 8, 72),
      new THREE.MeshBasicMaterial({ color: 0x3d5680 })
    );
    rim.rotation.x = Math.PI / 2;
    rim.position.set(0, TABLE_HEIGHT + 0.019, -GRAPH_DISTANCE);
    this.scene.add(rim);

    // The table's own fixed grid, drawn small and tight on its surface.
    const tableGrid = new THREE.GridHelper(GRAPH_DIAMETER, 16, 0x2b3a5c, 0x1d2740);
    tableGrid.position.set(0, TABLE_HEIGHT + 0.02, -GRAPH_DISTANCE);
    this.scene.add(tableGrid);
    this.tableTop = TABLE_HEIGHT + 0.02;
  }

  // ---------------------------------------------------------------------------
  // THE GRAPH. Everything inside this group is what the reader rotates.
  // ---------------------------------------------------------------------------
  buildGraphObjects() {
    this.graph = new THREE.Group();
    // The maths works in a box from -1 to +1, so half the graph diameter is
    // the right scale factor to turn maths units into metres.
    this.graph.scale.setScalar(GRAPH_DIAMETER / 2);
    this.graph.position.set(0, GRAPH_CENTRE_HEIGHT, -GRAPH_DISTANCE);
    this.scene.add(this.graph);

    const n = this.data.count;

    // Nodes. Low-detail spheres: at the size these appear, nobody will ever
    // count the facets, and the triangle budget is precious in a headset.
    this.nodes = new InstancedSet(new THREE.IcosahedronGeometry(1, 1), n, { emissive: 0x000000 });
    for (let i = 0; i < n; i++) {
      this.nodes.setColour(i, this.data.colours[i * 3], this.data.colours[i * 3 + 1], this.data.colours[i * 3 + 2]);
    }
    this.graph.add(this.nodes.mesh);

    // Edges as thin ROUND RIBBONS, never one-pixel lines: a one-pixel line in
    // a headset shimmers and breaks up, and reads as a rendering fault
    // (bible/part-03.md 3.4.2).
    const edgeCount = this.data.edges.length / 2;
    this.edges = new InstancedSet(new THREE.CylinderGeometry(1, 1, 1, 5, 1, true), edgeCount);
    for (let e = 0; e < edgeCount; e++) {
      const a = this.data.edges[e * 2];
      this.edges.setColour(e,
        this.data.colours[a * 3] * 0.38,
        this.data.colours[a * 3 + 1] * 0.38,
        this.data.colours[a * 3 + 2] * 0.38);
    }
    this.graph.add(this.edges.mesh);

    // Drop-stems and their shadow dots on the table. These live OUTSIDE the
    // graph group, in room space, because a stem must always hang straight
    // down to the real floor no matter how the graph is rotated. That is the
    // whole point of the cue.
    this.stems = new InstancedSet(new THREE.CylinderGeometry(1, 1, 1, 4, 1, true), MAX_STEMS);
    // The shadow dot geometry is laid flat ONCE, at construction, rather than
    // rotating the whole instanced mesh. That way every instance position below
    // is a plain room-space point and needs no mental gymnastics to read.
    const shadowGeometry = new THREE.CircleGeometry(1, 10);
    shadowGeometry.rotateX(-Math.PI / 2);
    this.shadows = new InstancedSet(shadowGeometry, MAX_STEMS);
    for (let i = 0; i < MAX_STEMS; i++) {
      this.stems.setColour(i, 0.20, 0.27, 0.40);
      this.shadows.setColour(i, 0.22, 0.30, 0.45);
    }
    this.scene.add(this.stems.mesh);
    this.scene.add(this.shadows.mesh);

    // The tesseract: sixteen corner beads and thirty-two edges.
    // NIR, 2026-09-03: "half as bright as it is now" in the real pages (this
    // file); the gym/tutorial keeps its own brighter tesseract in wgym.js.
    // Every colour and emissive value below is exactly half of what it was.
    const t = this.data.tesseract;
    this.tesseractNodes = new InstancedSet(new THREE.IcosahedronGeometry(1, 1), t.vertices.length, { emissive: 0x080c10 });
    for (let i = 0; i < t.vertices.length; i++) this.tesseractNodes.setColour(i, 0.48, 0.47, 0.40);
    this.tesseractEdges = new InstancedSet(new THREE.CylinderGeometry(1, 1, 1, 6, 1, true), t.edges.length, { emissive: 0x050a10 });
    for (let e = 0; e < t.edges.length; e++) this.tesseractEdges.setColour(e, 0.41, 0.43, 0.31);
    this.graph.add(this.tesseractNodes.mesh);
    this.graph.add(this.tesseractEdges.mesh);

    // Cluster labels. Text is the ONE thing exempt from the projection size
    // cue, because shimmering, resizing text is unreadable
    // (bible/part-05.md 5.3.6). So these sprites keep a constant angular size.
    // The regions are named by the SCENE, not by this file. A real edition
    // names them with the tags that model chose for itself, so the floating
    // words over a galaxy are that editor's own vocabulary; the placeholder
    // world supplies its eight invented categories instead.
    this.labels = [];
    for (const cluster of (this.data.clusters || CLUSTERS)) {
      const sprite = makeTextSprite(cluster.label, cluster.colour);
      this.graph.add(sprite);
      this.labels.push({ sprite, cluster });
    }
  }

  // ---------------------------------------------------------------------------
  // EXTRA FOUR-DIMENSIONAL OBJECTS
  // ---------------------------------------------------------------------------

  /**
   * Hand a set of 4D points to the scene so they get rotated and projected with
   * everything else. Returns the arrays that will hold the results, which the
   * caller reads after update() has run.
   */
  registerPointSet(name, points4) {
    const count = points4.length / 4;
    const entry = {
      points4,
      out3: new Float32Array(count * 3),
      outW: new Float32Array(count),
      outScale: new Float32Array(count),
      count,
    };
    this.extraSets.set(name, entry);
    this.expectedProjections = 2 + this.extraSets.size;
    return entry;
  }

  unregisterPointSet(name) {
    this.extraSets.delete(name);
    this.expectedProjections = 2 + this.extraSets.size;
  }

  // ---------------------------------------------------------------------------
  // MODES
  // ---------------------------------------------------------------------------

  /** Switch between the calm slice mode and the whole-structure awe mode. */
  setMode(mode) {
    this.mode = mode;
    this.targetEpsilon = mode === 'projection' ? PROJECTION_EPSILON : DEFAULT_EPSILON;
    this.noteInput();
    return this.mode;
  }

  toggleMode() {
    return this.setMode(this.mode === 'slice' ? 'projection' : 'slice');
  }

  /** Move the slab through the fourth dimension. The MRI-scanner gesture. */
  swim(delta) {
    this.w0 = Math.max(-1.2, Math.min(1.2, this.w0 + delta));
    this.noteInput();
  }

  /** Any input at all pauses the idle wobble (bible/part-05.md 5.2 item 4). */
  noteInput() { this.idleMilliseconds = 0; }

  /** Back to the canonical view AND the home slab, as one act. */
  resetView() {
    this.view.reset();
    this.w0 = this.homeW;
    this.setMode('slice');
    this.noteInput();
  }

  // ---------------------------------------------------------------------------
  // THE FRAME
  // ---------------------------------------------------------------------------

  /**
   * Called once per rendered frame. deltaMs is real elapsed milliseconds.
   *
   * The order here matters and is worth reading: first the slab animates
   * toward its target thickness, then the idle wobble may nudge the rotation,
   * then ONE projection pass turns 4D into 3D, and only then does anything get
   * written into the picture. Nothing after the projection is allowed to touch
   * the fourth dimension again.
   */
  update(deltaMs) {
    // 1. The slab eases toward its target, so switching modes is a 600 ms
    //    swell rather than a jump-cut (part-05.md 5.2 mode 2 item 1).
    if (this.epsilon !== this.targetEpsilon) {
      const step = (PROJECTION_EPSILON - DEFAULT_EPSILON) * (deltaMs / MODE_TRANSITION_MS);
      if (this.epsilon < this.targetEpsilon) {
        this.epsilon = Math.min(this.targetEpsilon, this.epsilon + step);
      } else {
        this.epsilon = Math.max(this.targetEpsilon, this.epsilon - step);
      }
    }

    // 2. The idle wobble. A completely still 4D projection is indistinguishable
    //    from a strange 3D object, so after five quiet seconds in projection
    //    mode we add a tiny slow oscillation in the XW plane. Under two degrees
    //    of amplitude: enough for the brain to read the extra dimension from
    //    motion parallax, far too small to disturb anyone
    //    (bible/part-05.md 5.2 mode 2 item 4).
    this.idleMilliseconds += deltaMs;
    if (this.wobbleEnabled && this.mode === 'projection' && this.idleMilliseconds > 5000) {
      const seconds = this.idleMilliseconds / 1000;
      const amplitudeRadians = THREE.MathUtils.degToRad(1.6);
      const rate = amplitudeRadians * Math.cos(seconds * 0.9) * 0.9;
      this.view.rotate('xw', rate * (deltaMs / 1000));
    }

    // 3. THE ONE PROJECTION PASS for the graph, and one for the tesseract.
    //    Both eyes of the headset consume these same numbers.
    const before = this.view.projectionCount;
    this.view.projectAll(this.data.points4, this.out3, this.outW, this.outScale);
    this.view.projectAll(this.tesseractPoints4, this.tesseractOut3, this.tesseractOutW, this.tesseractOutScale);
    for (const set of this.extraSets.values()) {
      this.view.projectAll(set.points4, set.out3, set.outW, set.outScale);
    }
    this.projectionsThisFrame = this.view.projectionCount - before;

    // 4. Turn the numbers into the picture.
    this.updateNodes();
    this.updateEdges();
    this.updateStems();
    this.updateTesseract();
    this.updateLabels();
  }

  updateNodes() {
    const n = this.data.count;
    if (!this.showGraph) { this.nodes.finish(0); return; }
    for (let i = 0; i < n; i++) {
      const visible = slabVisibility(this.outW[i], this.w0, this.epsilon);
      this.nodeVisibility[i] = visible;
      if (visible <= 0) { this.nodes.hide(i); continue; }
      // RADIUS = BASE RADIUS TIMES THE PROJECTION SCALE, AND NOTHING ELSE.
      let size = this.data.radii[i] * this.outScale[i];
      // The hovered and focused nodes are marked by BRIGHTNESS, not by size,
      // so that size never lies about the fourth dimension.
      const highlighted = (i === this.hoveredNode || i === this.focusedNode);
      this.nodes.placePoint(i, this.out3[i * 3], this.out3[i * 3 + 1], this.out3[i * 3 + 2],
        size, visible);
      const boost = highlighted ? 2.2 : 1;
      this.nodes.setColour(i,
        Math.min(1, this.data.colours[i * 3] * boost),
        Math.min(1, this.data.colours[i * 3 + 1] * boost),
        Math.min(1, this.data.colours[i * 3 + 2] * boost));
    }
    this.nodes.finish(n);
  }

  updateEdges() {
    const count = this.data.edges.length / 2;
    if (!this.showGraph) { this.edges.finish(0); return; }
    for (let e = 0; e < count; e++) {
      const a = this.data.edges[e * 2];
      const b = this.data.edges[e * 2 + 1];
      // An edge is only as visible as its dimmer end, so edges fade out of the
      // slab together with the nodes they join.
      const visible = Math.min(this.nodeVisibility[a], this.nodeVisibility[b]);
      if (visible <= 0.01) { this.edges.hide(e); continue; }
      const thickness = 0.0022 * (this.outScale[a] + this.outScale[b]) * 0.5;
      this.edges.placeSegment(e,
        this.out3[a * 3], this.out3[a * 3 + 1], this.out3[a * 3 + 2],
        this.out3[b * 3], this.out3[b * 3 + 1], this.out3[b * 3 + 2],
        thickness, visible);
    }
    this.edges.finish(count);
  }

  /**
   * Drop-stems. These are computed in ROOM space, not graph space, because the
   * stem must hang vertically to the real table however the graph is turned.
   * Only the most visible few hundred nodes get one, per the budget.
   */
  updateStems() {
    if (!this.stemsEnabled || !this.showGraph) {
      this.stems.finish(0); this.shadows.finish(0); return;
    }
    const scale = this.graph.scale.x;
    const originX = this.graph.position.x;
    const originY = this.graph.position.y;
    const originZ = this.graph.position.z;
    let used = 0;
    for (let i = 0; i < this.data.count && used < MAX_STEMS; i++) {
      const visible = this.nodeVisibility[i];
      if (visible < 0.5) continue;   // only solid nodes get a stem
      const x = originX + this.out3[i * 3] * scale;
      const y = originY + this.out3[i * 3 + 1] * scale;
      const z = originZ + this.out3[i * 3 + 2] * scale;
      if (y <= this.tableTop + 0.004) continue;
      this.stems.placeSegment(used, x, this.tableTop, z, x, y, z, 0.0011, 1);
      this.shadows.placePoint(used, x, this.tableTop + 0.0015, z, 0.006 * this.outScale[i], 1);
      used++;
    }
    this.stems.finish(used);
    this.shadows.finish(used);
  }

  updateTesseract() {
    const t = this.data.tesseract;
    if (!this.showTesseract) {
      this.tesseractNodes.finish(0); this.tesseractEdges.finish(0); return;
    }
    const visibilityOf = new Array(t.vertices.length);
    for (let i = 0; i < t.vertices.length; i++) {
      // The tesseract is the teaching object, so it stays visible in slice mode
      // rather than being sliced away: it is the thing the reader is learning
      // to read. It still shows its w through size, stems and the gauge.
      // The tesseract is NOT sliced away. It is the object the reader is
      // learning to read, so it stays solid in both modes and shows its w
      // through size, stems and the wrist gauge instead of through fading.
      // Dithering it as well would turn it into a cloud of dots, which teaches
      // nobody anything.
      const visible = 1;
      visibilityOf[i] = visible;
      const size = 0.022 * this.tesseractOutScale[i];
      this.tesseractNodes.placePoint(i,
        this.tesseractOut3[i * 3], this.tesseractOut3[i * 3 + 1], this.tesseractOut3[i * 3 + 2],
        size, visible);
    }
    this.tesseractNodes.finish(t.vertices.length);

    for (let e = 0; e < t.edges.length; e++) {
      const [a, b] = t.edges[e];
      const visible = Math.min(visibilityOf[a], visibilityOf[b]);
      const thickness = 0.0055 * (this.tesseractOutScale[a] + this.tesseractOutScale[b]) * 0.5;
      this.tesseractEdges.placeSegment(e,
        this.tesseractOut3[a * 3], this.tesseractOut3[a * 3 + 1], this.tesseractOut3[a * 3 + 2],
        this.tesseractOut3[b * 3], this.tesseractOut3[b * 3 + 1], this.tesseractOut3[b * 3 + 2],
        thickness, visible);
    }
    this.tesseractEdges.finish(t.edges.length);
  }

  /**
   * Cluster labels sit at the average position of their members, so they follow
   * the rotation honestly, but their SIZE never changes.
   */
  updateLabels() {
    for (const entry of this.labels) entry.sum = [0, 0, 0, 0];
    for (let i = 0; i < this.data.count; i++) {
      if (this.nodeVisibility[i] < 0.5) continue;
      const entry = this.labels[this.data.clusterOf[i]];
      entry.sum[0] += this.out3[i * 3];
      entry.sum[1] += this.out3[i * 3 + 1];
      entry.sum[2] += this.out3[i * 3 + 2];
      entry.sum[3] += 1;
    }
    for (const entry of this.labels) {
      const count = entry.sum[3];
      if (count < 3 || !this.showGraph) { entry.sprite.visible = false; continue; }
      entry.sprite.visible = true;
      entry.sprite.position.set(
        entry.sum[0] / count,
        entry.sum[1] / count + 0.14,
        entry.sum[2] / count);
    }
  }

  /**
   * Which node is the reader pointing at? Works from the ALREADY PROJECTED
   * positions, so what you can point at is exactly what you can see. Picking
   * runs against nodes only, never edges (bible/part-05.md 5.5.1).
   *
   * The ray is given in room space. The assisted-aim cone is generous on
   * purpose: a human arm holding a controller at chest distance wobbles, and
   * fighting that wobble is what makes VR pointing feel bad.
   */
  pick(rayOrigin, rayDirection, coneRadians = 0.045) {
    const scale = this.graph.scale.x;
    let best = -1;
    let bestScore = Infinity;
    const ox = rayOrigin.x, oy = rayOrigin.y, oz = rayOrigin.z;
    const dx = rayDirection.x, dy = rayDirection.y, dz = rayDirection.z;
    for (let i = 0; i < this.data.count; i++) {
      if (this.nodeVisibility[i] < 0.35) continue;
      const px = this.graph.position.x + this.out3[i * 3] * scale - ox;
      const py = this.graph.position.y + this.out3[i * 3 + 1] * scale - oy;
      const pz = this.graph.position.z + this.out3[i * 3 + 2] * scale - oz;
      const along = px * dx + py * dy + pz * dz;
      if (along <= 0.05) continue;                       // behind the hand
      const distance = Math.hypot(px, py, pz);
      const sideways = Math.sqrt(Math.max(0, distance * distance - along * along));
      const allowed = coneRadians * along + this.data.radii[i] * this.outScale[i] * scale;
      if (sideways > allowed) continue;
      // Prefer the node nearest the centre of the ray, then the nearest one.
      const score = (sideways / allowed) * 2 + along * 0.1;
      if (score < bestScore) { bestScore = score; best = i; }
    }
    return best;
  }

  /**
   * Turn a projected 3D position from the maths' unit box into a real position
   * in the room, in metres. Used wherever something outside the graph group
   * needs to know where a node actually is: stems, labels, the pointing cursor.
   */
  toRoomSpace(out3, index, target) {
    const scale = this.graph.scale.x;
    target.set(
      this.graph.position.x + out3[index * 3] * scale,
      this.graph.position.y + out3[index * 3 + 1] * scale,
      this.graph.position.z + out3[index * 3 + 2] * scale);
    return target;
  }

  /** Facts for the debug HUD and for the wrist gauge. */
  status() {
    let solid = 0;
    for (let i = 0; i < this.data.count; i++) if (this.nodeVisibility[i] >= 0.999) solid++;
    return {
      mode: this.mode,
      w0: this.w0,
      epsilon: this.epsilon,
      hyperPlane: this.view.activeHyperPlane,
      solidNodes: solid,
      totalNodes: this.data.count,
      hovered: this.hoveredNode,
      focused: this.focusedNode,
      projectionsThisFrame: this.projectionsThisFrame,
      histogram: this.histogram,
      bandName: nearestBandName(this.w0, this.bands),
    };
  }
}


/**
 * Which named w band is the slab sitting in right now, in plain words.
 *
 * The bands can be supplied by the caller, because a real magazine of news and
 * explanations has different landmarks along the fourth dimension than the
 * placeholder world did. Without an argument it falls back to the placeholder
 * bands, so old callers keep working.
 */
export function nearestBandName(w0, bands = W_BANDS) {
  let best = bands[0];
  for (const band of bands) {
    if (Math.abs(band.w - w0) < Math.abs(best.w - w0)) best = band;
  }
  return best;
}


/**
 * A text label drawn onto a canvas and shown as a sprite that does NOT shrink
 * with distance. Crude but durable: no font files to load, no text-layout
 * library to rot in five years. bible/part-04.md wants a baked label atlas
 * eventually; this is the honest small version of that idea.
 */
export function makeTextSprite(text, colour = 0xffffff, options = {}) {
  const scale = options.scale ?? 0.055;
  // A single letter on a canvas eight times wider than it is tall comes out
  // tiny, because the sprite is stretched to that shape and the letter only
  // occupies a sliver of it. Short labels therefore get a square canvas.
  // (This is why Nir saw no letter F on the beads. Leave the option in.)
  const square = options.square ?? false;
  const canvas = document.createElement('canvas');
  canvas.width = square ? 256 : 1024;
  canvas.height = square ? 256 : 128;
  const context = canvas.getContext('2d');
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: texture,
    // sizeAttenuation false is the whole trick: constant angular size, so text
    // never shimmers or resizes as the projection scale changes (5.3.6).
    sizeAttenuation: false,
    depthWrite: false,
    transparent: true,
  }));
  sprite.scale.set(square ? scale : scale * 8, scale, 1);

  // The sprite can be re-lettered without building a new object, so that
  // messages in VR cost no allocation per frame.
  sprite.setText = (newText) => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = square ? 'bold 170px system-ui, sans-serif' : 'bold 60px system-ui, sans-serif';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    const width = context.measureText(newText).width + (square ? 40 : 48);
    const height = square ? 200 : 84;
    context.fillStyle = 'rgba(6, 8, 14, 0.78)';
    context.fillRect((canvas.width - width) / 2, (canvas.height - height) / 2, width, height);
    context.fillStyle = '#' + colour.toString(16).padStart(6, '0');
    context.fillText(newText, canvas.width / 2, canvas.height / 2);
    texture.needsUpdate = true;
  };
  sprite.setText(text);
  return sprite;
}
