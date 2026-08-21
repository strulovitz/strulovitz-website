/*
================================================================================
 main.js  --  THE TWO BODIES: MOUSE AND KEYBOARD, AND THE QUEST 3
================================================================================

 Owned by: bible/part-05.md, section 5.4 (rotation controls, Tier 1), 5.2
 (the two modes), 5.5 (pointing and hovering) and 5.8 (the flat-screen
 mappings).

 LAW 1 in one sentence: nothing ships without its VR version. So this file has
 exactly one state machine, driven by two different bodies. The mouse and the
 controllers touch the SAME Panorama object and the SAME View4D matrix, which
 is why a link shared from a laptop opens the identical sight in a headset.

 THE COMFORT PROMISES THIS FILE KEEPS (bible/part-05.md 5.1.4 and 5.9)

 1. The reader is never moved. The room is fixed; the graph is what turns. The
    only thing that ever moves the camera is the reader's own neck.
 2. Analog rotation is capped at 25 degrees per second. Snap rotations take
    300 milliseconds with an ease in and out.
 3. There is NO rotational inertia. Motion stops the instant input stops.
    Drifting geometry is nauseating and is forbidden.
 4. Every gesture is reversible: undo covers rotation, reset covers everything,
    and both are on the first ring of the hand menu.
================================================================================
*/

import * as THREE from '../../vendor/three.module.min.js';
import { Panorama, makeTextSprite, nearestBandName } from './panorama.js';
import { buildSyntheticScene, W_BANDS } from '../scenes/synthetic.js';
import { HYPER_PLANES } from '../lib/fourd.js';

// bible/part-05.md 5.1.4: the comfort cap, in degrees per second.
const MAX_ROTATION_DEGREES_PER_SECOND = 25;
const SNAP_MILLISECONDS = 300;
// A full sweep of the slab through the whole fourth dimension takes about four
// seconds, so that swimming feels like a deliberate journey (5.2.3).
const SWIM_UNITS_PER_SECOND = 0.5;

const debugRequested = new URLSearchParams(location.search).has('debug');

// -----------------------------------------------------------------------------
// SET UP THE PICTURE
// -----------------------------------------------------------------------------

const data = buildSyntheticScene(200);
const panorama = new Panorama(data);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.xr.enabled = true;
// 72 frames per second is the Quest 3 target that bible/part-04.md demands.
renderer.xr.setFramerate?.(72);
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.05, 60);
// On a flat screen the reader needs to see the WHOLE object, so the camera
// stands further back than a person would stand at the real table. In VR this
// camera is ignored entirely: there, the reader's own head is the camera, and
// the holotable is placed at the distance a real table would be.
camera.position.set(0, 1.48, 1.75);
camera.lookAt(0, 1.24, -1.15);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// -----------------------------------------------------------------------------
// SNAP ROTATIONS: THE ONE ANIMATION ALLOWED TO RUN BY ITSELF
// -----------------------------------------------------------------------------

// A snap is a 90 degree turn in a plane, eased over 300 ms. It is stored as a
// little bit of state rather than a timer, so it cannot outlive the frame loop
// and it stops instantly if the view is reset.
let snap = null;

function startSnap(plane, direction) {
  if (snap) return;                        // one snap at a time, no queueing
  panorama.view.pushHistory();             // a snap is a deliberate act, so undo covers it
  snap = { plane, remaining: (Math.PI / 2) * direction, elapsed: 0, total: SNAP_MILLISECONDS };
  panorama.noteInput();
}

