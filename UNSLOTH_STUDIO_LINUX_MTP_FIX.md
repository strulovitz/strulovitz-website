# Unsloth Studio on Debian 13 — Fixing "llama-server never became healthy" (Large Model / MTP)

**Author:** Nir Strulovitz
**Date:** 18 August 2026
**Machine:** Debian GNU/Linux 13 (trixie), RTX 5090 Laptop GPU (24 GB VRAM), 62 GB RAM, NVIDIA driver 580.95.05, CUDA 13.0

---

## 1. The problem

Unsloth Studio installed and opened, but every large GGUF model failed to load with:

```
Failed to load model: llama-server started but never became healthy on its local
/health endpoint. Try a smaller context length or a more quantized GGUF, and if
you use a VPN or HTTP proxy make sure localhost bypasses it
(NO_PROXY=127.0.0.1,localhost).
```

The same models loaded fine on Windows 11 on the same machine.

---

## 2. Root causes (two separate issues)

### 2a. The bundled llama.cpp binary was too old for MTP

Unsloth Studio downloads a prebuilt llama.cpp from `unslothai/llama.cpp`.
At install time that was release **`b10360`**, the latest Unsloth prebuilt.

DeepSeek V4 Pro uses **MTP (Multi-Token Prediction)** speculative decoding,
with an *embedded draft head* (`nextn` layers). The `b10360` binary predated
this feature. The Studio log showed:

```
llama-server failed to start with speculative drafter (embedded head);
the prebuilt may predate it; retrying without speculative decoding
```

So the server had to fail once and retry *without* the speed boost.

### 2b. The load timeout was too short

Unsloth Studio polls `llama-server`'s `/health` endpoint for only
**600 seconds (10 minutes)**. Loading a 400–535 GB model takes longer than
that, so the load timed out even though it would eventually finish.

The hard-coded value lives in the Studio backend:
`studio/backend/core/inference/llama_cpp.py`, three call sites passing
`timeout = 600.0` to `_wait_for_health(...)`.

---

## 3. The fix

### 3a. Compile llama.cpp from source (CUDA + MTP)

The official upstream `ggml-org/llama.cpp` no longer publishes CUDA Linux
binaries (only CPU/Vulkan for Linux). So we compiled from source, using
**Unsloth's own fork**, because it also carries Unsloth's custom flags
(`--fit`, `--spec-default`, `--kv-unified`, `--chat-template-kwargs`) that
Unsloth Studio passes to the server. The fork's `master` branch (commit
`d32676d`, 18 Aug 2026) already contains `src/models/deepseek4.cpp` with full
MTP/`nextn` support.

Prerequisites (all present):
- `nvcc` (CUDA 13.0.88)
- `gcc`/`g++` 14.2, `cmake` 3.31, `git`

Commands:

```bash
git clone --depth 1 https://github.com/unslothai/llama.cpp
cd llama.cpp
cmake -B build \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_ARCHITECTURES=120 \
  -DGGML_NATIVE=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA_FA_ALL_QUANTS=ON
cmake --build build --config Release -j 20
```

Notes:
- `CMAKE_CUDA_ARCHITECTURES=120` targets the RTX 5090 (compute capability 12.0).
- The build produces `build/bin/llama-server` (a small loader) plus
  `libllama-server-impl.so`, `libggml-cuda.so` (~82 MB), and friends.

### 3b. Install to a permanent location

```bash
DEST="$HOME/.local/unsloth-llama-cpp"
mkdir -p "$DEST"
cp -a build/bin/. "$DEST/"
# The binaries bake in a RUNPATH pointing at the build dir; fix it to $ORIGIN
sudo apt-get install -y patchelf
find "$DEST" -maxdepth 1 -type f -exec file {} \; \
  | grep ELF | cut -d: -f1 \
  | while read f; do patchelf --set-rpath '$ORIGIN' "$f"; done
```

Verify:

```bash
cd "$DEST"
./llama-server --list-devices
# -> CUDA0: NVIDIA GeForce RTX 5090 Laptop GPU
./llama-server --help | grep draft-mtp
```

### 3c. Point Unsloth Studio at the new binary

