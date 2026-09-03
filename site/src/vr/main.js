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
import { loadGalaxy, loadEditionList } from '../scenes/galaxy.js';
import { WGym, hasGraduated } from '../scenes/wgym.js';
import { HYPER_PLANES } from '../lib/fourd.js';

// bible/part-05.md 5.1.4: the comfort cap, in degrees per second.
const MAX_ROTATION_DEGREES_PER_SECOND = 25;
const SNAP_MILLISECONDS = 300;
// A full sweep of the slab through the whole fourth dimension takes about four
// seconds, so that swimming feels like a deliberate journey (5.2.3).
const SWIM_UNITS_PER_SECOND = 0.5;

const debugRequested = new URLSearchParams(location.search).has('debug');

/**
 * The plane that shares NOTHING with each hyper-plane. Turning in a plane and
 * in its partner at the same time is a "double rotation", the motion that only
 * four dimensions allow. XW's partner is YZ, YW's is XZ, ZW's is XY.
 */
const PARTNER_PLANE = { xw: 'yz', yw: 'xz', zw: 'xy' };

// -----------------------------------------------------------------------------
// SET UP THE PICTURE
// -----------------------------------------------------------------------------

/*
 * WHICH WORLD ARE WE FLYING THROUGH?
 *
 * If real editions have been built, we fly through one of them. Which one comes
 * from ?edition=<model folder name>, defaulting to whichever edition the roster
 * names as the site's face (config/editions.toml). If nothing has been built
 * yet - a fresh clone, or a machine with no content - we fall back to the
 * placeholder world, so the four-dimensional machinery can always be examined
 * and taught even with an empty magazine.
 *
 * Each edition is its OWN world, because each model chose its own tags, wrote
 * its own encyclopedia entries and decided for itself what links to what
 * (DECISIONS.md decision 20).
 */
let editionList = null;
let data = null;

// ?world=placeholder forces the invented world even when real editions exist.
// It is how the automated checks exercise the four-dimensional machinery
// against a known fixed scene, and how the lessons can be taught on an empty
// magazine. A reader never needs it.
const wantsPlaceholder = new URLSearchParams(location.search).get('world') === 'placeholder';

try {
  if (wantsPlaceholder) throw new Error('the placeholder world was asked for');
  editionList = await loadEditionList();
  const asked = new URLSearchParams(location.search).get('edition');
  const known = (editionList.editions || []).map((e) => e.model_slug);
  const chosen = known.includes(asked) ? asked : editionList.default_model_slug;
  if (chosen) data = await loadGalaxy(chosen);
} catch (whyNot) {
  console.info('No real editions available, using the placeholder world:', whyNot.message);
}

const usingRealContent = data !== null;
if (!usingRealContent) data = buildSyntheticScene(200);

// The named regions of the fourth dimension. A real galaxy carries its own,
// because a magazine of news and explanations has different landmarks than the
// six-band placeholder world did.
const BANDS = data.bands || W_BANDS;

const panorama = new Panorama(data);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.xr.enabled = true;
// 72 frames per second is the Quest 3 target that bible/part-04.md demands.
renderer.xr.setFramerate?.(72);
document.body.appendChild(renderer.domElement);

// How close and how far the flat-screen camera may ever get. Without these,
// scrolling forward flies THROUGH the object and out the far side, where there
// is nothing to see and no obvious way back. Nir found exactly that, and worse,
// nothing on the page would put it right again.
const MIN_VIEW_DISTANCE = 1.15;
const MAX_VIEW_DISTANCE = 5.5;

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.05, 60);
// On a flat screen the reader needs to see the WHOLE object, so the camera
// stands further back than a person would stand at the real table. In VR this
// camera is ignored entirely: there, the reader's own head is the camera, and
// the holotable is placed at the distance a real table would be.
const CAMERA_HOME = new THREE.Vector3(0, 1.48, 1.75);
const CAMERA_LOOK_AT = new THREE.Vector3(0, 1.24, -1.15);
camera.position.copy(CAMERA_HOME);
camera.lookAt(CAMERA_LOOK_AT);

/** Put the flat-screen camera back where it started. */
function resetCamera() {
  camera.position.copy(CAMERA_HOME);
  camera.lookAt(CAMERA_LOOK_AT);
}

/**
 * THE ONE WAY HOME. Resetting has to put back everything the reader can move,
 * which on a flat screen includes the camera and the panning of the table, not
 * only the rotation. Anything that can be moved must be resettable, or the
 * promise "you can never get lost" is false.
 */
function resetEverything() {
  panorama.resetView();
  panorama.graph.position.set(0, 1.30, -1.15);
  panorama.graph.scale.setScalar(0.8);
  resetCamera();
}

/** How far the flat-screen camera is from the middle of the graph, in metres. */
function viewDistance() {
  return camera.position.distanceTo(panorama.graph.position);
}

/**
 * How much the object's APPARENT SIZE has been changed by the reader, ever,
 * added up as a fraction. Only two things count: rolling the wheel, and
 * stretching the object between two hands.
 *
 * WHY IT IS AN ACCUMULATOR AND NOT A MEASUREMENT. The obvious way to measure
 * apparent size is the distance from the camera to the object -- and that is
 * wrong, because SLIDING the object sideways also changes that distance a
 * little. Nir spotted it immediately: "the dragging is also affecting the
 * resizing, the moving is NOT resizing". So instead of measuring a quantity
 * that two different gestures both disturb, we count the gestures that
 * genuinely resize, at the moment they happen.
 */