function advanceSnap(deltaMs) {
  if (!snap) return;
  const before = easeInOut(Math.min(1, snap.elapsed / snap.total));
  snap.elapsed += deltaMs;
  const after = easeInOut(Math.min(1, snap.elapsed / snap.total));
  const fraction = after - before;
  panorama.view.rotate(snap.plane, snap.remaining * fraction);
  if (snap.elapsed >= snap.total) snap = null;
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

/** Rotate under the comfort cap. Returns the angle actually applied. */
function rotateCapped(plane, requestedRadians, deltaMs) {
  const maximum = THREE.MathUtils.degToRad(MAX_ROTATION_DEGREES_PER_SECOND) * (deltaMs / 1000);
  const clamped = Math.max(-maximum, Math.min(maximum, requestedRadians));
  if (clamped !== 0) {
    panorama.view.rotate(plane, clamped);
    panorama.noteInput();
  }
  return clamped;
}


// =============================================================================
// BODY ONE: MOUSE AND KEYBOARD (bible/part-05.md 5.8)
// =============================================================================

const pointer = { x: 0, y: 0, insideWindow: false };
let dragging = null;

renderer.domElement.addEventListener('pointerdown', (event) => {
  renderer.domElement.setPointerCapture(event.pointerId);
  dragging = {
    button: event.button,
    shift: event.shiftKey,
    lastX: event.clientX,
    lastY: event.clientY,
  };
});

renderer.domElement.addEventListener('pointerup', () => { dragging = null; });

renderer.domElement.addEventListener('pointermove', (event) => {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  pointer.insideWindow = true;
  if (!dragging) return;
  const dx = event.clientX - dragging.lastX;
  const dy = event.clientY - dragging.lastY;
  dragging.lastX = event.clientX;
  dragging.lastY = event.clientY;

  if (dragging.button === 2) {
    // Right-drag pans the holotable, per 5.8.1.
    panorama.graph.position.x += dx * 0.0015;
    panorama.graph.position.y -= dy * 0.0015;
    return;
  }

  const speed = 0.006;
  if (dragging.shift || event.shiftKey) {
    // SHIFT plus drag is the hyper-rotation, in whichever plane TAB selected.
    panorama.view.rotate(panorama.view.activeHyperPlane, -dy * speed);
    panorama.noteInput();
  } else {
    // Plain drag is ordinary 3D rotation: sideways is yaw (the XZ plane),
    // up and down is pitch (the YZ plane).
    panorama.view.rotate('xz', dx * speed);
    panorama.view.rotate('yz', dy * speed);
    panorama.noteInput();
  }
});

renderer.domElement.addEventListener('contextmenu', (event) => event.preventDefault());

renderer.domElement.addEventListener('wheel', (event) => {
  event.preventDefault();
  if (event.ctrlKey) {
    // CTRL plus wheel swims the slab, per 5.8.3.
    panorama.swim(Math.sign(event.deltaY) * -0.03);
    return;
  }
  // Otherwise the wheel dollies the camera. This moves the READER on a flat
  // screen, which is fine: there is no vestibular system to upset behind a
  // monitor. In VR it never happens.
  const direction = new THREE.Vector3(0, 0, 0).subVectors(panorama.graph.position, camera.position).normalize();
  camera.position.addScaledVector(direction, -Math.sign(event.deltaY) * 0.08);
}, { passive: false });

const keysHeld = new Set();

window.addEventListener('keydown', (event) => {
  const key = event.key.toLowerCase();
  keysHeld.add(key);

  if (key === 'tab') {
    event.preventDefault();
    setStatusFlash(`Hyper-plane: ${panorama.view.cycleHyperPlane().toUpperCase()}`);
    return;
  }
  if (key === 'e') { setStatusFlash(`Mode: ${panorama.toggleMode()}`); return; }
  if (key === 'home') { panorama.resetView(); setStatusFlash('View reset'); return; }
  if (key === 'z' && (event.ctrlKey || event.metaKey)) {
    setStatusFlash(panorama.view.undo() ? 'Undid one rotation' : 'Nothing left to undo');
    return;
  }
  if (event.shiftKey && (key === 'arrowleft' || key === 'arrowright')) {
    event.preventDefault();
    startSnap(panorama.view.activeHyperPlane, key === 'arrowleft' ? -1 : 1);
    setStatusFlash(`Snap 90 degrees in ${panorama.view.activeHyperPlane.toUpperCase()}`);
    return;
  }
  if (key === 'g') { panorama.stemsEnabled = !panorama.stemsEnabled; setStatusFlash(`Drop-stems ${panorama.stemsEnabled ? 'on' : 'off'}`); }
  if (key === 't') { panorama.showTesseract = !panorama.showTesseract; setStatusFlash(`Tesseract ${panorama.showTesseract ? 'shown' : 'hidden'}`); }
  if (key === 'n') { panorama.showGraph = !panorama.showGraph; setStatusFlash(`Fake news graph ${panorama.showGraph ? 'shown' : 'hidden'}`); }
});

window.addEventListener('keyup', (event) => keysHeld.delete(event.key.toLowerCase()));

/** Keys that are held down rather than tapped, checked once per frame. */
function applyHeldKeys(deltaMs) {
  const seconds = deltaMs / 1000;
  if (keysHeld.has('w')) panorama.swim(SWIM_UNITS_PER_SECOND * seconds);
  if (keysHeld.has('s')) panorama.swim(-SWIM_UNITS_PER_SECOND * seconds);
}

// The hover card on a flat screen is plain HTML, because HTML text is crisper
// than anything drawn inside a 3D canvas and costs nothing.
const hoverCard = document.getElementById('hover-card');

function updateScreenHover() {
  if (renderer.xr.isPresenting || !pointer.insideWindow) return;
  const ray = new THREE.Raycaster();
  ray.setFromCamera(new THREE.Vector2(pointer.x, pointer.y), camera);
  const found = panorama.pick(ray.ray.origin, ray.ray.direction, 0.012);
  panorama.hoveredNode = found;
  if (found < 0) { hoverCard.style.display = 'none'; return; }
  const band = W_BANDS[data.bandOf[found]];
  hoverCard.style.display = 'block';
  hoverCard.innerHTML =
    `<strong>${data.labels[found]}</strong>` +
    `<span>Placeholder node, not real content.</span>` +
    `<span class="band">${band.name} &middot; w = ${data.points4[found * 4 + 3].toFixed(2)}</span>` +
    `<span class="plain">${band.plain}</span>`;
  const x = ((pointer.x + 1) / 2) * window.innerWidth;
  const y = ((1 - pointer.y) / 2) * window.innerHeight;
  hoverCard.style.left = `${Math.min(window.innerWidth - 300, x + 18)}px`;
  hoverCard.style.top = `${Math.max(10, y - 20)}px`;
}

renderer.domElement.addEventListener('click', () => {
  if (panorama.hoveredNode >= 0) {
    focusNode(panorama.hoveredNode);
  }
});

/**
 * Focusing a node makes it the pivot, so that rotating afterwards means "turn
 * the world around THIS thing" (bible/part-05.md 5.4, the pivot rule).
 */
function focusNode(index) {
  panorama.focusedNode = index;
  const b = index * 4;
  panorama.view.setPivot(data.points4[b], data.points4[b + 1], data.points4[b + 2], data.points4[b + 3]);
  setStatusFlash(`Focused: ${data.labels[index]} (rotation now turns around it)`);
}


// =============================================================================
// BODY TWO: THE QUEST 3 (bible/part-05.md 5.4, Tier 1 controls)
// =============================================================================

// A plain "Enter VR" button, written by hand rather than imported from a
// three.js example, so that nothing in the deployed site depends on a file we
// did not read. bible LAW 4: the server holds static files only, and every one
// of them should be one we understand.
const vrButton = document.getElementById('enter-vr');
const vrNote = document.getElementById('vr-note');

if (navigator.xr) {
  navigator.xr.isSessionSupported('immersive-vr').then((supported) => {
    if (!supported) {
      vrButton.disabled = true;
      vrNote.textContent = 'This browser has WebXR but no headset session available.';
      return;
    }
    vrButton.disabled = false;
    vrNote.textContent = 'Headset detected. Put it on and press Enter VR.';
  });
} else {
  vrButton.disabled = true;
  vrNote.textContent = window.isSecureContext
    ? 'No WebXR in this browser. The flat-screen version below is the same 4D world.'
    : 'WebXR needs a secure connection (https). The flat-screen version works anyway.';
}

vrButton.addEventListener('click', async () => {
  if (renderer.xr.isPresenting) {
    renderer.xr.getSession().end();
    return;
  }
  try {
    const session = await navigator.xr.requestSession('immersive-vr', {
      optionalFeatures: ['local-floor', 'bounded-floor', 'hand-tracking'],
    });
    renderer.xr.setReferenceSpaceType('local-floor');
    await renderer.xr.setSession(session);
    vrButton.textContent = 'Leave VR';
    session.addEventListener('end', () => { vrButton.textContent = 'Enter VR'; });
  } catch (error) {
    vrNote.textContent = `Could not start VR: ${error.message}`;
  }
});

// ---- The two hands ---------------------------------------------------------

const hands = [0, 1].map((index) => {
  const grip = renderer.xr.getControllerGrip(index);
  const controller = renderer.xr.getController(index);
  panorama.scene.add(grip);
  panorama.scene.add(controller);

  // A simple physical stub for the controller, and a pointing ray on it. Kept
  // deliberately plain: a GLTF controller model would be one more downloaded
  // file that must still work in five years (bible 0.2, longevity beats flash).
  const body = new THREE.Mesh(
    new THREE.CapsuleGeometry(0.011, 0.075, 4, 8),
    new THREE.MeshLambertMaterial({ color: 0x8899bb })
  );
  body.rotation.x = Math.PI / 2;
  grip.add(body);

  const rayLine = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -1)]),
    new THREE.LineBasicMaterial({ color: 0x9fd0ff, transparent: true, opacity: 0.6 })
  );
  rayLine.scale.z = 1.4;
  rayLine.visible = false;
  controller.add(rayLine);

  const cursor = new THREE.Mesh(
    new THREE.SphereGeometry(0.006, 8, 6),
    new THREE.MeshBasicMaterial({ color: 0xdff0ff })
  );
  cursor.visible = false;
  panorama.scene.add(cursor);

  return {
    index, grip, controller, rayLine, cursor,
    previousButtons: [],
    grabbing: false,
    grabOffset: new THREE.Vector3(),
  };
});

