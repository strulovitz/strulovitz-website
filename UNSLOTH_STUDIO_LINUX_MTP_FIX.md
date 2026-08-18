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

---

## 4. Summary

| Piece | Before | After |
|-------|--------|-------|
| llama.cpp backend | Unsloth prebuilt `b10360` (no MTP) | Compiled from Unsloth fork `master` with CUDA + MTP |
| CUDA support | prebuilt CUDA 13 | source-built for sm_120 |
| Load timeout | 600 s | (optionally) 3600 s |
| Location | `~/.unsloth/llama.cpp` | `~/.local/unsloth-llama-cpp` |

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