let apparentSizeTravel = 0;

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
  if (snap.elapsed >= snap.total) {
    gym.noteSnap();
    snap = null;
  }
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
    if (plane === 'xw' || plane === 'yw' || plane === 'zw') {
      gym.noteHyperRotation(plane, clamped);
    }
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
    gym.noteHyperRotation(panorama.view.activeHyperPlane, -dy * speed);

    // AND SIDEWAYS DRIVES THE PARTNER PLANE AT THE SAME TIME. This is the flat
    // screen's honest version of the two-handed twist, and it is the one motion
    // that has no three-dimensional imitation at all: turning in two
    // completely separate planes at once. In three dimensions any two rotations
    // share an axis, so they add up to a single ordinary turn. In four
    // dimensions XY and ZW share nothing, so both happen genuinely at once and
    // the object never repeats itself. Nir's complaint was that lesson 5 "just
    // rotates the cube normally", and he was right: one plane at a time IS an
    // ordinary turn to the eye.
    if (doubleRotationAllowed() && Math.abs(dx) > 0) {
      const partner = PARTNER_PLANE[panorama.view.activeHyperPlane];
      panorama.view.rotate(partner, dx * speed);
      gym.noteHyperRotation(partner, dx * speed);
    }
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
  // Otherwise the wheel dollies the camera, which is what part-05.md 5.8.1
  // asks for. Moving the READER is fine on a flat screen: there is no
  // vestibular system to upset behind a monitor. In VR it never happens.
  //
  // But it is CLAMPED, in both directions. Scrolling forward used to carry the
  // camera straight through the object and out the other side, leaving a blank
  // screen and no obvious way back.
  const direction = new THREE.Vector3().subVectors(panorama.graph.position, camera.position);
  const distance = direction.length();
  direction.divideScalar(distance);
  const step = -Math.sign(event.deltaY) * Math.max(0.06, distance * 0.09);
  const wanted = distance - step;
  let landed = wanted;
  if (wanted < MIN_VIEW_DISTANCE) {
    landed = MIN_VIEW_DISTANCE;
    camera.position.copy(panorama.graph.position).addScaledVector(direction, -MIN_VIEW_DISTANCE);
    setStatusFlash('That is as close as it goes. Press Home to stand back.');
  } else if (wanted > MAX_VIEW_DISTANCE) {
    landed = MAX_VIEW_DISTANCE;
    camera.position.copy(panorama.graph.position).addScaledVector(direction, -MAX_VIEW_DISTANCE);
  } else {
    camera.position.addScaledVector(direction, step);
  }
  // Count how much this roll of the wheel actually changed the apparent size.
  apparentSizeTravel += Math.abs(landed - distance) / Math.max(0.2, distance);
  panorama.noteInput();
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
  if (key === 'home') {
    resetEverything();
    gym.noteReset();
    setStatusFlash('Everything back where it started');
    return;
  }
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
  if (key === 'l') {
    gymOffer.style.display = 'none';
    resetEverything();
    gym.start();
    setStatusFlash('Lessons, from the beginning');
    return;
  }
  if (gym.active && (key === 'enter' || key === ' ')) { advanceGym(); return; }
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
  const band = BANDS[data.bandOf[found]];
  hoverCard.style.display = 'block';
  if (usingRealContent) {
    // What a reader gets on hover, and nothing more: the one-line summary,
    // where they are in the fourth dimension, and - for a story - the small
    // picture this edition made for it. Nir asked for exactly this - the
    // TLDR and a small picture - and not the whole article, which is what
    // clicking is for.
    const kind = data.kinds[found] === 'concept'
      ? 'an explanation, written to last'
      : 'a story that happened';
    const tags = (data.tagsOf[found] || []).slice(0, 4)
      .map((tag) => `<em>${escapeForHtml(tag)}</em>`).join(' ');
    const thumb = data.thumbsOf ? data.thumbsOf[found] : null;
    hoverCard.innerHTML =
      (thumb ? `<img class="pic" src="${thumb}" alt="">` : '') +
      `<strong>${escapeForHtml(data.labels[found])}</strong>` +
      `<span>${escapeForHtml(data.summaries[found])}</span>` +
      (tags ? `<span class="tags">${tags}</span>` : '') +
      `<span class="band">${band.name} &middot; ${kind}</span>` +
      `<span class="plain">Click to read it &middot; ${data.shortName}'s edition</span>`;
    // A picture that fails to load quietly leaves the card rather than
    // showing a broken-image box (an edition that rendered no picture for a
    // story simply has none shipped). Attached as a listener here, because
    // inline event handlers are forbidden on this site (bible/part-07.md 7.3).
    const pic = hoverCard.querySelector('img.pic');
    if (pic) pic.addEventListener('error', () => pic.remove());
  } else {
    hoverCard.innerHTML =
      `<strong>${data.labels[found]}</strong>` +
      `<span>Placeholder node, not real content.</span>` +
      `<span class="band">${band.name} &middot; w = ${data.points4[found * 4 + 3].toFixed(2)}</span>` +
      `<span class="plain">${band.plain}</span>`;
  }
  const x = ((pointer.x + 1) / 2) * window.innerWidth;
  const y = ((1 - pointer.y) / 2) * window.innerHeight;
  hoverCard.style.left = `${Math.min(window.innerWidth - 300, x + 18)}px`;
  hoverCard.style.top = `${Math.max(10, y - 20)}px`;
}