const rightHand = hands[1];
const leftHand = hands[0];

// ---- The wrist gauge (bible/part-05.md 5.3.2) -------------------------------

/**
 * The w-gauge is a real instrument strapped to the left forearm, not a floating
 * heads-up display. That is deliberate: anything glued to the view fights the
 * inner ear and reads as smearing (5.1.5). A glance at your wrist to check
 * "where am I in the fourth dimension" becomes natural within minutes.
 *
 * It shows: the whole range of w as a vertical bar, the slab's position and
 * thickness, a silhouette of how much content lives at each w, the focused
 * node's w as a bright tick, and which hyper-plane the stick is driving.
 *
 * NOTE FOR ANY FUTURE AGENT: there is not one hue in here that means w. The
 * bar is monochrome on purpose. LAW 2.
 */
const gaugeCanvas = document.createElement('canvas');
gaugeCanvas.width = 256;
gaugeCanvas.height = 512;
const gaugeContext = gaugeCanvas.getContext('2d');
const gaugeTexture = new THREE.CanvasTexture(gaugeCanvas);
gaugeTexture.colorSpace = THREE.SRGBColorSpace;
const gaugePanel = new THREE.Mesh(
  new THREE.PlaneGeometry(0.075, 0.15),
  new THREE.MeshBasicMaterial({ map: gaugeTexture, transparent: true })
);
// Lying on the forearm, angled up toward the face like a watch face.
gaugePanel.position.set(0.015, 0.045, 0.06);
gaugePanel.rotation.set(-Math.PI * 0.32, 0, 0.15);
leftHand.grip.add(gaugePanel);

