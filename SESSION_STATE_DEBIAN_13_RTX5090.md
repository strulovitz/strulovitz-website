# Session State: Unsloth Studio + DeepSeek V4 Pro on Debian 13 (RTX 5090)

> This file is a hand-off note written by the AI (DeepSeek V4 Pro in OpenCode)
> so that a **fresh session on THIS machine** can pick up exactly where we left
> off. Read this first.
>
> The GitHub repo containing this file: `github.com/strulovitz/strulovitz-website`

---

## 1. The machine

- OS: **Debian GNU/Linux 13 (trixie)**
- GPU: **NVIDIA GeForce RTX 5090 Laptop GPU**, 24 GB VRAM, compute capability **12.0** (sm_120)
- NVIDIA driver: **580.95.05**, CUDA **13.0** (`nvcc` = V13.0.88, in `/usr/local/cuda-13.0`)
- CPU: Intel Core Ultra 9 275HX (24 threads)
- RAM: 62 GB, swap 61 GB
- Desktop: GNOME
- User: `nir`, home `/home/nir`
- sudo password is known to the user (do NOT store it in any file)

## 2. The original problem

Unsloth Studio installed and opened, but every large GGUF model (DeepSeek V4 Pro
Q1/Q2, Kimi K3) failed to load with:

```
Failed to load model: llama-server started but never became healthy on its local
/health endpoint. Try a smaller context length or a more quantized GGUF ...
```

The same models worked on Windows 11 on the same machine.

Two root causes were identified from the logs:

1. **The bundled llama.cpp prebuilt was too old.** Unsloth's prebuilt release
   `b10360` predates DeepSeek V4 Pro's MTP (Multi-Token Prediction) speculative
   decoding with an *embedded draft head* (`nextn` layers). The Studio log said
   "speculative drafter (embedded head); the prebuilt may predate it; retrying
   without speculative decoding".
2. **The load timeout was too short.** Studio polls `llama-server`'s `/health`
   for only 600 s; a ~500 GB model takes longer, so it timed out.

## 3. What we did (already done — do NOT redo)

1. **Uninstalled** the original `.deb` install completely (package, `~/.unsloth`,
   shortcut, config dirs, the `.deb` file).
2. **Reinstalled** via the official curl script
   (`curl -fsSL https://unsloth.ai/install.sh | sh`) into `~/.unsloth/studio`.
3. **Compiled llama.cpp from source** using **Unsloth's fork**
   (`unslothai/llama.cpp`, `master` branch, commit `d32676d`, 18 Aug 2026) —
   because it has Unsloth's custom flags (`--fit`, `--spec-default`,
   `--kv-unified`) AND `src/models/deepseek4.cpp` with full MTP support.
   Upstream `ggml-org/llama.cpp` no longer ships CUDA Linux binaries (only
   CPU/Vulkan for Linux), so source build was required.

   Build command (run in the cloned repo):
   ```bash
   cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120 \
     -DGGML_NATIVE=ON -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA_FA_ALL_QUANTS=ON
   cmake --build build --config Release -j 20
   ```
   `120` = sm_120 for the RTX 5090.

4. **Installed the compiled binary** to `~/.local/unsloth-llama-cpp/`, with
   `patchelf --set-rpath '$ORIGIN'` on every ELF file (so it finds its libs
   from anywhere). `libggml-cuda.so` is ~82 MB, self-built for this GPU.
   The clone still exists at `/tmp/opencode/unsloth-llama-src/` (may be wiped
   on reboot — the installed binary at `~/.local/unsloth-llama-cpp/` is what
   matters).

5. **Pointed Unsloth Studio at the new binary** via the env var
   `UNSLOTH_LLAMA_CPP_PATH=$HOME/.local/unsloth-llama-cpp`, set in THREE places:
   - `~/.bashrc` (line 1)
   - `~/.profile` (line 1)
   - `~/.config/environment.d/unsloth.conf`  ← the one that matters for the
     GNOME desktop app, because GUI apps don't read `~/.bashrc`.

6. **Raised the load timeout** 600 s → 3600 s in the Studio backend:
   `~/.unsloth/studio/unsloth_studio/lib/python3.13/site-packages/studio/backend/core/inference/llama_cpp.py`
   — three call sites `_wait_for_health(timeout = 3600.0)` at lines ~9105, ~16032, ~16775.
   ⚠️ This is inside the installed app and is RESET by `unsloth studio update`.

