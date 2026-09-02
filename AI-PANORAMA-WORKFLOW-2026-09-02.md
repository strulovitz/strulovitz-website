# AI Panorama Workflow — Local Image Generation (ComfyUI + FLUX.2)

Written 2026-09-02 by Claude Sonnet 5 in OpenCode, on desktop-linux (Linux Mint 22, RTX 4070 Ti 12GB, 64GB RAM). This document exists so that if OpenCode restarts, crashes, or a different agent picks this up, they can continue from exactly this point without losing anything. Read this whole file before doing anything else on this topic.

## WHAT THIS IS FOR

This work belongs to the site's illustrated-images feature: every knowledge-graph node and every article gets an AI-generated image. FLUX.2-dev is the model Nir has chosen for this, and it is now part of the fleet (see `bible/part-00.md` 0.9 and `bible/part-06.md` 6.9.1).

## WHAT WE DID TODAY, STEP BY STEP

1. Pulled the repo (`git -C /home/nir/strulovitz-website pull`) — picked up a large batch of new content from another agent session on desktop-windows (7 home pages, 7 about pages per image model, lightbox, coming-soon pages for Laser Chess/Evil Genius/Second Opinion/Cheerleader). Unrelated to today's ComfyUI work, noted for completeness.

2. Confirmed hardware: RTX 4070 Ti, 12282 MiB VRAM; 62Gi RAM; ComfyUI already installed at `/home/nir/ai-art/ComfyUI` (Python venv at `/home/nir/ai-art/venv`) from an earlier session, with three unrelated SDXL checkpoints already present (RealVisXL, Juggernaut-X, zavychromaxl).

3. Researched the real FLUX.2 model family on Hugging Face (verified against the actual repos rather than trusting a pasted summary at face value):
   - **FLUX.2 [dev]** — 32B params, guidance-distilled, the full open-weight FLUX.2 model (there is also FLUX.2 [pro], API-only, not downloadable).
   - **FLUX.2 [klein]** — a *separate*, smaller, distilled-to-4-steps family (9B or 4B). Not a "fast mode of dev" — a different architecture Black Forest Labs trained specifically for speed.
   - Text encoder for FLUX.2-dev is **Mistral-Small-3.2-24B-Instruct-2506** (fixed by training — cannot be swapped for Qwen or anything else; the model's cross-attention was trained on Mistral's embedding space specifically).
   - Confirmed real GGUF quantized file sizes directly from the `city96/FLUX.2-dev-gguf` and `unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF` repos rather than estimating.

4. Installed **ComfyUI-GGUF** custom node (`city96/ComfyUI-GGUF`, cloned into `custom_nodes/`, `pip install -r requirements.txt` inside the venv) — this lets ComfyUI load `.gguf` quantized diffusion models and text encoders with automatic VRAM/RAM offloading.

5. **First attempt: Q8_0** (max quality). Downloaded `flux2-dev-Q8_0.gguf` (33GB) + `Mistral-Small-3.2-24B-Instruct-2506-Q8_0.gguf` (24GB) + `flux2-vae.safetensors`. Result: RAM swap climbed unboundedly (4.5GB to 18GB+ over ~20 minutes with no sign of finishing) — the 57GB combined resident size left too little real headroom once the OS and ComfyUI itself were accounted for. Stopped it.

6. **Second attempt: Q6_K**. Started downloading, but switched plan mid-way to go straight to Q4 instead. All Q8 and partial Q6 files deleted.

7. **Third attempt: Q4_K_M** (the one that worked). Downloaded `flux2-dev-Q4_K_M.gguf` (19GB) + `Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf` (14GB). First generation attempt hit a VRAM OOM caused by a workflow bug, not a hardware limit: the workflow used a real second CLIPTextEncode call for an empty negative prompt, and the 24B Mistral text encoder needs close to the full 12GB VRAM during each encode pass, so encoding twice back-to-back overflowed. Fixed by using the standard FLUX pattern instead: `FluxGuidance` node (embeds guidance strength into the positive conditioning) + `ConditioningZeroOut` (produces a zero negative conditioning WITHOUT a second encoder pass) + `KSampler` with `cfg=1.0`. This is a real, permanent lesson about how FLUX models should be wired in ComfyUI — save it for every future FLUX workflow.

