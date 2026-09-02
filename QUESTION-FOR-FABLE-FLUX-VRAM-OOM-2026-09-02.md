# Question for Fable — FLUX.2-dev keeps running out of VRAM on some images, not others

## The machine
- Desktop Linux Mint 22, NVIDIA GeForce RTX 4070 Ti, **12282 MiB total VRAM**
  (ComfyUI reports a usable device limit of 11.59 GiB after driver/OS overhead).
- 64GB system RAM.
- ComfyUI is started with the `--lowvram` flag.

## The models (both GGUF quantized, via the ComfyUI-GGUF custom node)
- Diffusion model: `flux2-dev-Q4_K_M.gguf` — FLUX.2-dev, 32B params, Q4_K_M quant, ~19GB on disk.
- Text encoder: `Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf` — this is FLUX.2-dev's
  fixed, trained-together text encoder (24B params, Q4_K_M quant, ~14GB on disk). It
  cannot be swapped for a smaller encoder — FLUX.2-dev's cross-attention was trained
  specifically on this encoder's embedding space.
- VAE: `flux2-vae.safetensors` (336MB, not quantized).

## The exact ComfyUI API workflow graph used for every image
```
UnetLoaderGGUF(flux2-dev-Q4_K_M.gguf)
CLIPLoaderGGUF(Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf, type=flux2)
VAELoader(flux2-vae.safetensors)
CLIPTextEncode(text=<the image prompt>, clip=<CLIPLoaderGGUF output>)
FluxGuidance(conditioning=<CLIPTextEncode output>, guidance=4.0)
ConditioningZeroOut(conditioning=<CLIPTextEncode output>)   # negative, zeroed, NOT a second encode pass
EmptyLatentImage(width=1024, height=1024, batch_size=1)
KSampler(model=<UnetLoaderGGUF>, positive=<FluxGuidance>, negative=<ConditioningZeroOut>,
         latent_image=<EmptyLatentImage>, seed=<per-story seed>, steps=28, cfg=1.0,
         sampler_name=euler, scheduler=simple, denoise=1.0)
VAEDecode(samples=<KSampler>, vae=<VAELoader>)
SaveImage(images=<VAEDecode>)
```
This exact graph was already fixed once before (an earlier version used a real second
`CLIPTextEncode` call for an empty negative prompt, which ran the 24B encoder twice per
image and OOM'd every time; switching to `FluxGuidance` + `ConditioningZeroOut` fixed
that specific bug on 2026-09-02, confirmed working on a test image).

## What the Python driver script does before every single image (not just after a failure)
```python
def force_clean_vram(client, *, min_free_gb=10.5, timeout_s=60.0):
    client.post(f"{COMFY_URL}/free", json={"unload_models": True, "free_memory": True})
    started = time.monotonic()
    while time.monotonic() - started < timeout_s:
        free_gb = vram_free_bytes(client) / (1024 ** 3)   # reads ComfyUI's own /system_stats
        if free_gb >= min_free_gb:
            return free_gb
        time.sleep(1.0)
    return vram_free_bytes(client) / (1024 ** 3)   # gives up and proceeds anyway after 60s
```
This calls ComfyUI's own `/free` endpoint (`unload_models: true, free_memory: true`) and
then polls ComfyUI's own `/system_stats` endpoint — real numbers straight from the GPU
driver, not a guess — waiting until it reports at least 10.5GB free before submitting
the next image's job. This runs before EVERY image, not just after a crash.

## The actual failures, verbatim, from tonight's real batch run
Batch of 30 images (30 missing illustrations across 5 stories x models). Images #1 and
#2 succeeded. Images #3, #4, #5, #6 (the very next four in the queue) ALL failed with
the identical error shape:

```
torch.OutOfMemoryError: Allocation on device 0 would exceed allowed memory. (out of memory)
Currently allocated : 9.43 GiB
Requested           : 640.00 MiB
Device limit        : 11.59 GiB
Free (according to CUDA): 7.12 MiB
```
(Image #4 and #5 show 9.45 GiB and 9.44 GiB allocated respectively — same shape.)

The traceback in every failure is identical: it fails inside `CLIPTextEncode`, specifically
inside the Mistral text encoder's MLP layer (`down_proj(activation(gate_proj(x)) * up_proj(x))`),
while dequantizing GGUF weights on the fly (`ComfyUI-GGUF/dequant.py` -> `.to(dtype)`).

So: `force_clean_vram` DID verify 10.5GB+ free right before the job was submitted. But by
the time `CLIPTextEncode` actually runs inside that same job, 9.43 GiB is ALREADY allocated
(presumably from ComfyUI loading/dequantizing the UNet + CLIP model weights themselves for
this job), leaving only a sliver of the 11.59 GiB device limit — not enough for the 640MB
this particular encode step needs.

## The one pattern we've noticed, unconfirmed
- Image #1 (succeeded): prompt is 1461 characters.
- Image #2 (succeeded): prompt is 955 characters.
- Image #3 (failed, DeepSeek): prompt is 979 characters.
- This does NOT cleanly correlate with prompt length alone (image #3's prompt, at 979
  chars, is barely longer than image #2's 955-char prompt that succeeded, yet #2 worked
  and #3 didn't). So prompt length alone does not obviously explain it — there may be a
  cumulative effect (e.g., GPU memory fragmentation getting slightly worse job over job
  even after `/free` is called, so each successive job has slightly less real headroom
  even though `/system_stats` reports the same "free" number), or something about how
  ComfyUI-GGUF dequantizes on first use per job that isn't fully undone by `/free`.

## What we're asking Fable
1. Is `/system_stats`'s reported "free" VRAM number actually trustworthy right before
   submitting a new job when using `--lowvram` + GGUF-quantized models with on-the-fly
   dequantization, or can PyTorch's allocator report memory as "free" that is actually
   fragmented into pieces too small to satisfy a single allocation request (classic
   fragmentation, not genuine low memory)?
2. Given a 24B-parameter text encoder that MUST be used (FLUX.2-dev's trained pair, not
   swappable) on a 12GB card, what is the correct fix here — options we can think of but
   don't know how to properly evaluate:
   a. Force the CLIPTextEncode / CLIPLoaderGGUF node to run on CPU only (accept a much
      slower text-encoding step, in exchange for it never competing with the UNet for
      VRAM at all)?
   b. Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (or similar) to reduce
      fragmentation, given the earlier session's notes say forcing a different allocator
      backend outright CRASHED ComfyUI — is `expandable_segments` different/safer from
      that crash?
   c. Load/unload the UNet and CLIP model as two fully separate ComfyUI API calls (encode
      text first with ONLY the CLIP loaded, free it completely, THEN load only the UNet
      for sampling) instead of one graph that has both loaded at once?
   d. Something about how ComfyUI-GGUF's on-the-fly dequantization keeps a temporary
      full-precision copy of tensors in VRAM during the cast, and whether there's a
      setting to dequantize directly to a smaller working buffer instead?
3. Is there a way to make `force_clean_vram`'s pre-flight check actually meaningful (i.e.
   verify a single large contiguous allocation is possible, not just that some free bytes
   exist in total), so the script can KNOW a job will fail before submitting it, rather
   than discovering it via a crash?

We are not asking you to guess blindly — if there's genuinely no way to know without
Nir trying something and reporting back what happens, say so plainly and tell us exactly
what to try first and what real-world evidence (which log lines, which `nvidia-smi` or
`/system_stats` numbers) would tell us whether it worked, so we don't waste his time on
things that don't matter.