7. **Restored the desktop app** (the native window, not the browser). Reinstalled
   `Unsloth-Desktop-0_1_800_beta-Ubuntu.deb` (from
   `github.com/unslothai/unsloth/releases/download/v0.1.800-beta/`). The desktop
   app's menu entry is `Unsloth.desktop` (`Exec=unsloth-studio`). Removed the
   stale browser launcher `~/.local/share/applications/unsloth-studio.desktop`.

## 4. Current state (what exists right now)

- Desktop app installed: `dpkg -l | grep unsloth` → `0.1.800-beta`.
- Desktop app binary: `/usr/bin/unsloth-studio`.
- Backend: `~/.unsloth/studio/unsloth_studio/` (shared by desktop + server).
- **llama-server in use: the official Unsloth b10472 prebuilt**
  at `~/.local/unsloth-llama-cpp-b10472/llama-server` (build 10472, commit
  `7a556b8f9`, ggml 0.20.1, compiled for sm_120). It has the **"UD" (Unsloth
  Dynamic) quant types** + Kimi K3 vision (`libmtmd`) that Kimi K3 needs. See §10.
  Verified it reports `CUDA0: NVIDIA GeForce RTX 5090 Laptop GPU`.
- **Fallback builds still on disk (do NOT delete):**
  - our hand-compiled build `~/.local/unsloth-llama-cpp/llama-server` (fork
    master commit `d32676d`, no UD quant support — that is why Kimi K3 failed
    on it), and
  - the bundled prebuilt `~/.unsloth/llama.cpp/build/bin/` (b10360).
  The env var picks which one Studio uses; it currently points at b10472.
  Do NOT copy binaries between these dirs (lib version mismatches segfault).
- The timeout fix is applied (3600 s).
- The `q_lora_rank` MLA fix is applied (§8.1) — makes Auto mode skip the futile
  MTP attempt for DeepSeek V4 Pro.
- **18 Aug 2026 (evening): FULL SUCCESS TEST.** The model was re-downloaded
  (`teamblobfish/DeepSeek-V4-Pro-GGUF`, `Q2_K-XL`, ~534 GB), loaded, and answered
  a test prompt. The compiled MTP llama-server + 3600 s timeout are proven good.
  See §8 for the full result and the three new findings.

## 5. What STILL needs to be done (the remaining work)

1. **Log out / log back in** (or reboot) so the GNOME desktop app picks up the
   UPDATED `UNSLOTH_LLAMA_CPP_PATH` (now → b10472, §10).
2. **Load Kimi K3 and test it** (should now work with b10472). Then confirm
   DeepSeek V4 Pro 0813 still loads too (b10472 is newer, so it should).
3. **Delete the old DeepSeek V4 Pro `Q2_K-XL`** when done (frees ~574 GB) — Nir
   does this from the GUI.
4. **After any `unsloth studio update`, re-apply BOTH local site-packages fixes:**
   - the 3600 s load timeout (§3.6)
   - the `q_lora_rank` MLA fix (§8.1)
   These are the only two edits an update wipes (they are Python-side, so they
   survive llama.cpp swaps).
5. Logs to watch while loading / chatting (§6):
   - Studio server logs: `~/.unsloth/studio/logs/server/`
   - llama-server logs: `~/.unsloth/studio/logs/llama-server/`
   - backend log: `~/.unsloth/studio/tauri.log`

## 6. How to verify things quickly

```bash
# The compiled binary sees the GPU?
~/.local/unsloth-llama-cpp/llama-server --list-devices

# Supports MTP?
~/.local/unsloth-llama-cpp/llama-server --help | grep -E "draft-mtp|spec-type"

# Timeout fix still applied? (should show 3600.0, not 600.0)
grep -n "_wait_for_health(timeout" \
  ~/.unsloth/studio/unsloth_studio/lib/python3.13/site-packages/studio/backend/core/inference/llama_cpp.py

# Env var set?
grep -rn UNSLOTH_LLAMA_CPP_PATH ~/.bashrc ~/.profile ~/.config/environment.d/unsloth.conf
```

## 7. Notes / gotchas

- The 600 s timeout fix lives in site-packages and is reset by
  `unsloth studio update`. Re-apply after any update (see §6).
- Don't trust search-engine AI for version numbers (Google AI Search invented
  `b10456` and "v0.1.0"). Verify against the GitHub API:
  `curl -fsSL https://api.github.com/repos/unslothai/llama.cpp/releases | grep tag_name`.
- The source clone is under `/tmp/opencode/unsloth-llama-src/` and will be lost
  on reboot — not a problem; only the installed binary is needed.