8. **Success.** Full run: 28 steps, 1024x1024, ~6.3 seconds/step once warmed up, ~7 minutes total including first-load. Test prompt: "a photorealistic red apple sitting on a wooden table, soft window light, shallow depth of field." Nir confirmed the result looked great. Output saved at `/home/nir/ai-art/ComfyUI/output/flux2dev_test_00001_.png`.

## EXACT CURRENT STATE OF THE MACHINE (desktop-linux)

Files in place, verified sizes:
- `/home/nir/ai-art/ComfyUI/models/diffusion_models/flux2-dev-Q4_K_M.gguf` (19 GB)
- `/home/nir/ai-art/ComfyUI/models/text_encoders/Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf` (14 GB)
- `/home/nir/ai-art/ComfyUI/models/vae/flux2-vae.safetensors` (336 MB)
- `/home/nir/ai-art/ComfyUI/custom_nodes/ComfyUI-GGUF/` (custom node, installed and working)
- Three unrelated SDXL checkpoints from an earlier session in `models/checkpoints/` (RealVisXL, Juggernaut-X, zavychromaxl) — untouched, not used today.

Disk: `/home/nir` has 1.1TB free (of 1.7TB) after all downloads.

ComfyUI process: was running on `127.0.0.1:8188` at the end of this session (started via `python /home/nir/ai-art/ComfyUI/main.py --listen 127.0.0.1 --port 8188`, backgrounded with `setsid nohup ... < /dev/null &` so it survives the tool's shell closing). It will NOT survive an actual reboot or OpenCode restart killing the process tree — check with `ps aux | grep main.py` and restart if needed using the exact command above (venv must be activated first: `source /home/nir/ai-art/venv/bin/activate`).

Working test workflow (JSON API format) was saved at `/tmp/opencode/flux2_workflow_q4_v2.json` — **this is in /tmp, which does NOT survive a reboot.** If it's gone, rebuild it: UnetLoaderGGUF (flux2-dev-Q4_K_M.gguf) → CLIPLoaderGGUF (Mistral Q4_K_M, type=flux2) → CLIPTextEncode (your prompt) → FluxGuidance (guidance=4.0) for positive, ConditioningZeroOut (same CLIPTextEncode output) for negative → EmptyLatentImage (1024x1024) → KSampler (cfg=1.0, steps=28, sampler=euler, scheduler=simple) → VAEDecode (flux2-vae.safetensors) → SaveImage. Worth saving this workflow JSON into the repo under a `comfy/` folder (Part 06, 6.9.3 mentions `comfy/style.md` as the expected location for image-generation config) so it survives properly — not done yet, worth doing next session.

## PART 2 — `pipeline/stages/images.py` BUILT AND WORKING (2026-09-02, same day, continued)

"Our actual images" turned out to mean exactly what `WHERE-WE-STAND-2026-08-22.md`
item #1 already said: render the 38 illustration prompts the eight models
already wrote, using this local FLUX.2-dev setup, same seed for every edition.
That stage now exists and has produced its first real image successfully. This
section is the complete, no-rediscovery-needed account of how it works and
every trap that was hit building it, so no future agent (including a future
me) has to burn an hour finding these out again.

### THE FILE

`pipeline/stages/images.py`. Same conventions as every other stage
(`render_edition.py` was the template): `--story`/`--all`, `--model`/`--all-models`,
`--again` to redo, writes to the job ledger via `lib/db.py`, never edits or
retries because a picture "looks wrong" (decision 16 applies to pictures too —
only a real ComfyUI failure is retried, never an ugly-but-successful result).

```
cd pipeline && uv run stages/images.py --story <slug> --model <id>
cd pipeline && uv run stages/images.py --all --all-models
```

ComfyUI must already be answering on `127.0.0.1:8188` — the script checks and
exits with a clear message if it is not, it does not try to start it.

### WHERE THE OUTPUT GOES (already decided by Nir, decision 22, now implemented)

```
content/stories/<story>/editions/<company--model>/images/
    article.png     the full-size 1024x1024 illustration
    thumbnail.png    a 400x400 copy, DERIVED from article.png with PIL after
                     the fact — never downloaded separately, so a hover card
                     never has to fetch the full-size file
    meta.json        model, seed, steps, guidance, the exact prompt used, when,
                     and how many seconds it took
```

### THE FIXED SEED

`IMAGE_SEED = 42`, a constant at the top of the file, used for every single
edition of every story. This is not a placeholder to "improve later" — it is
the deliberate point. The only thing that should ever differ between one
edition's picture and another's is the quality of that edition's own
paragraph, never a different roll of the dice.

### THE COMFYUI GRAPH, AND WHY IT IS SHAPED THIS WAY

`build_workflow()` builds this exact node graph, proven working:

```
UnetLoaderGGUF (flux2-dev-Q4_K_M.gguf)
CLIPLoaderGGUF (Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf, type=flux2)
VAELoader (flux2-vae.safetensors)
CLIPTextEncode (the model's own paragraph)
  -> FluxGuidance (guidance=4.0)          -> positive conditioning
  -> ConditioningZeroOut                  -> negative conditioning
EmptyLatentImage (1024x1024)
KSampler (seed=42, steps=28, cfg=1.0, sampler=euler, scheduler=simple)
VAEDecode
SaveImage
```

**Why `FluxGuidance` + `ConditioningZeroOut` instead of a second, real
`CLIPTextEncode` call for an empty negative prompt:** the text encoder here is
the full 24-billion-parameter Mistral-Small model, and encoding a prompt with
it uses close to the entire 12GB of VRAM on this card by itself. Two encode
passes back to back — one for the real prompt, one for an empty negative —
overflow the card. `ConditioningZeroOut` produces a correctly-shaped zero
conditioning tensor from the SAME encode pass's output, with `cfg=1.0` so the
sampler does not even look at the negative side. This is the standard,
correct way to wire any FLUX model in ComfyUI, not a workaround specific to
this GPU — worth remembering for any future FLUX workflow, on any machine.

### THE REAL TIMING AND VRAM NUMBERS, MEASURED, NOT GUESSED

- Idle GPU memory between jobs: **~600 MiB**.
- Fully loaded during generation: **~11.3–11.8 GiB** — this is a genuinely
  tight fit on a 12GB card. There is no headroom for a second job at the same
  time.
- One 1024x1024, 28-step image, Q4_K_M quantization, `cfg=1.0`: **about 300
  seconds (5 minutes)** end to end on this RTX 4070 Ti, including model
  loading if it was not already warm.
- **40 images at this rate is about 3.3 hours of GPU time. $0.00.**

### TRAP 1 — THE BASH TOOL'S OWN TIMEOUT KILLS THE CLIENT, NOT THE JOB

Running `uv run stages/images.py ...` directly as a normal foreground command
gets killed by the terminal tool's own timeout (120 seconds by default) long
before a 5-minute image finishes. **The job keeps running on the ComfyUI
SERVER anyway** — ComfyUI's queue and GPU work are entirely independent of
whichever HTTP client submitted the job and does not care if that client goes
away. So killing the script does NOT cancel the render; it just means nothing
is left running to receive the finished PNG and write it to disk.

**The fix:** always launch `images.py` detached and backgrounded —
```
(setsid nohup uv run stages/images.py --story <slug> --model <id> \
  > /tmp/opencode/images_run.log 2>&1 < /dev/null &)
```
— then poll `/tmp/opencode/images_run.log`, `nvidia-smi`, and
`curl -s http://127.0.0.1:8188/queue` in separate, short tool calls
(`sleep 60`, `sleep 100`, etc., each with an explicit larger `timeout`
parameter on the bash tool call itself if the sleep is close to 120s) until
the log shows a result. Never assume a 5-minute job can run inside one
foreground tool call.

### TRAP 2 — A KILLED CLIENT + A RETRY CAN SUBMIT TWO JOBS AT ONCE, WHICH REALLY DOES OOM

Because of Trap 1, killing the script does not cancel the server-side job. If
you then simply re-run the same command while the first job is still sitting
in ComfyUI's queue as `running`, **two jobs now compete for VRAM back to
back**, and the second one to try to encode text gets a real CUDA
out-of-memory error (`Currently allocated: 9.66 GiB, Requested: 640.00 MiB,
Device limit: 11.59 GiB`) — even though a single job fits fine with room to
spare. This is exactly what happened on the first real attempt today, and the
error looked alarming but had nothing to do with the model, the quantization,
or the workflow being wrong.

**The fix, before ever retrying after an interruption:**
```
curl -s http://127.0.0.1:8188/queue | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(len(d['queue_running']), len(d['queue_pending']))"
nvidia-smi --query-gpu=memory.used --format=csv
```
If either queue is non-empty, or GPU memory is not back down near the ~600MiB
idle baseline, **wait** — do not submit a new job on top of an old one still
finishing. `POST http://127.0.0.1:8188/interrupt` can be tried but does not
reliably free memory instantly; waiting for the number to drop is the
trustworthy signal, not the interrupt call itself.

### THE FIRST REAL IMAGE, AND WHAT "NOTHING IS EVER FIXED" MEANT IN PRACTICE

The first successful render — Grok 4.6's own illustration paragraph for the
Kimi K3 story — came out with a visible hand at the drafting table, even
though Grok's own paragraph explicitly said "no robot hands." That is FLUX.2
doing its own thing with a prompt that asked it not to, and per decision 16 it
was published exactly as rendered, not retried, not touched, not noted as a
defect anywhere the image itself is shown. This document records it here as
an honest example of what "we never fix a model's output, or the picture
made from it" looks like when it actually happens, not just as a rule on paper.

Committed and pushed as the first proof image:
`content/stories/2026-07-17-kimi-k3/editions/x-ai--grok-4.6/images/`.

## WHAT STILL NEEDS TO BE DONE

1. **Run the full batch** — `uv run stages/images.py --all --all-models` for
   the remaining ~39 illustrations, backgrounded per Trap 1 above, checked
   periodically rather than watched continuously (3+ hours of GPU time).
2. Build `comfy/style.md` (the style bible: consistent palette, no text in
   images, no real faces, no logo imitation — Part 06 §6.9.4). Note: this rule
   already lives inside every model's own illustration-prompt instructions
   (see `IMAGE_PROMPT_ONLY` in `render_edition.py`), so it is not a new
   invention — this item is only about writing it down once, centrally, for
   future prompt templates.
3. **THE READING PAGES** (`pipeline/stages/build_pages.py`, not yet written) —
   clicking a node still opens nothing. Each page needs the full-size
   illustration at the top; the hover card needs the thumbnail. Both files
   now exist on disk for every rendered edition; nothing reads them yet.
4. Check Part 01 of the Bible for which physical machine is meant to run
   ComfyUI in the Bible's own naming — note that the Bible's "Atlas/Forge"
   names are retired (see `AGENTS.md`); this machine is called `desktop-linux`
   everywhere from now on, in code, in docs, and in conversation.
5. Longer-standing, unrelated to today: the tesseract's brightness (Nir's
   parked question, ask "how dim?" in plain terms); the stem-vs-mesh linking
   design question (his choice, do not pick for him).

## HOW TO RESUME IF THIS SESSION IS LOST

1. Read this file completely, both Part 1 and Part 2.
2. `git -C /home/nir/strulovitz-website pull`
3. Check if ComfyUI is running: `ps aux | grep main.py`. If not: `source /home/nir/ai-art/venv/bin/activate && (setsid nohup python /home/nir/ai-art/ComfyUI/main.py --listen 127.0.0.1 --port 8188 > /tmp/opencode/comfyui.log 2>&1 < /dev/null &)`, wait ~20s, confirm with `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8188/` (expect 200).
4. Before submitting any image job, check `http://127.0.0.1:8188/queue` and
   `nvidia-smi --query-gpu=memory.used --format=csv` are both idle (Trap 2
   above) — never assume the GPU is free just because no error was printed.
5. Run `pipeline/stages/images.py` ALWAYS backgrounded (Trap 1 above), never
   as a plain foreground command expected to finish within one tool call.
6. If "our actual images" or similar comes up again: it means rendering the
   illustration prompts already written by the eight models — this is now
   DONE as a working stage; check whether the full 40-image batch has been
   run yet before assuming it still needs building from scratch.