let gaugeClock = 0;

function drawGauge(status) {
  const c = gaugeContext;
  const width = gaugeCanvas.width, height = gaugeCanvas.height;
  c.clearRect(0, 0, width, height);
  c.fillStyle = 'rgba(8, 11, 18, 0.92)';
  c.fillRect(0, 0, width, height);
  c.strokeStyle = '#3a4a68';
  c.lineWidth = 3;
  c.strokeRect(3, 3, width - 6, height - 6);

  const top = 56, bottom = height - 34;
  const yFor = (w) => bottom - ((w + 1) / 2) * (bottom - top);

  // The density silhouette: how much of the world lives at each w.
  const buckets = status.histogram.length;
  c.fillStyle = 'rgba(120, 150, 200, 0.30)';
  for (let i = 0; i < buckets; i++) {
    const w = (i / (buckets - 1)) * 2 - 1;
    const barWidth = status.histogram[i] * 110;
    c.fillRect(width - 26 - barWidth, yFor(w) - 4, barWidth, 8);
  }

  // The band names, so the fourth dimension always has words attached to it.
  c.font = '17px system-ui, sans-serif';
  c.textAlign = 'left';
  for (const band of W_BANDS) {
    c.fillStyle = '#7f92b4';
    c.fillRect(28, yFor(band.w) - 1, 12, 2);
    c.fillText(band.name, 46, yFor(band.w) + 6);
  }

  // The slab: where the reader is standing in the fourth dimension.
  const slabTop = yFor(status.w0 + status.epsilon / 2);
  const slabBottom = yFor(status.w0 - status.epsilon / 2);
  c.fillStyle = 'rgba(215, 235, 255, 0.22)';
  c.fillRect(20, slabTop, width - 44, Math.max(3, slabBottom - slabTop));
  c.fillStyle = '#eaf4ff';
  c.fillRect(14, yFor(status.w0) - 2, width - 32, 4);

  // The focused node's own tick.
  if (status.focused >= 0) {
    const w = data.points4[status.focused * 4 + 3];
    c.fillStyle = '#ffd479';
    c.fillRect(10, yFor(w) - 2, 16, 5);
  }

  c.fillStyle = '#dfe9ff';
  c.font = 'bold 22px system-ui, sans-serif';
  c.textAlign = 'center';
  c.fillText(status.mode === 'slice' ? 'SLICE' : 'PROJECTION', width / 2, 32);

  // The three-segment hyper-plane indicator (bible/part-05.md 5.4, Tier 1.2).
  const segmentWidth = 62;
  HYPER_PLANES.forEach((plane, i) => {
    const x = 22 + i * (segmentWidth + 8);
    const active = plane === status.hyperPlane;
    c.fillStyle = active ? '#eaf4ff' : 'rgba(120, 140, 175, 0.25)';
    c.fillRect(x, height - 28, segmentWidth, 20);
    c.fillStyle = active ? '#0a0f18' : '#93a4c4';
    c.font = 'bold 16px system-ui, sans-serif';
    c.fillText(plane.toUpperCase(), x + segmentWidth / 2, height - 13);
  });

  gaugeTexture.needsUpdate = true;
}