- There is a SEPARATE machine (Linux Mint 22, RTX 4070 Ti) that will need the
  same treatment later. The guide for that is in the sibling file
  `UNSLOTH_STUDIO_LINUX_MTP_FIX.md` in this same repo (see §9 there: RTX 4070 Ti
  = `CMAKE_CUDA_ARCHITECTURES=89`).

## 8. The big test (18 Aug 2026) — RESULT: it works

Full test done on 18 Aug 2026. **The compiled MTP-capable llama-server + the
3600 s timeout DO load and run the model; the original bug is fixed.** The test
also surfaced three new findings, now handled/documented below.

### 8.1 NEW FIX — DeepSeek V4 Pro MTP was "trying in vain" (q_lora_rank)

On load, Studio emitted `--spec-type draft-mtp --spec-draft-n-max 2`, then
llama-server aborted:

```
load_model: context type MTP requested but model doesn't contain MTP layers
llama_server: exiting due to model loading error
```

Studio then auto-retried WITHOUT speculative decoding, and the retry succeeded.
So the model loads either way, but the first (MTP) attempt is wasted.

Root cause (confirmed by reading the GGUF header of the model):

- The deepseek4 GGUF metadata advertises `deepseek4.nextn_predict_layers`
  (an MTP head), **but the actual MTP tensors were stripped by this `Q2_K-XL`
  quantization**. Metadata and reality disagree → llama-server aborts.
- Separately, Studio's "is this an MLA model (so drop MTP under Auto)" check
  only looks for `{arch}.attention.kv_lora_rank`. DeepSeek V4 Pro uses
  `{arch}.attention.q_lora_rank` instead (§8.2), so the model was NOT detected
  as MLA and the drop-MTP policy never fired.

Fix (applied 18 Aug 2026 in the same `llama_cpp.py` as the timeout fix): teach
the backend that `q_lora_rank` also means MLA. Four edits:

1. metadata map — add `f"{arch}.attention.q_lora_rank": "q_lora_rank"` right
   after the existing `kv_lora_rank` mapping.
2. `__init__` — `self._q_lora_rank: Optional[int] = None` (next to `_kv_lora_rank`).
3. the two reset blocks (`_read_gguf_metadata` and the unload/reset block) —
   add `self._q_lora_rank = None`.
4. `_build_speculative_flags`, the `_auto_mla_embedded_mtp` guard becomes:
   `and (self._kv_lora_rank is not None or self._q_lora_rank is not None)`.

Result: Auto mode now correctly drops MTP for DeepSeek V4 Pro (falls back to
ngram-mod / spec-off) instead of trying MTP and retrying.

> ⚠️ Like the timeout fix, this lives in site-packages and is RESET by
> `unsloth studio update`. Re-apply both after any update.

### 8.2 DeepSeek V4 Pro GGUF metadata facts (for future reference)

The Q2_K-XL first-shard header contains these keys:

```
general.architecture            = deepseek4
deepseek4.attention.head_count
deepseek4.attention.head_count_kv
deepseek4.attention.q_lora_rank          <- MLA signal (NOT kv_lora_rank)
deepseek4.attention.output_lora_rank
deepseek4.attention.indexer.head_count
deepseek4.nextn_predict_layers           <- MTP head advertised
```

`kv_lora_rank` is ABSENT; `q_lora_rank` is present. Older DeepSeek used
`kv_lora_rank`; `deepseek4` uses `q_lora_rank`. Any MLA detection that only
checks `kv_lora_rank` will miss it.

### 8.3 Gotcha — the model is far bigger than RAM ("stuck at 11 %, freezing")

The `Q2_K-XL` GGUF is **~534 GB**, split into 13 shards. The machine has
**62 GB RAM + 24 GB VRAM** (~8× too small). Observed consequences:

- The load is memory-mapped (`mmap`), so llama-server itself reports
  "model loaded" in ~23 s — but Studio's progress bar sat at ~11 % and the whole
  desktop froze for ~20–50 min while the OS paged the model in/out. The "stuck
  at 11 %" is a *progress-reporting + thrashing* symptom, not an infinite hang —
  it eventually finishes if you wait. (A warm page cache makes a reload much
  faster.)
- Generation works but is slow (active experts are paged from NVMe per token).
- Once, the first chat message froze the desktop app window (stop button
  unresponsive, zero requests hit the logs). Closing + reopening Unsloth cleared
  it; the second attempt answered fine.

Rule of thumb for this box: models below ~40 GB run from memory comfortably;
bigger models work via mmap but slowly.

