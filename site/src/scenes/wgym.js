/*
================================================================================
 wgym.js  --  THE FOUR-DIMENSIONAL GYM: FIVE LESSONS, ABOUT SIXTY SECONDS
================================================================================

 Owned by: bible/part-05.md 5.7. Milestone 1 asks for this to be built FIRST,
 as the test harness for the rotation and projection code, and then kept as the
 onboarding (part-13.md 13.2, build item 6).

 WHY IT MATTERS MORE THAN IT LOOKS. Nobody has ever seen four dimensions. A
 visitor who is simply dropped into a 4D graph will decide, within about eight
 seconds, that the site is broken or that they are stupid, and leave. Neither is
 true, and both are our fault. These five lessons exist so that a stranger
 acquires a genuinely new perceptual skill before they are asked to read
 anything.

 THE ONE RULE THAT SHAPES EVERY LESSON: each one is gated on DOING, never on
 reading. A lesson passes when the reader has performed the thing, not when they
 have clicked "next". Lesson 4 is the real examination, and it is the whole
 project in miniature: watch an object turn through a direction that should not
 exist, then point at the bead you were following. When somebody passes that,
 their brain has learned something almost nobody's brain has learned.

 IT MUST NEVER TRAP ANYONE. Skip is always available, on every lesson, in both
 bodies. A tutorial you cannot leave is a cage.
================================================================================
*/

import * as THREE from '../../vendor/three.module.min.js';
import { InstancedSet, makeTextSprite } from '../vr/panorama.js';
import { buildTesseract } from './synthetic.js';
import { HYPER_PLANES } from '../lib/fourd.js';

// Where the gym remembers that you have graduated, so it only interrupts once.
const STORAGE_KEY = 'ai-panorama.gym.graduated.v1';

/** Has this visitor finished the gym before? */
export function hasGraduated() {
  try { return localStorage.getItem(STORAGE_KEY) === 'yes'; } catch { return false; }
}
function rememberGraduation() {
  try { localStorage.setItem(STORAGE_KEY, 'yes'); } catch { /* private mode; fine */ }
}


export class WGym {
  /**
   * panorama  the scene, whose View4D and holotable the gym borrows
   * hooks     { onLesson(lesson), onDone(), setFlash(text) } so the two bodies
   *           (screen and headset) can each show the instructions their own way
   */
  constructor(panorama, hooks = {}) {
    this.panorama = panorama;
    this.hooks = hooks;
    this.active = false;
    this.lessonIndex = -1;
    // NOTHING ADVANCES BY ITSELF. Nir's own words after the first real session:
    // "the lessons are going to the next one without the user being aware, he
    // just drops into a new lesson because the software decided the previous
    // lesson was through". So a finished lesson SAYS it is finished and then
    // waits. The reader presses Next. Doing the task still unlocks it -- the
    // gating is unchanged -- but leaving is always the reader's own decision.
    // Three states: 'doing', 'passed', 'failed'.
    this.state = 'doing';
    this.lessonTime = 0;
    this.passedTime = 0;      // how long the pass condition has held
    this.attempts = 0;
    this.tier2Offered = false;

    this.buildToys();
    this.lessons = this.defineLessons();
  }