Unsloth Studio resolves `llama-server` in this order (from its own source):
1. `LLAMA_SERVER_PATH` (direct path)
2. `UNSLOTH_LLAMA_CPP_PATH` (directory containing `llama-server`)
3. `~/.unsloth/llama.cpp` (the old prebuilt)

We use `UNSLOTH_LLAMA_CPP_PATH`, set in two places:

1. `~/.bashrc` (terminal launches):
   ```bash
   export UNSLOTH_LLAMA_CPP_PATH="$HOME/.local/unsloth-llama-cpp"
   ```
2. `~/.local/share/unsloth/launch-studio.sh` (desktop icon) — added the same
   `export` right after the header.

### 3d. Raise the load timeout (recommended)

In `studio/backend/core/inference/llama_cpp.py`, change the three
`_wait_for_health(timeout = 600.0)` call sites to a larger value, e.g.
`timeout = 3600.0`.

> This edit is inside the installed app and is reset by `unsloth studio update`.

### 3e. Recognize `q_lora_rank` as MLA (DeepSeek V4 Pro) — recommended

DeepSeek V4 Pro uses architecture `deepseek4` and stores its MLA signal in
`{arch}.attention.q_lora_rank` (NOT `kv_lora_rank`, which older DeepSeek used).
Studio's "is this an MLA model, so drop MTP under Auto" check only reads
`kv_lora_rank`, so it misses deepseek4 and can try MTP in vain (the Q2_K_* quants
advertise `nextn_predict_layers` but strip the actual draft tensors → llama-server
aborts, then Studio retries without spec; see note 11). Four small edits in the
same `llama_cpp.py`:

1. metadata map — add `f"{arch}.attention.q_lora_rank": "q_lora_rank"` next to
   the existing `kv_lora_rank` mapping.
2. `__init__` — add `self._q_lora_rank: Optional[int] = None`.
3. the two reset blocks — add `self._q_lora_rank = None`.
4. `_build_speculative_flags`, the `_auto_mla_embedded_mtp` guard → append
   `or self._q_lora_rank is not None` to the lora-rank check.

> Reset by `unsloth studio update` (same as the timeout fix).

---

## 4. Summary

| Piece | Before | After |
|-------|--------|-------|
| llama.cpp backend | Unsloth prebuilt `b10360` (no MTP) | Compiled from Unsloth fork `master` with CUDA + MTP (or official `b10472` prebuilt for "UD" quants, §7) |
| CUDA support | prebuilt CUDA 13 | source-built for the GPU (sm_120 = RTX 5090; sm_89 = RTX 4070 Ti) |
| Load timeout | 600 s | 3600 s (§3d) |
| MLA detection | `kv_lora_rank` only | also `q_lora_rank` (§3e, for DeepSeek V4 Pro) |
| Location | `~/.unsloth/llama.cpp` | `~/.local/unsloth-llama-cpp` (or `-b10472`) via `UNSLOTH_LLAMA_CPP_PATH` |

---

## 5. Useful commands

```bash
# See which llama-server Unsloth would use
echo "$UNSLOTH_LLAMA_CPP_PATH"

# Check the new binary sees the GPU
~/.local/unsloth-llama-cpp/llama-server --list-devices

# Start Unsloth Studio
unsloth studio -p 8888

# Re-apply the timeout fix after an update
grep -n "timeout = 600.0" ~/.unsloth/studio/unsloth_studio/lib/python3.13/site-packages/studio/backend/core/inference/llama_cpp.py
```

---

## 6. Notes to my future self (next machine — Linux Mint 22)

Dear future me (DeepSeek V4 Pro in OpenCode), when doing this again on the
Linux Mint 22 machine, remember these things:

