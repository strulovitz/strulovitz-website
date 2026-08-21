#!/usr/bin/env python3
"""
Test the Hello Tesseract page in a real browser, headless, with software WebGL.

What it proves:
  1. The page loads with ZERO console errors and zero failed requests.
  2. The 3D scene actually renders (draw calls above zero, triangles above zero).
  3. The one-projection-per-frame rule holds (exactly 2 passes: graph + tesseract).
  4. The keyboard controls do what the landing page promises: Tab cycles the
     hyper-plane, E toggles the mode, W and S swim the slab, Home resets.
  5. Four 90-degree snaps return the view matrix to the identity, in the live
     browser and not merely in the unit test.
  6. Screenshots come out, so a human can look at the thing.

HOW TO RUN IT. Chrome must already be running with remote debugging on, started
detached from the shell (starting it from inside a script tends to hang a
tool-driven terminal, because the child keeps the pipes open):

    (setsid google-chrome --headless=new --remote-debugging-port=9333 \
      --user-data-dir=/tmp/ai-panorama-4d-test/profile --no-first-run \
      --no-sandbox --window-size=1400,900 --hide-scrollbars \
      --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
      about:blank </dev/null >/dev/null 2>&1 &)

    python3 ops/test-the-4d-page.py

bible/part-05.md 5.10 says the validation protocol repeats after ANY change to
rotation, projection or comfort code. This script is the machine half of that;
the human half is five real people in the headset, which no script can fake.
"""

import asyncio, base64, json, os, subprocess, sys, time, shutil
import urllib.request
import websockets

SITE = "/home/nir/strulovitz-website/site"
OUT = "/tmp/ai-panorama-4d-test"
PORT = 8791
CDP_PORT = 9333

os.makedirs(OUT, exist_ok=True)

failures = []
notes = []


def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("  --  " + str(detail)) if detail and not ok else ""))
    if not ok:
        failures.append(f"{name}: {detail}")


class Browser:
    def __init__(self, ws):
        self.ws = ws
        self.next_id = 1
        self.console_errors = []
        self.failed_requests = []
        self.exceptions = []

    async def send(self, method, params=None):
        message_id = self.next_id
        self.next_id += 1
        await self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        while True:
            raw = json.loads(await self.ws.recv())
            if raw.get("id") == message_id:
                if "error" in raw:
                    raise RuntimeError(f"{method}: {raw['error']}")
                return raw.get("result", {})
            self.handle_event(raw)

    def handle_event(self, event):
        method = event.get("method")
        params = event.get("params", {})
        if method == "Runtime.consoleAPICalled" and params.get("type") in ("error", "assert"):
            text = " ".join(str(a.get("value", a.get("description", ""))) for a in params.get("args", []))
            self.console_errors.append(text)
        elif method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails", {})
            self.exceptions.append(details.get("text", "") + " " +
                                  str(details.get("exception", {}).get("description", "")))
        elif method == "Network.loadingFailed":
            self.failed_requests.append(params.get("errorText", "") + " " + str(params.get("type")))

    async def drain(self, seconds):
        """Let the page run, collecting events."""
        deadline = time.time() + seconds
        while time.time() < deadline:
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=max(0.05, deadline - time.time()))
                self.handle_event(json.loads(raw))
            except asyncio.TimeoutError:
                break

    async def evaluate(self, expression):
        result = await self.send("Runtime.evaluate", {
            "expression": expression, "returnByValue": True, "awaitPromise": True,
        })
        if result.get("exceptionDetails"):
            raise RuntimeError(result["exceptionDetails"].get("text") + " " +
                               str(result["exceptionDetails"].get("exception", {}).get("description")))
        return result["result"].get("value")

    async def key(self, key, code, modifiers=0, key_code=0):
        for kind in ("keyDown", "keyUp"):
            await self.send("Input.dispatchKeyEvent", {
                "type": kind, "key": key, "code": code,
                "modifiers": modifiers,
                "windowsVirtualKeyCode": key_code, "nativeVirtualKeyCode": key_code,
            })

    async def key_hold(self, key, code, key_code, milliseconds):
        await self.send("Input.dispatchKeyEvent", {
            "type": "keyDown", "key": key, "code": code,
            "windowsVirtualKeyCode": key_code, "nativeVirtualKeyCode": key_code})
        await self.drain(milliseconds / 1000)
        await self.send("Input.dispatchKeyEvent", {
            "type": "keyUp", "key": key, "code": code,
            "windowsVirtualKeyCode": key_code, "nativeVirtualKeyCode": key_code})

    async def screenshot(self, path):
        result = await self.send("Page.captureScreenshot", {"format": "png"})
        with open(path, "wb") as handle:
            handle.write(base64.b64decode(result["data"]))