// ---- The hand menu (bible/part-05.md 5.5.5) ---------------------------------

/**
 * The menu appears AT THE HAND, never in the middle of the view (Part 00, 0.7,
 * invariant 2). Its first two items are Undo and Reset, in that fixed order,
 * because a reader must never be afraid to experiment: the way home is always
 * two clicks, from anywhere, forever.
 */
const MENU_ITEMS = [
  { key: 'undo', label: 'Undo rotation' },
  { key: 'reset', label: 'Reset view' },
  { key: 'mode', label: 'Slice / Projection' },
  { key: 'home', label: 'Home slab (w = 0)' },
  { key: 'stems', label: 'Drop-stems on / off' },
];

const menuCanvas = document.createElement('canvas');
menuCanvas.width = 512; menuCanvas.height = 320;
const menuContext = menuCanvas.getContext('2d');
const menuTexture = new THREE.CanvasTexture(menuCanvas);
menuTexture.colorSpace = THREE.SRGBColorSpace;
const menuPanel = new THREE.Mesh(
  new THREE.PlaneGeometry(0.20, 0.125),
  new THREE.MeshBasicMaterial({ map: menuTexture, transparent: true, depthWrite: false })
);
menuPanel.position.set(0.06, 0.06, -0.05);
menuPanel.rotation.set(-0.45, 0.4, 0);
menuPanel.visible = false;
leftHand.grip.add(menuPanel);

let menuHighlight = -1;

function drawMenu() {
  const c = menuContext;
  c.clearRect(0, 0, 512, 320);
  c.fillStyle = 'rgba(9, 13, 21, 0.94)';
  c.fillRect(0, 0, 512, 320);
  c.strokeStyle = '#41567c'; c.lineWidth = 4; c.strokeRect(2, 2, 508, 316);
  MENU_ITEMS.forEach((item, i) => {
    const y = 18 + i * 58;
    const active = i === menuHighlight;
    c.fillStyle = active ? '#dceaff' : 'rgba(90, 110, 145, 0.22)';
    c.fillRect(14, y, 484, 50);
    c.fillStyle = active ? '#0a0f18' : '#cddcf5';
    c.font = 'bold 30px system-ui, sans-serif';
    c.textAlign = 'left';
    c.fillText(item.label, 30, y + 34);
  });
  menuTexture.needsUpdate = true;
}
drawMenu();

function runMenuItem(key) {
  if (key === 'undo') setStatusFlash(panorama.view.undo() ? 'Undid one rotation' : 'Nothing left to undo');
  if (key === 'reset') { panorama.resetView(); setStatusFlash('View reset'); }
  if (key === 'mode') setStatusFlash(`Mode: ${panorama.toggleMode()}`);
  if (key === 'home') { panorama.w0 = 0; setStatusFlash('Slab back to the established news'); }
  if (key === 'stems') { panorama.stemsEnabled = !panorama.stemsEnabled; }
}