1. **Uninstall first with the official script, not by hand.**
   Unsloth ships a matching uninstaller:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/unslothai/unsloth/main/scripts/uninstall.sh | sh
   ```
   It removes the install dir, launcher, desktop shortcut and PATH entries
   cleanly. (I did it manually on Debian because the earlier `.deb` install
   left bits everywhere — on a clean install the script is enough.)

2. **Check prerequisites before anything else.** The build needs
   `nvcc` (CUDA toolkit), `gcc`/`g++`, `cmake`, `git`, and `patchelf`.
   On Mint, install with:
   ```bash
   sudo apt-get install -y build-essential cmake git patchelf
   ```
   Plus the NVIDIA CUDA toolkit matching that machine's driver/GPU.
   Find the GPU compute capability first:
   ```bash
   nvidia-smi --query-gpu=name,compute_cap --format=csv
   ```
   and map it to the right `CMAKE_CUDA_ARCHITECTURES` (RTX 5090 = `120`,
   4090 = `89`, 3090 = `86`, 2080 = `75`, etc.). This is the number that
   varies between machines — everything else is the same.

3. **The key env var is `UNSLOTH_LLAMA_CPP_PATH`.** Point it at the compiled
   `llama-server` directory and Unsloth Studio will use it instead of its own
   prebuilt. Set it in `~/.bashrc` AND in `~/.local/share/unsloth/launch-studio.sh`
   so both terminal and desktop-icon launches pick it up.

4. **Fix the RUNPATH after copying the build** (it's baked to the build dir).
   `patchelf --set-rpath '$ORIGIN'` on every ELF file in the install dir, or
   `llama-server` won't find `libggml-cuda.so` from its new home.

5. **Raise the 600 s timeout** in `llama_cpp.py` (three call sites) to
   `3600.0`, or large models will still time out even with MTP fixed.

6. **The MTP fix is version-dependent.** Unsloth's prebuilt `b10360` was too
   old for DeepSeek V4 Pro's embedded draft head. By the time this is read,
   Unsloth may have shipped a newer prebuilt — check the release tag first:
   `cat ~/.unsloth/llama.cpp/UNSLOTH_PREBUILT_INFO.json | grep release_tag`.
   If it's newer than `b10360` and already lists MTP/draft-mtp, you may not
   need to compile at all.

7. **Don't trust search-engine AI for version numbers.** Google AI Search
   invented a release `b10456` and a "v0.1.0 semantic versioning" that do not
   exist. Always verify against the real GitHub API:
   ```bash
   curl -fsSL https://api.github.com/repos/unslothai/llama.cpp/releases | grep tag_name
   curl -fsSL https://api.github.com/repos/ggml-org/llama.cpp/releases | grep tag_name
   ```

8. **The important part to remember:** the real bug was never the install.
   It was (a) an old llama.cpp lacking MTP, and (b) a 600 s timeout too short
   for a ~500 GB model. Fix both and it works.

9. **Desktop app vs server version — do not mix them up.** There are two ways
   to install, and they give different "faces" of the same program:
   - The **`.deb` file** (from `https://unsloth.ai/download/linux`) = the
     **desktop app**: a native window with an app-menu icon.
   - The **`curl -fsSL https://unsloth.ai/install.sh | sh`** script = the
     **server version**: runs `unsloth studio` and opens in a **browser**
     (`http://127.0.0.1:8888`), and asks you to **create a password** on first
     launch (normal security step, not an error).
   On the Debian 13 machine we started with the `.deb` (desktop app), then
   switched to the curl script during troubleshooting and unexpectedly lost the
   native window. The fix was to **reinstall the `.deb` on top** — the backend
   (and therefore the compiled MTP binary and timeout edits) lives in
   `~/.unsloth/studio` and is shared by both, so reinstalling the `.deb` only
   brings back the window without undoing the fixes.

10. **RTX 4070 Ti = compute capability 8.9, so `CMAKE_CUDA_ARCHITECTURES=89`.**
    On the Linux Mint 22 machine with the RTX 4070 Ti, use `89` instead of
    `120`. Confirm before building:
    ```bash
    nvidia-smi --query-gpu=name,compute_cap --format=csv
    ```
    Everything else in this guide is identical.

11. **DeepSeek V4 Pro ("deepseek4") advertises MTP but some quants strip the
    actual tensors.** The GGUF metadata has `nextn_predict_layers`, but the
    `Q2_K_*` quantizations omit the draft-head tensors, so llama-server aborts
    with "context type MTP requested but model doesn't contain MTP layers" and
    Studio retries without spec. That retry still works — the load is not
    broken, it just wastes one attempt (and can look "stuck" while it retries).