  // ---------------------------------------------------------------------------
  // THE TOYS. One simple object per lesson, built once, shown as needed.
  // ---------------------------------------------------------------------------
  buildToys() {
    const panorama = this.panorama;
    this.group = new THREE.Group();
    panorama.graph.add(this.group);
    this.group.visible = false;

    // LESSON 1: one honest cube, to be grabbed, moved and stretched. It is
    // ordinary three-dimensional on purpose: the first ten seconds must feel
    // completely familiar, so that the fourth dimension arrives as a door and
    // not as a wall.
    this.cube = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 0.5, 0.5),
      new THREE.MeshLambertMaterial({ color: 0x6ec6ff })
    );
    this.cube.visible = false;
    this.group.add(this.cube);

    // LESSON 2: a ladder of five beads at five different depths in the fourth
    // dimension. Only one is lit. You cannot reach it by moving; you have to
    // swim.
    this.ladderCount = 5;
    const ladder = new Float64Array(this.ladderCount * 4);
    for (let i = 0; i < this.ladderCount; i++) {
      const w = -0.8 + i * 0.4;
      ladder[i * 4] = 0;              // x
      ladder[i * 4 + 1] = -0.12 + i * 0.19;  // y, so they also make a visible ladder
      ladder[i * 4 + 2] = 0;          // z
      ladder[i * 4 + 3] = w;          // w: the whole point
    }
    this.ladderPoints = ladder;
    this.ladderSet = panorama.registerPointSet('gym-ladder', ladder);
    this.ladderBeads = new InstancedSet(new THREE.IcosahedronGeometry(1, 2), this.ladderCount);
    this.group.add(this.ladderBeads.mesh);
    this.ladderTarget = 3;   // the lit one. Not the middle: the middle is free.

    // LESSONS 3 and 5: a tesseract of its own, so the gym never disturbs the
    // real one on the table.
    const tesseract = buildTesseract(0.34);
    this.tesseract = tesseract;
    const points = new Float64Array(tesseract.vertices.length * 4);
    tesseract.vertices.forEach((v, i) => {
      points[i * 4] = v[0]; points[i * 4 + 1] = v[1];
      points[i * 4 + 2] = v[2]; points[i * 4 + 3] = v[3];
    });
    this.tesseractSet = panorama.registerPointSet('gym-tesseract', points);
    this.tesseractNodes = new InstancedSet(new THREE.IcosahedronGeometry(1, 1), tesseract.vertices.length);
    this.tesseractEdges = new InstancedSet(new THREE.CylinderGeometry(1, 1, 1, 6, 1, true), tesseract.edges.length);
    for (let i = 0; i < tesseract.vertices.length; i++) this.tesseractNodes.setColour(i, 0.96, 0.94, 0.82);
    for (let e = 0; e < tesseract.edges.length; e++) this.tesseractEdges.setColour(e, 0.85, 0.88, 0.64);
    this.group.add(this.tesseractNodes.mesh);
    this.group.add(this.tesseractEdges.mesh);

    // LESSON 4: six beads, each with a letter, arranged so that no two look
    // alike from any one angle. One of them is yours to follow.
    this.markedCount = 6;
    const marked = new Float64Array(this.markedCount * 4);
    // Spread widely across the view and kept in its clear upper middle, with
    // every bead at a different depth in the fourth dimension so that a
    // hyper-rotation genuinely shuffles them.
    // Positions chosen by MEASURING where they land on screen, not by guessing:
    // no two beads and no two letters may sit on top of each other, or the
    // question "which one was it?" is unanswerable through no fault of the
    // reader. Every bead also sits at a different depth in the fourth
    // dimension, so a hyper-rotation genuinely shuffles them.
    const places = [
      [-0.66, 0.10, 0.15, -0.60],
      [0.64, 0.14, -0.15, 0.15],
      [-0.34, -0.20, 0.50, 0.62],
      [0.36, -0.24, 0.45, -0.25],
      [0.10, 0.56, -0.45, 0.45],
      [-0.60, 0.60, -0.40, -0.05],
    ];
    places.forEach((p, i) => {
      marked[i * 4] = p[0]; marked[i * 4 + 1] = p[1];
      marked[i * 4 + 2] = p[2]; marked[i * 4 + 3] = p[3];
    });
    this.markedPoints = marked;
    this.markedSet = panorama.registerPointSet('gym-marked', marked);
    this.markedBeads = new InstancedSet(new THREE.IcosahedronGeometry(1, 2), this.markedCount);
    this.group.add(this.markedBeads.mesh);
    this.markedNames = ['A', 'B', 'C', 'D', 'E', 'F'];
    // Two sets of letters: ordinary white ones, and a big gold one for the bead
    // you have been asked to follow. Nir looked for an F and could not find it,
    // which is the worst possible failure for the lesson that matters most.
    this.markedLabels = this.markedNames.map((name) => {
      const sprite = makeTextSprite(name, 0xdfe9ff, { scale: 0.055, square: true });
      sprite.visible = false;
      this.group.add(sprite);
      return sprite;
    });
    this.markedTargetLabels = this.markedNames.map((name) => {
      const sprite = makeTextSprite(name, 0xffd479, { scale: 0.10, square: true });
      sprite.visible = false;
      this.group.add(sprite);
      return sprite;
    });
    this.markedTarget = 0;
    this.markedAnswer = -1;      // what the reader pointed at
    this.hyperTour = null;       // the slow rotation the gym performs itself
  }

  // ---------------------------------------------------------------------------
  // THE FIVE LESSONS
  // ---------------------------------------------------------------------------
  defineLessons() {
    const panorama = this.panorama;

    return [
      {
        // ---- 1. TABLE MANNERS -------------------------------------------
        title: 'Lesson 1 of 5: it is an object on a table',
        screen: 'Right-click and drag to slide it around. Roll the mouse wheel to make it bigger and smaller.',
        headset: 'Squeeze one hand to pick it up and move it. Squeeze both hands and pull them apart to make it bigger.',
        teaches: 'You never move. The object does. That is why nobody gets sick in here.',
        done: 'You moved it and you resized it. Notice that YOU did not move at all: '
            + 'the room stayed exactly where it was. Everything in here works that way, '
            + 'and it is the reason nobody feels ill.',
        begin: () => {
          this.cube.visible = true;
          this.cube.position.set(0, 0, 0);
          this.moved = 0;
          this.scaled = 0;
          this.lastGraphPosition = panorama.graph.position.clone();
          this.lastGraphScale = panorama.graph.scale.x;
          this.lastViewDistance = this.hooks.viewDistance ? this.hooks.viewDistance() : null;
        },
        tick: () => {
          this.moved += panorama.graph.position.distanceTo(this.lastGraphPosition);
          this.lastGraphPosition.copy(panorama.graph.position);

          // "Bigger" happens two different ways, and BOTH have to count.
          // In the headset, two hands pull the object itself larger, so the
          // graph's own scale changes. On a flat screen the wheel moves the
          // camera closer instead, and the object's scale never changes at all
          // -- which is why this lesson used to be impossible to finish with a
          // mouse. What the reader experiences in both cases is APPARENT size,
          // so that is what gets measured, as a fraction rather than in metres.
          const scale = panorama.graph.scale.x;
          this.scaled += Math.abs(scale - this.lastGraphScale) / Math.max(0.01, scale);
          this.lastGraphScale = scale;

          if (this.hooks.viewDistance) {
            const distance = this.hooks.viewDistance();
            if (this.lastViewDistance !== null) {
              this.scaled += Math.abs(distance - this.lastViewDistance) / Math.max(0.2, distance);
            }
            this.lastViewDistance = distance;
          }

          this.cube.rotation.y += 0.004;
        },
        // Both things must have happened: moved it, and changed its size.
        passed: () => this.moved > 0.12 && this.scaled > 0.10,
        progress: () => `moved ${Math.min(100, Math.round(this.moved / 0.12 * 100))}%, resized ${Math.min(100, Math.round(this.scaled / 0.10 * 100))}%`,
        end: () => { this.cube.visible = false; },
      },

      {
        // ---- 2. THE SLAB ------------------------------------------------
        title: 'Lesson 2 of 5: swim to the lit bead',
        screen: 'Hold W or S. You are moving a slice through the fourth dimension. Bring the gold bead into it.',
        headset: 'Hold the left trigger and push the left stick forwards or back. Bring the gold bead into the slice.',
        teaches: 'Faint beads are outside your slice, not gone. Nothing here ever just disappears.',
        done: 'The gold bead went solid. That is what just happened: it was always '
            + 'there, but it sat at a different depth in the fourth dimension, and you '
            + 'moved your slice onto it. The faint ones are still there too, outside '
            + 'your slice. Nothing in here ever simply disappears.',
        begin: () => {
          panorama.setMode('slice');
          panorama.w0 = -0.9;
          this.beadsVisible = true;
        },
        tick: () => { /* the drawing loop handles it */ },
        passed: () => {
          const w = this.ladderSet.outW[this.ladderTarget];
          return Math.abs(w - panorama.w0) <= panorama.epsilon * 0.5;
        },
        // Held for a moment, so that sweeping past it by accident is not a pass.
        holdFor: 500,
        progress: () => {
          const w = this.ladderSet.outW[this.ladderTarget];
          const distance = Math.abs(w - panorama.w0);
          return distance <= panorama.epsilon * 0.5
            ? 'in the slice, hold it there'
            : `${distance.toFixed(2)} away in the fourth dimension`;
        },
        end: () => { this.beadsVisible = false; },
      },

      {
        // ---- 3. THE TESSERACT -------------------------------------------
        title: 'Lesson 3 of 5: four quarter turns come home',
        screen: 'Press Tab until it says XW, then hold Shift and tap the right arrow four times.',
        headset: 'Click the left stick until the arm instrument says XW, then flick the left stick sideways four times.',
        teaches: 'It turns inside out on the way. That is normal, and it is a loop, not a fall.',
        done: 'Four quarter turns and it is exactly back where it started. On the way '
            + 'it passed through itself and came out inside-out, and nothing was broken '
            + 'when it did. A turn through the fourth dimension is a loop, not a fall.',
        begin: () => {
          panorama.setMode('projection');
          panorama.view.reset();
          this.tesseractVisible = true;
          this.snapsDone = 0;
        },
        tick: () => { /* snaps are counted from outside, by noteSnap() */ },
        passed: () => this.snapsDone >= 4,
        progress: () => `${this.snapsDone} of 4 quarter turns`,
        end: () => { this.tesseractVisible = false; },
      },

      {
        // ---- 4. FIND IT AGAIN. The examination. --------------------------
        title: 'Lesson 4 of 5: follow one bead through the turn',
        screen: 'Watch bead {NAME}. The gym will turn everything through the fourth dimension. Then click the bead that was {NAME}.',
        headset: 'Watch bead {NAME}. The gym will turn everything through the fourth dimension. Then point at the bead that was {NAME} and pull the trigger.',
        teaches: 'This is the skill. Almost nobody has it, and you now do.',
        done: 'That was the right bead. You just followed an object through a turn in a '
            + 'direction that does not exist in the room you are sitting in. Almost '
            + 'nobody can do that. You can.',
        wrong: 'Not that one. It is genuinely hard, and getting it wrong is the normal '
            + 'first answer. Watch it again, slower this time.',
        begin: () => {
          panorama.setMode('projection');
          panorama.view.reset();
          this.markedVisible = true;
          this.markedAnswer = -1;
          this.markedTarget = Math.floor(Math.random() * this.markedCount);
          this.phase = 'look';
          this.phaseTime = 0;
          // Slower every time it is failed. Failing must feel like a gentle
          // replay, never like a punishment (part-05.md 5.7 lesson 4).
          this.tourSeconds = 4 + this.attempts * 2.5;
          this.hyperTour = null;
        },
        tick: (deltaMs) => {
          this.phaseTime += deltaMs;
          if (this.phase === 'look' && this.phaseTime > 2600) {
            this.phase = 'turning';
            this.phaseTime = 0;
            // A single hyper-rotation, chosen at random, performed slowly by
            // the gym itself so the reader can just watch.
            this.hyperTour = {
              plane: HYPER_PLANES[Math.floor(Math.random() * HYPER_PLANES.length)],
              remaining: (Math.PI / 2) * (Math.random() < 0.5 ? 1 : -1),
              total: this.tourSeconds * 1000,
              done: 0,
            };
          }
          if (this.phase === 'turning' && this.hyperTour) {
            const tour = this.hyperTour;
            const step = Math.min(deltaMs, tour.total - tour.done);
            panorama.view.rotate(tour.plane, tour.remaining * (step / tour.total));
            tour.done += step;
            if (tour.done >= tour.total) { this.phase = 'answer'; this.phaseTime = 0; }
          }
        },
        // Labels are hidden during and after the turn: that is what makes it a
        // test of tracking rather than of reading.
        passed: () => this.markedAnswer >= 0 && this.markedAnswer === this.markedTarget,
        failed: () => this.markedAnswer >= 0 && this.markedAnswer !== this.markedTarget,
        progress: () => {
          if (this.phase === 'look') return `keep your eye on ${this.markedNames[this.markedTarget]}`;
          if (this.phase === 'turning') return 'turning through the fourth dimension...';
          return 'now: which one was it?';
        },
        end: () => { this.markedVisible = false; this.hyperTour = null; },
      },

      {
        // ---- 5. THE TWIST. Optional, and the reward. ---------------------
        title: 'Lesson 5 of 5: two turns at once (optional)',
        screen: 'Hold Shift and drag DIAGONALLY, in circles. Up and down turns one plane; '
              + 'left and right turns a completely separate one AT THE SAME TIME. Watch it: '
              + 'it never comes back to the same shape. Then press Home.',
        headset: 'Squeeze BOTH hands and turn them against each other. Your two hands together '
               + 'reach turns that one hand cannot. Then open the menu and choose Reset.',
        teaches: 'Two separate turns at once. Only four dimensions allow that.',
        done: 'That is the one motion with no three-dimensional imitation at all. In three '
            + 'dimensions any two turns share an axis, so they always add up to one ordinary '
            + 'turn. In four dimensions those two planes share nothing, so both happen for '
            + 'real at the same time and the shape never repeats. In the headset your two '
            + 'hands do this together, and it is now unlocked for you.',
        optional: true,
        begin: () => {
          panorama.setMode('projection');
          panorama.view.reset();
          this.tesseractVisible = true;
          this.planesUsed = new Set();
          this.twisted = 0;
          this.resetAfter = false;
        },
        tick: () => { /* counted from outside, by noteHyperRotation and noteTwist */ },
        passed: () => (this.planesUsed.size >= 2 || this.twisted > 0.6) && this.resetAfter,
        progress: () => {
          const part = this.twisted > 0.6
            ? 'twisted'
            : `${this.planesUsed.size} of 2 planes used`;
          return this.resetAfter ? 'done' : `${part}, then reset the view`;
        },
        end: () => {
          this.tesseractVisible = false;
          this.tier2Offered = true;
        },
      },
    ];
  }

  // ---------------------------------------------------------------------------
  // RUNNING
  // ---------------------------------------------------------------------------

  start(fromLesson = 0) {
    this.active = true;
    this.group.visible = true;
    this.panorama.showGraph = false;
    this.panorama.showTesseract = false;
    this.beadsVisible = false;
    this.tesseractVisible = false;
    this.markedVisible = false;
    this.attempts = 0;
    this.enterLesson(fromLesson);
  }

  enterLesson(index) {
    if (this.lesson && this.lesson.end) this.lesson.end();
    this.lessonIndex = index;
    if (index >= this.lessons.length) { this.finish(); return; }
    this.lesson = this.lessons[index];
    this.lessonTime = 0;
    this.passedTime = 0;
    this.state = 'doing';
    // Every lesson but the first starts from the canonical view, so a stray
    // turn made at the end of one lesson cannot quietly ruin the next one.
    // Nir hit exactly that: "maybe it is because I did another rotation by
    // mistake from the previous lesson".
    if (index > 0) this.panorama.view.reset();
    // And put the camera back too, so that a lesson can never begin with the
    // reader accidentally parked inside the object from the lesson before.
    if (index > 0) this.hooks.resetCamera?.();
    this.lesson.begin();
    this.hooks.onLesson?.(this.describe());
  }

  /** Skip the current lesson. Always available, in both bodies. */
  skipLesson() {
    if (!this.active) return;
    this.enterLesson(this.lessonIndex + 1);
  }

  /** Leave the gym entirely, right now, without finishing. */
  quit() {
    if (!this.active) return;
    if (this.lesson && this.lesson.end) this.lesson.end();
    this.lesson = null;
    this.active = false;
    this.group.visible = false;
    this.panorama.showGraph = true;
    this.panorama.showTesseract = true;
    this.panorama.resetView();
    this.hooks.onDone?.({ graduated: false });
  }

  finish() {
    rememberGraduation();
    this.lesson = null;
    this.active = false;
    this.group.visible = false;
    this.panorama.showGraph = true;
    this.panorama.showTesseract = true;
    // Graduation drops the reader into slice mode at w = 0, among the
    // established news, which is exactly where every session begins
    // (part-05.md 5.7, and 5.2 mode 1).
    this.panorama.resetView();
    this.hooks.onDone?.({ graduated: true, tier2: this.tier2Offered });
  }

  /** What the instructions should say right now, for either body. */
  describe() {
    if (!this.lesson) return null;
    const name = this.markedNames[this.markedTarget];
    const last = this.lessonIndex === this.lessons.length - 1;
    return {
      index: this.lessonIndex,
      count: this.lessons.length,
      title: this.lesson.title,
      screen: this.lesson.screen.replace(/\{NAME\}/g, name),
      headset: this.lesson.headset.replace(/\{NAME\}/g, name),
      teaches: this.lesson.teaches,
      optional: !!this.lesson.optional,
      progress: this.lesson.progress ? this.lesson.progress() : '',
      state: this.state,
      // What the reader sees the moment the task is done. It must say what
      // actually happened, because "the colour changed and I did not
      // understand what happened" is a failure of explanation, not of the
      // reader.
      done: this.state === 'passed' ? (this.lesson.done ?? 'Done.') : '',
      wrong: this.state === 'failed' ? (this.lesson.wrong ?? 'Not that one.') : '',
      nextLabel: this.state === 'passed'
        ? (last ? 'Finish' : 'Next lesson')
        : 'Skip this one',
      isLast: last,
    };
  }

  // ---- things the controls tell the gym about --------------------------------

  noteSnap() { if (this.active && this.lesson === this.lessons[2]) this.snapsDone++; }

  noteHyperRotation(plane, radians) {
    if (!this.active || this.lesson !== this.lessons[4]) return;
    if (Math.abs(radians) > 0.02) this.planesUsed.add(plane);
  }

  noteTwist(amount) {
    if (!this.active || this.lesson !== this.lessons[4]) return;
    this.twisted += amount;
  }

  noteReset() {
    if (this.active && this.lesson === this.lessons[4]) this.resetAfter = true;
  }

  /**
   * The reader pointed at something. Returns true if the gym consumed it, so
   * that the ordinary graph picking stays out of the way during a lesson.
   */
  notePick(roomPoint) {
    if (!this.active || !this.markedVisible || this.phase !== 'answer') return false;
    let best = -1, bestDistance = Infinity;
    const scratch = new THREE.Vector3();
    for (let i = 0; i < this.markedCount; i++) {
      this.panorama.toRoomSpace(this.markedSet.out3, i, scratch);
      const distance = scratch.distanceTo(roomPoint);
      if (distance < bestDistance) { bestDistance = distance; best = i; }
    }
    if (best < 0 || bestDistance > 0.25) return false;
    this.markedAnswer = best;
    return true;
  }

  /** Which bead is nearest a pointing ray, in room space. For the cursor. */
  beadUnderRay(origin, direction) {
    if (!this.active || !this.markedVisible) return -1;
    const scratch = new THREE.Vector3();
    let best = -1, bestScore = Infinity;
    for (let i = 0; i < this.markedCount; i++) {
      this.panorama.toRoomSpace(this.markedSet.out3, i, scratch);
      scratch.sub(origin);
      const along = scratch.dot(direction);
      if (along <= 0.05) continue;
      const sideways = Math.sqrt(Math.max(0, scratch.lengthSq() - along * along));
      if (sideways > 0.09) continue;
      if (sideways < bestScore) { bestScore = sideways; best = i; }
    }
    return best;
  }

  // ---------------------------------------------------------------------------
  // EVERY FRAME
  // ---------------------------------------------------------------------------

  update(deltaMs) {
    if (!this.active || !this.lesson) return;
    this.lessonTime += deltaMs;

    // Once a verdict is in, the lesson freezes and waits for the reader. Its
    // tick stops running too, so nothing keeps moving under their hands while
    // they read what just happened.
    if (this.state === 'doing') {
      this.lesson.tick?.(deltaMs);

      if (this.lesson.failed?.()) {
        this.state = 'failed';
        this.attempts++;
      } else if (this.lesson.passed()) {
        this.passedTime += deltaMs;
        if (this.passedTime >= (this.lesson.holdFor ?? 0)) {
          this.state = 'passed';
          this.attempts = 0;
        }
      } else {
        this.passedTime = 0;
      }
    }

    this.hooks.onLesson?.(this.describe());
  }

  /** The reader pressed Next. The only way forward. */
  goNext() {
    if (!this.active) return;
    this.enterLesson(this.lessonIndex + 1);
  }

  /** The reader pressed Back. Always allowed, including from the first lesson. */
  goBack() {
    if (!this.active) return;
    if (this.lessonIndex <= 0) { this.enterLesson(0); return; }
    this.enterLesson(this.lessonIndex - 1);
  }

  /** After a wrong answer: watch it again, more slowly. */
  retry() {
    if (!this.active) return;
    this.enterLesson(this.lessonIndex);
  }

  /**
   * Put the toys where the projection says they are. Called AFTER the scene's
   * one projection pass, never before, so the toys and the graph can never
   * disagree about where the fourth dimension currently points.
   */
  draw() {
    // Lesson 2's ladder.
    if (this.beadsVisible) {
      for (let i = 0; i < this.ladderCount; i++) {
        const isTarget = i === this.ladderTarget;
        // Beads outside the slice fade to ghosts rather than vanishing, which is
        // the very lesson being taught here.
        const distance = Math.abs(this.ladderSet.outW[i] - this.panorama.w0);
        const inside = distance <= this.panorama.epsilon * 0.5;
        const visible = inside ? 1 : Math.max(0.12, 1 - distance);
        if (isTarget) this.ladderBeads.setColour(i, 1.0, 0.83, 0.35);
        else this.ladderBeads.setColour(i, 0.42, 0.52, 0.68);
        this.ladderBeads.placePoint(i,
          this.ladderSet.out3[i * 3], this.ladderSet.out3[i * 3 + 1], this.ladderSet.out3[i * 3 + 2],
          (isTarget ? 0.062 : 0.045) * this.ladderSet.outScale[i], visible);
      }
      this.ladderBeads.finish(this.ladderCount);
    } else {
      this.ladderBeads.finish(0);
    }

    // Lessons 3 and 5: the gym's own tesseract.
    if (this.tesseractVisible) {
      const vertices = this.tesseract.vertices.length;
      for (let i = 0; i < vertices; i++) {
        this.tesseractNodes.placePoint(i,
          this.tesseractSet.out3[i * 3], this.tesseractSet.out3[i * 3 + 1], this.tesseractSet.out3[i * 3 + 2],
          0.024 * this.tesseractSet.outScale[i], 1);
      }
      this.tesseractNodes.finish(vertices);
      this.tesseract.edges.forEach(([a, b], e) => {
        this.tesseractEdges.placeSegment(e,
          this.tesseractSet.out3[a * 3], this.tesseractSet.out3[a * 3 + 1], this.tesseractSet.out3[a * 3 + 2],
          this.tesseractSet.out3[b * 3], this.tesseractSet.out3[b * 3 + 1], this.tesseractSet.out3[b * 3 + 2],
          0.006 * (this.tesseractSet.outScale[a] + this.tesseractSet.outScale[b]) * 0.5, 1);
      });
      this.tesseractEdges.finish(this.tesseract.edges.length);
    } else {
      this.tesseractNodes.finish(0);
      this.tesseractEdges.finish(0);
    }

    // Lesson 4: the six beads. Labels show only while looking, never during or
    // after the turn: otherwise it is a reading test, not a tracking test.
    if (this.markedVisible) {
      const showLabels = this.phase === 'look';
      for (let i = 0; i < this.markedCount; i++) {
        const isTarget = i === this.markedTarget;
        const highlight = showLabels && isTarget;
        if (highlight) this.markedBeads.setColour(i, 1.0, 0.83, 0.35);
        else this.markedBeads.setColour(i, 0.62, 0.72, 0.88);
        this.markedBeads.placePoint(i,
          this.markedSet.out3[i * 3], this.markedSet.out3[i * 3 + 1], this.markedSet.out3[i * 3 + 2],
          0.055 * this.markedSet.outScale[i], 1);
        const label = isTarget ? this.markedTargetLabels[i] : this.markedLabels[i];
        const other = isTarget ? this.markedLabels[i] : this.markedTargetLabels[i];
        other.visible = false;
        label.visible = showLabels;
        if (showLabels) {
          label.position.set(
            this.markedSet.out3[i * 3],
            this.markedSet.out3[i * 3 + 1] + (isTarget ? 0.11 : 0.085),
            this.markedSet.out3[i * 3 + 2]);
        }
      }
      this.markedBeads.finish(this.markedCount);
    } else {
      this.markedBeads.finish(0);
      this.markedLabels.forEach((label) => { label.visible = false; });
      this.markedTargetLabels.forEach((label) => { label.visible = false; });
    }
  }
}