/** Point the right hand at the menu panel and see which row is under the ray. */
const menuScratch = {
  planeNormal: new THREE.Vector3(),
  planePoint: new THREE.Vector3(),
  hit: new THREE.Vector3(),
  local: new THREE.Vector3(),
  origin: new THREE.Vector3(),
  direction: new THREE.Vector3(),
};

function menuRowUnderRay(hand) {
  if (!menuPanel.visible) return -1;
  menuPanel.updateWorldMatrix(true, false);
  menuScratch.planeNormal.set(0, 0, 1).transformDirection(menuPanel.matrixWorld).normalize();
  menuScratch.planePoint.setFromMatrixPosition(menuPanel.matrixWorld);
  menuScratch.origin.setFromMatrixPosition(hand.controller.matrixWorld);
  menuScratch.direction.set(0, 0, -1).transformDirection(hand.controller.matrixWorld).normalize();
  const denominator = menuScratch.direction.dot(menuScratch.planeNormal);
  if (Math.abs(denominator) < 1e-5) return -1;
  const t = menuScratch.planePoint.clone().sub(menuScratch.origin).dot(menuScratch.planeNormal) / denominator;
  if (t < 0 || t > 2) return -1;
  menuScratch.hit.copy(menuScratch.origin).addScaledVector(menuScratch.direction, t);
  menuScratch.local.copy(menuScratch.hit);
  menuPanel.worldToLocal(menuScratch.local);
  const halfWidth = 0.20 / 2, halfHeight = 0.125 / 2;
  if (Math.abs(menuScratch.local.x) > halfWidth || Math.abs(menuScratch.local.y) > halfHeight) return -1;
  const fraction = (halfHeight - menuScratch.local.y) / (halfHeight * 2);
  const row = Math.floor(fraction * MENU_ITEMS.length);
  return Math.max(0, Math.min(MENU_ITEMS.length - 1, row));
}

// ---- Reading the controllers once per frame ---------------------------------

/**
 * Buttons on a WebXR gamepad, by index, for the Quest 3 Touch controllers:
 *   0 = trigger, 1 = squeeze (grip), 3 = thumbstick click,
 *   4 = lower face button (X on the left hand, A on the right),
 *   5 = upper face button (Y on the left hand, B on the right).
 * Axes: 2 = thumbstick sideways, 3 = thumbstick forwards and back.
 */
const BUTTON = { TRIGGER: 0, SQUEEZE: 1, STICK: 3, FACE_LOWER: 4, FACE_UPPER: 5 };

let snapFlickArmed = true;
let twoHandStart = null;