12. **"deepseek4" models use `q_lora_rank`, not `kv_lora_rank`.** Studio's
    Auto-mode "drop MTP for MLA models" rule only checks `kv_lora_rank`, so it
    misses deepseek4 and tries MTP in vain (item 11). Fix: in `llama_cpp.py`
    add `f"{arch}.attention.q_lora_rank": "q_lora_rank"` to the metadata map,
    init + reset `_q_lora_rank`, and extend the `_auto_mla_embedded_mtp` guard
    to `or self._q_lora_rank is not None`. Re-apply after
    `unsloth studio update`. (Full detail: session-state file §8.)

13. **A ~500 GB model on 62 GB RAM works, but slowly.** Loading is memory-mapped
    (`mmap`), so llama-server reports "model loaded" quickly, yet the desktop can
    freeze for tens of minutes while the OS pages 534 GB through 62 GB RAM, and
    generation is slow because experts are read from NVMe per token. On this
    hardware, prefer models that fit in RAM+VRAM (~40 GB or less) for comfort.

14. **"UD" (Unsloth Dynamic) quantizations need the b10472-mix prebuilt, not
    the fork master source.** Kimi K3's `UD-Q1_0` GGUF uses a new ggml type
    (`type 66`); a fork-master source build fails with
    `invalid ggml type 66. should be in [0, 43)`. The UD/IQ1_XXXS types + the
    kimi-k3 vision tower (PR #70) only ship in the `b10472-mix` prebuilt. So:
    use the official prebuilt
    (`app-b10472-mix-4b653db-linux-x64-cuda13-newer.tar.gz`, RUNPATH `$ORIGIN`,
    no patchelf needed) for such models — or recompile from the b10472 *source*
    commit `7a556b8f9` if you want a custom sm_120 build. (Full detail:
    session-state file §10.)

---

## 7. What the full Debian 13 test taught us (18 Aug 2026)

Everything below was confirmed by actually loading models on the Debian 13
machine (RTX 5090). It applies to the Linux Mint 22 machine too.

### 7a. DeepSeek V4 Pro 0813 (IQ1_M) — the one we'll run — has NO MTP

`6block/DeepSeek-V4-Pro-0813-GGUF`, `IQ1_M` = a **single** 372 GB `.gguf`
(arch `deepseek4`, fields `q_lora_rank` + `output_lora_rank`). Its header has
**no `nextn_predict_layers` and no draft tensors** — so no MTP at all. It loads
with `--spec-default` on the first try (no futile MTP attempt), and answers.
This is the "YOU" model Nir means when he says DeepSeek V4 Pro 0813.

### 7b. The Q2_K-XL DeepSeek *does* advertise MTP (but strips the tensors)

`teamblobfish/DeepSeek-V4-Pro-GGUF` `Q2_K-XL` (13 shards, ~534 GB) has
`deepseek4.nextn_predict_layers` in its header but NO actual draft tensors.
Without the §3e fix, Studio emits `--spec-type draft-mtp`, llama-server aborts
("model doesn't contain MTP layers"), and Studio retries without spec — the
"trying in vain" wasted attempt. With §3e applied, Auto drops MTP for deepseek4
and loads cleanly. (This is why §3e matters even if the 0813 model itself has
no MTP.)

### 7c. Frontend can freeze after the model loads (restart fixes it)

On the first big-model chat, the desktop app window froze once: the message
never reached the model (llama-server stayed idle, 0% GPU, no request in the
logs), and the stop button did nothing. Closing and reopening Unsloth fixed it;
the second attempt worked. Not our fix's fault — a Studio frontend stall. If the
GUI looks stuck, check the llama-server log: if it shows nothing new, just
restart the app (the model is still on disk, so no re-download).

### 7d. Models far bigger than RAM "work but slowly" (the 11% freeze)

534 GB / 372 GB models on 62 GB RAM load via `mmap` (llama-server says "model
loaded" in ~23 s) but the desktop can freeze for tens of minutes while the OS
pages the model in/out, and generation is slow (reads from NVMe per token).
Prefer models that fit in RAM+VRAM for comfort. This is physics, not a bug.

### 7e. The three site-packages edits to re-apply after `unsloth studio update`

1. 3600 s timeout (§3d, three `_wait_for_health` call sites)
2. `q_lora_rank` MLA fix (§3e)
(That's it — everything else is a llama.cpp binary chosen via
`UNSLOTH_LLAMA_CPP_PATH`, which survives updates.)



