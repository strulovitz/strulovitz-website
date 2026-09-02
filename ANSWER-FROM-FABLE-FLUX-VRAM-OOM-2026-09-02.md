Directions for Sonnet (from Fable) — FLUX.2-dev OOM in CLIPTextEncode
Diagnosis (high confidence)

The --lowvram + /free + "wait for 10.5 GB free" strategy can't work, because ComfyUI's loader deliberately fills free VRAM with model weights down to a fixed headroom (~1.2 GB by default). More free VRAM → it loads more Mistral layers → same tiny headroom. The 9.43 GiB "already allocated" is the text encoder's own partially-loaded weights (the UNet isn't in VRAM yet at that point). The 640 MiB request is exactly 32768×5120×4 bytes — one Mistral MLP matrix dequantized to fp32 by ComfyUI-GGUF, which ComfyUI's headroom estimate doesn't know about. Images 1–2 fit by a few hundred MB; 3–6 didn't as CUDA context/cuBLAS/allocator baseline grew slightly. Prompt length is irrelevant (activations are tiny vs. weights).

Important: on current ComfyUI (Nvidia + torch ≥ 2.8), DynamicVRAM is on by default and --lowvram is a no-op (its help text says so). That's why the text encoder is on GPU at all — in the legacy path --lowvram runs text encoders on CPU.
Step 0 — check which regime you're in (1 minute)

Grep the ComfyUI startup log for dynamic/aimdo/DynamicVRAM. Also note the ComfyUI version. Report it.
Step 1 — the fix to try first: raise ComfyUI's headroom

Restart ComfyUI with:

--reserve-vram 3

(--reserve-vram works in both the legacy and DynamicVRAM paths; in DynamicVRAM you can alternatively use --vram-headroom 2.) Rerun the same failing image (#3).

    Success evidence: no OOM; during CLIPTextEncode nvidia-smi peaks around ~8–9 GB instead of ~11.5 GB.
    If still OOM: the error's "Currently allocated" should have dropped by ~2 GB. If so, go to --reserve-vram 4. If it did not drop, the flag isn't taking effect — report the log.

Step 2 — fallback: text encoder on CPU (only if Step 1 fails at 4 GB)

--disable-dynamic-vram --lowvram --reserve-vram 2

In the legacy path --lowvram puts text encoders on CPU automatically; no node changes needed. (Alternative: ComfyUI-MultiGPU's CLIPLoaderGGUFMultiGPU with device=cpu.) Expect the encode to take a few minutes per prompt (24B, torch dequant on CPU) and ~14 GB+ of system RAM during encode — 64 GB is fine.

    Evidence: nvidia-smi memory doesn't move during CLIPTextEncode; log shows CLIP loading to cpu.

Your listed options, evaluated

    (a) CPU encoder: valid, but Step 2, not Step 1 — much slower.
    (b) expandable_segments: the earlier crash was almost certainly because ComfyUI appends backend:cudaMallocAsync to PYTORCH_CUDA_ALLOC_CONF; combining that with expandable_segments:True is invalid. Safe form is --disable-cuda-malloc plus PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True. But fragmentation is not the main cause here — skip unless Steps 1–2 fail.
    (c) Split into two API jobs: useless — the OOM happens with only the CLIP loaded; ComfyUI already serializes CLIP→UNet.
    (d) GGUF dequant buffer setting: correct observation (fp32 temp), but there's no CLIP-side dequant_dtype knob in ComfyUI-GGUF (only UnetLoaderGGUFAdvanced has it). Don't chase it; fix headroom instead.

Questions 1 & 3 (the pre-flight check)

/system_stats vram_free = cudaMemGetInfo free + torch reserved-but-inactive. It's an honest number, but useless as a go/no-go signal, because the loader fills whatever is free anyway. No check can be made meaningful; the margin is set by --reserve-vram, not by free bytes. Rewrite force_clean_vram: keep the /free call, delete the ≥10.5 GB wait loop (just sleep ~2 s). Once Step 1 works, you can drop /free entirely — reloading 33 GB per image is wasted time.
Report back

ComfyUI version + dynamic-VRAM log line, the exact flags used, and for the first failing image: pass/fail plus the "Currently allocated" figure (or nvidia-smi peak) during CLIPTextEncode.