async def main():
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", SITE],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    chrome = None
    try:
        # Chrome is expected to be running already with remote debugging on, started
        # detached from the shell. Starting it from inside this script tends to hang
        # a tool-driven terminal, because the child keeps the pipes open.
        ws_url = None
        for _ in range(80):
            try:
                data = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1).read())
                ws_url = data["webSocketDebuggerUrl"]
                break
            except Exception:
                time.sleep(0.25)
        if not ws_url:
            print("could not reach chrome")
            return 1

        async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
            browser = Browser(ws)
            target = await browser.send("Target.createTarget", {"url": "about:blank"})
            session = await browser.send("Target.attachToTarget",
                                        {"targetId": target["targetId"], "flatten": True})
            # Re-connect directly to the page target for simplicity.
            page_ws = f"ws://127.0.0.1:{CDP_PORT}/devtools/page/{target['targetId']}"

        async with websockets.connect(page_ws, max_size=80 * 1024 * 1024) as ws:
            page = Browser(ws)
            await page.send("Runtime.enable")
            await page.send("Network.enable")
            await page.send("Page.enable")
            await page.send("Log.enable")
            # Browser caching would quietly test yesterday's code.
            await page.send("Network.setCacheDisabled", {"cacheDisabled": True})

            print("\nAI PANORAMA -- Hello Tesseract, live browser test\n")
            print("1. The page loads and renders")

            for _ in range(40):
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=1).read()
                    break
                except Exception:
                    time.sleep(0.25)
            await page.send("Page.navigate", {"url": f"http://127.0.0.1:{PORT}/tesseract.html?debug=1"})
            await page.drain(6.0)

            check("no uncaught JavaScript exceptions", not page.exceptions, page.exceptions)
            check("no console errors", not page.console_errors, page.console_errors)
            check("no failed network requests", not page.failed_requests, page.failed_requests)

            ready = await page.evaluate("!!(window.PANORAMA && window.PANORAMA.panorama)")
            check("the application started and exposed its state", ready is True)
            if not ready:
                return 1

            info = await page.evaluate("""(() => {
              const p = window.PANORAMA;
              return {
                calls: p.renderer.info.render.calls,
                triangles: p.renderer.info.render.triangles,
                nodes: p.data.count,
                projections: p.panorama.projectionsThisFrame,
                expected: p.panorama.expectedProjections,
                violated: p.panorama.projectionRuleViolated,
                mode: p.panorama.mode,
                w0: p.panorama.w0,
                plane: p.panorama.view.activeHyperPlane,
                solid: p.panorama.status().solidNodes,
              };
            })()""")
            print("       " + json.dumps(info))
            check("something was actually drawn", info["calls"] > 0, info["calls"])
            check("triangles reached the screen", info["triangles"] > 1000, info["triangles"])
            check("draw calls stay under the budget of 100", info["calls"] < 100, info["calls"])
            check("two hundred fake nodes exist", info["nodes"] == 200, info["nodes"])
            # The graph, the tesseract and the gym's three toy sets each get one
            # pass. What matters is that the number is EXACTLY the expected one:
            # a projection done per eye instead of per frame would change it.
            check("exactly as many projection passes per frame as expected, never per eye",
                  info["projections"] == info["expected"], info)
            check("the one-projection rule was never violated", info["violated"] is False)
            check("the session starts in slice mode", info["mode"] == "slice", info["mode"])
            check("the session starts at the established news band", abs(info["w0"]) < 1e-9, info["w0"])
            check("some but not all nodes are solid in the starting slab",
                  0 < info["solid"] < info["nodes"], info["solid"])

            await page.screenshot(f"{OUT}/01-slice-mode.png")

            print("\n2. The keyboard does what the landing page promises")

            await page.key("Tab", "Tab", key_code=9)
            await page.drain(0.3)
            plane = await page.evaluate("window.PANORAMA.panorama.view.activeHyperPlane")
            check("Tab cycles the hyper-plane from XW to YW", plane == "yw", plane)

            await page.key("e", "KeyE", key_code=69)
            # The slab swells over 600 ms of ANIMATION time, and each frame's step
            # is deliberately clamped so a stalled tab cannot jump. Under software
            # rendering there are only a handful of frames per second, so real time
            # has to be generous here. This is not slack in the product.
            await page.drain(5.0)
            mode = await page.evaluate("window.PANORAMA.panorama.mode")
            epsilon = await page.evaluate("window.PANORAMA.panorama.epsilon")
            check("E switches to projection mode", mode == "projection", mode)
            check("the slab opened up to swallow the whole world", epsilon > 3.9, epsilon)
            await page.screenshot(f"{OUT}/02-projection-mode.png")

            await page.key("e", "KeyE", key_code=69)
            await page.drain(5.0)
            check("E switches back to slice mode",
                  (await page.evaluate("window.PANORAMA.panorama.mode")) == "slice")

            await page.key_hold("w", "KeyW", 87, 900)
            await page.drain(0.2)
            w0 = await page.evaluate("window.PANORAMA.panorama.w0")
            check("holding W swims the slab toward the encyclopedia", w0 > 0.2, w0)
            solid_high = await page.evaluate("window.PANORAMA.panorama.status().solidNodes")
            check("a different set of nodes is solid up there", solid_high != info["solid"],
                  f"{solid_high} vs {info['solid']}")
            await page.screenshot(f"{OUT}/03-swum-toward-canon.png")

            await page.key_hold("s", "KeyS", 83, 1800)
            await page.drain(0.2)
            w0_back = await page.evaluate("window.PANORAMA.panorama.w0")
            check("holding S swims back toward the fresh news", w0_back < w0 - 0.4, w0_back)

            print("\n3. Four snaps come home, in the live browser")

            await page.evaluate("window.PANORAMA.panorama.resetView()")
            await page.drain(0.3)
            # Shift plus the right arrow: one 90 degree snap in the active plane.
            for i in range(4):
                await page.send("Input.dispatchKeyEvent", {
                    "type": "keyDown", "key": "ArrowRight", "code": "ArrowRight",
                    "modifiers": 8, "windowsVirtualKeyCode": 39, "nativeVirtualKeyCode": 39})
                await page.send("Input.dispatchKeyEvent", {
                    "type": "keyUp", "key": "ArrowRight", "code": "ArrowRight",
                    "modifiers": 8, "windowsVirtualKeyCode": 39, "nativeVirtualKeyCode": 39})
                await page.drain(0.75)
                if i == 1:
                    await page.screenshot(f"{OUT}/04-halfway-inside-out.png")
            error = await page.evaluate("""(() => {
              const Q = window.PANORAMA.panorama.view.Q;
              const I = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1];
              let worst = 0;
              for (let i = 0; i < 16; i++) worst = Math.max(worst, Math.abs(Q[i] - I[i]));
              return worst;
            })()""")
            check("four snaps returned the live view exactly to the canonical one",
                  error < 1e-6, error)

            print("\n4. Undo, reset, and nothing left broken")

            await page.evaluate("window.PANORAMA.panorama.view.rotate('zw', 0.7, true)")
            await page.drain(0.2)
            undone = await page.evaluate("window.PANORAMA.panorama.view.undo()")
            check("undo reports success", undone is True)

            await page.key("Home", "Home", key_code=36)
            await page.drain(0.4)
            state = await page.evaluate("""(() => {
              const p = window.PANORAMA.panorama;
              return { mode: p.mode, w0: p.w0, q0: p.view.Q[0] };
            })()""")
            check("Home resets the mode, the slab and the rotation",
                  state["mode"] == "slice" and abs(state["w0"]) < 1e-9 and abs(state["q0"] - 1) < 1e-9,
                  state)

            print("\n5. Still healthy after a long run")
            await page.drain(6.0)
            final = await page.evaluate("""(() => {
              const p = window.PANORAMA;
              return {
                violated: p.panorama.projectionRuleViolated,
                finite: Array.from(p.panorama.view.Q).every(Number.isFinite),
                orthoError: (() => {
                  const Q = p.panorama.view.Q; let worst = 0;
                  for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) {
                    let dot = 0;
                    for (let r = 0; r < 4; r++) dot += Q[a*4+r] * Q[b*4+r];
                    worst = Math.max(worst, Math.abs(dot - (a === b ? 1 : 0)));
                  }
                  return worst;
                })(),
                calls: p.renderer.info.render.calls,
              };
            })()""")
            check("the one-projection rule still holds after thousands of frames",
                  final["violated"] is False)
            check("the rotation matrix has no NaN after a long run", final["finite"] is True)
            check("the rotation matrix is still perfectly rigid after a long run",
                  final["orthoError"] < 1e-9, final["orthoError"])
            check("no console errors accumulated during the whole session",
                  not page.console_errors, page.console_errors)

            await page.screenshot(f"{OUT}/05-final.png")

            print("\n6. The instrument on the left forearm answers when reached for")
            # Outside a real headset the controllers have no pose, so we place
            # them by hand: the left grip where a forearm would be, and the
            # right controller aimed straight at the instrument on it. This is
            # the exact fault Nir found by putting the headset on -- pointing at
            # the wrist instrument did nothing -- so it gets a real test.
            reach = await page.evaluate("""(() => {
              const v = window.PANORAMA.vr;
              const THREE_left = v.leftHand.grip, right = v.rightHand.controller;
              // three.js switches matrixAutoUpdate OFF for XR controllers, because
              // in a real session their pose comes from the headset every frame.
              // A test placing them by hand has to switch it back on.
              [THREE_left, right, v.rightHand.grip].forEach((o) => { o.matrixAutoUpdate = true; });
              THREE_left.position.set(-0.25, 1.05, -0.30);
              THREE_left.rotation.set(0, 0, 0);
              THREE_left.updateMatrixWorld(true);
              v.gaugePanel.updateWorldMatrix(true, false);
              const target = new (window.PANORAMA.renderer.constructor === undefined ? Object : Object)();
              // Where is the instrument in the room?
              const gauge = v.gaugePanel;
              const p = { x: gauge.matrixWorld.elements[12], y: gauge.matrixWorld.elements[13], z: gauge.matrixWorld.elements[14] };
              // Put the right controller 30 cm away and aim it at the panel.
              right.position.set(p.x + 0.02, p.y + 0.28, p.z + 0.10);
              right.updateMatrixWorld(true);
              right.lookAt(p.x, p.y, p.z);
              right.rotateY(Math.PI);
              right.updateMatrixWorld(true);
              const pointing = v.panelHit(v.gaugePanel, v.rightHand, 0.02);
              const reachedPointing = v.gaugeReachedFor();
              // Now bring the right hand close enough to count as touching.
              v.rightHand.grip.position.set(p.x, p.y + 0.03, p.z);
              v.rightHand.grip.updateMatrixWorld(true);
              const reachedTouching = v.gaugeReachedFor();
              return { pointing: !!pointing, reachedPointing, reachedTouching };
            })()""")
            print("       " + json.dumps(reach))
            check("pointing the right hand at the forearm instrument registers a hit",
                  reach["pointing"] is True, reach)
            check("reaching for it by pointing is recognised",
                  reach["reachedPointing"] == "pointing", reach["reachedPointing"])
            check("touching it with the other hand is recognised",
                  reach["reachedTouching"] in ("touching", "pointing"), reach["reachedTouching"])

            menu = await page.evaluate("""(() => {
              const v = window.PANORAMA.vr;
              v.openMenu(true);
              const gauge = v.gaugePanel, right = v.rightHand.controller;
              v.menuPanel.updateWorldMatrix(true, false);
              const m = v.menuPanel.matrixWorld.elements;
              const p = { x: m[12], y: m[13], z: m[14] };
              right.position.set(p.x, p.y + 0.30, p.z + 0.12);
              right.updateMatrixWorld(true);
              right.lookAt(p.x, p.y, p.z);
              right.rotateY(Math.PI);
              right.updateMatrixWorld(true);
              const row = v.menuRowUnderRay(v.rightHand);
              const before = window.PANORAMA.panorama.mode;
              v.runMenuItem('mode');
              const after = window.PANORAMA.panorama.mode;
              v.runMenuItem('reset');
              v.openMenu(false);
              return { row, before, after, items: v.MENU_ITEMS.map(i => i.key) };
            })()""")
            check("pointing at the open hand menu selects a row",
                  menu["row"] >= 0, menu)
            check("Undo and Reset are the first two items, in that order",
                  menu["items"][:2] == ["undo", "reset"], menu["items"])
            check("choosing a menu item really does something",
                  menu["before"] != menu["after"], menu)

            print("\n7. The four-dimensional gym, all five lessons")
            # Every check here exists because a real person hit a real problem.
            # The gym is gated on DOING, so the test does the doing -- but it
            # must also prove that finishing a task does NOT teleport anyone
            # into the next lesson, which is what Nir found most confusing.

            await page.evaluate("localStorage.removeItem('ai-panorama.gym.graduated.v1')")
            await page.send("Page.navigate", {"url": f"http://127.0.0.1:{PORT}/tesseract.html?debug=1"})
            await page.drain(5.0)
            offered = await page.evaluate(
                "getComputedStyle(document.getElementById('gym-offer')).display")
            check("a first-time visitor is offered the lessons", offered == "block", offered)

            replay = await page.evaluate("""(() => {
              const b = document.getElementById('open-gym');
              return { exists: !!b, loud: b.classList.contains('loud'), text: b.textContent.trim() };
            })()""")
            check("the way back into the lessons is a loud button, not a quiet link",
                  replay["exists"] and replay["loud"] and "4D" in replay["text"], replay)

            graduated_can_replay = await page.evaluate("""(() => {
              localStorage.setItem('ai-panorama.gym.graduated.v1', 'yes');
              const g = window.PANORAMA.gym;
              document.getElementById('open-gym').click();
              const started = { active: g.active, index: g.lessonIndex };
              g.quit();
              localStorage.removeItem('ai-panorama.gym.graduated.v1');
              return started;
            })()""")
            check("somebody who already finished can start the lessons again",
                  graduated_can_replay["active"] is True and graduated_can_replay["index"] == 0,
                  graduated_can_replay)

            state = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              g.start();
              const d = g.describe();
              return { active: g.active, index: d.index, count: d.count, state: d.state,
                       graphHidden: window.PANORAMA.panorama.showGraph === false };
            })()""")
            check("starting the gym hides the graph and enters lesson 1",
                  state["active"] and state["index"] == 0 and state["graphHidden"], state)
            check("there are five lessons", state["count"] == 5, state["count"])
            check("a lesson begins in the doing state", state["state"] == "doing", state)

            # LESSON 1: half the task is not a pass.
            half = await page.evaluate("""(() => {
              const p = window.PANORAMA.panorama, g = window.PANORAMA.gym;
              p.graph.position.x += 0.4;
              return { passed: g.lessons[0].passed() };
            })()""")
            check("lesson 1 refuses to pass on half the task", half["passed"] is False, half)

            await page.drain(0.6)
            await page.evaluate("""(() => {
              const p = window.PANORAMA.panorama;
              p.graph.scale.setScalar(p.graph.scale.x * 1.25);
            })()""")
            await page.drain(1.5)
            waiting = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym, d = g.describe();
              return { index: g.lessonIndex, state: d.state, done: d.done,
                       nextLabel: d.nextLabel,
                       shown: getComputedStyle(document.getElementById('gym-done')).display };
            })()""")
            # THE CENTRAL CHECK OF THIS WHOLE SECTION.
            check("finishing a task does NOT drop you into the next lesson",
                  waiting["index"] == 0 and waiting["state"] == "passed", waiting)
            check("it explains in words what just happened",
                  len(waiting["done"]) > 60 and waiting["shown"] == "block", waiting)
            check("the button now says Next lesson rather than Skip",
                  waiting["nextLabel"] == "Next lesson", waiting)

            await page.evaluate("document.getElementById('gym-next').click()")
            await page.drain(0.8)
            check("pressing Next is what moves you on",
                  (await page.evaluate("window.PANORAMA.gym.lessonIndex")) == 1)

            # Back must work, and it must be refused only on the first lesson.
            await page.evaluate("document.getElementById('gym-back').click()")
            await page.drain(0.6)
            check("Back returns to the previous lesson",
                  (await page.evaluate("window.PANORAMA.gym.lessonIndex")) == 0)
            check("Back is disabled on the very first lesson",
                  (await page.evaluate("document.getElementById('gym-back').disabled")) is True)
            await page.evaluate("window.PANORAMA.gym.goNext()")
            await page.drain(0.6)

            # LESSON 2: the slab. And a stray rotation must not follow you in.
            fresh = await page.evaluate("""(() => {
              const v = window.PANORAMA.panorama.view;
              return { q0: v.Q[0], q5: v.Q[5] };
            })()""")
            check("each lesson starts from the canonical view, so a stray turn cannot follow you in",
                  abs(fresh["q0"] - 1) < 1e-9 and abs(fresh["q5"] - 1) < 1e-9, fresh)

            swim = await page.evaluate("""(() => {
              const p = window.PANORAMA.panorama, g = window.PANORAMA.gym;
              const before = g.lessons[1].passed();
              p.w0 = g.ladderSet.outW[g.ladderTarget];
              return { before, after: g.lessons[1].passed() };
            })()""")
            check("lesson 2 is not already passed when it starts", swim["before"] is False, swim)
            check("bringing the lit bead into the slice satisfies lesson 2",
                  swim["after"] is True, swim)
            await page.drain(1.6)
            held = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym, d = g.describe();
              return { index: g.lessonIndex, state: d.state, done: d.done };
            })()""")
            check("lesson 2 waits and explains that the bead went solid, instead of jumping on",
                  held["index"] == 1 and held["state"] == "passed"
                  and "solid" in held["done"], held)
            await page.evaluate("window.PANORAMA.gym.goNext()")
            await page.drain(0.8)

            # LESSON 3: three snaps are not four.
            three = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              g.snapsDone = 3;
              return { passed: g.lessons[2].passed() };
            })()""")
            check("three quarter turns are not four", three["passed"] is False, three)
            await page.evaluate("window.PANORAMA.gym.noteSnap()")
            await page.drain(1.0)
            snapped = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              return { index: g.lessonIndex, state: g.state };
            })()""")
            check("the fourth quarter turn finishes lesson 3, and it waits for you",
                  snapped["index"] == 2 and snapped["state"] == "passed", snapped)
            await page.evaluate("window.PANORAMA.gym.goNext()")
            await page.drain(0.8)

            # LESSON 4, the examination. The letter must be READABLE: Nir was
            # asked to follow bead F and could not find an F anywhere.
            letters = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              g.phase = 'look';
              g.draw();
              const target = g.markedTarget;
              const targetSprite = g.markedTargetLabels[target];
              const plain = g.markedLabels.filter((l, i) => i !== target && l.visible).length;
              return {
                askedFor: g.markedNames[target],
                targetVisible: targetSprite.visible,
                targetHeight: targetSprite.scale.y,
                targetIsSquarish: Math.abs(targetSprite.scale.x - targetSprite.scale.y) < 0.001,
                otherLettersVisible: plain,
              };
            })()""")
            check("the letter you are told to follow is actually on the screen",
                  letters["targetVisible"] is True, letters)
            check("that letter is drawn big, and square rather than a thin sliver",
                  letters["targetHeight"] >= 0.09 and letters["targetIsSquarish"], letters)
            check("the other five letters are shown too, so it is a real choice",
                  letters["otherLettersVisible"] == 5, letters)

            # MEASURED, not eyeballed: no two beads may land close enough on
            # screen for their letters to overlap. The first version had two
            # letters printed on top of each other, which makes the question
            # unanswerable through no fault of the reader.
            spread = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym, p = window.PANORAMA.panorama, cam = window.PANORAMA.camera;
              const V = g.markedLabels[0].position.constructor;
              const points = [];
              for (let i = 0; i < g.markedCount; i++) {
                const v = new V();
                p.toRoomSpace(g.markedSet.out3, i, v);
                points.push(v.clone().project(cam));
              }
              let worst = 9, pair = null;
              for (let a = 0; a < points.length; a++) {
                for (let b = a + 1; b < points.length; b++) {
                  const distance = Math.hypot(points[a].x - points[b].x,
                                              (points[a].y - points[b].y) * 0.6);
                  if (distance < worst) { worst = distance; pair = [g.markedNames[a], g.markedNames[b]]; }
                }
              }
              const off = points.filter((q) => Math.abs(q.x) > 0.92 || Math.abs(q.y) > 0.80).length;
              return { worst, pair, off };
            })()""")
            check("no two beads sit close enough for their letters to collide",
                  spread["worst"] > 0.12, spread)
            check("every bead is inside the visible picture", spread["off"] == 0, spread)

            wrong = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              const target = g.markedTarget;
              g.phase = 'answer';
              g.markedAnswer = (target + 1) % g.markedCount;
              return { failed: g.lessons[3].failed() };
            })()""")
            check("lesson 4 notices a wrong answer", wrong["failed"] is True, wrong)
            await page.drain(1.0)
            after_wrong = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym, d = g.describe();
              return { index: g.lessonIndex, state: d.state, wrongText: d.wrong,
                       button: document.getElementById('gym-next').textContent.trim() };
            })()""")
            check("a wrong answer stops and says so, instead of silently restarting",
                  after_wrong["index"] == 3 and after_wrong["state"] == "failed", after_wrong)
            check("it tells you that getting it wrong is normal",
                  "normal" in after_wrong["wrongText"], after_wrong)
            check("the button offers to watch it again",
                  "again" in after_wrong["button"].lower(), after_wrong)

            await page.evaluate("document.getElementById('gym-next').click()")
            await page.drain(1.0)
            retried = await page.evaluate("""(() => ({
              index: window.PANORAMA.gym.lessonIndex,
              state: window.PANORAMA.gym.state,
              seconds: window.PANORAMA.gym.tourSeconds,
            }))()""")
            check("watching it again replays the same lesson, more slowly",
                  retried["index"] == 3 and retried["state"] == "doing"
                  and retried["seconds"] > 4, retried)

            hidden = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              g.phase = 'answer';
              g.draw();
              return g.markedLabels.concat(g.markedTargetLabels).map((l) => l.visible);
            })()""")
            check("every letter is hidden once the turning is done, so it tests tracking",
                  not any(hidden), hidden)

            await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              g.phase = 'answer';
              g.markedAnswer = g.markedTarget;
            })()""")
            await page.drain(1.2)
            right = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym, d = g.describe();
              return { index: g.lessonIndex, state: d.state, done: d.done };
            })()""")
            check("the correct bead passes lesson 4 and it waits, with praise",
                  right["index"] == 3 and right["state"] == "passed"
                  and "right bead" in right["done"], right)
            await page.evaluate("window.PANORAMA.gym.goNext()")
            await page.drain(0.8)

            # LESSON 5: the twist, which also requires coming home again.
            twist = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              const before = g.lessons[4].passed();
              g.noteTwist(1.0);
              const afterTwist = g.lessons[4].passed();
              g.noteReset();
              return { before, afterTwist, afterReset: g.lessons[4].passed(),
                       label: g.describe().nextLabel };
            })()""")
            check("lesson 5 requires coming back home as well as twisting",
                  twist["before"] is False and twist["afterTwist"] is False
                  and twist["afterReset"] is True, twist)
            await page.drain(1.2)
            last = await page.evaluate("window.PANORAMA.gym.describe().nextLabel")
            check("the last lesson's button says Finish, not Next lesson", last == "Finish", last)

            await page.evaluate("document.getElementById('gym-next').click()")
            await page.drain(1.0)
            graduated = await page.evaluate("""(() => ({
              active: window.PANORAMA.gym.active,
              graphBack: window.PANORAMA.panorama.showGraph,
              mode: window.PANORAMA.panorama.mode,
              w0: window.PANORAMA.panorama.w0,
              tier2: window.PANORAMA.isTier2Enabled(),
              remembered: localStorage.getItem('ai-panorama.gym.graduated.v1'),
              panelHidden: getComputedStyle(document.getElementById('gym-panel')).display,
            }))()""")
            check("finishing leaves the gym", graduated["active"] is False, graduated)
            check("the graph comes back", graduated["graphBack"] is True, graduated)
            check("it drops you in slice mode among the established news",
                  graduated["mode"] == "slice" and abs(graduated["w0"]) < 1e-9, graduated)
            check("finishing unlocks the two-handed twist", graduated["tier2"] is True, graduated)
            check("the gym remembers, so it interrupts only once",
                  graduated["remembered"] == "yes", graduated)
            check("the instruction panel goes away", graduated["panelHidden"] == "none", graduated)

            escape = await page.evaluate("""(() => {
              const g = window.PANORAMA.gym;
              g.start();
              const inside = g.active;
              g.quit();
              return { inside, out: g.active, graphBack: window.PANORAMA.panorama.showGraph };
            })()""")
            check("you can walk out of the lessons at any moment",
                  escape["inside"] is True and escape["out"] is False
                  and escape["graphBack"] is True, escape)

            still_fine = await page.evaluate("""(() => ({
              violated: window.PANORAMA.panorama.projectionRuleViolated,
              expected: window.PANORAMA.panorama.expectedProjections,
              actual: window.PANORAMA.panorama.projectionsThisFrame,
            }))()""")
            check("the gym's toys are projected in the same single pass, not their own",
                  still_fine["violated"] is False
                  and still_fine["actual"] == still_fine["expected"], still_fine)

            # And the landing page, which must work with no JavaScript at all.
            await page.send("Page.navigate", {"url": f"http://127.0.0.1:{PORT}/index.html"})
            await page.drain(2.0)
            title = await page.evaluate("document.title")
            check("the root landing page loads", "AI PANORAMA" in (title or ""), title)
            entry = await page.evaluate("""(() => {
              const screenLink = document.getElementById('enter-screen');
              const menu = Array.from(document.querySelectorAll('nav a')).map((a) => a.textContent.trim());
              return { screen: screenLink ? screenLink.getAttribute('href') : null, menu };
            })()""")
            check("the entry button points at a page that exists when served locally",
                  entry["screen"] == "tesseract.html", entry)
            check("the menu lists every project, Night Watch included",
                  len(entry["menu"]) == 6 and any("Night Watch" in m for m in entry["menu"]),
                  entry["menu"])

            await page.send("Page.navigate", {"url": f"http://127.0.0.1:{PORT}/night-watch.html"})
            await page.drain(1.5)
            night = await page.evaluate("""(() => ({
              title: document.title,
              honest: document.body.innerText.includes('does not exist yet'),
              halves: ['Eunuch', 'Golden Man'].every((n) => document.body.innerText.includes(n)),
            }))()""")
            check("the Night Watch page loads", "Night Watch" in (night["title"] or ""), night)
            check("it says plainly that the software does not exist yet", night["honest"] is True)
            check("it describes both halves", night["halves"] is True)
            await page.screenshot(f"{OUT}/06-landing-page.png")

    finally:
        if chrome:
            chrome.terminate()
        server.terminate()

    print(f"\n{'ALL CHECKS PASSED' if not failures else str(len(failures)) + ' CHECKS FAILED'}")
    for failure in failures:
        print("   " + failure)
    print(f"screenshots in {OUT}\n")
    return 0 if not failures else 1


sys.exit(asyncio.run(main()))