### 8.4 The bundled llama.cpp "update available" prompt — safe to skip

Studio offered "New llama.cpp update: unknown → b10472-mix-4b653db (219 MB)".
That would only upgrade the BUNDLED prebuilt in `~/.unsloth/llama.cpp`. At the
time we skipped it because our compiled build (via the env var) already handled
DeepSeek. LATER we discovered b10472 is REQUIRED for Kimi K3's "UD" quant format
(§10) — and we installed it to a fresh dir + repointed the env var, NOT via the
GUI button. Do NOT copy binaries between the dirs (lib version mismatches
segfault); the env-var route is the only correct one.

## 9. Kimi K3 (UD-Q1_0, 467 GB) — 18 Aug 2026 (downloaded; header checked)

Third big model on this machine. Repo `unsloth/Kimi-K3-GGUF`, variant
`UD-Q1_0` = **467 GB**, split into **11 shards**
(`Kimi-K3-UD-Q1_0-00001-of-00011.gguf` …). Shard 1 is a tiny **6.9 MB
metadata-only** shard; the weights start in shard 2 (~49 GB each).

- **Architecture is NOT MLA.** Kimi K3 is a 2.8T-parameter MoE with **Kimi Delta
  Attention (KDA)** + **Attention Residuals (AttnRes)**, 1M context, native
  vision. So the §8.1 `q_lora_rank` MLA fix does NOT apply here — that fix is
  specific to DeepSeek `deepseek4`. The backend already maps
  `{arch}.kda.head_dim` → `kda_head_dim`, so KDA is handled.
- **What DOES apply (already in place, do NOT redo):** the compiled
  Unsloth-fork llama-server (the Kimi K3 README itself says it needs the
  `unslothai/llama.cpp` fork) + the 3600 s timeout (467 GB takes a long time).
- **MTP status: CONFIRMED NONE (checked 18 Aug 2026).** The shard-1 header has
  `general.architecture = kimi-k3`, `kimi-k3.kda.head_dim`,
  `kimi-k3.attention.q_lora_rank`, `kimi-k3.attention.kv_lora_rank` — and NO
  `nextn_predict_layers` / no draft tensors. So Kimi K3 has no MTP head → no
  futile MTP attempt; it loads with `--spec-default` on the first try (same as
  DeepSeek 0813 in §8). Note it DOES carry `kv_lora_rank`, so the backend's
  existing MLA detection would already classify it — harmless here, since there
  is no MTP to drop.

## 10. Kimi K3 needs the b10472 build ("UD" quant) — Option A done (18 Aug 2026)

**Symptom:** loading Kimi K3 failed immediately with
`gguf_init_from_reader: tensor 'blk.1.ffn_down_exps.weight' has invalid ggml
type 66. should be in [0, 43)` (plus a CLIP/mmproj error). Type 66 = a new
**"UD" (Unsloth Dynamic)** quant type that our hand-compiled fork-master build
(commit `d32676d`) does not have. Fork master has NO UD support — it only ships
in the **`b10472-mix` prebuilt** (release body lists PR #91 IQ1_XS/XXS/XXXS and
PR #70 kimi-k3 vision tower).

**Fix (Option A, the official-build route):**
1. Downloaded `app-b10472-mix-4b653db-linux-x64-cuda13-newer.tar.gz` (218 MB)
   from `github.com/unslothai/llama.cpp/releases/download/b10472-mix-4b653db/`.
2. Extracted (flat bundle: `llama-server` + `libggml-cuda.so` etc., RUNPATH
   `$ORIGIN`, so no patchelf needed) to `~/.local/unsloth-llama-cpp-b10472/`.
3. Verified: `--list-devices` → RTX 5090; `--version` → build 10472, commit
   `7a556b8f9`; `libggml-cuda.so` contains `iq1_xxxs` + `compute_120a` kernels.
4. Repointed `UNSLOTH_LLAMA_CPP_PATH` → `$HOME/.local/unsloth-llama-cpp-b10472`
   in `~/.bashrc`, `~/.profile`, `~/.config/environment.d/unsloth.conf`.
5. (pending at write time) log out/in, test Kimi K3, then re-test DeepSeek.

**Fallback if b10472 misbehaves:** point the env var back to
`~/.local/unsloth-llama-cpp` (d32676d) for DeepSeek, or recompile from the
b10472 source (`llama.cpp-source-commit-7a556b8f...tar.gz`) for sm_120 (Option B).
The two Python fixes (timeout §3.6, q_lora_rank §8.1) live in site-packages and
survive any llama.cpp swap.
