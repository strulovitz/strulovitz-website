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

## WHAT STILL NEEDS TO BE DONE

1. Build `comfy/style.md` (the style bible: consistent palette, no text in images, no real faces, no logo imitation — Part 06 §6.9.4).
2. Build the prompt-from-claims templating and wire it into the pipeline so Atlas can send `{image_prompt_id, prompt, seed}` to Forge's ComfyUI over Tailscale per Part 06 §6.9.3.
3. Check Part 01 of the Bible for which physical machine is meant to run ComfyUI in the final architecture (Atlas/Forge naming) — this machine is desktop-linux, not yet confirmed which Bible role that maps to.
4. Apply this to Nir's actual images — ask him directly what those are when resuming; this document doesn't know yet.
5. Longer-standing, unrelated to today: reading pages for graph nodes still don't exist (`pipeline/stages/build_pages.py` not yet written); the tesseract's brightness (Nir's parked question, ask "how dim?" in plain terms); the stem-vs-mesh linking design question (his choice).

## HOW TO RESUME IF THIS SESSION IS LOST

1. Read this file completely.
2. `git -C /home/nir/strulovitz-website pull`
3. Check if ComfyUI is running: `ps aux | grep main.py`. If not: `source /home/nir/ai-art/venv/bin/activate && (setsid nohup python /home/nir/ai-art/ComfyUI/main.py --listen 127.0.0.1 --port 8188 > /tmp/opencode/comfyui.log 2>&1 < /dev/null &)`, wait ~20s, confirm with `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8188/` (expect 200).
4. Ask Nir what "our actual images" means concretely before generating anything — this document intentionally does not guess.