function readControllers(deltaMs) {
  const session = renderer.xr.getSession();
  if (!session) { hands.forEach((h) => { h.rayLine.visible = false; h.cursor.visible = false; }); return; }

  for (const source of session.inputSources) {
    if (!source.gamepad) continue;
    const isRight = source.handedness === 'right';
    const hand = isRight ? rightHand : leftHand;
    const pad = source.gamepad;
    const buttons = pad.buttons.map((b) => b.pressed);
    const pressed = (i) => buttons[i] && !hand.previousButtons[i];
    const held = (i) => buttons[i];
    const axisX = pad.axes[2] ?? 0;
    const axisY = pad.axes[3] ?? 0;
    const deadZone = 0.15;

    if (isRight) {
      // ---- RIGHT HAND: ordinary 3D rotation, and pointing ----
      if (Math.abs(axisX) > deadZone) rotateCapped('xz', axisX * 0.9 * (deltaMs / 1000) * 3, deltaMs);
      if (Math.abs(axisY) > deadZone) rotateCapped('yz', axisY * 0.9 * (deltaMs / 1000) * 3, deltaMs);

      hand.rayLine.visible = true;
      const origin = new THREE.Vector3().setFromMatrixPosition(hand.controller.matrixWorld);
      const direction = new THREE.Vector3(0, 0, -1).transformDirection(hand.controller.matrixWorld).normalize();

      // The menu, if open, takes the ray before the graph does.
      const row = menuRowUnderRay(hand);
      if (row >= 0) {
        if (row !== menuHighlight) { menuHighlight = row; drawMenu(); }
        hand.cursor.visible = false;
        if (pressed(BUTTON.TRIGGER)) runMenuItem(MENU_ITEMS[row].key);
      } else {
        if (menuHighlight !== -1) { menuHighlight = -1; drawMenu(); }
        const found = panorama.pick(origin, direction);
        panorama.hoveredNode = found;
        if (found >= 0) {
          const scale = panorama.graph.scale.x;
          hand.cursor.visible = true;
          hand.cursor.position.set(
            panorama.graph.position.x + panorama.out3[found * 3] * scale,
            panorama.graph.position.y + panorama.out3[found * 3 + 1] * scale,
            panorama.graph.position.z + panorama.out3[found * 3 + 2] * scale);
          if (pressed(BUTTON.TRIGGER)) {
            focusNode(found);
            // A short haptic tap confirms the pick by feel, so the reader does
            // not need to look for confirmation (bible/part-05.md 5.3.5).
            source.gamepad.hapticActuators?.[0]?.pulse?.(0.4, 40);
          }
        } else {
          hand.cursor.visible = false;
        }
      }

      // A-button toggles the mode from the right hand as well, because reaching
      // across hands for a common action is a small daily annoyance.
      if (pressed(BUTTON.FACE_LOWER)) panorama.toggleMode();
    } else {
      // ---- LEFT HAND: the fourth dimension lives here ----
      if (held(BUTTON.TRIGGER)) {
        // Trigger held: SWIM the slab through w. The MRI-scanner gesture.
        // Pushing the stick away from the body travels toward the encyclopedia.
        if (Math.abs(axisY) > deadZone) {
          panorama.swim(-axisY * SWIM_UNITS_PER_SECOND * (deltaMs / 1000));
        }
      } else if (Math.abs(axisY) > deadZone) {
        // Trigger not held: HYPER-ROTATE in the active plane, rate capped.
        rotateCapped(panorama.view.activeHyperPlane, -axisY * 0.9 * (deltaMs / 1000) * 3, deltaMs);
      }

      // A sideways flick snaps ninety degrees. Four flicks always come home.
      if (Math.abs(axisX) > 0.75 && snapFlickArmed && !held(BUTTON.TRIGGER)) {
        startSnap(panorama.view.activeHyperPlane, Math.sign(axisX));
        snapFlickArmed = false;
      }
      if (Math.abs(axisX) < 0.3) snapFlickArmed = true;

      // Clicking the stick cycles which hyper-plane the stick drives.
      if (pressed(BUTTON.STICK)) {
        panorama.view.cycleHyperPlane();
        source.gamepad.hapticActuators?.[0]?.pulse?.(0.3, 30);
      }

      // X toggles slice and projection mode.
      if (pressed(BUTTON.FACE_LOWER)) panorama.toggleMode();
      // Y opens and closes the hand menu.
      if (pressed(BUTTON.FACE_UPPER)) {
        menuPanel.visible = !menuPanel.visible;
        menuHighlight = -1;
        drawMenu();
      }
    }

    // ---- GRIPS: move the graph with one hand, scale it with two ----
    hand.grabbing = held(BUTTON.SQUEEZE);
    hand.previousButtons = buttons;
  }

  applyGrips();
}

/**
 * One hand gripping moves the graph. Two hands gripping scale it. The reader
 * never moves; the object does. That contract is the backbone of the comfort
 * design (bible/part-05.md 5.1.3).
 */
const gripScratch = { a: new THREE.Vector3(), b: new THREE.Vector3(), previous: new THREE.Vector3() };

function applyGrips() {
  const gripping = hands.filter((h) => h.grabbing);
  if (gripping.length === 2) {
    gripScratch.a.setFromMatrixPosition(hands[0].grip.matrixWorld);
    gripScratch.b.setFromMatrixPosition(hands[1].grip.matrixWorld);
    const distance = gripScratch.a.distanceTo(gripScratch.b);
    const centre = gripScratch.a.clone().add(gripScratch.b).multiplyScalar(0.5);
    if (!twoHandStart) {
      twoHandStart = { distance, scale: panorama.graph.scale.x, centre: centre.clone(), position: panorama.graph.position.clone() };
    } else {
      const ratio = THREE.MathUtils.clamp(distance / twoHandStart.distance, 0.35, 3.5);
      panorama.graph.scale.setScalar(twoHandStart.scale * ratio);
      panorama.graph.position.copy(twoHandStart.position).add(centre.clone().sub(twoHandStart.centre));
    }
    return;
  }
  twoHandStart = null;

  if (gripping.length === 1) {
    const hand = gripping[0];
    gripScratch.a.setFromMatrixPosition(hand.grip.matrixWorld);
    if (!hand.grabStart) {
      hand.grabStart = { hand: gripScratch.a.clone(), graph: panorama.graph.position.clone() };
    } else {
      panorama.graph.position.copy(hand.grabStart.graph).add(gripScratch.a.clone().sub(hand.grabStart.hand));
    }
  }
  for (const hand of hands) if (!hand.grabbing) hand.grabStart = null;
}