renderer.domElement.addEventListener('click', () => {
  // During a lesson the gym's own beads are what the reader is pointing at, so
  // it gets first refusal on the click before the graph sees it.
  if (gym.active) {
    const ray = new THREE.Raycaster();
    ray.setFromCamera(new THREE.Vector2(pointer.x, pointer.y), camera);
    const scratch = new THREE.Vector3();
    const bead = gym.beadUnderRay(ray.ray.origin, ray.ray.direction);
    if (bead >= 0) {
      panorama.toRoomSpace(gym.markedSet.out3, bead, scratch);
      if (gym.notePick(scratch)) return;
    }
  }
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
// THE FOUR-DIMENSIONAL GYM (bible/part-05.md 5.7)
// =============================================================================

// Instructions on a flat screen are plain HTML. In the headset the same words go
// on a panel over the table, because HTML does not exist inside a VR session.
const gymPanelElement = document.getElementById('gym-panel');
const gymTitle = document.getElementById('gym-title');
const gymInstruction = document.getElementById('gym-instruction');
const gymProgress = document.getElementById('gym-progress');
const gymDots = document.getElementById('gym-dots');
const gymOffer = document.getElementById('gym-offer');
const gymDone = document.getElementById('gym-done');
const gymNext = document.getElementById('gym-next');
const gymBack = document.getElementById('gym-back');

const gymCanvas = document.createElement('canvas');
gymCanvas.width = 1024; gymCanvas.height = 320;
const gymContext = gymCanvas.getContext('2d');
const gymTexture = new THREE.CanvasTexture(gymCanvas);
gymTexture.colorSpace = THREE.SRGBColorSpace;
const gymVrPanel = new THREE.Mesh(
  new THREE.PlaneGeometry(0.66, 0.207),
  new THREE.MeshBasicMaterial({ map: gymTexture, transparent: true, depthWrite: false })
);
// Body-anchored above and behind the table, never glued to the head: head-locked
// text fights the inner ear and reads as smearing (part-05.md 5.1.5).
gymVrPanel.position.set(0, 1.78, -1.05);
gymVrPanel.visible = false;
panorama.scene.add(gymVrPanel);

function drawGymVrPanel(lesson) {
  const c = gymContext;
  c.clearRect(0, 0, 1024, 320);
  c.fillStyle = 'rgba(8, 12, 20, 0.93)';
  c.fillRect(0, 0, 1024, 320);
  c.strokeStyle = '#41567c'; c.lineWidth = 5; c.strokeRect(3, 3, 1018, 314);
  c.textAlign = 'left';
  c.fillStyle = '#ffd479';
  c.font = 'bold 34px system-ui, sans-serif';
  c.fillText(lesson.title, 34, 60);
  c.fillStyle = '#eaf4ff';
  c.font = '30px system-ui, sans-serif';
  wrapText(c, lesson.headset, 34, 116, 956, 38);
  const verdict = lesson.state === 'passed' ? lesson.done
                : lesson.state === 'failed' ? lesson.wrong : '';
  if (verdict) {
    // A finished lesson replaces the instruction with what actually happened,
    // and says which button carries on. In a headset there is nothing to click.
    c.fillStyle = 'rgba(8, 12, 20, 0.97)';
    c.fillRect(8, 86, 1008, 190);
    c.fillStyle = lesson.state === 'failed' ? '#ffb3a0' : '#a8e6b0';
    c.font = '27px system-ui, sans-serif';
    wrapText(c, verdict, 34, 122, 956, 34);
    c.fillStyle = '#ffd479';
    c.font = 'bold 26px system-ui, sans-serif';
    c.fillText(lesson.state === 'failed'
      ? 'Press A on your right hand to watch it again'
      : `Press A on your right hand to continue (${lesson.nextLabel})`, 34, 268);
  } else {
    c.fillStyle = '#8fa3c4';
    c.font = '26px system-ui, sans-serif';
    c.fillText(lesson.progress, 34, 262);
  }
  // Always visible, in both states: how to carry on, and how to get OUT.
  c.fillStyle = '#7f92b4';
  c.font = '22px system-ui, sans-serif';
  c.fillText('A = carry on      Y = menu: back, skip, or leave the lessons', 34, 302);
  gymTexture.needsUpdate = true;
}

/** Draw text across several lines, because a canvas will not do it for you. */
function wrapText(context, text, x, y, maxWidth, lineHeight) {
  const words = text.split(' ');
  let line = '';
  let cursorY = y;
  for (const word of words) {
    const attempt = line ? `${line} ${word}` : word;
    if (context.measureText(attempt).width > maxWidth && line) {
      context.fillText(line, x, cursorY);
      line = word;
      cursorY += lineHeight;
    } else {
      line = attempt;
    }
  }
  if (line) context.fillText(line, x, cursorY);
}

const gym = new WGym(panorama, {
  // The gym asks how much the reader has resized things. It gets a count of the
  // resizing gestures actually performed, not a measurement of anything that
  // sliding the object could disturb as well.
  apparentSize: () => apparentSizeTravel,
  resetCamera: resetEverything,
  onLesson: (lesson) => {
    if (!lesson) return;
    // A lesson is running, so the invitation to start one must be out of the
    // way. It was covering the very toys the reader is meant to be looking at.
    gymOffer.style.display = 'none';
    gymPanelElement.style.display = 'block';
    gymTitle.textContent = lesson.title;
    gymInstruction.textContent = renderer.xr.isPresenting ? lesson.headset : lesson.screen;
    gymProgress.textContent = lesson.progress;
    // A filled circle for every lesson already behind you.
    gymDots.textContent = '\u25cf '.repeat(lesson.index) + '\u25cb '.repeat(lesson.count - lesson.index);

    // The verdict, in words, and only then a button. Nothing moves on its own.
    const verdict = lesson.state === 'passed' ? lesson.done
                  : lesson.state === 'failed' ? lesson.wrong : '';
    gymDone.textContent = verdict;
    gymDone.style.display = verdict ? 'block' : 'none';
    gymDone.className = lesson.state === 'failed' ? 'wrong' : '';
    gymPanelElement.className = lesson.state === 'passed' ? 'passed'
                              : lesson.state === 'failed' ? 'failed' : '';
    gymNext.textContent = lesson.state === 'failed' ? 'Watch it again' : lesson.nextLabel;
    gymBack.disabled = lesson.index === 0;

    gymVrPanel.visible = renderer.xr.isPresenting;
    drawGymVrPanel(lesson);
  },
  onDone: (result) => {
    gymPanelElement.style.display = 'none';
    gymVrPanel.visible = false;
    resetEverything();
    if (result.graduated) {
      tier2Enabled = true;
      setStatusFlash('You can now follow an object through the fourth dimension. Welcome in.');
    }
  },
  setFlash: (text) => setStatusFlash(text),
});

// Tier 2, the two-handed twist, is off until the gym is finished: it is the
// reward, and Tier 1 is the product (part-05.md 5.4).
let tier2Enabled = hasGraduated();

/** Tier 2 is unlocked, or we are inside the lesson that teaches it. */
function doubleRotationAllowed() {
  return tier2Enabled || (gym.active && gym.lessonIndex === 4);
}

document.getElementById('reset-all').addEventListener('click', () => {
  resetEverything();
  gym.noteReset();
  setStatusFlash('Everything back where it started');
});

document.getElementById('gym-start').addEventListener('click', () => {
  gymOffer.style.display = 'none';
  resetEverything();
  gym.start();
});
document.getElementById('gym-skip-all').addEventListener('click', () => {
  gymOffer.style.display = 'none';
  gym.quit();
});
// Buttons give up focus after a click, or the space bar keeps pressing them
// again afterwards and the reader gets mysterious jumps.
for (const button of document.querySelectorAll('button')) {
  button.addEventListener('click', () => button.blur());
}

gymNext.addEventListener('click', () => advanceGym());
gymBack.addEventListener('click', () => gym.goBack());
document.getElementById('gym-quit').addEventListener('click', () => gym.quit());

/** One place decides what "carry on" means, so the screen and the headset agree. */
function advanceGym() {
  if (!gym.active) return;
  if (gym.state === 'failed') gym.retry();
  else gym.goNext();
}
document.getElementById('open-gym').addEventListener('click', () => {
  // This button is also the rescue button: whatever state the reader has got
  // themselves into, pressing it puts the world back and starts lesson 1.
  gymOffer.style.display = 'none';
  resetEverything();
  gym.start();
});

// First visit gets the offer, once. Everyone else is left alone.
if (!hasGraduated()) gymOffer.style.display = 'block';


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
let gaugeWasLit = false;

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
  for (const band of BANDS) {
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

  c.fillStyle = gaugeLit ? '#ffd479' : '#dfe9ff';
  c.font = 'bold 22px system-ui, sans-serif';
  c.textAlign = 'center';
  c.fillText(status.mode === 'slice' ? 'SLICE' : 'PROJECTION', width / 2, 32);

  // A one-line instruction, on the instrument itself, so nobody has to
  // remember which button opens the menu.
  c.font = '15px system-ui, sans-serif';
  c.fillStyle = gaugeLit ? '#ffd479' : '#7f92b4';
  c.fillText(gaugeLit ? 'pull trigger for menu' : 'touch or point here', width / 2, height - 40);

  // When the reader reaches for it, the whole instrument brightens, so the
  // answer to "is this thing alive?" arrives before any button is pressed.
  if (gaugeLit) {
    c.strokeStyle = '#ffd479';
    c.lineWidth = 6;
    c.strokeRect(4, 4, width - 8, height - 8);
  }

  // The three-segment hyper-plane indicator (bible/part-05.md 5.4, Tier 1.2).
  const segmentWidth = 62;
  HYPER_PLANES.forEach((plane, i) => {
    const x = 22 + i * (segmentWidth + 8);
    const active = plane === status.hyperPlane;
    c.fillStyle = active ? '#eaf4ff' : 'rgba(120, 140, 175, 0.25)';
    c.fillRect(x, height - 30, segmentWidth, 22);
    c.fillStyle = active ? '#0a0f18' : '#93a4c4';
    c.font = 'bold 16px system-ui, sans-serif';
    c.fillText(plane.toUpperCase(), x + segmentWidth / 2, height - 14);
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
const BASE_MENU_ITEMS = [
  { key: 'undo', label: 'Undo rotation' },
  { key: 'reset', label: 'Reset view' },
  { key: 'mode', label: 'Slice / Projection' },
  { key: 'home', label: 'Home slab (w = 0)' },
  { key: 'stems', label: 'Drop-stems on / off' },
  { key: 'gym', label: 'The 4D lessons' },
];

/**
 * The menu is built fresh every time it opens, because during a lesson the
 * reader needs the lesson's own controls -- carry on, go back, and above all a
 * way OUT. Everything the flat screen offers has to be reachable in the headset
 * too, or the headset is the poor relation.
 */
let MENU_ITEMS = BASE_MENU_ITEMS;

function buildMenu() {
  if (gym.active) {
    const lesson = gym.describe();
    MENU_ITEMS = [
      { key: 'next', label: lesson ? lesson.nextLabel : 'Next lesson' },
      { key: 'back', label: 'Back one lesson' },
      { key: 'quit', label: 'Leave the lessons' },
      { key: 'reset', label: 'Reset view' },
      { key: 'undo', label: 'Undo rotation' },
    ];
  } else {
    MENU_ITEMS = BASE_MENU_ITEMS;
  }
  drawMenu();
}

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
let gaugeLit = false;

function drawMenu() {
  const c = menuContext;
  const width = menuCanvas.width, height = menuCanvas.height;
  c.clearRect(0, 0, width, height);
  c.fillStyle = 'rgba(9, 13, 21, 0.94)';
  c.fillRect(0, 0, width, height);
  c.strokeStyle = '#41567c'; c.lineWidth = 4; c.strokeRect(2, 2, width - 4, height - 4);
  // Rows are sized from the panel and the number of items, so the menu can grow
  // and shrink -- during a lesson it carries different things -- without any
  // item ever falling off the bottom.
  const rowHeight = (height - 24) / MENU_ITEMS.length;
  MENU_ITEMS.forEach((item, i) => {
    const y = 12 + i * rowHeight;
    const active = i === menuHighlight;
    c.fillStyle = active ? '#dceaff' : 'rgba(90, 110, 145, 0.22)';
    c.fillRect(14, y + 2, width - 28, rowHeight - 6);
    c.fillStyle = active ? '#0a0f18' : '#cddcf5';
    c.font = `bold ${Math.min(30, Math.floor(rowHeight * 0.52))}px system-ui, sans-serif`;
    c.textAlign = 'left';
    c.fillText(item.label, 30, y + rowHeight * 0.66);
  });
  menuTexture.needsUpdate = true;
}
drawMenu();

function runMenuItem(key) {
  if (key === 'next') { advanceGym(); buildMenu(); return; }
  if (key === 'back') { gym.goBack(); buildMenu(); return; }
  if (key === 'quit') { gym.quit(); menuPanel.visible = false; return; }
  if (key === 'undo') setStatusFlash(panorama.view.undo() ? 'Undid one rotation' : 'Nothing left to undo');
  if (key === 'reset') { resetEverything(); gym.noteReset(); setStatusFlash('Everything back where it started'); }
  if (key === 'mode') setStatusFlash(`Mode: ${panorama.toggleMode()}`);
  if (key === 'gym') { gymOffer.style.display = 'none'; resetEverything(); gym.start(); }
  if (key === 'home') {
    panorama.w0 = panorama.homeW;
    setStatusFlash('Slab back to where most of the magazine lives');
  }
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

/**
 * Where does a hand's pointing ray land on a flat panel?
 *
 * Returns null for a miss, or { u, v } giving the position on the panel from 0
 * to 1 across and from 0 (top) to 1 (bottom). The panel's own size is read
 * from its geometry, so nothing has to be kept in step by hand.
 *
 * The tolerance is generous on purpose: a real arm holding a controller wobbles,
 * and a small target that must be hit precisely is the difference between a
 * control that feels alive and one that feels broken.
 */
function panelHit(panel, hand, tolerance = 0.012) {
  if (!panel.visible) return null;
  panel.updateWorldMatrix(true, false);
  menuScratch.planeNormal.set(0, 0, 1).transformDirection(panel.matrixWorld).normalize();
  menuScratch.planePoint.setFromMatrixPosition(panel.matrixWorld);
  menuScratch.origin.setFromMatrixPosition(hand.controller.matrixWorld);
  menuScratch.direction.set(0, 0, -1).transformDirection(hand.controller.matrixWorld).normalize();
  const denominator = menuScratch.direction.dot(menuScratch.planeNormal);
  if (Math.abs(denominator) < 1e-5) return null;
  const t = menuScratch.planePoint.clone().sub(menuScratch.origin).dot(menuScratch.planeNormal) / denominator;
  // Behind the hand, or absurdly far away, is a miss. Note that a panel on your
  // own forearm is only ten or twenty centimetres away, so the near limit has
  // to be tiny.
  if (t < 0.01 || t > 2.5) return null;
  menuScratch.hit.copy(menuScratch.origin).addScaledVector(menuScratch.direction, t);
  menuScratch.local.copy(menuScratch.hit);
  panel.worldToLocal(menuScratch.local);
  const parameters = panel.geometry.parameters;
  const halfWidth = parameters.width / 2, halfHeight = parameters.height / 2;
  if (Math.abs(menuScratch.local.x) > halfWidth + tolerance) return null;
  if (Math.abs(menuScratch.local.y) > halfHeight + tolerance) return null;
  return {
    u: (menuScratch.local.x + halfWidth) / (halfWidth * 2),
    v: (halfHeight - menuScratch.local.y) / (halfHeight * 2),
    distance: t,
  };
}

function menuRowUnderRay(hand) {
  const hit = panelHit(menuPanel, hand);
  if (!hit) return -1;
  const row = Math.floor(hit.v * MENU_ITEMS.length);
  return Math.max(0, Math.min(MENU_ITEMS.length - 1, row));
}

/**
 * Is the right hand pointing at, or physically near, the instrument on the left
 * forearm? Either one opens the menu.
 *
 * WHY THIS EXISTS, and it is worth remembering: the instrument was designed as
 * a DIAL, something to read, not a button. The first person to put the headset
 * on immediately tried to touch it with his other hand, and then tried to point
 * at it. When a person reaches for a thing, the thing should answer. So it now
 * answers, while still being a dial: touching or pointing opens the menu that
 * lives on the same arm.
 */
function gaugeReachedFor() {
  const hit = panelHit(gaugePanel, rightHand, 0.02);
  if (hit) return 'pointing';
  gaugePanel.updateWorldMatrix(true, false);
  menuScratch.planePoint.setFromMatrixPosition(gaugePanel.matrixWorld);
  menuScratch.origin.setFromMatrixPosition(rightHand.grip.matrixWorld);
  // Eight centimetres counts as "touching", which allows for the fact that the
  // controller is held in a fist a few centimetres behind the fingertips.
  if (menuScratch.origin.distanceTo(menuScratch.planePoint) < 0.08) return 'touching';
  return null;
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
let twistAnnounced = false;
// How long both grips have been squeezed, and how much turning has come out of
// it. Nir squeezed both hands and "moved them in all directions" with nothing
// happening -- because the gesture needs the WRISTS to turn, not the arms to
// travel. Sliding two closed fists through the air is a rotation of nothing.
let bothGripsMilliseconds = 0;
let twistSinceGrip = 0;
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

      // Reaching for the wrist instrument opens the menu, whether the reader
      // points at it or bumps into it with the other hand.
      const reach = gaugeReachedFor();
      if (reach && !menuPanel.visible) {
        gaugeLit = true;
        if (reach === 'touching' || pressed(BUTTON.TRIGGER)) {
          menuPanel.visible = true;
          menuHighlight = -1;
          buildMenu();
          source.gamepad.hapticActuators?.[0]?.pulse?.(0.35, 45);
        }
      } else {
        gaugeLit = false;
      }

      // The menu, if open, takes the ray before the graph does.
      const row = menuRowUnderRay(hand);
      if (row >= 0) {
        if (row !== menuHighlight) { menuHighlight = row; drawMenu(); }
        hand.cursor.visible = false;
        if (pressed(BUTTON.TRIGGER)) runMenuItem(MENU_ITEMS[row].key);
      } else {
        if (menuHighlight !== -1) { menuHighlight = -1; drawMenu(); }
        // A lesson's beads come before the graph's nodes. Note that this does
        // NOT skip the rest of the hand: the buttons below still have to work
        // while the reader is pointing at something.
        let gymTookThePoint = false;
        if (gym.active) {
          const bead = gym.beadUnderRay(origin, direction);
          if (bead >= 0) {
            gymTookThePoint = true;
            const scratch = new THREE.Vector3();
            panorama.toRoomSpace(gym.markedSet.out3, bead, scratch);
            hand.cursor.visible = true;
            hand.cursor.position.copy(scratch);
            if (pressed(BUTTON.TRIGGER) && gym.notePick(scratch)) {
              source.gamepad.hapticActuators?.[0]?.pulse?.(0.4, 40);
            }
          }
        }
        const found = gymTookThePoint ? -1 : panorama.pick(origin, direction);
        if (!gymTookThePoint) panorama.hoveredNode = found;
        if (found >= 0 && !gymTookThePoint) {
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
        } else if (!gymTookThePoint) {
          hand.cursor.visible = false;
        }
      }

      // A-button carries the lessons forward, since there is nothing to click
      // inside a headset. Outside a lesson it toggles the mode, because
      // reaching across hands for a common action is a small daily annoyance.
      if (pressed(BUTTON.FACE_LOWER)) {
        if (gym.active && gym.state !== 'doing') advanceGym();
        else panorama.toggleMode();
      }
      // B on the right hand opens the menu too. Two buttons for one action is
      // not clutter when the action is the way home.
      if (pressed(BUTTON.FACE_UPPER)) {
        menuPanel.visible = !menuPanel.visible;
        menuHighlight = -1;
        buildMenu();
      }
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
        buildMenu();
      }
    }

    // ---- GRIPS: move the graph with one hand, scale it with two ----
    hand.grabbing = held(BUTTON.SQUEEZE);
    hand.previousButtons = buttons;
  }

  applyGrips(deltaMs);
}

/**
 * One hand gripping moves the graph. Two hands gripping scale it. The reader
 * never moves; the object does. That contract is the backbone of the comfort
 * design (bible/part-05.md 5.1.3).
 */
const gripScratch = { a: new THREE.Vector3(), b: new THREE.Vector3(), previous: new THREE.Vector3() };

function applyGrips(deltaMs) {
  const gripping = hands.filter((h) => h.grabbing);

  // TIER 2, THE TWIST. With both hands squeezed and the gesture unlocked, the
  // two controllers' turning drives a full four-dimensional rotation: your left
  // hand and right hand together reach turns that no single plane can. It uses
  // per-frame differences, so releasing either hand stops it dead, with no
  // inertia (part-05.md 5.4 Tier 2, and 5.1.4).
  if (gripping.length === 2 && doubleRotationAllowed()) {
    const left = deltaQuaternion(hands[0]);
    const right = deltaQuaternion(hands[1]);
    if (left && right) {
      panorama.view.twist(left, right);
      panorama.noteInput();
      const amount = Math.abs(left.x) + Math.abs(left.y) + Math.abs(left.z) +
                     Math.abs(right.x) + Math.abs(right.y) + Math.abs(right.z);
      gym.noteTwist(amount * 4);
      twistSinceGrip += amount;
      // Say out loud that the gesture has been recognised, the first time it
      // happens. Squeezing both hands and feeling nothing is indistinguishable
      // from the feature being broken.
      if (!twistAnnounced && amount > 0.004) {
        twistAnnounced = true;
        setStatusFlash('Both hands together: you are now turning it in two planes at once.');
      }
    }
    // Squeezing hard, holding on, and nothing happening: the reader is almost
    // certainly moving their arms instead of turning their wrists. Say so,
    // rather than letting them conclude it is broken.
    bothGripsMilliseconds += deltaMs;
    if (bothGripsMilliseconds > 1400 && twistSinceGrip < 0.02) {
      bothGripsMilliseconds = 0;
      setStatusFlash('Turn your WRISTS against each other, like opening a stiff jar. '
        + 'Moving your arms about will not do it.');
    }
    twoHandStart = null;
    return;
  }
  hands.forEach((h) => { h.previousQuaternion = null; });
  bothGripsMilliseconds = 0;
  twistSinceGrip = 0;

  if (gripping.length === 2) {
    gripScratch.a.setFromMatrixPosition(hands[0].grip.matrixWorld);
    gripScratch.b.setFromMatrixPosition(hands[1].grip.matrixWorld);
    const distance = gripScratch.a.distanceTo(gripScratch.b);
    const centre = gripScratch.a.clone().add(gripScratch.b).multiplyScalar(0.5);
    if (!twoHandStart) {
      twoHandStart = { distance, scale: panorama.graph.scale.x, centre: centre.clone(), position: panorama.graph.position.clone() };
    } else {
      const ratio = THREE.MathUtils.clamp(distance / twoHandStart.distance, 0.35, 3.5);
      const previousScale = panorama.graph.scale.x;
      panorama.graph.scale.setScalar(twoHandStart.scale * ratio);
      // Stretching the object between two hands is the other way of resizing it.
      apparentSizeTravel += Math.abs(panorama.graph.scale.x - previousScale) /
                            Math.max(0.01, previousScale);
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

/**
 * How much has this hand turned since the last frame, as a unit quaternion?
 * Returns null on the first frame of a grip, because there is nothing to compare
 * against yet and inventing a rotation there would make the object jump.
 */
const quaternionScratch = { current: new THREE.Quaternion(), delta: new THREE.Quaternion(), inverse: new THREE.Quaternion() };
function deltaQuaternion(hand) {
  hand.grip.updateWorldMatrix(true, false);
  quaternionScratch.current.setFromRotationMatrix(hand.grip.matrixWorld);
  if (!hand.previousQuaternion) {
    hand.previousQuaternion = quaternionScratch.current.clone();
    return null;
  }
  quaternionScratch.inverse.copy(hand.previousQuaternion).invert();
  quaternionScratch.delta.multiplyQuaternions(quaternionScratch.current, quaternionScratch.inverse);
  hand.previousQuaternion.copy(quaternionScratch.current);
  const d = quaternionScratch.delta;
  return { w: d.w, x: d.x, y: d.y, z: d.z };
}


// =============================================================================
// THE SHARED HEADS-UP INFORMATION
// =============================================================================

const statusLine = document.getElementById('status-line');
const flashLine = document.getElementById('flash-line');
const debugPanel = document.getElementById('debug-panel');
if (debugRequested) debugPanel.style.display = 'block';

let flashUntil = 0;
/**
 * Show a message long enough to READ. Nir: "in every place that there is like a
 * message box it appears for a split second and disappears immediately, I
 * cannot read it."
 *
 * Two changes from the naive version. The time on screen depends on how much
 * there is to read, because a fixed two seconds is generous for "View reset"
 * and useless for a sentence. And when the time is up the message does not
 * vanish: it dims and stays until something replaces it, so a reader who looks
 * away and back has not lost it. Nothing important should ever be gone forever
 * because somebody blinked.
 */
function setStatusFlash(text) {
  flashLine.textContent = text;
  flashLine.style.opacity = '1';
  const readingTime = 2200 + text.length * 55;
  flashUntil = performance.now() + Math.min(14000, Math.max(4000, readingTime));
}

// A small message that floats over the table in VR, so a reader in a headset
// gets the same confirmations a reader on a screen gets.
const vrFlash = makeTextSprite('', 0xdfe9ff, { scale: 0.06 });
vrFlash.position.set(0, 1.72, -1.05);
vrFlash.visible = false;
panorama.scene.add(vrFlash);
let vrFlashText = '';

function updateReadouts(status, now, deltaMs, fps) {
  // Dimmed, not deleted.
  if (now > flashUntil) flashLine.style.opacity = '0.42';

  const band = nearestBandName(status.w0, BANDS);
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
      `projections this frame  ${status.projectionsThisFrame} of ${panorama.expectedProjections} expected   (never per eye)\n` +
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

  // The gym may turn the view itself during lesson 4, so its thinking happens
  // BEFORE the projection, and its drawing AFTER it. That order is what keeps
  // the toys and the graph from ever disagreeing about which way is w.
  gym.update(deltaMs);

  panorama.update(deltaMs);

  if (gym.active) gym.draw();

  // THE ONE-PROJECTION ASSERT (bible/part-04.md 4.9.3). The picture is drawn
  // once, for both eyes, from one projection pass. If a future change ever
  // starts projecting per eye, this counter changes and the debug HUD says so
  // out loud instead of the mistake hiding as vague discomfort.
  if (panorama.projectionsThisFrame !== panorama.expectedProjections) {
    panorama.projectionRuleViolated = true;
  }

  updateScreenHover();

  gaugeClock += deltaMs;
  const status = panorama.status();
  if (gaugeClock > 90 || gaugeLit !== gaugeWasLit) { drawGauge(status); gaugeClock = 0; gaugeWasLit = gaugeLit; }
  updateReadouts(status, now, deltaMs, fps);

  renderer.render(panorama.scene, camera);
});

// Make a few things reachable from the browser console, and from the automatic
// browser test. The VR controls cannot be exercised by a headless browser
// otherwise, and "I could not activate the thing on my arm" is exactly the kind
// of fault that unit tests never catch and a real person finds in ten seconds.
window.PANORAMA = {
  panorama, renderer, camera, data, gym,
  isTier2Enabled: () => tier2Enabled,
  doubleRotationAllowed, PARTNER_PLANE,
  flashState: () => ({ text: flashLine.textContent, opacity: flashLine.style.opacity }),
  resetEverything, viewDistance,
  apparentSize: () => apparentSizeTravel,
  limits: { MIN_VIEW_DISTANCE, MAX_VIEW_DISTANCE },
  vr: { panelHit, gaugeReachedFor, menuRowUnderRay, runMenuItem,
        rebuildMenu: buildMenu,
        menuKeys: () => MENU_ITEMS.map((item) => item.key),
        gaugePanel, menuPanel, hands, leftHand, rightHand,
        isMenuOpen: () => menuPanel.visible,
        openMenu: (open) => { menuPanel.visible = open; drawMenu(); } },
};


// -----------------------------------------------------------------------------
// READING WHAT YOU FOUND, AND CHANGING WHOSE WORLD YOU ARE IN
// -----------------------------------------------------------------------------

/**
 * Escaping anything that came from a model before it is put into the page.
 *
 * Every word in a hover card was written by an AI model that had just been
 * reading web pages collected from strangers. It is therefore untrusted text
 * and is escaped, always (bible/part-07.md, and LAW 8's hostile-input rule
 * followed all the way to the last mile).
 */
function escapeForHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/**
 * Build the edition switcher from whatever editions exist. Nothing about any
 * particular model is written into this page, so a model added tomorrow appears
 * here on its own (DECISIONS.md decision 18).
 */
const editionPick = document.getElementById('edition-pick');
if (editionPick) {
  if (!usingRealContent || !editionList) {
    editionPick.innerHTML = '<option>no editions built yet</option>';
    editionPick.disabled = true;
  } else {
    for (const edition of editionList.editions) {
      const option = document.createElement('option');
      option.value = edition.model_slug;
      const counts = edition.counts || {};
      option.textContent = `${edition.short_name} - ${counts.stories || 0} stories, ${counts.concepts || 0} ideas`;
      option.selected = edition.model_slug === data.modelSlug;
      editionPick.appendChild(option);
    }
    editionPick.addEventListener('change', () => {
      // A full page load on purpose: a different edition is a different world,
      // with different nodes in different places, and pretending otherwise by
      // morphing between them would teach the reader something false.
      const url = new URL(location.href);
      url.searchParams.set('edition', editionPick.value);
      location.assign(url.toString());
    });
  }
}

/**
 * Clicking a node opens what it says. The hover card gives the one-liner; the
 * click gives the article. Only ever in a new tab, so a reader never loses the
 * position they had worked to reach in the fourth dimension.
 */
if (usingRealContent) {
  renderer.domElement.addEventListener('click', () => {
    if (renderer.xr.isPresenting) return;
    const found = panorama.hoveredNode;
    if (found === undefined || found < 0) return;
    const page = data.pageOf[found];
    if (page) window.open(page, '_blank', 'noopener');
  });
}