// =============================================================================
// THE SHARED HEADS-UP INFORMATION
// =============================================================================

const statusLine = document.getElementById('status-line');
const flashLine = document.getElementById('flash-line');
const debugPanel = document.getElementById('debug-panel');
if (debugRequested) debugPanel.style.display = 'block';

let flashUntil = 0;
function setStatusFlash(text) {
  flashLine.textContent = text;
  flashLine.style.opacity = '1';
  flashUntil = performance.now() + 2600;
}

// A small message that floats over the table in VR, so a reader in a headset
// gets the same confirmations a reader on a screen gets.
const vrFlash = makeTextSprite('', 0xdfe9ff, { scale: 0.06 });
vrFlash.position.set(0, 1.72, -1.05);
vrFlash.visible = false;
panorama.scene.add(vrFlash);
let vrFlashText = '';

function updateReadouts(status, now, deltaMs, fps) {
  if (now > flashUntil) flashLine.style.opacity = '0';

  const band = nearestBandName(status.w0);
  statusLine.textContent =
    `${status.mode === 'slice' ? 'Slice' : 'Projection'} mode` +
    `  |  slab at w = ${status.w0.toFixed(2)} (${band.name}: ${band.plain})` +
    `  |  hyper-plane ${status.hyperPlane.toUpperCase()}` +
    `  |  ${status.solidNodes} of ${status.totalNodes} nodes solid here`;

  if (debugRequested) {
    debugPanel.textContent =
      `frames per second        ${fps.toFixed(1)}\n` +
      `draw calls              ${renderer.info.render.calls}\n` +
      `triangles               ${renderer.info.render.triangles}\n` +
      `projections this frame  ${status.projectionsThisFrame}   (must be 2: graph + tesseract, never per eye)\n` +
      `one-projection rule     ${panorama.projectionRuleViolated ? 'VIOLATED' : 'holding'}\n` +
      `slab thickness          ${status.epsilon.toFixed(3)}\n` +
      `undo stack              ${panorama.view.history.length}\n` +
      `presenting in VR        ${renderer.xr.isPresenting}`;
  }

  if (renderer.xr.isPresenting) {
    vrFlash.visible = now < flashUntil;
    if (vrFlash.visible && flashLine.textContent !== vrFlashText) {
      vrFlashText = flashLine.textContent;
      vrFlash.setText(vrFlashText);
    }
  } else {
    vrFlash.visible = false;
  }
}


// =============================================================================
// THE FRAME LOOP
// =============================================================================

let previousTime = performance.now();
let frameCount = 0;
let fpsAccumulator = 0;
let fps = 0;

renderer.setAnimationLoop(() => {
  const now = performance.now();
  // Clamp the step: if the browser tab was hidden for a minute, we must not
  // apply a minute's worth of rotation in one jump.
  const deltaMs = Math.min(50, now - previousTime);
  previousTime = now;

  frameCount++;
  fpsAccumulator += deltaMs;
  if (fpsAccumulator > 500) {
    fps = (frameCount * 1000) / fpsAccumulator;
    frameCount = 0; fpsAccumulator = 0;
  }

  advanceSnap(deltaMs);
  applyHeldKeys(deltaMs);
  readControllers(deltaMs);

  panorama.update(deltaMs);

  // THE ONE-PROJECTION ASSERT (bible/part-04.md 4.9.3). The picture is drawn
  // once, for both eyes, from one projection pass. If a future change ever
  // starts projecting per eye, this counter changes and the debug HUD says so
  // out loud instead of the mistake hiding as vague discomfort.
  if (panorama.projectionsThisFrame !== 2) panorama.projectionRuleViolated = true;

  updateScreenHover();

  gaugeClock += deltaMs;
  const status = panorama.status();
  if (gaugeClock > 90) { drawGauge(status); gaugeClock = 0; }
  updateReadouts(status, now, deltaMs, fps);

  renderer.render(panorama.scene, camera);
});

// Make a few things reachable from the browser console, for testing by hand.
window.PANORAMA = { panorama, renderer, camera, data };
